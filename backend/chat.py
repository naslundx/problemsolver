import os
import openai


# Setup
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY


def get_response(openai_prompt, content):
    content = content.strip()
    if not content.endswith("?"):
        content += "?"

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": openai_prompt},
            {"role": "user", "content": content[:100]},
        ],
    )
    return chat_completion.choices[0].message.content
