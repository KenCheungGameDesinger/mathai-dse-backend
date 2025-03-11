# tools/math.py
from typing import List, Dict, Any, Optional

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool, StructuredTool
from app.managers.agents.prompts import math
from langchain.output_parsers import PydanticOutputParser
from app import API_KEY_OPENAI
import json
from pydantic import BaseModel

# llm_reasoning = ChatOpenAI(openai_api_key=API_KEY_OPENAI, model_name="o3-mini", temperature=1)
# llm_reasoning = ChatOpenAI(openai_api_key=API_KEY_OPENAI, model_name="ft:gpt-4o-2024-08-06:exmersive:solve-steps:B8rhf1lw", temperature=0.1)
llm_reasoning = ChatOpenAI(openai_api_key=API_KEY_OPENAI,
                           model_name="ft:gpt-4o-2024-08-06:exmersive:step-accuracy:B9mdBujp", temperature=0.1)


# region solve solution
def solve_math(topic: str, steps_instruction: str, question: str) -> List[str]:
    """
    解答數學問題
    """
    print("in solve_math")
    step_list =[]
    last_len = 0
    for i in range(5):
        formatted_prompt = math.solve_math_new.format(topic=topic, steps_instruction=steps_instruction,
                                                  question=question,
                                                  steps=step_list)
        print(formatted_prompt)
        res = llm_reasoning.invoke(formatted_prompt)
        content_str = json.loads(res.content)

        step_indices = [json.loads(step)["step_index"] for step in step_list]
        if json.loads(content_str)['step_index'] in step_indices:
            break
        step_list.append(content_str)
    return step_list


class SolutionMathInput(BaseModel):
    topic: str
    steps_instruction: str
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
    return res


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
