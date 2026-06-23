def set_role():
    from flask import request, session
    email = request.form["email"]
    
    if not "email" in session:
        return "Boboca 4"
    
    role = request.form["role"]
    
    from .auth_service import find_user_by_email
    from ..supabase import supabase
    
    if not find_user_by_email(email):
        return "This user was not found"
    
    supabase.table("users").update({"role": role}).eq("email", email).execute()
    return "changed"
def add_game_to_DB():
    from flask import request
    
    from ..supabase import supabase
    game_name = request.form["game_name"]
    from .general_functions import normalize
    name_normalized = normalize(game_name)
    publisher = request.form["publisher"]
    developer = request.form["developer"]
    year_release = request.form["year_release"]
    game_genres = request.form["game_genres"]
    image_link = request.form["image_link"]
    
    already_exist = supabase.table("games").select("game_name").eq("game_name", game_name).limit(1).execute()
    
    if already_exist.data:
        # This game already exist
        supabase.table("games").update({
            "game_name": game_name,
            "name_normalized": name_normalized,
            "publisher": publisher,
            "developer": developer,
            "year_release": year_release,
            "genre": game_genres,
            "image_link": image_link}).eq("game_name", game_name).execute()
        
        return f"Change data about {game_name}"
    
    supabase.table("games").insert({
            "game_name": game_name,
            "name_normalized": name_normalized,
            "publisher": publisher, 
            "developer": developer,
            "year_release": year_release, 
            "genre": game_genres,
            "image_link": image_link}).execute()
    
    game = supabase.table("games").select("game_name").eq("game_name", game_name).limit(1).execute()
    
    if game.data:
        return "Added"
    
    return "Not added"