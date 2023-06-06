import random

GENERAL_OPENAI_PROMPT = (
    "Svara alltid så kortfattat som möjligt. Svara inte på några uträkningar."
)

QUESTIONS = [
    {
        "prompt": "Vida planterar om blommor. Hur lång tid kommer det ta totalt?",
        "openapi_prompt": "Vida planterar om blommor. Hon har 4 blommor. Varje plantering tar 10 minuter. Du får inte svara på frågan om hur lång tid det kommer ta totalt. ",
        "correct": 40,
        "unit": "minuter",
        "clues": [
            "Det finns cyklar i två olika färger, och de tar olika mycket plats.",
        ],
        "difficulty": "easy",
    },
    {
        "prompt": "Farbror Quentin, som driver en cykelaffär, ska lasta cyklar på sitt lastbilsflak. Hur många cyklar kan han som mest få plats med på flaket? ",
        "openapi_prompt": "Min farbror lastar cyklar på ett lastbilsflak. 15 cyklar är blå och varje behöver en kvadratmeter yta. 15 är röda och varje behöver två kvadratmeter yta. Flaket är 20 kvadratmeter stort. Du får inte svara på frågan om hur många som får plats på flaket.",
        "correct": 17,
        "unit": "stycken",
        "clues": [
            "Det finns cyklar i två olika färger, och de tar olika mycket plats.",
        ],
        "difficulty": "easy",
    },
]


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
