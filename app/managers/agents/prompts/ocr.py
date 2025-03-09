from langchain.prompts import PromptTemplate

question_ocr = PromptTemplate(
    input_variables=["image_data"],
    template=("""
        As a OCR tool, not to talk, but giving output directly. 
        Extract the full mathematical problem from the following Base64-encoded image, 
        including both textual descriptions and mathematical expressions:
        
        Rule:
        - Include instructions or objective from the image
        - Do not add any additional explanatory text.
        - Do not solve it
        
        Do not:
        - add "Here is your math expression in validated LaTeX block mode, as requested:"
        
        image shown as base64 data:
        {image_data}
        
        Example:
        $$
        \\text{Simplify } \\frac{{(m^5 n^{-2})^6}}{{m^4 n^{-3}}} \\text{ and express your answer with positive indices:}
        $$
        """
    )
)
