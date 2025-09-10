from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import os

from src.chat import get_response
from src.settings import MAX_QUESTION_LENGTH
from src.data import (
    create_game,
    increment_game_progress,
    fetch_game_progress,
    fetch_question_count,
    load_seed_from_game_uuid,
    save_chat,
)
from src.questions import (
    get_question,
    get_answer,
    get_clue,
    get_prompt,
)
from src.helpers import generate_uuid_and_seed


app = Flask(__name__, static_folder="../frontend/dist/", static_url_path="/")
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
        "game_progress": question_id,
    }


@app.get("/api/progress")
@cross_origin()
def progress():
    game_uuid = request.args.get("game_uuid")
    progress = fetch_game_progress(game_uuid)
    return {
        "game_uuid": game_uuid,
        "game_progress": progress
    }


@app.post("/api/start")
@cross_origin()
def start():
    data = json.loads(request.data)
    question_id = data.get("question_id")
    game_uuid = data.get("game_uuid")

    progress = fetch_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    seed = load_seed_from_game_uuid(game_uuid)
    question = get_question(question_id, seed)
    return {
        "game_uuid": game_uuid,
        "prompt": question.prompt,
        "question": question.question,
        "unit": question.unit,
        "image_url": question.image,
        "interview": question.interview,
    }


@app.post("/api/chat")
@cross_origin()
def chat():
    data = json.loads(request.data)
    game_uuid = data.get("game_uuid")
    question_id = data.get("question_id")

    progress = fetch_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    seed = load_seed_from_game_uuid(game_uuid)
    question = data.get("question")[:MAX_QUESTION_LENGTH]
    interview_index = data.get("interview_index")
    prompt = get_prompt(question_id, interview_index, seed)
    response = get_response(prompt, question)
    save_chat(question_id, question, response)

    return {
        "game_uuid": game_uuid,
        "question": question,
        "response": response
    }

@app.post("/api/answer")
@cross_origin()
def answer():
    data = json.loads(request.data)
    game_uuid = data.get("game_uuid")
    question_id = data.get("question_id")

    progress = fetch_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    seed = load_seed_from_game_uuid(game_uuid)
    answer = data.get("answer")
    correct_answer = get_answer(question_id, seed)
    is_correct = str(answer) == str(correct_answer)
    clue = ""

    if is_correct:
        increment_game_progress(game_uuid, question_id)
    else:
        clue = get_clue(question_id)

    return {
        "game_uuid": game_uuid,
        "is_correct": is_correct,
        "clue": clue
    }


@app.get("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", "5000"))
    app.run(threaded=True, port=PORT)
