from langchain.prompts import PromptTemplate

latex_conversion = PromptTemplate(
    input_variables=["math_expression"],
    template=(
        "請將以下數學表達式轉換為標準的 LaTeX 格式，並按照以下範例格式展示：\n\n"
        "你的輸入: {math_expression}\n\n"
        "注意你不可以加入其他內容，你只是一個轉換工具"
        +"""
        每一個math statement都需要用來'$' or '$$'包裹
        """+
        "* Some Validated Example:\n"
        "* $$\\frac{{d}}{{dx}} \\left( 3x^2 + 2x \\right)$$,\n"
        "* $$6x + 2$$,\n"
        "* Differentiate $3x^2$ (The first term): $$\\frac{{d}}{{dx}} \\left( 3x^2 \\right) = 6x$$\n"
        "* Combine the results: $$\\therefore\\ \\frac{{d}}{{dx}} \\left( 3x^2 + 2x \\right) = 6x + 2$$\n\n"
        "請輸出轉換後的標準格式."

    )
)
