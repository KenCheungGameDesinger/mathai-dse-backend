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
llm_reasoning = ChatOpenAI(openai_api_key=API_KEY_OPENAI, model_name="ft:gpt-4o-2024-08-06:exmersive:solve-steps:B8rhf1lw", temperature=0.1)


# region solve solution
def solve_math(math_question: str) -> str:
    """
    解答數學問題
    """
    formatted_prompt = math.solve_math.format(math_question=math_question)
    return llm_reasoning.invoke(formatted_prompt)


solve_math_tool = Tool(
    name="solve_math",
    func=solve_math,
    description="解答數學問題"
)


# endregion

# region evaluation
def evaluate_math(question: str, steps: List[str], final_answer: str, sample_answer: Optional[dict] = "") -> Dict[str, Any]:
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
