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
            "email": email, 
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
    
    from flask import render_template
    from .SteamWebAPI_Service import get_MostPlayed_games, get_header_images, get_game_names
    
    games = get_MostPlayed_games()
    header_images = get_header_images(games)
    game_names = get_game_names(games)
    return render_template(
        "home.html",
        image_card1=header_images[0], game_name1= game_names[0],
        image_card2=header_images[1], game_name2= game_names[1],
        image_card3=header_images[2], game_name3= game_names[2],
        image_card4=header_images[3], game_name4= game_names[3],
        image_card5=header_images[4], game_name5= game_names[4])