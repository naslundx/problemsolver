import random
import json

GENERAL_OPENAI_PROMPT = (
    "Svara alltid så kortfattat som möjligt. Svara inte på några uträkningar."
)

with open("backend/questions.json") as f:
    QUESTIONS = json.loads(f.read())


def get_count():
    return len(QUESTIONS)


def get_question(index):
    question = QUESTIONS[index]

    return (
        question["prompt"],
        question["openapi_prompt"] + GENERAL_OPENAI_PROMPT,
        question["unit"],
    )


def get_answer(index):
    question = QUESTIONS[index]

    return question["correct"]


def get_clue(index):
    question = QUESTIONS[index]

    return random.choice(question["clues"])


def get_image(index):
    question = QUESTIONS[index]

    return question["image"]
