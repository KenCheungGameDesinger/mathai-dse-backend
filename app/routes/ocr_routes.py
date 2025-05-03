import base64
import os

from flask import Blueprint, request, jsonify
from app.services.ocr_service import ocr_questions, ocr_answers
from app.services.question_bank_service import match_topic

ocr_bp = Blueprint('ocr', __name__)


# Check if route is working
@ocr_bp.route("/ping", methods=["GET"])
def ping():
    hd = request.headers.get("X-Added-Req")
    return jsonify({"success": True, "message": "pong", "header": hd})


# OCR 接口
@ocr_bp.route("/extract", methods=["POST"])
def extract():
    try:
        file = request.json.get("image_data", "")
        if (file == ""):
            return jsonify({"success": False, "error": "image_data: No image data provided."}), 400

        # if "," in file:
        #     file = file.split(",")[1]
        #
        # # 補齊 padding
        # file = file + '=' * (-len(file) % 4)
        # image_data = base64.b64decode(file)
        # # check if dir exists
        # dir_path = 'cache/images'
        # if not os.path.exists(dir_path):
        #     os.makedirs(dir_path)
        # with open(os.path.join(dir_path, 'temp.png'), 'wb') as f:
        #     f.write(image_data)

        extracted_text = ocr_questions(file)
        topic_matched = match_topic(extracted_text)
        # match topic
        data = jsonify({"success": True, "text": extracted_text, "topic": topic_matched})
        return data
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
