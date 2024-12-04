from flask import Blueprint, request, jsonify
from app.services.openai_service import generate_completion

openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get("prompt")
        response = generate_completion(prompt)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})