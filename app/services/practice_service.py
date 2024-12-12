import json
import random
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_practice_questions(base_question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Create a similar problem to the one given, with the same structure but different numbers. "
                    "After understanding the mathematics topic, you can also make small changes in the pattern."
                    "Provide the new problem in LaTeX format"
                    # "- Wrap equations in \\[...\\]. "
                    # "- Use \\\\ for new lines where needed. "
                    f"Original Problem: {base_question}"  # Dynamically embed the problem
                    r"output pure strings, don't add any prefix or suffix"
                    r"- every sentence should wrap by exact'\text{}' in Latex, but not '\\text{}'."
                    r"\text{} should not wrap with Latex math."
                    "- output should include online value without key"
                    # "no need to add escape slashes"
                    "the output shouldn't include invisible characters like spaces, tabs, newlines, etc."
                    "response example:"
                    r'topic:string'
                ),
            }
        ],
        # stream=True
    )
    variations = response.choices[0].message.content
    print(variations)
    print(variations)
    # for chunk in response:
    #     if chunk.choices[0].delta.content is not None:
    #         output = chunk.choices[0].delta.content
    #         variations = output
    #         yield variations

    return variations
