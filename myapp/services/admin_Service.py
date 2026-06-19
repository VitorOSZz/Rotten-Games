def set_role():
    from flask import request
    email = request.form["email"]
    role = request.form["role"]
    
    from .auth_service import find_user_by_email
    
    from ..supabase import supabase
    
    supabase.table("users").update({"role": role}).eq("email", email).execute()
    
def add_game_to_DB():
    from flask import request
    
    game_name = request.form["game_name"]
    publisher = request.form["publisher"]
    year_release = request.form["year_release"]
    game_genres = request.form["game_genres"]
    
    from ..supabase import supabase
    
    supabase.table("games").insert({
            "game_name": game_name,
            "publisher": publisher, 
            "year_release": year_release, 
            "genre": game_genres}).execute()