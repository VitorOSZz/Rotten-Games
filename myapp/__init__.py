# Flask
from flask import Flask
from myapp.extensions import bcrypt
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    
    from secrets import token_hex
    app.secret_key = token_hex()
    bcrypt.init_app(app)
    return app