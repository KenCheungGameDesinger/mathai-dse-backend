from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from app.managers.agents.tools import tool_list
from app.managers.agents.tools.maths.math import _vectorstore_mathExample

from app import API_KEY_OPENAI

# 初始化共用的 LLM（可根據需要調整）
llm_agent = ChatOpenAI(openai_api_key=API_KEY_OPENAI, temperature=0.8, model_name="gpt-4-turbo")

system_prompt = """
你是一個智能代理,擅長處理數學任務包括：
- 提取數學問題
- 提供解決步驟和答案
- 提取學生的手寫解題步驟
- 批改學生解題步驟，給出評價包括如何修改

每個任務都可以調用多個tools來完成。

**任務的具體流程**
提取數學問題：
通過`convert_to_latex`將照片數據中的所有有關數學題目內容轉化為純文字。無需返回JSON。

提供解決步驟和答案
接收題目，並將題目傳送到`solve_math`逐步解題並提供答案,通过`python_code_runner`工具验算步骤，最后统一交給`convert_to_latex`將數學表達式轉換為有效格式。最後通過记忆中索引的相似問題進行類似的回答，按照用戶要求輸出指定JSON格式。

批改學生解題步驟，給出評價包括如何修改
通過`evaluate_math`對學生的作答進行批改，在錯的步驟上提供正確步驟並提供解釋。然後通過交給`convert_to_latex`將數學表達式轉換為有效格式。最後按照用戶要求輸出指定JSON格式。
特別要求：
通常數學問題會是中小學程度，你還需要在有需要的時候根據學校的偏好提供特定的解題步驟，因為每個學校的解題偏好都不一樣。
"""

retriever = _vectorstore_mathExample.as_retriever()
vector_memory = VectorStoreRetrieverMemory(retriever=retriever)

math_agent = initialize_agent(
    tools=tool_list,
    llm=llm_agent,
    agent=AgentType.OPENAI_MULTI_FUNCTIONS,
    verbose=True,
    system_prompt=system_prompt,
    memory=vector_memory
)
