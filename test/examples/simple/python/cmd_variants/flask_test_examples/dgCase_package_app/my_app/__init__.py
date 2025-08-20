# flask/package_app/myapp/__init__.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from package!"