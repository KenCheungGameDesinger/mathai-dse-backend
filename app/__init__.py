import os

from flask import Flask
from flask_cors import CORS, cross_origin
from openai import OpenAI

from app.managers.firebase.firestoreManager import db_instance
from app.routes.report_routes import report_bp

API_KEY_DEEPSEEK = os.getenv("DEEPSEEK_API_KEY")
API_KEY_OPENAI = os.getenv("OPENAI_API_KEY")
client_deepseek = OpenAI(api_key=API_KEY_DEEPSEEK, base_url="https://api.deepseek.com")
client_openai = OpenAI(api_key=API_KEY_OPENAI)


def create_app():
    app = Flask(__name__)
    # CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(app, origins="*")
    # 加載配置

    app.config.from_object('app.config.Config')
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 限制為 20MB

    # 註冊藍圖

    from .routes.ocr_routes import ocr_bp
    from .routes.practice_routes import practice_bp
    from .routes.solution_routes import solution_bp
    from .routes.database.question_bank_routes import question_bank_bp

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return 'Connecting...'

        # app.register_blueprint(image_blueprint, url_prefix="/api/image")

    app.register_blueprint(ocr_bp, url_prefix="/api/ocr")
    app.register_blueprint(solution_bp, url_prefix="/api/solution")
    app.register_blueprint(practice_bp, url_prefix="/api/practice")
    app.register_blueprint(question_bank_bp, url_prefix="/api/db/question_bank")
    app.register_blueprint(report_bp, url_prefix="/api/report")

    # app.register_blueprint(other_bp, url_prefix='/api/other')

    return app
