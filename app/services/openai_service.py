import os
import requests
from openai import OpenAI
def generate_completion(prompt):
    API_KEY = os.getenv("OPENAI_API_KEY")
    print(API_KEY)
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
    )

    return response.choices[0].message.content
