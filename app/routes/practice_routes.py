from flask import Blueprint, request, jsonify
from app.services.practice_service import generate_practice_questions

practice_bp = Blueprint("practice", __name__)


# 練習題生成接口
@practice_bp.route("/generate", methods=["POST"])
def generate():
    try:
        # base_question = request.json["base_question"]
        # num_questions = request.json.get("num_questions", 5)
        # questions = generate_practice_questions(base_question, num_questions)
        return jsonify({"success": True, "questions": [
            "Simplify (m^5 * n^2)^6 / m^4 * n^3",
            "Simplify (m^7 * n^2)^6 / m^3 * n^4",
            "Simplify (m^5 * n^3)^6 / m^5 * n^2",
            "Simplify (m^4 * n^2)^6 / m^2 * n^3",
            "Simplify (m^6 * n^1)^6 / m^3 * n^5"
        ]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
