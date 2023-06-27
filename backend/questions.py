from functools import lru_cache
import json
import re
import random
import uuid
from datetime import datetime
from .database import fetch_question, fetch_question_count


GENERAL_OPENAI_PROMPT = (
    "Svara alltid så kortfattat som möjligt. Svara inte på några uträkningar."
)

# with open("backend/questions.json") as f:
#     QUESTIONS = json.loads(f.read())

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
    return fetch_question_count()


def get_question(index, seed=None):
    question = fetch_question(index)
    variables = get_variables(index, seed)

    return (
        _process_text(question["prompt"], variables),
        question["unit"],
        question["image"],
    )


def get_prompt(index, seed=None):
    question = fetch_question(index)
    variables = get_variables(index, seed)
    return _process_text(question["openapi_prompt"] + GENERAL_OPENAI_PROMPT, variables)


@lru_cache()
def get_variables(index, seed=None):
    if seed is not None:
        random.seed(seed)

    result = {}
    question = fetch_question(index)

    if "variables" in question:
        for key, values in question["variables"].items():
            if key == "other":
                for item in values:
                    result[item] = random.choice(SPECIAL_VARS[item])
                continue

            result[key] = str(random.randint(values[0], values[1]))

    return result


def get_answer(index, seed=None):
    question = fetch_question(index)
    variables = get_variables(index, seed)

    return _process_text(question["correct"], variables)


def get_clue(index):
    question = fetch_question(index)

    return random.choice(question["clues"])


# TODO store stats