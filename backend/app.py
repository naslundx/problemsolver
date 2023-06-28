from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import os

from .chat import get_response
from .database import (
    create_game,
    increment_game_progress,
    fetch_game_progress,
    fetch_question_count,
    save_chat,
)
from .questions import (
    get_question,
    get_answer,
    get_clue,
    get_prompt,
)
from .helpers import generate_uuid_and_seed


app = Flask(__name__)  # , static_folder="../frontend/dist/", static_url_path="/")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.get("/api/info")
@cross_origin()
def info():
    return {
        "question_count": fetch_question_count(),
    }


@app.post("/api/create")
@cross_origin()
def create():
    game_uuid, seed = generate_uuid_and_seed()
    question_id = 0
    create_game(game_uuid, seed, question_id)
    return {
        "game_uuid": game_uuid,
        "seed": seed,
        "game_progress": question_id,
    }


@app.get("/api/progress")
@cross_origin()
def progress():
    game_uuid = request.args.get("game_uuid")
    progress = fetch_game_progress(game_uuid) or 0
    return {"game_progress": progress}


@app.post("/api/start")
@cross_origin()
def start():
    data = json.loads(request.data)
    question_id = data.get("question_id")
    game_uuid = data["game_uuid"]
    seed = data.get("seed")

    progress = fetch_game_progress(game_uuid)
    print(question_id, game_uuid, seed, progress)
    if progress is None or progress < question_id:
        return {}, 403

    prompt, question, unit, image, interview = get_question(question_id, seed)
    return {
        "prompt": prompt,
        "question": question,
        "unit": unit,
        "image_url": image,
        "interview": interview,
    }


@app.post("/api/play")
@cross_origin()
def play():
    data = json.loads(request.data)
    action = data["action"]
    game_uuid = data["game_uuid"]
    question_id = data["question_id"]
    seed = data["seed"]

    progress = fetch_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    if action == "chat":
        question = data["question"][:75]
        interview_index = data["interview_index"]
        prompt = get_prompt(question_id, interview_index, seed)
        response = get_response(prompt, question)
        save_chat(question_id, question, response)
        return {"response": response}

    if action == "answer":
        answer = data["answer"]
        correct = get_answer(question_id, seed)
        is_correct = str(answer) == str(correct)
        clue = ""

        if is_correct:
            increment_game_progress(game_uuid, question_id)
        else:
            clue = get_clue(question_id)

        return {"is_correct": is_correct, "clue": clue}

    return {}, 400


# @app.get("/")
# def index():
#     return app.send_static_file("index.html")


if __name__ == "__main__":
    PORT = os.environ.get("PORT", 5000)
    app.run(threaded=True, host="0.0.0.0", port=PORT)
