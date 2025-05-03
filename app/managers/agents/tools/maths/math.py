# tools/math.py
from typing import List, Dict, Any, Optional

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool, StructuredTool
from langchain_community.embeddings import OpenAIEmbeddings

from app.managers.agents.prompts import math
from langchain.output_parsers import PydanticOutputParser
from app import API_KEY_OPENAI
import json
from pydantic import BaseModel

from app.managers.RAG.vectorstore import build_vectorstore
from app.managers.RAG.retriever import retrieve_examples

mathExampleDocs = [
    "app/managers/RAG/docs/Law of index algo.docx",
    "app/managers/RAG/docs/Law of index_example_1-20 *5variation.docx",
    "app/managers/RAG/docs/Law of index_example_1-40 base.docx",
    "app/managers/RAG/docs/Law of index_example_21-40 *5variation.docx",
]

llm_reasoning = ChatOpenAI(openai_api_key=API_KEY_OPENAI,
                           model_name="ft:gpt-4o-2024-08-06:exmersive:soln-wellaround:BMSGlkkQ", temperature=0.1)

_vectorstore_mathExample = build_vectorstore(mathExampleDocs,
                                             OpenAIEmbeddings(model="text-embedding-3-large"))


# region solve solution
def solve_math(topic: str, question: str, steps_instruction: Optional[str] = "None specified") -> List[str]:
    """
    解答數學問題
    """
    print("in solve_math")

    # TODO: get similar question
    similar_question = retrieve_examples(question, _vectorstore_mathExample)
    # print("similar_question", similar_question[0])
    answer_prompt = math.solve_math_answer.format(math_question=question, topic=topic,
                                                  similar_question=similar_question)
    print("answer_prompt", answer_prompt)
    final_answer = llm_reasoning.invoke(answer_prompt)
    final_answer = json.loads(json.loads(final_answer.content)).get("final_answer")
    final_answer = final_answer.replace('\x0c', r'\f')

    step_list = []
    last_len = 0
    for i in range(5):
        formatted_prompt = math.solve_math_steps.format(topic=topic, steps_instruction=steps_instruction,
                                                        question=question,
                                                        final_answer=final_answer,
                                                        steps=step_list,
                                                        similar_question=similar_question)
        res = llm_reasoning.invoke(formatted_prompt)
        content_str = json.loads(res.content)

        step_indices = [json.loads(step)["step_index"] for step in step_list]
        if json.loads(content_str)['step_index'] in step_indices:
            break
        step_list.append(content_str)

    if len(step_list) > 1:
        i = 0
        while i < len(step_list) - 1:
            if json.loads(step_list[i])["step"] == json.loads(step_list[i + 1])["step"]:
                step_list.pop(i)
                for j in range(i, len(step_list)):
                    step = json.loads(step_list[j])
                    step["step_index"] -= 1
                    step_list[j] = json.dumps(step)
            else:
                i += 1

    return step_list


class SolutionMathInput(BaseModel):
    topic: str
    steps_instruction: Optional[str] = ""
    question: str


solve_math_tool = StructuredTool.from_function(
    name="solve_math",
    func=solve_math,
    args_schema=SolutionMathInput,
    description="解答數學問題"
)


# endregion

# region evaluation
def evaluate_math(question: str, steps: List[str], final_answer: str, sample_answer: Optional[dict] = "") -> Dict[
    str, Any]:
    print("in evaluate")
    formatted_prompt = math.evaluate_math.format(
        question=question,
        steps="\n".join(steps),
        final_answer=final_answer,
        sample_answer=sample_answer
    )
    print(formatted_prompt)
    res = llm_reasoning.invoke(formatted_prompt)
    return res.content


class EvaluateMathInput(BaseModel):
    question: str
    steps: List[str]
    final_answer: str
    sample_answer: Optional[dict] = ""


evaluate_math_tool = StructuredTool.from_function(
    name="evaluate_math",
    func=evaluate_math,
    args_schema=EvaluateMathInput,
    description=f"""
    評估學生的數學問題，答案和步驟並給出解釋。評估需要根據參考答案進行批改。
    """
)

# endregion
