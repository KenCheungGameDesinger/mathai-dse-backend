import os

from openai import OpenAI

from app import client_deepseek, client_openai




# def test_llm_client():
#     API_KEY_DEEPSEEK = os.getenv("DEEPSEEK_API_KEY")
#     API_KEY_OPENAI = os.getenv("OPENAI_API_KEY")
#     client_deepseek = OpenAI(api_key=API_KEY_DEEPSEEK, base_url="https://api.deepseek.com")
#     client_openai = OpenAI(api_key=API_KEY_OPENAI)
#
#     print(client_deepseek.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": "Hello!"}]))
#     print(client_openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello!"}]))
#
# test_llm_client()