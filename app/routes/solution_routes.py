from flask import Blueprint, request, jsonify
from app.services.solution_service import solve_math_problem, evaluate_student_answer

solution_bp = Blueprint("solution", __name__)


# 解題接口
@solution_bp.route("/solve", methods=["POST"])
def solve():
    try:
        latex_equation = request.json.get("question", "")
        if (latex_equation == ""):
            return jsonify({"success": False, "error": "question: No latex equation provided."}), 400
        solution = solve_math_problem(latex_equation)
        return jsonify({"success": True, "solution": solution})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@solution_bp.route("/evaluate", methods=["POST"])
def evaluate():
    try:

        steps = request.json.get("steps", "")
        final_answer = request.json.get("final_answer", "")
        question = request.json.get("question", "")
        if (steps == ""):
            return jsonify({"success": False, "error": "steps: No steps provided."}), 400
        if (final_answer == ""):
            return jsonify({"success": False, "error": "answer: No answer provided."}), 400
        evaluation = evaluate_student_answer(question, steps, final_answer)
        return jsonify({"success": True, "evaluation": evaluation, "model": "gpt-4o-2024-08-06"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
