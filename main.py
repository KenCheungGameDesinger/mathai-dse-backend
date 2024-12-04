from flask import Flask, request, jsonify
from flask_cors import CORS
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import requests
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Global variables for Google Drive
gauth = None

drive = None

API_KEY = ""
client = OpenAI(api_key=API_KEY)



@app.route('/')
def index():
    return 'Connecting...'


# Authenticate Google Drive
@app.route('/auth_drive', methods=['GET'])
def authenticate_drive():
    global gauth, drive
    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.json")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile("mycreds.json")
        elif gauth.access_token_expired:
            gauth.Refresh()
            gauth.SaveCredentialsFile("mycreds.json")
        else:
            gauth.Authorize()
        drive = GoogleDrive(gauth)
        return jsonify({"status": "success", "message": "Google Drive authenticated successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Upload file to Google Drive
@app.route('/upload_drive', methods=['POST'])
def upload_to_drive():
    try:
        global drive
        if drive is None:
            return jsonify({"status": "error", "message": "Drive not authenticated. Call /auth_drive first."})

        file = request.files['file']
        folder_path = request.form.get('folder_path', 'root')

        # Get or create the target folder
        folder_id = get_or_create_folder(folder_path)
        file_metadata = {'title': file.filename, 'parents': [{'id': folder_id}]}
        gfile = drive.CreateFile(file_metadata)
        gfile.SetContentFile(file.filename)
        gfile.Upload()
        gfile.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        return jsonify({"status": "success", "link": gfile['alternateLink']})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Helper to get or create folder
def get_or_create_folder(folder_path):
    folder_names = folder_path.split('/')
    parent_id = 'root'

    for folder_name in folder_names:
        folder_list = drive.ListFile({
            'q': f"'{parent_id}' in parents and title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        }).GetList()

        if folder_list:
            folder_id = folder_list[0]['id']
        else:
            folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder',
                               'parents': [{'id': parent_id}]}
            folder = drive.CreateFile(folder_metadata)
            folder.Upload()
            folder_id = folder['id']

        parent_id = folder_id
    return parent_id


# Extract text or LaTeX from an image
@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        data = request.json
        image_url = data['image_url']
        prompt = data['prompt']

        # Call OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": {"type": "image_url", "url": image_url}}
                ]
            }
        )
        result = response.json()
        return jsonify({"status": "success", "response": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Add endpoints for hint generation, validation, and step-by-step solutions
@app.route('/generate_hint', methods=['POST'])
def generate_hint():
    # Implementation similar to extract_text
    pass


@app.route('/validate_answer', methods=['POST'])
def validate_answer():
    # Implementation similar to extract_text
    pass


@app.route('/step_by_step', methods=['POST'])
def step_by_step():
    # Implementation similar to extract_text
    pass


def chat(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
    )
    return response.choices[0].message.content

@app.route('/chat_stream', methods=['GET'])
def chat_stream():
    # print(request.json)
    # user_input = request.json['user_input']
    def generate():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    {
                        "role": "user",
                        "content": "tell me long story",
                    }
                ],
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content
    return generate(), {'Content-Type': 'text/plain'}

@app.route('/chat', methods=['POST'])
def handle_chat():
    user_input = request.json['user_input']
    response = chat(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
