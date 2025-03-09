from langchain_community.chat_models import ChatOpenAI
from app.managers.agents.prompts import ocr as conversion_prompt
from app.managers.agents.prompts import ocr
from app import API_KEY_OPENAI
from langchain.tools import Tool

# 初始化 LLM
llm = ChatOpenAI(openai_api_key=API_KEY_OPENAI, model_name="gpt-4-vision-preview")


def extract_question(image_data: str) -> str:
    """
    從 Base64 編碼的圖像中提取完整的數學問題，包括文本描述和數學表達式，並轉換為 LaTeX 格式
    """
    prompt = ocr.question_ocr.format(image_data=image_data)
    print(prompt)
    return llm.predict(prompt)


extract_question_tool = Tool(
    name="extract_question",
    func=extract_question,
    description="從 Base64 編碼的圖像中提取完整的數學問題，包括文本描述和數學表達式，並轉換為 LaTeX 格式"
)
