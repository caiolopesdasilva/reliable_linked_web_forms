from flask import Flask
from .config import Development

def create_app(app_config='development'):

    app=Flask(__name__)
    
    print(config)
    app.config.from_object(Development())
    from app.main.routes import main

    app.register_blueprint(main)

    return app