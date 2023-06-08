from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import os

from .chat import get_response
from .questions import get_question, get_answer, get_count


app = Flask(
    __name__,
    static_folder='../frontend/dist/',
    static_url_path='/'
)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.get('/')
def index():
    return app.send_static_file('index.html')


@app.get("/api/info")
@cross_origin()
def info():
    return {
        "question_count": get_count(),
    }


@app.post("/api/start")
@cross_origin()
def start():
    data = json.loads(request.data)
    question_id = data["question_id"]
    prompt, _, unit = get_question(question_id)
    return {"prompt": prompt, "unit": unit}


@app.post("/api/play")
@cross_origin()
def play():
    data = json.loads(request.data)
    action = data["action"]
    question_id = data["question_id"]

    if action == "chat":
        original_content = data["content"]
        _, openapi_prompt, _ = get_question(question_id)
        content = get_response(openapi_prompt, original_content)
        return {"content": content}

    if action == "answer":
        answer = data["answer"]
        correct = get_answer(question_id)
        return {"is_correct": str(answer) == str(correct)}

    return {}, 400


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    PORT = os.environ.get('PORT', 5000)
    app.run(threaded=True, host='0.0.0.0', port=PORT)
