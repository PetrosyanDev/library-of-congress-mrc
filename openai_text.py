from openai import OpenAI
import json

with open("secrets.json", "r") as f:
    key = json.loads(f.read())

client = OpenAI(api_key=key["api_key"])

def GenerateText(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Provide a concise book description in a single paragraph without quotes, book title, author name, or line breaks"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content

