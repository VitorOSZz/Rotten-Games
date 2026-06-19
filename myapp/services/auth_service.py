from myapp.supabase import supabase
from myapp.extensions import bcrypt

def find_user_by_email(email): 
    response = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    return response

def register_user(name: str, email: str, password: str):
    existing_user = find_user_by_email(email).data
    
    if len(existing_user) > 0:
        raise ValueError("Email already exists")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        supabase.table("users").insert({
            "name": name,
            "email": email.lower(), 
            "password_hash": hashed_password, 
            "role": "user"}).execute()
        return True

def try_register_user():
    from flask import request, url_for, redirect
    
    name = request.form["name"]
    email = request.form["email"]
    from .validations import validate_name, validate_email, validate_password

    try:
        validate_name()
        validate_email()
        validate_password()
    except Exception as ex:
        return str(ex)
    
    password = request.form["first_password"]
    
    try:
        register_user(name, email, password)
    except ValueError as ex:
        # Implement a new html/pop up for this email already exist in the database.
        return str(ex)
    
    return redirect(url_for("main.login"))

def try_login():
    
    from flask import request
    
    email = request.form["email"]
    password = request.form["password"]
    
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )
    # Email not exist in database.
    if not response.data:
        return "User not found."
    
    user = response.data[0]
    
    # Password isn't correct.
    if not bcrypt.check_password_hash(user["password_hash"], password):
        return "Password incorrect."
    
    from flask import session, redirect
    session["role"] = user["role"]
    session["email"] = user["email"]

    return redirect("/")