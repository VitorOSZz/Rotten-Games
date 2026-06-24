# Flask
from flask import Flask
from myapp.extensions import bcrypt
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    
    import os
    from dotenv import load_dotenv
    app.secret_key = os.getenv("SECRET_KEY")
    bcrypt.init_app(app)
    return app