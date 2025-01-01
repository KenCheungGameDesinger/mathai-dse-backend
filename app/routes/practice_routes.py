import json

from flask import Blueprint, request, jsonify

from app import db_instance
from app.services.practice_service import generate_practice_questions

practice_bp = Blueprint("practice", __name__)


# 練習題生成接口
@practice_bp.route("/generate", methods=["POST"])
def generate():
    try:
        base_question = request.json["base_question"]

        questions = generate_practice_questions(base_question)
        # print(questions)
        # questions = ""
        # for question in generate_practice_questions(base_question, num_questions):
        #     questions += question
        #     print(question)
        return jsonify({"success": True, "questions": questions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


QUESTION_BANK_COLLECTION = "math-similar-question"


# 取得題庫
@practice_bp.route("/<topic>", methods=["GET"])
def get_questionbank_by_topic(topic):
    try:
        questionbank = db_instance.get_collection(QUESTION_BANK_COLLECTION)
        questionbank = [question for question in questionbank
                        if question.get("solution", {}).get("topic") == topic]
        return jsonify({"success": True, "questions": questionbank})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
