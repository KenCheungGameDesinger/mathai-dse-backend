from langchain.prompts import PromptTemplate

solve_math_answer = PromptTemplate(
    input_variables=["math_question", "topic"],
    template=(
        """
        You are an AI model specialized in solving mathematical and logical problems. Given a question and relevant topic details, your task is to predict the final answer.  
        
        **Question:** {math_question}
        **Topic:** {topic}
        
        Follow these rules:  
        1. Analyze the question carefully and provide a precise and accurate final answer.  
        2. Do not include steps, only provide the final answer.  
        3. The final answer must be in JSON format as follows:  
        
        Example Output Format:
        {{
          "final_answer": "<your answer here>"
        }}
        
        """
    )
)

solve_math_steps = PromptTemplate(
    input_variables=["topic", "steps_instruction", "question", "final_answer", "steps"],
    template=(
        """
As a math expert, you need to provide an extra step for my math problem based on the known topic and known steps.
Note that you cannot output two steps at the same time, but rather infer the next step based on the existing steps.

Topic:
{topic}

Instruction:
Use following algorithm to solve:
{steps_instruction}

Terminate Policy:
If you think there are no more steps and you are done, do not add any more steps.
If the maths operation of next step is same as one of the existing steps, do not add any more steps, and return object with {{step_index: 0, step: "" }}

Question:
{question}

Final Answer:
{final_answer}

existing steps:
{steps}

Output Format:
{{
    "step_index": int,
    "step:": str
}}
        """
    )
)

evaluate_math = PromptTemplate(
    input_variables=["question", "steps", "final_answer", "sample_answer"],
    template="""
    你是一位專業的數學老師，請仔細批改學生的解題過程。

    **問題**:
    {question}
    
    **學生的解題步驟**:
    {steps}

    **學生的最終答案**:
    {final_answer}
    
    **參考答案**
    {sample_answer}
    

    **批改要求**：
    - 返回的数据需要包含所有学生的步骤
    - 逐步檢查每個步驟是否回答了對應題目，僅僅使用對了rules是不能當做true的 (`correct`: true/false)。
    - 若有錯誤，請提供詳細解釋 (`comment`) 並指導如何修改。
    - 判定最終答案是否正確 (`final_answer`: true/false)。
    
    **批改的時候注意不同情況**
    - 首先需要判斷學生遞交的步驟過程是否和問題無關：則標記所有步驟錯.（因為學生有可能把其他題目的作答上傳到其他題目上）
    - 如果"wrong expression and variables are used",那麽所有步驟都應該是錯的
    - 步驟部分正確：逐個步驟批改是否正確，並需要在comment提供正確的步驟序列
    - 當學生應用了正確的rules，但並非使用題目中的變量，或運算步驟不符合上下搵時，則記錯。
        
    - **請務必返回以下 JSON 格式**：
        {{
            "final_answer": false,
            "steps": [
                {{
                    "step": "Step copy from student steps (學生的解題步驟)",
                    "correct": false,
                    "comment": "Explanation of correctness"
                }}
            ]
        }}
        
        最後通過工具轉換為有效的Latex
    """
)
