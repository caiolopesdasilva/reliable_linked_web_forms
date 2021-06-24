from flask import Flask
from .config import Development, TESTING
from .main.routes import main


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.config['SECRET_KEY'] = '12312312313'
    print(config)
    app.config.from_object(Development())
    return app
