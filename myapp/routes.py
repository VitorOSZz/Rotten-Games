from myapp.supabase import supabase
from flask import Blueprint, jsonify, request, render_template, url_for

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

@bp.route("/test-db")
def test_db():
    response = (
        supabase.table("users")
        .insert({
            "email": "teste2@gmail.com",
            "password_hash": "senha123hash",
            "role": "user"
        })
        .execute()
    )

    return str(response.data)