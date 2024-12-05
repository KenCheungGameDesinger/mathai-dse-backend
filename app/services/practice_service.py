import random
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_practice_questions(base_question, num_questions):
    variations = []
    for i in range(num_questions):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Create {num_questions} similar problem to the one given, with the same structure but different numbers. "
                        "After understanding the mathematics topic, you can also make small changes in the pattern."
                        "Provide the new problem in LaTeX format only for each single element in the list. "
                        "- Wrap equations in \\[...\\]. "
                        "- Use \\\\ for new lines where needed. "
                        f"Original Problem: {base_question}"  # Dynamically embed the problem
                        r"output use list of strings as json value, don't add any prefix or suffix"
                        "the output shouldn't include invisible characters like spaces, tabs, newlines, etc."
                        "response example:"
                        "["
                                r'"Simplify (m^5 * n^2)^6 / m^4 * n^3",'
                                r'"Simplify (m^7 * n^2)^6 / m^3 * n^4",'
                                r'Simplify (m^5 * n^3)^6 / m^5 * n^2'
                            ']'
                    ),
                }
            ],
            # stream=True
        )
        variations = response.choices[0].message.content
        # for chunk in response:
        #     if chunk.choices[0].delta.content is not None:
        #         output = chunk.choices[0].delta.content
        #         variations = output
        #         yield variations

    return variations
