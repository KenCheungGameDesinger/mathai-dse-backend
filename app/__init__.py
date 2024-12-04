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
    from .routes.openai_routes import openai_bp
    from .routes.drive_routes import drive_bp
    # from .routes.other_routes import other_bp

    @app.route('/', methods=['GET'])
    def index():
        key = os.getenv("OPENAI_API_KEY")
        print("KEY",key)
        return 'Connecting...'+"API",str(key)

    app.register_blueprint(openai_bp, url_prefix='/api/openai')
    app.register_blueprint(drive_bp, url_prefix='/api/drive')
    # app.register_blueprint(other_bp, url_prefix='/api/other')

    return app
