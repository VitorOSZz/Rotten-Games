from flask import redirect, url_for, request
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

def register_user(email, password):
    existing_user = find_user_by_email(email).data
    
    if len(existing_user) > 0:
        raise ValueError("Email already exists")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        supabase.table("users").insert({
            "email": email, 
            "password_hash": hashed_password, 
            "role": "user"}).execute()
        return True
    
def register():

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