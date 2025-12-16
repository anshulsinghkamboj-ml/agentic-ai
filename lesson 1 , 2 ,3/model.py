import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_PROMPT = (
    "Return JSON with:\n"
    "goal: string\n"
    "steps: list of strings\n"
    "done: boolean"
)

def call_model(prompt: str = BASE_PROMPT):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You output ONLY valid JSON. No commentary."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
