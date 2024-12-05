from flask import Flask
from flask_cors import CORS
import os
def create_app():
    app = Flask(__name__)
    CORS(app)
    # 加載配置

    app.config.from_object('app.config.Config')
    # print("key", app.config['OPENAI_API_KEY'])
    # print("key", os.getenv('OPENAI_API_KEY'))
    # 註冊藍圖
    from .routes.drive_routes import drive_bp

    from .routes.ocr_routes import ocr_bp
    from .routes.practice_routes import practice_bp
    from .routes.solution_routes import solution_bp

    @app.route('/', methods=['GET'])
    def index():
        return 'Connecting...'

    app.register_blueprint(drive_bp, url_prefix='/api/drive')

    # app.register_blueprint(image_blueprint, url_prefix="/api/image")
    app.register_blueprint(ocr_bp, url_prefix="/api/ocr")
    app.register_blueprint(practice_bp, url_prefix="/api/practice")
    app.register_blueprint(solution_bp, url_prefix="/api/solution")
    # app.register_blueprint(other_bp, url_prefix='/api/other')

    return app
