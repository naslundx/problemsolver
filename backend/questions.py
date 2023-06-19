import json
import re
import random
from datetime import datetime

GENERAL_OPENAI_PROMPT = (
    "Svara alltid så kortfattat som möjligt. Svara inte på några uträkningar."
)

with open("backend/questions.json") as f:
    QUESTIONS = json.loads(f.read())

SPECIAL_VARS = {"F_NAME": ["Vida", "Matilda", "Julia", "Cecilia"]}


def _process_text(text, variables):
    if len(variables) == 0:
        return text

    while True:
        match = re.search("\{\{(.*?)\}\}", text)
        if match is None:
            break

        data = match.groups()[0]
        start, end = match.span()

        for key, value in variables.items():
            data = data.replace(key, value)

        try:
            data = str(eval(data))
        except:
            pass

        text = text[:start] + data + text[end:]

    return text


def get_count():
    return len(QUESTIONS)


def get_seed():
    date = datetime.utcnow() - datetime(1970, 1, 1)
    seconds = date.total_seconds()
    milliseconds = round(seconds * 1000)
    return milliseconds


def get_question(index, seed=None):
    question = QUESTIONS[index]
    variables = get_variables(index, seed)

    return (
        _process_text(question["prompt"], variables),
        _process_text(question["openapi_prompt"] + GENERAL_OPENAI_PROMPT, variables),
        question["unit"],
    )


def get_variables(index, seed=None):
    if seed is not None:
        random.seed(seed)

    result = {}
    question = QUESTIONS[index]

    if "variables" in question:
        for key, values in question["variables"].items():
            if key == "other":
                for item in values:
                    result[item] = random.choice(SPECIAL_VARS[item])
                continue

            result[key] = str(random.randint(values[0], values[1]))

    return result


def get_answer(index, seed=None):
    question = QUESTIONS[index]
    variables = get_variables(index, seed)

    return _process_text(question["correct"], variables)


def get_clue(index):
    question = QUESTIONS[index]

    return random.choice(question["clues"])


def get_image(index):
    question = QUESTIONS[index]

    return question["image"]
