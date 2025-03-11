from langchain.prompts import PromptTemplate

solve_math = PromptTemplate(
    input_variables=["math_question"],
    template=("""
       "你是一位數學專家，請解答以下數學問題：\n\n數學問題：{math_question}\n\n"
       你的每一個步驟不應該只顯示修改的部分，而需要顯示整個完整的部分作為展示。例如當你簡化一個項的時候，不要忘了展示完整的式子.
       當你的步驟是修改分子的時候，步驟的展示需要包含分母。
       而你只需要展示每個步驟的最終形態，而不需要只針對修改的部分單獨顯示。
       **不要對修改的部分單獨展示。**
       Output Sample with out ```json and ```:
       {{
        final_answer: string;
        steps: string[];
        topic: string;
        }}
        """)
)

solve_math_new = PromptTemplate(
    input_variables=["topic","steps_instruction","question","steps"],
    template=("""
As a math expert, you need to provide an extra step for my math problem based on the known topic and known steps. 
Note that you cannot output two steps at the same time, but rather infer the next step based on the existing steps.

Topic:
{topic}

Instruction:
Use following algorithm to solve:
{steps_instruction}

If you think there are no more steps and you are done, do not add any more steps.

Quesition:
{question}

existing steps:
{steps}

Example Output Format:
{{"step_index": 1, "step": "..."}},
        """)
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
                    "step": "Step description",
                    "correct": false,
                    "comment": "Explanation of correctness"
                }}
            ]
        }}
        
        最後通過工具轉換為有效的Latex
    """
)
