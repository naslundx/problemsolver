from flask import Flask, request
import os

from src.chat import get_response
from src.settings import DEBUG, MAX_QUESTION_LENGTH
from src.data import (
    create_game,
    increment_game_progress,
    fetch_game_progress,
    fetch_question_count,
    fetch_seed_from_game_uuid,
    save_chat,
)
from src.questions import (
    get_question,
    get_answer,
    get_clue,
    get_prompt,
)
from src.helpers import generate_uuid_and_seed, is_valid_uuid


app = Flask(__name__, static_folder="../frontend/dist/", static_url_path="/")


if DEBUG:
    print("Debug version is running!")


@app.get("/api/info")
def info():
    return {
        "question_count": fetch_question_count(),
    }


@app.route("/api/game", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        game_uuid, seed = generate_uuid_and_seed()
        create_game(game_uuid, seed, 0)
    else:
        game_uuid = request.args.get("game_uuid")
        if not game_uuid or not is_valid_uuid(game_uuid):
            return {}, 400

    progress = (
        fetch_game_progress(game_uuid) if not DEBUG else (fetch_question_count() - 1)
    )

    return {
        "game_uuid": game_uuid,
        "game_progress": progress,
    }


@app.post("/api/start")
def start():
    data = request.get_json(silent=True) or {}
    question_id = data.get("question_id")
    game_uuid = data.get("game_uuid")

    if not game_uuid or not is_valid_uuid(game_uuid) or question_id is None:
        return {}, 400

    if not DEBUG:
        progress = fetch_game_progress(game_uuid)
        if question_id > progress + 1:
            return {}, 403

    seed = fetch_seed_from_game_uuid(game_uuid)
    question = get_question(question_id, seed)
    return {
        "game_uuid": game_uuid,
        "prompt": question.prompt,
        "question": question.question,
        "unit": question.unit,
        "image_url": question.image,
        "chat": question.chat,
    }


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    if (
        "question" not in data
        or "chat_index" not in data
        or "game_uuid" not in data
        or "question_id" not in data
    ):
        return {}, 400

    game_uuid = data.get("game_uuid")
    if not is_valid_uuid(game_uuid):
        return {}, 400
    question_id = data.get("question_id")

    if not DEBUG:
        progress = fetch_game_progress(game_uuid)
        if progress < question_id:
            return {}, 403

    seed = fetch_seed_from_game_uuid(game_uuid)
    question = data.get("question")[:MAX_QUESTION_LENGTH]
    chat_index = data.get("chat_index")
    prompt = get_prompt(question_id, chat_index, seed)
    response = get_response(prompt, question)
    save_chat(game_uuid, chat_index, question_id, question, response)

    return {"game_uuid": game_uuid, "question": question, "response": response}


@app.post("/api/answer")
def submit_answer():
    data = request.get_json(silent=True) or {}
    game_uuid = data.get("game_uuid")
    question_id = data.get("question_id")

    if not game_uuid or not is_valid_uuid(game_uuid) or question_id is None:
        return {}, 400

    if not game_uuid or question_id is None:
        return {}, 400

    progress = fetch_game_progress(game_uuid)
    if progress < question_id:
        return {}, 403

    seed = fetch_seed_from_game_uuid(game_uuid)
    answer = data.get("answer")
    correct_answer = get_answer(question_id, seed)
    is_correct = str(answer) == str(correct_answer)
    clue = ""

    if is_correct:
        increment_game_progress(game_uuid, question_id)
    else:
        clue = get_clue(question_id)

    return {"game_uuid": game_uuid, "is_correct": is_correct, "clue": clue}


@app.get("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", threaded=True, port=PORT)
