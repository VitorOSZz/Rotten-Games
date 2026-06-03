from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("main", __name__)

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/users")
def users():
    return jsonify({"test": "test Yes"})