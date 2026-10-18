from flask import Flask
from my_app.hello_as_bp.handlers import hello as hello_bp

app = Flask(__name__)
app.register_blueprint(hello_bp)