from flask import Blueprint, request, jsonify
from app.services.latex_service import solve_math_problem

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
