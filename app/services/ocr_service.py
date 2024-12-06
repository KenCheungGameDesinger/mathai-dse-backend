# import pytesseract
import json

from openai import OpenAI
import os


def ocr_questions(image_file):
    API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY)
    # img = client.images.analyze(url=image_file, feature_types=['text'])
    response = client.chat.completions.create(
        model="gpt-4o",
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
                            r"- every sentence should wrap by exact '\text{}' in Latex, no double slash."
                            "Latex should be have single slash."
                            "- Do not add any explanatory text outside of LaTeX."
                            "Latex format: "
                            r"- response in latex should use '\text{}' in Latex."
                            r"- dont use double-slash to wrap the sentence in Latex."
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
    print(response)
    return response


def ocr_answers(image_file):
    API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY)
    # img = client.images.analyze(url=image_file, feature_types=['text'])
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract the text or mathematical answer from the image in LaTeX format only. "
                            "Use the following structure: "
                            "- Wrap all equations in json format. "
                            "- the response json have to include 'steps' and 'final_answer'"
                            "- student might copy the question on top, but dont include it."
                            "- steps means the middle steps that student write. Including his sentence for each step. put each single step in to a list."
                            r"- Sentence in step is also in Latex format, the format should be display with mathquill, e.g. text: \text{},but dont use $"
                            r"every text in json value should wrap '\text{...} in LaTex"
                            "- final answer means the final answer written by student."
                            "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
                            "- don't add and prefix or suffix to wrap the json."
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
    print(response)
    return json.loads(response)
