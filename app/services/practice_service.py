import random

def generate_practice_questions(base_question, num_questions):
    variations = []
    for _ in range(num_questions):
        modified_question = base_question.replace(
            "6", str(random.randint(2, 10))
        )  # 替換題目中的某些部分以生成新問題
        variations.append(modified_question)
    return variations
