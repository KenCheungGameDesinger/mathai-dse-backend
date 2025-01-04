# import pytesseract
import json
from pydantic import BaseModel, Field
from openai import OpenAI
import os

from typing import List


class OCRResponse(BaseModel):
    steps: List[str] = Field(..., description=("List of steps, each with LaTeX formatted"
                                               "Inside the steps:"
                                               "must directly express the student's solution step"
                                               "if there is no text, then no need to add"
                                               "The student's solution step, expressed explicitly. "
                                               r"Equations should use LaTeX formatting, making the mathematical operations clear. wrap text with '\text{}'"
                                               "every steps should only have one '=' equal symbol."
                                               "steps is recognition from image to text"
                                               r"if the image include text, then the step should wrap text with '\text{}'"
                                               r"use space `\ ` to separate text and mathematical expression, example: \text{for} \ y:"
                                               ))
    final_answer: str = Field(..., description="Final answer in LaTeX syntax, e.g. \text{The final answer is 42}")


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
                            r" you Must not nest math equation inside `\text{}`"
                            r"Incorrect: \\text{1. Simplify \\( \\left(\\frac{m^5 n^{-2}}{m^4 n^{-3}}\\right)^6 \\) and express your answer with positive indices}\\"
                            r"Incorrect: \\text{Evaluate:} \\int \\frac{2+x}{(1+x)^2} \\, dx"
                            r"Correct: \\text{Evaluate:} \\int \\frac{2+x}{(1+x)^2} dx"
                            r"Correct: \\text{1. Simplify } \\left( \\frac{m^5 n^{-2}}{m^4 n^{-3}} \\right)^6 \\text{ and express your answer with positive indices}"
                            r"if there is no mathematical problem, return empty string"
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


# 如果不准確，使用gpt-4o模型
def ocr_answers(image_file):
    API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=API_KEY)
    # img = client.images.analyze(url=image_file, feature_types=['text'])
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        temperature=0,
        response_format=OCRResponse,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            'Extract the answer in LaTeX format only.Return as a JSON with two keys:'
                            r"You should only return the exact content of the image in LaTeX format."
                            r"don't add other content that not showing in image and don't solve it"
                            r'- "steps": List of LaTeX-formatted steps; if there is text, then wrap sentences with `\text{}`.'
                            r"Example: \text{1. Subtract y from both sides: \newline <Latex formula>}"
                            r"Example: <Latex formula>}"
                            '- "final_answer": The final LaTeX answer.'
                            # "Extract the text or mathematical answer from the image in LaTeX format only. "
                            # "Use the following structure: "
                            # "- Wrap all equations in json format. "
                            # "- the response json have to include 'steps' and 'final_answer'"
                            # "- student might copy the question on top, but dont include it."
                            # "- steps means the middle steps that student write. Including his sentence for each step. put each single step in to a list."
                            # r"- Sentence in step is also in Latex format, the format should be display with mathquill, e.g. text: \text{},but dont use $"
                            # r"every text in json value should wrap '\text{...} in LaTex"
                            # "- final answer means the final answer written by student."
                            # "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
                            # "- don't add and prefix or suffix to wrap the json."
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
    return json.loads(response)
