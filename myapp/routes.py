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
        register()
    return render_template("register.html")

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/users")
def users():
    return jsonify({"test": "test Yes"})