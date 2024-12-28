# import sympy as sp
import json

from openai import OpenAI
import os
from pydantic import BaseModel, Field
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SolutionModel(BaseModel):
    steps: List[str] = Field(..., description="List of solution steps in LaTeX format.")
    final_answer: str = Field(..., description="The final answer in LaTeX format.")

def solve_math_problem(latex_equation):
    Model_ID = "ft:gpt-4o-2024-08-06:exmersive:solve:AheNBEHi"
    # Model_ID = "gpt-4o-mini"
    response = client.chat.completions.create(
        model=Model_ID,
        # model="ft:gpt-4o-2024-08-06:exmersive:solve:AheNBEHi",
        messages=[
            {
                "role": "system",
                "content": """
                The assistant is a math tutor that provides detailed, step-by-step solutions to math problems. 
                The steps is not need to repeat the question and dont include final answer. 
                All responses must be in JSON format and include:
                1. `steps`: A list of solution steps, formatted in logical order.
                2. `final_answer`: The final answer to the problem.
                3. `topic`: Chapter in HKDSE
                Latex content:
                - MUST use `\\newline` to before `=` and `:` in beginning and between of calculations
                - use space between text and mathematical expression: 'text\\'
                # - use `\\text{}` to wrap text, dont "text\\ text\\ text\\"
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
    response_json = json.loads(response)
    response_json["raw_response"] = response
    return response_json, Model_ID


def solve_math_problem_v2(latex_equation):
    Model_ID = "ft:gpt-4o-2024-08-06:exmersive:solve:AheNBEHi"
    #         All responses must be in JSON format and include:
    #         1. `steps`: A list of solution steps, formatted in logical order.
    #         2. `final_answer`: The final answer to the problem.
    #         3. `topic`: Chapter in HKDSE
    prompt = (
        """
        The assistant is a math tutor that provides detailed, step-by-step solutions to math problems. 
        The steps is not need to repeat the question and dont include final answer. 
        Latex content:
        - MUST use `\newline` to before `=` and `:` in beginning and between of calculations
        - use `\text{}` to wrap text.
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
        1. If a step is not logically connected to the problem, mark it incorrect and provide the correct continuation.
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
