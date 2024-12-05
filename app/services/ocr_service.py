# import pytesseract
from openai import OpenAI
import os


def perform_ocr(image_file):
    API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY)
    # img = client.images.analyze(url=image_file, feature_types=['text'])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract the text or mathematical problem from the image in LaTeX format only. "
                            "Use the following structure: "
                            "- place the sentence in one line."
                            "- dont add and prefix or suffix to wrap the sentence in a LaTeX environment."
                            "- Do not add any explanatory text outside of LaTeX."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_file}
                    },
                ],
            }
        ],
    )
    response = response.choices[0].message.content
    # print(response)
    return response
