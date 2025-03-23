import os

from openai import OpenAI

from app import db_instance
from app.config import Config

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fetch_topics():
    """
    從 Firestore 獲取所有題目的主題
    """
    try:
        questionbank = db_instance.get_collection(Config.QUESTION_BANK_COLLECTION)

        topics = set()
        for question in questionbank:
            topic = question.get("solution", {}).get("topic")
            if topic:
                topics.add(topic)

        return {"success": True, "topics": list(topics)}

    except Exception as e:
        return {"success": False, "error": str(e)}


def match_topic(question: str):
    """
    使用 GPT-4 Turbo 解析數學問題 (LaTeX)，匹配最合適的 topic。

    :param question: LaTeX 格式的數學表達式
    :return: 最可能的 topic
    """
    try:
        # **(1) 獲取所有可選 topics**
        topics_obj = fetch_topics()  # 返回一個列表，如 ["Algebra", "Calculus", "Probability", "Geometry"]

        # **(2) 構造 Prompt**
        prompt = f"""
        你是一個數學題目的分類助手，負責根據 LaTeX 格式的數學問題來匹配最合適的主題。
        已知可能的主題列表：
        {topics_obj.get("topics")}

        請分析以下數學問題，並選擇最適合的 topic返回結果：
        問題（LaTeX）：{question}
        
        指引：
        - 只能返回一個主題
        - 返回主題的時候需要和主題列表的字符串一致
        - 不得加入其他任何文字或符號

        你的回答格式應該是：
        <最佳匹配主題>
        """

        # **(3) 調用 GPT-4 Turbo**
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "你是一個數學題目分類工具。"},
                      {"role": "user", "content": prompt}],
            temperature=0.1  # 控制一致性
        )
        gpt_output = response.choices[0].message.content.strip()
        # topic = gpt_output.replace("Topic:", "").strip()

        # return topic if topic in topics else "Unknown Topic"
        return gpt_output if gpt_output in topics_obj.get("topics") else "Unknown Topic"

    except Exception as e:
        return f"Error: {str(e)}"
