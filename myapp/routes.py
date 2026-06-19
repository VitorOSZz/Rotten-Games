from myapp.services.auth_service import register_user
from flask import Blueprint, jsonify, request, render_template, url_for, redirect

bp = Blueprint("main", __name__)

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        from .services.auth_service import try_register_user
        
        return try_register_user()

    return render_template("register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # admin go to admin painel
        from .services.auth_service import try_login
        
        return try_login()
    
    return render_template("login.html")

@bp.route("/users")
def users():
    return jsonify({"test": "test Yes"})