from flask import Blueprint, request, jsonify
from app.services.openai_service import generate_completion
from app.services.ocr_service import perform_ocr

ocr_bp = Blueprint('ocr', __name__)

# OCR 接口
@ocr_bp.route("/extract", methods=["POST"])
def extract():
    try:
        latex_text = r"\[ \text{Simplify } \frac{(m^{5} n^{-2})^{6}}{m^{4} n^{-3}} \text{ and express your answer with positive indices.} \]"
        # file = request.files["image"]
        # extracted_text = perform_ocr(file)
        return jsonify({"success": True, "text": latex_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})