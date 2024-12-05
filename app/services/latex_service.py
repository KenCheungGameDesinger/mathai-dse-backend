# import sympy as sp
import json

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def solve_math_problem(latex_equation):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    "Solve the given problem step by step in LaTeX format for expressing mathematics only. "
                    "Use the following structure: "
                    "- Wrap all equations in json format. "
                    "- the response json have to include 'topic', 'steps' and 'final answer'"
                    "- topics means the name of the problem in HKDSE mathematics. "
                    "- steps means the steps to solve the problem. Including instruction for each step. put each single step in to a list."
                    "- instructions in step is also in Latex format."
                    "- final answer means the final answer of the problem."
                    "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
                    "- don't add and prefix or suffix to wrap the json."
                    f"Problem: {latex_equation}"  # Dynamically embed the problem
                    "Example output: "
                    "{'topic': 'Simplify', 'steps': ['Simplify (m^5 * n^2)^6 / m^4 * n^3', 'Simplify (m^7 * n^2)^6 / m^3 * n^4', 'Simplify (m^5 * n^3)^6 / m^5 * n^2'], 'final answer': 'Simplify (m^5 * n^3)^6 / m^5 * n^2'}"
                )
            }
        ]
    )

    response = response.choices[0].message.content
    return json.loads(response)
