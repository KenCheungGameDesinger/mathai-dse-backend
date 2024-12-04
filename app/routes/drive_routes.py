from flask import Blueprint, request, jsonify
from app.services.drive_service import upload_file

drive_bp = Blueprint('drive', __name__)

@drive_bp.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        folder_path = request.form.get('folder_path', 'root')
        link = upload_file(file, folder_path)
        return jsonify({"status": "success", "link": link})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
