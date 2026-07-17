from dataclasses import dataclass
from typing import Any
from functools import lru_cache
from ftfy import fix_encoding
import re
import random
from .data import fetch_question


SPECIAL_VARS = {
    "F_NAME": ["Astrid", "Julia", "Cecilia", "Alice"],
    "M_NAME": ["Marcus", "Quention", "Lars", "David"],
}


@dataclass(frozen=True)
class Question:
    prompt: str
    question: str
    unit: str
    image: str
    chat: list[dict[str, Any]]


def _process_text(text: str, variables: dict[str, str] | None = None) -> str:
    if not variables:
        return fix_encoding(text)

    while True:
        match = re.search(r"\{\{(.*?)\}\}", text)
        if match is None:
            break

        data = match.groups()[0]
        start, end = match.span()

        for key, value in variables.items():
            data = data.replace(key, value)

        data = str(eval(data))  # pylint: disable=eval-used

        text = text[:start] + data + text[end:]

    return fix_encoding(text)


def get_question(question_id: int, seed: int | None = None) -> Question:
    question = fetch_question(question_id)
    variables = get_variables(question_id, seed)
    chat = question["chat"]
    for option in chat:
        option["name"] = _process_text(option["name"], variables)
        option["prompt"] = _process_text(option["prompt"], variables)

    return Question(
        prompt=_process_text(question["prompt"], variables),
        question=_process_text(question["question"]),
        unit=question["unit"],
        image=question["image"],
        chat=chat,
    )


def get_prompt(index: int, chat_index: int, seed: int | None = None) -> str:
    question = fetch_question(index)
    chat = question["chat"]
    variables = get_variables(index, seed)
    prompt = chat[chat_index]["prompt"]

    return _process_text(prompt, variables)


@lru_cache()
def get_variables(index: int, seed: int | None) -> dict[str, str]:
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


def get_answer(index: int, seed: int) -> str:
    question = fetch_question(index)
    variables = get_variables(index, seed)

    res = _process_text(question["correct"], variables)
    return str(res)


def get_clue(index: int) -> str:
    question = fetch_question(index)

    res = random.choice(question["clues"])
    return str(res)


# TODO store stats
