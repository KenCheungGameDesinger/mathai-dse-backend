# import sympy as sp
import json

from openai import OpenAI
import os
from pydantic import BaseModel, Field
from typing import List

from app import client_deepseek

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SolutionModel(BaseModel):
    steps: List[str] = Field(..., description=(
        "steps is List of string that solution steps in string math LaTeX format. Not JSON."
        "Do not include JSON or dictionary in the steps, it should be a list of string in math latex."
        "inside the steps, it should not be a JSON or dictionary, it should be a list of string in math latex."

    ))
    final_answer: str = Field(..., description=(
        "The final answer is a string in math LaTeX format. Not JSON"
        "Do not include JSON or dictionary in the final_answer, it should be a string in math latex."
        "inside the final_answer, it should not be a JSON or dictionary, it should be a string in math latex."
    ))
    topic: str = Field(..., description=("You can only use this topic: "
                                         "- Algebraic Exponents with Rational Expression"
                                         "- Rearranging algebraic formulas"
                                         "- Greatest Common Factor (GCF)"
                                         ))


def solve_math_problem_deepseek(latex_equation):
    Model_ID = "deepseek-chat"
    prompt = (
        """
        The assistant is a math tutor that provides detailed, step-by-step solutions to math problems. 
        The steps is not need to repeat the question and dont include final answer. 
        Latex content:
        - MUST use `\\newline` to before `=` and `:` in **beginning** and between of calculations, NOT **last**; e.g.: `... \newline`=...
        - dont use slashes at the end of sentence for steps
        - use `\text{}` to wrap text.
        - r"Incorrect: \\text{1. Simplify \\( \\left(\\frac{m^5 n^{-2}}{m^4 n^{-3}}\\right)^6 \\) and express your answer with positive indices}\\"
        - r"Correct: \\text{1. Simplify } \\left( \\frac{m^5 n^{-2}}{m^4 n^{-3}} \\right)^6 \\text{ and express your answer with positive indices}"
        All mathematical expressions must use LaTeX syntax compatible with React-MathQuill. 
        Steps logic by Topics:
        - Algebraic Exponents with Rational Expression
        1. Apply exponent rules: Multiply powers in the fraction
        2. Apply quotient rule: Subtract exponents with the same base
        3. Convert negative exponents: Rewrite as positive exponents
        4. Write final answer: Simplify and present in standard form
        - Rearranging algebraic formulas
        1: Isolate the term with the subject in one side
        2 : Multiply through with -1 to give you a positive equation
        3: Combine the right-hand side and find a common denomin ator
        4: Take the reciprocal of both side to solve for subject
        - Greatest Common Factor (GCF)
        1: Identify difference squares of factor that divides all the terms in an exp ression
        2: Use the previous factorize answer in exp ression 
        3: Factor out common terms by grouping
        e.g. question: \\text{Factorize }\\ m^2-4n^2+5m+10n final_answer: (m+2n)(m-2n+5)
        EXAMPLE JSON OUTPUT:
        {
            "final_answer": "\\frac{r^{13}}{s^{13}}",
            "steps": [
                "\\text{1. Apply exponent rules: } \\left( r^3s^{-2} \\right)^4 \\text{ becomes:} \\newline = r^{3\\cdot4}s^{-2\\cdot4}\\newline = r^{12}s^{-8}",
                "\\text{2. Combine with the denominator:} \\newline = \\frac{r^{12}s^{-8}}{r^{-1}s^5}",
                "\\text{3. Apply quotient rule: } \\newline = r^{12-(-1)}s^{-8-5}\\newline = r^{12+1}s^{-8-5}\\newline = r^{13}s^{-13}",
                "\\text{4. Convert negative exponents: Rewrite as positive indices} \\newline = r^{13}\\cdot\\frac{1}{s^{13}}",
                "\\text{5. Simplify: } \\newline = \\frac{r^{13}}{s^{13}}"
            ],
            "topic": "Algebraic Exponents with Rational Expression"
        }
        """
    )
    try:
        response = client_deepseek.chat.completions.create(
            model=Model_ID,
            response_format={
                'type': 'json_object'
            },
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"Problem: {latex_equation}"
                }
            ]
        )

        response = response.choices[0].message.content
        # print(type(json.loads(response)))
        # print(json.loads(response))
        response_json = json.loads(response)
        return response_json, Model_ID

    except Exception as e:
        print(e)
        return str(e)


def solve_math_problem_openai(latex_equation):
    # Model_ID = "ft:gpt-4o-2024-08-06:exmersive:solve:AheNBEHi"
    Model_ID = "gpt-4o-2024-08-06"
    #         All responses must be in JSON format and include:
    #         1. `steps`: A list of solution steps, formatted in logical order.
    #         2. `final_answer`: The final answer to the problem.
    #         3. `topic`: Chapter in HKDSE
    prompt = (
        """
        The assistant is a math tutor that provides detailed, step-by-step solutions to math problems. 
        The steps is not need to repeat the question and dont include final answer. 
        Latex content:
        - MUST use `\\newline` to before `=` and `:` in **beginning** and between of calculations, NOT **last**; e.g.: `... \newline`=...
        - dont use slashes at the end of sentence for steps
        - use `\text{}` to wrap text.
        - r"Incorrect: \\text{1. Simplify \\( \\left(\\frac{m^5 n^{-2}}{m^4 n^{-3}}\\right)^6 \\) and express your answer with positive indices}\\"
        - r"Correct: \\text{1. Simplify } \\left( \\frac{m^5 n^{-2}}{m^4 n^{-3}} \\right)^6 \\text{ and express your answer with positive indices}"
        All mathematical expressions must use LaTeX syntax compatible with React-MathQuill. 
        Steps logic by Topics:
        - Algebraic Exponents with Rational Expression
        1. Apply exponent rules: Multiply powers in the fraction
        2. Apply quotient rule: Subtract exponents with the same base
        3. Convert negative exponents: Rewrite as positive exponents
        4. Write final answer: Simplify and present in standard form
        - Rearranging algebraic formulas
        1: Isolate the term with the subject in one side
        2 : Multiply through with -1 to give you a positive equation
        3: Combine the right-hand side and find a common denomin ator
        4: Take the reciprocal of both side to solve for subject
        - Greatest Common Factor (GCF)
        1: Identify difference squares of factor that divides all the terms in an exp ression
        2: Use the previous factorize answer in exp ression 
        3: Factor out common terms by grouping
        e.g. question: \\text{Factorize }\\ m^2-4n^2+5m+10n final_answer: (m+2n)(m-2n+5)
        """
    )
    try:
        response = client.beta.chat.completions.parse(
            model=Model_ID,
            response_format=SolutionModel,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"Problem: {latex_equation}"
                }
            ]
        )

        response = response.choices[0].message.content
        # print(type(json.loads(response)))
        # print(json.loads(response))
        response_json = json.loads(response)
        return response_json, Model_ID

    except Exception as e:
        print(e)
        return str(e)


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
            "criteria for each step:"
            "- if the step is not related to the original question, then it is incorrect, then the following comment should be the correct steps"
            "- if the step can be the step answering the question, and the step is calculating correctly, then the following comment should be the correct steps"
            "- even the steps is not your expecting steps, but it's right then say this is correct steps"
        )
    )
    comment: str = Field(
        ...,
        description=(
            r"if step is incorrect for answering question, give explanation with \\text{}"
            "and state the correct mathematical expression step in Latex format"
            "use strictly Latex format"
            "use `\\` to put space between text and mathematical expression"
            "For correct steps, leave it blank."
            "- MUST use `\\newline` to before `=` and `:` in beginning and between of calculations"
            # r"Format the comment using math LaTeX formatting, making the mathematical operations clear. wrap text with '\text{}'"
            # r"use '\newline' to break line for separating text sentences and math equation."
            r"\\text{This step is incorrect because it does not relate to the original question. You should ... the expression: }"
            r"\\text{explaination...:} \newline \\frac{(p^{4}q^{-3})^{5}}{p^{2}q^{-4}}."

        )
    )


class EvaluateOutput(BaseModel):
    steps: List[StepEvaluation] = Field(
        ...,
        description=(
            "A list of evaluations corresponding to each step in the student's solution. "
            "steps is telling what is answer if student is incorrect for questions."
            "step is telling student what is correct steps for answering question."
            # "Each evaluation includes the step's correctness and feedback."
            # r"use '\newline' to break line for beginning of a mathematical equation e.g. '=' or end of text with ':'"
            # "don't make sentence with math equation in one line"
        )
    )
    final_answer: bool = Field(
        ...,
        description=(
            r"return true if student final_answer is the solution of the question"
            "ignore the whether the steps is correct or not"
        )
    )


def evaluate_student_answer(question, steps, final_answer):
    # Model_ID = "ft:gpt-4o-2024-08-06:exmersive:solve:AheNBEHi"
    Model_ID = "gpt-4o-2024-08-06"
    prompt = (
        """
        You are an evaluator of a student's math solution. Carefully review all the provided steps and the final answer. For each step:
        - Indicate whether it is correct (`correct`: true/false).
        - If the step is incorrect, explain why and provide the corrected step (`comment`).
        
        **Guidelines**:
        1. If a step is not logically connected to the problem, mark it incorrect and provide the correct continuation and you must show in comment that "".
        2. If a step is mathematically valid (even if not your expected approach), mark it correct.
        3. Only mark a step incorrect if there is a clear mistake in logic, calculation, or relevance to the problem.
        4. Allow skip steps
        
        Finally, evaluate the final answer:
        - Indicate whether the final answer is correct (`final_answer`: true/false).
        
        **Example Output**:
        ```json
        {
          "steps": [
            {"step": "Step description", "correct": true/false, "comment": "Explanation of correctness or corrections"}
          ],
          "final_answer": true/false
        }

        """
    )
    try:
        response = client.beta.chat.completions.parse(
            # model="gpt-4o-2024-08-06",
            model=Model_ID,
            response_format=EvaluateOutput,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": (
                        f"Problem: {question}"
                        f"Steps: {steps}"
                        f"Final Answer: {final_answer}"
                    )
                }
            ]
        )

        response = response.choices[0].message.content
        # print(type(json.loads(response)))
        # print(json.loads(response))
        response_json = json.loads(response)
        # response_json["model"] = "ft:gpt-4o-2024-08-06:exmersive:solve:AheNBEHi"
        return response_json, Model_ID

    except Exception as e:
        print(e)
        return str(e)
