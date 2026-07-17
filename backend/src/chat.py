from openai import OpenAI
from typing import Iterable
from openai.types.chat import ChatCompletionMessageParam
from .helpers import get_env_key


OPENAI_API_KEY = get_env_key("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


GENERAL_OPENAI_PROMPT = """
Följande regler är jätteviktiga:
    - Svara alltid så kortfattat som möjligt.
    - Svara inte på några uträkningar.
    - Om du inte förstår, svara bara 'Jag förstår inte'.
    - Om du inte vet, svara bara 'Jag vet inte'.

Nu till min fråga:
"""


def get_response(openai_prompt: str, content: str) -> str:
    content = content.strip()
    if not content.endswith("?"):
        content += "?"

    full_prompt = f"{openai_prompt} {GENERAL_OPENAI_PROMPT} {content[:100]}"
    messages: Iterable[ChatCompletionMessageParam] = [
        {"role": "user", "content": full_prompt}
    ]

    chat_completion = client.chat.completions.create(
        model=get_env_key("OPENAI_MODEL") or "gpt-4o-mini",
        messages=messages,
    )
    return chat_completion.choices[0].message.content or ""
