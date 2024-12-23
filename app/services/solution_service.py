# import sympy as sp
import json

from openai import OpenAI
import os
from pydantic import BaseModel, Field
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# class SolutionModel(BaseModel):
#     steps: List[str] = Field(..., description="List of solution steps in LaTeX format.")
#     final_answer: str = Field(..., description="The final answer in LaTeX format.")

def solve_math_problem(latex_equation):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # model="ft:gpt-4o-2024-08-06:exmersive::AhbDUq1W",
        messages=[
            # {
            #     "role": "user",
            #     "content": (
            #         "Solve the given problem step by step in LaTeX format nested in JSON for expressing mathematics only. "
            #         "Use the following structure: "
            #         "- dont add and prefix or suffix to wrap the sentence in a LaTeX and json environment."
            #         r"- every sentence should wrap by exact '\\text{}' but not '\\text{}' in Latex."
            #         "- Do not add any explanatory text outside of LaTeX."
            #         "- Wrap all equations in json format. "
            #         "- the response json have to include 'topic', 'steps' and 'final answer'"
            #         "- topics means the name of the problem in HKDSE mathematics. "
            #         "- steps means the steps to solve the problem. Including instruction for each step. put each single step in to a list with Latex."
            #         "- instructions in step is also in Latex format."
            #         "- final answer means the final answer of the problem."
            #         "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
            #         "- don't add and prefix or suffix to wrap the json."
            #         r"use '\newline' to break line for separating text sentences and math equation."
            #         r"\\text{This step is incorrect because it does not relate to the original question.} \\text{You should start with the expression: } \\newline \\frac{(p^{4}q^{-3})^{5}}{p^{2}q^{-4}}."
            #         "you must follow the habit in hand writing that start new line with each steps and each sentence with ':'"
            #         "you should leave a space after text and before math equation"
            #         # r"must put '\newline' before each '=' equal sign"
            #         f"Problem: {latex_equation}"  # Dynamically embed the problem
            #         "json format example: "
            #         r'{"final answer": "m^{6} n^{6}","steps": ["\\text{Step 1: Start with the expression} \\newline \\left( \\frac{m^{5} n^{-2}}{m^{4} n^{-3}} \\right)^{6}","\\text{Step 2: Apply the power of a quotient rule} \\newline = \\frac{(m^{5} n^{-2})^{6}}{(m^{4} n^{-3})^{6}}","\\text{Step 3: Simplify the numerators and denominators using the power rule for exponents} \\newline = \\frac{m^{30} n^{-12}}{m^{24} n^{-18}}","\\text{Step 4: Apply the quotient rule for exponents on } m \\text{ and } n \\newline = m^{30-24} n^{-12 - (-18)}","\\text{Step 5: Simplify the exponents} \\newline = m^{6} n^{6}","\\text{Step 6: Write the final answer with positive indices} \\newline = m^{6} n^{6}"],"topic": "Simplifying Expressions with Indices" }'
            #         "Latex Example: "
            #         r'\\text{Simplify } \\left( \\frac{m^{5} n^{-2}}{m^{4} n^{-3}} \\right)^{6} \\text{ and express your answer with positive indices.}'
            #     )
            # }
            {
                "role": "system",
                "content": """
                The assistant is a math tutor that provides detailed, step-by-step solutions to math problems. 
                All responses must be in JSON format and include:
                1. `steps`: A list of solution steps, formatted in logical order.
                2. `final_answer`: The final answer to the problem.
                3. `topic`: Chapter in HKDSE
                Latex content:
                - use `\\newline` to before `=` and `:` 
                - use space between text and mathematical expression: 'text\\'
                All mathematical expressions must use LaTeX syntax compatible with React-MathQuill. 
                Handle invalid or incomplete inputs gracefully by returning an error message in JSON format, explaining the issue.
                Steps logic by Topics:
                - Algebraic Exponents with Rational Expression
                1. Apply exponent rules: Multiply powers in the fraction
                2. Apply quotient rule: Subtract exponents with the same base
                3. Convert negative exponents: Rewrite as positive exponents
                4. Write final answer: Simplify and present in standard form
                - 
                """
            },
            {
                "role": "user",
                "content": (
                    "response json format example: "
                    "{{steps:str[], final_answer:str}, topic: str}"
                    r'{{"final answer": "m^{6} n^{6}","steps": ["\\text{Step 1: Start with the expression} \\newline \\left( \\frac{m^{5} n^{-2}}{m^{4} n^{-3}} \\right)^{6}","\\text{Step 2: Apply the power of a quotient rule} \\newline = \\frac{(m^{5} n^{-2})^{6}}{(m^{4} n^{-3})^{6}}","\\text{Step 3: Simplify the numerators and denominators using the power rule for exponents} \\newline = \\frac{m^{30} n^{-12}}{m^{24} n^{-18}}","\\text{Step 4: Apply the quotient rule for exponents on } m \\text{ and } n \\newline = m^{30-24} n^{-12 - (-18)}","\\text{Step 5: Simplify the exponents} \\newline = m^{6} n^{6}","\\text{Step 6: Write the final answer with positive indices} \\newline = m^{6} n^{6}"],"topic": "Simplifying Expressions with Indices" }}'
                )},
            {
                "role": "user",
                "content": f"Problem: {latex_equation}"
            }
        ]
    )

    response = response.choices[0].message.content
    response = response.replace("```json", "").replace("```", "")

    print(response)
    return json.loads(response)


class StepEvaluation(BaseModel):
    step: str = Field(
        ...,
        description=(
            # "The student's solution step, expressed explicitly. "
            "The correct solution step for answering question"
            "Equations should be pure math latex, and every step should start with '='"
            # r"Equations should use LaTeX formatting, making the mathematical operations clear. wrap text with '\text{}'"
        )
    )
    correct: bool = Field(
        ...,
        description=(
            "A boolean indicating whether the step is correct for answering question. "
            "correct is not only mathematically correct but also related to the original question."
            "`True` if the step is correct, and `False` otherwise."
        )
    )
    comment: str = Field(
        ...,
        description=(
            r"if step is incorrect for answering question, give pure text explanation with \\text{}"
            "For correct steps, leave it blank."
            # r"Format the comment using math LaTeX formatting, making the mathematical operations clear. wrap text with '\text{}'"
            # r"use '\newline' to break line for separating text sentences and math equation."
            r"\\text{This step is incorrect because it does not relate to the original question. You should ... the expression: }"

        )
    )


class EvaluateOutput(BaseModel):
    steps: List[StepEvaluation] = Field(
        ...,
        description=(
            "A list of evaluations corresponding to each step in the student's solution. "
            "steps is telling what is answer if student is incorrect for questions."
            # "Each evaluation includes the step's correctness and feedback."
            # r"use '\newline' to break line for beginning of a mathematical equation e.g. '=' or end of text with ':'"
            # "don't make sentence with math equation in one line"
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
        "You are a teacher evaluating a student's solution to a math problem. "
        "View every single steps of the student's steps and final_answer. "
        "Student works should answering the question"
        "You should tell three things in steps:"
        "- For each step, tell whether is this student step correct or not by 'correct':bool"
        r"- if step is incorrect, put the correct steps in 'comment':string"
        " Finally, tell whether the final answer is correct or not by 'final_answer':bool"
        "criteria for each step:"
        "- if the step is not related to the original question, then it is incorrect, then the following comment should be the correct steps"
        "- if the step is related to the original question, and the step is incorrect, then the following comment should be the correct steps"
        "eventually, student can compare their own steps and correct steps with each other"
        "Steps logic by Topics:"
        "- Algebraic Exponents with Rational Expression"
        "1. Apply exponent rules: Multiply powers in the fraction"
        "2. Apply quotient rule: Subtract exponents with the same base"
        "3. Convert negative exponents: Rewrite as positive exponents"
        "4. Write final answer: Simplify and present in standard form"
        "reply examples: "
        r"{steps:[{step:string, correct:bool, comment:string}], final_answer:bool}"
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
