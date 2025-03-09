from flask import Blueprint, request, jsonify
from app.services.solution_service import solve_math_problem_deepseek, solve_math_problem_agent, \
    solve_math_problem_openai, \
    evaluate_student_answer_openai, evaluate_student_answer_deepseek, evaluate_student_answer_agent

solution_bp = Blueprint("solution", __name__)


# 解題接口
@solution_bp.route("/solve", methods=["POST"])
def solve():
    try:
        latex_equation = request.json.get("question", "")
        if (latex_equation == ""):
            return jsonify({"success": False, "error": "question: No latex equation provided."}), 400
        solution = solve_math_problem_agent(latex_equation)
        data = {"success": True, "solution": solution, "model": "o3-mini"}
        return jsonify({"success": True, "solution": solution, "model": "o3-mini"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@solution_bp.route("/evaluate", methods=["POST"])
def evaluate():
    try:

        steps = request.json.get("steps", "")
        final_answer = request.json.get("final_answer", "")
        question = request.json.get("question", "")
        sampleAnswer = request.json.get("sample_answer", "")

        if (steps == ""):
            return jsonify({"success": False, "error": "steps: No steps provided."}), 400
        if (final_answer == ""):
            return jsonify({"success": False, "error": "answer: No answer provided."}), 400
        evaluation = evaluate_student_answer_agent(question, steps, final_answer,str(sampleAnswer))
        return jsonify({"success": True, "evaluation": evaluation})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
