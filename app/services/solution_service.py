# import sympy as sp
import json

from openai import OpenAI
import os
from pydantic import BaseModel, Field
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def solve_math_problem(latex_equation):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    "Solve the given problem step by step in LaTeX format nested in JSON for expressing mathematics only. "
                    "Use the following structure: "
                    "- dont add and prefix or suffix to wrap the sentence in a LaTeX and json environment."
                    r"- every sentence should wrap by exact '\\text{}' but not '\\text{}' in Latex."
                    "- Do not add any explanatory text outside of LaTeX."
                    "- Wrap all equations in json format. "
                    "- the response json have to include 'topic', 'steps' and 'final answer'"
                    "- topics means the name of the problem in HKDSE mathematics. "
                    "- steps means the steps to solve the problem. Including instruction for each step. put each single step in to a list with Latex."
                    "- instructions in step is also in Latex format."
                    "- final answer means the final answer of the problem."
                    "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
                    "- don't add and prefix or suffix to wrap the json."
                    r"use '\newline' to break line for separating text sentences and math equation."
                    r"\\text{This step is incorrect because it does not relate to the original question.} \\text{You should start with the expression: } \\newline \\frac{(p^{4}q^{-3})^{5}}{p^{2}q^{-4}}."
                    "you must follow the habit in hand writing that start new line with each steps and each sentence with ':'"
                    "you should leave a space after text and before math equation"
                    # r"must put '\newline' before each '=' equal sign"
                    f"Problem: {latex_equation}"  # Dynamically embed the problem
                    "json format example: "
                    r'{"final answer": "m^{6} n^{6}","steps": ["\\text{Step 1: Start with the expression} \\newline \\left( \\frac{m^{5} n^{-2}}{m^{4} n^{-3}} \\right)^{6}","\\text{Step 2: Apply the power of a quotient rule} \\newline = \\frac{(m^{5} n^{-2})^{6}}{(m^{4} n^{-3})^{6}}","\\text{Step 3: Simplify the numerators and denominators using the power rule for exponents} \\newline = \\frac{m^{30} n^{-12}}{m^{24} n^{-18}}","\\text{Step 4: Apply the quotient rule for exponents on } m \\text{ and } n \\newline = m^{30-24} n^{-12 - (-18)}","\\text{Step 5: Simplify the exponents} \\newline = m^{6} n^{6}","\\text{Step 6: Write the final answer with positive indices} \\newline = m^{6} n^{6}"],"topic": "Simplifying Expressions with Indices" }'
                    "Latex Example: "
                    r'\\text{Simplify } \\left( \\frac{m^{5} n^{-2}}{m^{4} n^{-3}} \\right)^{6} \\text{ and express your answer with positive indices.}'
                )
            }
        ]
    )

    response = response.choices[0].message.content
    # print(response)
    return json.loads(response)


class StepEvaluation(BaseModel):
    step: str = Field(
        ...,
        description=(
            # "The student's solution step, expressed explicitly. "
            "The correct solution step for answering question"
            r"Equations should use LaTeX formatting, making the mathematical operations clear. wrap text with '\text{}'"
        )
    )
    correct: bool = Field(
        ...,
        description=(
            "A boolean indicating whether the step is correct. "
            "`True` if the step is correct, and `False` otherwise."
        )
    )
    comment: str = Field(
        ...,
        description=(
            r"if step is incorrect, comment the common mistakes with pure sentence wrap by \\text{}, no math in comment "
            "For correct steps, the comment highlights common mistakes to watch out for."
            r"Format the comment using math LaTeX formatting, making the mathematical operations clear. wrap text with '\text{}'"
            # r"use '\newline' to break line for separating text sentences and math equation."
            r"\\text{This step is incorrect because it does not relate to the original question. You should start with the expression: }"

        )
    )


class EvaluateOutput(BaseModel):
    steps: List[StepEvaluation] = Field(
        ...,
        description=(
            "A list of evaluations corresponding to each step in the student's solution. "
            "Each evaluation includes the step's correctness and feedback."
            r"use '\newline' to break line for beginning of a mathematical equation e.g. '=' or end of text with ':'"
            "don't make sentence with math equation in one line"
        )
    )
    final_answer: bool = Field(
        ...,
        description=(
            r"return true if student final answer is correct for answering the question"
        )
    )


def evaluate_student_answer(question, steps, final_answer):
    prompt = (
        "For each student step comment whether correct or not for answering the question, and command if not correct showing why incorrect and showing right steps. "
        "For correct comment showing remind about what student easy to fall in incorrect. "
        # "Use the following structure: "
        # r"- Wrap all equations in json format"
        # "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
        # r"- all value in the steps and comment should use Latex format capable"
        # r"- don't add and header to wrap the json. e.g. ```json"
        # "- Output for list corresponding each student step comment. "
        # "- key included: 'step', 'correct', 'comment'"
        # "your responese should can be parsed by json.loads."
        # "don't add ```json and ```"
        # "Example output: "
        # "[{'step': 'Simplify (m^5 * n^2)^6 / m^4 * n^3', 'correct': True, 'comment': 'Remind: student should be careful about the power of m and n'}, "
        # "{'step': 'Simplify (m^7 * n^2)^6 / m^3 * n^4', 'correct': False, 'comment': 'Incorrect: the power of m and n are not changed. Right steps are: Simplify (m^5 * n^3)^6 / m^5 * n^2'}, "
        # r"{'step': 'Simplify (m^5 * n^3)^6 / m^5 * n^2', 'correct': True, 'comment': '...'}]"
    )
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            response_format=EvaluateOutput,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": json.dumps({"question": question, "steps": steps, "answer": final_answer})
                }
            ]
        )

        response = response.choices[0].message.content
        # print(response)
        return json.loads(response)

    except Exception as e:
        print(e)
        return str(e)
