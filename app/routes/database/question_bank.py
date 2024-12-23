from flask import Blueprint, request, jsonify
from app.managers.firebase.firestoreManager import db_instance

question_bank_bp = Blueprint("question_bank", __name__)

# Firestore 集合名稱
QUESTION_BANK_COLLECTION = "question_bank"


@question_bank_bp.route('/', methods=['GET'])
def index():
    """
    題庫 index
    """
    return "Question Bank"


@question_bank_bp.route('/add', methods=['POST'])
def add_question():
    """
    添加新題目到題庫。
    Request Body:
    {
        "question": "Solve x + 3 = 5",
        "solution": {
            "steps": ["Subtract 3 from both sides", "x = 2"],
            "final_answer": "x = 2"
        },
        "topic": "Algebra"
    }
    """
    try:
        data = request.json

        # 檢查是否包含所有必要字段
        # required_fields = {"question", "solution"}
        # if not required_fields.issubset(data.keys()):
        #     return jsonify({"error": "Missing required fields"}), 400

        # Check each required field individually
        if "question" not in data:
            return jsonify({"error": "Missing 'question' field"}), 400

        if "solution" not in data:
            return jsonify({"error": "Missing 'solution' field"}), 400

        # Check each solution field individually
        # if "steps" not in data["solution"]:
        #     return jsonify({"error": "Missing 'steps' in 'solution'"}), 400

        # if "final_answer" not in data["solution"]:
        #     return jsonify({"error": "Missing 'final_answer' in 'solution'"}), 400
        #
        # if "topic" not in data["solution"]:
        #     return jsonify({"error": "Missing 'topic' in 'solution'"}), 400
        # 檢查 solution 結構是否正確
        # solution_fields = {"steps", "final_answer", "topic"}
        # if not solution_fields.issubset(data["solution"].keys()):
        #     return jsonify({"error": "Invalid 'solution' format"}), 400

        # 將數據寫入 Firestore
        doc_ref = db_instance.add_document(QUESTION_BANK_COLLECTION, data)
        doc_id = doc_ref.get("document_id")  # 確保返回的鍵名稱清晰一致
        return jsonify({"message": "Question added successfully", "id": doc_id}), 201

    except ValueError as ve:
        return jsonify({"error": f"Invalid data: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@question_bank_bp.route('/delete/<string:document_id>', methods=['DELETE'])
def delete_question(document_id):
    """
    刪除指定的題目。
    URL參數:
        document_id: 待刪除文檔的ID
    """
    try:
        # 嘗試刪除指定文檔
        result = db_instance.delete_document(QUESTION_BANK_COLLECTION, document_id)
        return_code = 500
        if result["success"]:
            if result["success"]:
                return_code = 200
            else:
                return_code = 404

        return jsonify(result), return_code

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
