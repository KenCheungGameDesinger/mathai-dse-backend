from flask import Flask
from flask_cors import CORS

from app.managers.firebase.firestoreManager import db_instance


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # 加載配置

    app.config.from_object('app.config.Config')

    # print(db_instance.add_document("users", {"name": "Alice", "age": 25, "email": "alice@example.com"}, "user_1"))

    # print("key", app.config['OPENAI_API_KEY'])
    # print("key", os.getenv('OPENAI_API_KEY'))
    # 註冊藍圖
    from .routes.drive_routes import drive_bp

    from .routes.ocr_routes import ocr_bp
    from .routes.practice_routes import practice_bp
    from .routes.solution_routes import solution_bp
    from .routes.database.question_bank import question_bank_bp

    @app.route('/', methods=['GET'])
    def index():
        return 'Connecting...'

    app.register_blueprint(drive_bp, url_prefix='/api/drive')

    # app.register_blueprint(image_blueprint, url_prefix="/api/image")
    app.register_blueprint(ocr_bp, url_prefix="/api/ocr")
    app.register_blueprint(solution_bp, url_prefix="/api/solution")
    app.register_blueprint(practice_bp, url_prefix="/api/practice")

    app.register_blueprint(question_bank_bp, url_prefix="/api/db/question_bank")
    # app.register_blueprint(other_bp, url_prefix='/api/other')

    return app
