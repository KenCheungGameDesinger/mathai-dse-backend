from langchain_community.chat_models import ChatOpenAI
from app.managers.agents.prompts import conversion as conversion_prompt
from app import API_KEY_OPENAI
from langchain.tools import Tool


# 初始化 LLM
llm = ChatOpenAI(openai_api_key=API_KEY_OPENAI)

def convert_to_latex(math_expression: str) -> str:
    """ 
    驗證及轉換數學表達式為標準 LaTeX 格式。
    """
    prompt = conversion_prompt.latex_conversion.format(math_expression=math_expression)
    return llm.invoke(prompt)


convert_to_latex_tool = Tool(
    name="convert_to_latex",
    func=convert_to_latex,
    description="驗證並將句子中的數學表達式轉換為標準 LaTeX 格式"
)