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


def evaluate_student_answer(steps, final_answer):
    prompt = (
        "For each student step comment whether correct or not, and command if not correct showing why incorrect and showing right steps. "
        "For correct comment showing remind about what student easy to fall in incorrect. "
        "Use the following structure: "
        r"- Wrap all equations in json format"
        "- Include all steps explicitly in LaTeX with no text outside LaTeX formatting. "
        r"- all value in the steps and comment should use Latex format capable"
        r"- don't add and header to wrap the json. e.g. ```json"
        "- Output for list corresponding each student step comment. "
        "- key included: 'step', 'correct', 'comment'"
        "your responese should can be parsed by json.loads."
        "don't add ```json and ```"
        "Example output: "
        "[{'step': 'Simplify (m^5 * n^2)^6 / m^4 * n^3', 'correct': True, 'comment': 'Remind: student should be careful about the power of m and n'}, "
        "{'step': 'Simplify (m^7 * n^2)^6 / m^3 * n^4', 'correct': False, 'comment': 'Incorrect: the power of m and n are not changed. Right steps are: Simplify (m^5 * n^3)^6 / m^5 * n^2'}, "
        r"{'step': 'Simplify (m^5 * n^3)^6 / m^5 * n^2', 'correct': True, 'comment': '...'}]"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": json.dumps({"steps": steps, "answer": final_answer})
                }
            ]
        )

        response = response.choices[0].message.content
        print(response)
        return json.loads(response)

    except Exception as e:
        print(e)
        return str(e)