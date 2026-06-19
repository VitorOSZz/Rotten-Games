from myapp.services.auth_service import register_user
from flask import Blueprint, jsonify, request, render_template, url_for, redirect

bp = Blueprint("main", __name__)

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})

@bp.route("/admin_painel/<action>", methods=["GET", "POST"])
def admin_painel(action):
    from flask import session
    if not "email" in session:
        return "Boboca"
    
    from .services.auth_service import is_admin
    if not is_admin(session["email"]):
        return "Boboca 2"
    
    if request.method == "POST":
        if action == "change_role":
            from .services.admin_Service import set_role
            set_role()
        elif action == "games_database":
            from .services.admin_Service import add_game_to_DB
            add_game_to_DB()
    
    from .services.generate_pages import generate_admin
    return generate_admin()

@bp.route("/")
def index():
    from flask import session

    if "role" in session:
        if session["role"] == "user" or session["role"] == "specialist":
            from .services.generate_pages import generate_home
            return generate_home()
        elif session["role"] == "admin":
            return admin_painel("")
    
    return render_template("login.html")

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