# tools/translation.py
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from app import API_KEY_OPENAI
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(openai_api_key=API_KEY_OPENAI, model_name="gpt-4-turbo")

def translate(text: str, target_language: str = "英文") -> str:
    """
    將文本翻譯成指定語言（預設為英文）
    """
    prompt = PromptTemplate(
        input_variables=["text", "target_language"],
        template="請將以下翻譯成{target_language}：\n\n{text}\n\n翻譯結果："
    )
    formatted_prompt = prompt.format(text=text, target_language=target_language)
    return llm.predict(formatted_prompt)

translate_tool = Tool(
    name="translate",
    func=translate,
    description="將文本翻譯成指定語言"
)
#
# math_agent_translate_only = initialize_agent(
#     tools=[translate_tool],
#     llm=llm,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     system_prompt="你是一個翻譯機器人，可以將文本翻譯成指定語言"
# )