from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import os

from .chat import get_response
from .database import create_game, update_game_progress, get_game_progress
from .questions import (
    get_question,
    get_answer,
    get_count,
    get_image,
    get_clue,
    get_game,
)


app = Flask(__name__)  # , static_folder="../frontend/dist/", static_url_path="/")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.get("/api/info")
@cross_origin()
def info():
    return {
        "question_count": get_count(),
    }


@app.post("/api/create")
@cross_origin()
def create():
    game_uuid, seed = get_game()
    create_game(game_uuid, seed)
    return {"game_uuid": game_uuid, "seed": seed}


@app.post("/api/start")
@cross_origin()
def start():
    data = json.loads(request.data)
    question_id = data.get("question_id")
    game_uuid = data["game_uuid"]
    seed = data.get("seed")

    progress = get_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    prompt, _, unit, image = get_question(question_id, seed)
    return {"prompt": prompt, "unit": unit, "image_url": image}


@app.post("/api/play")
@cross_origin()
def play():
    data = json.loads(request.data)
    action = data["action"]
    game_uuid = data["game_uuid"]
    question_id = data["question_id"]
    seed = data["seed"]

    progress = get_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    if action == "chat":
        question = data["question"]
        _, openapi_prompt, _, _ = get_question(question_id, seed)
        response = get_response(openapi_prompt, question)

        return {"response": response}

    if action == "answer":
        answer = data["answer"]
        correct = get_answer(question_id, seed)
        is_correct = str(answer) == str(correct)
        clue = ""

        if is_correct:
            update_game_progress(game_uuid, question_id + 1)
        else:
            clue = get_clue(question_id)

        return {"is_correct": is_correct, "clue": clue}

    return {}, 400


# @app.get("/")
# def index():
#     return app.send_static_file("index.html")


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    PORT = os.environ.get("PORT", 5000)
    app.run(threaded=True, host="0.0.0.0", port=PORT)
