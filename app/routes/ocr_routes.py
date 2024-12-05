from flask import Blueprint, request, jsonify
from app.services.ocr_service import ocr_questions, ocr_answers

ocr_bp = Blueprint('ocr', __name__)


# OCR 接口
@ocr_bp.route("/extract", methods=["POST"])
def extract():
    try:
        # latex_text = r"\[ \text{Simplify } \frac{(m^{5} n^{-2})^{6}}{m^{4} n^{-3}} \text{ and express your answer with positive indices.} \]"
        file = request.json.get("image_data", "")
        if (file == ""):
            return jsonify({"success": False, "error": "image_data: No image data provided."}), 400

        # file = request.files['file']
        extracted_text = ocr_questions(file)
        return jsonify({"success": True, "text": extracted_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@ocr_bp.route("/extract_answer", methods=["POST"])
def extract_answer():
    try:
        file = request.json.get("image_data", "")
        if (file == ""):
            return jsonify({"success": False, "error": "image_data: No image data provided."}), 400

        # file = request.files['file']
        extracted_text = ocr_answers(file)
        return jsonify({"success": True, "text": extracted_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
