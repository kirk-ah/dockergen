# flask_case3_factory/myproject/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello from factory!"

    return app