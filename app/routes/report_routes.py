from datetime import datetime

from flask import Blueprint, request, jsonify

from app import db_instance

report_bp = Blueprint("report", __name__)

@report_bp.route("/solution-error", methods=["POST"])
def solution_error():
    try:
        data = request.json
        question = data.get("question")
        topic = data.get("topic")
        steps = data.get("steps")
        final_answer = data.get("final_answer")
        if topic is None or question is None or steps is None or final_answer is None:
            return jsonify({"error": "Missing required fields: topic, question, steps, final_answer"}), 400

        document_data = {"topic": topic, "question": question, "steps": steps, "final_answer": final_answer, "status": "pending","created_at": datetime.now()}
        doc = db_instance.add_document("maths/maintenance/report/solution/pending", document_data)

        return jsonify({"message": "Solution error reported successfully", "id": doc.get("document_id"), "document": doc.get("document_ref")}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500