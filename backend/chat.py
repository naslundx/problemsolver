import os
import openai


API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY


GENERAL_OPENAI_PROMPT = "Följande regler är jätteviktiga. Svara alltid så kortfattat som möjligt. Svara inte på några uträkningar. Om du inte förstår, svara bara 'Jag förstår inte'. Om du inte vet eller inte får svara, svara bara 'Jag vet inte'. Nu till min fråga:"


def get_response(openai_prompt, content):
    content = content.strip()
    if not content.endswith("?"):
        content += "?"

    full_prompt = f"{openai_prompt} {GENERAL_OPENAI_PROMPT} {content[:100]}"

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # "gpt-4"
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=250,
        # lower values like 0.2 will make it more focused and deterministic.
        temperature=0.25,
        # Positive values penalize new tokens based on whether they appear in the text so far,
        # increasing the model's likelihood to talk about new topics.
        presence_penalty=-0.5,
    )
    return chat_completion.choices[0].message.content
