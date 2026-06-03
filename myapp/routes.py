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
        
        email = request.form["email"]
        first_password = request.form["first_password"]
        second_password = request.form["second_password"]
        
        if first_password != second_password:
            return "Passwords isn't the same."
        
        try:
            register_user(email, first_password)
        except ValueError as ex:
            # Implement a new html/pop up for this email already exist in the database.
            return str(ex)
        
        return redirect(url_for("main.login"))

    return render_template("register.html")

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/users")
def users():
    return jsonify({"test": "test Yes"})