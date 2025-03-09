from app.managers.agents.tools.latex_converter import convert_to_latex_tool
from app.managers.agents.tools.math import solve_math_tool, evaluate_math_tool
from app.managers.agents.tools.translation import translate_tool
from app.managers.agents.tools.ocr import extract_question_tool

tool_list = [translate_tool, solve_math_tool, convert_to_latex_tool, extract_question_tool, evaluate_math_tool]
