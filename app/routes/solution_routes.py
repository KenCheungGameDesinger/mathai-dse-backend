from flask import Blueprint, request, jsonify
from app.services.solution_service import solve_math_problem, solve_math_problem_v2, evaluate_student_answer

solution_bp = Blueprint("solution", __name__)


# 解題接口
@solution_bp.route("/solve", methods=["POST"])
def solve():
    try:
        latex_equation = request.json.get("question", "")
        if (latex_equation == ""):
            return jsonify({"success": False, "error": "question: No latex equation provided."}), 400
        solution, model_id = solve_math_problem_v2(latex_equation)
        return jsonify({"success": True, "solution": solution, "model": model_id})
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
        evaluation, model_id = evaluate_student_answer(question, steps, final_answer)
        return jsonify({"success": True, "evaluation": evaluation, "model": model_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
