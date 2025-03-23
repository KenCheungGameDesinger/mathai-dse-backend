# import pytesseract
import json
from pydantic import BaseModel, Field
from openai import OpenAI
import os

from typing import List

from app import client_deepseek, client_openai
from app.managers.agents import agent_manager



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
    # API_KEY = os.getenv("OPENAI_API_KEY")
    # client = OpenAI(api_key=API_KEY)
    # img = client.images.analyze(url=image_file, feature_types=['text'])

    # region
    response = client_openai.chat.completions.create(
        model="gpt-4-turbo",
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
                            "Latex should be have single slash."
                            "- Do not add any explanatory text outside of LaTeX."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": str(image_file)}
                    },
                ],
            }
        ],
    )
    response = response.choices[0].message.content
    # endregion

    prompt = f"""
        convert math statement part to validated latex format with text, but dont solve it. dont add additional text.
        keep the instructions text or objectives of math question.
        `{response}`
        
        Requirement:
        your response should containt all text and latex.
        use block mode `$$` containt all the content
        Example:
        Simplify <latex> and express the answer...
        """
    print("prompt",prompt)
    response = agent_manager.math_agent.run(prompt)
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
