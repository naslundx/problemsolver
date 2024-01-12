from functools import lru_cache
import json
import re
import random
import uuid
from datetime import datetime
from .database import fetch_question, fetch_question_count


SPECIAL_VARS = {
    "F_NAME": ["Astrid", "Julia", "Cecilia", "Alice"],
    "M_NAME": ["Marcus", "Quention", "Lars", "David"],
}


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


def get_question(question_id, seed=None):
    question = fetch_question(question_id)
    interview = question["interview"]
    variables = get_variables(question_id, seed)
    for option in interview:
        option["name"] = _process_text(option["name"], variables)
        option["prompt"] = _process_text(option["prompt"], variables)

    return (
        _process_text(question["prompt"], variables),
        question["question"],
        question["unit"],
        question["image"],
        interview,
    )


def get_prompt(index, interview_index, seed=None):
    question = fetch_question(index)
    interview = question["interview"]
    variables = get_variables(index, seed)
    prompt = interview[interview_index]["prompt"]

    return _process_text(prompt, variables)


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
