def search_games():
    
    from flask import request
    user_search = request.form["games_search"]
    print(user_search)
    
    from ..supabase import supabase
    own_db = supabase.table("games") \
    .select("game_name", "image_link") \
    .ilike("name_normalized", f"%{user_search}%") \
    .limit(10) \
    .execute()
    
    db_games = own_db.data
    games = db_games
    
    for game in games:
        game["game_id"] = game["game_name"]
    
    import requests
    from urllib.parse import quote
    STEAM_ENDPOINT = f"https://store.steampowered.com/api/storesearch/?term={quote(user_search)}&l=english&cc=US"
    #"https://store.steampowered.com/api/storesearch/?term=batman&l=english&cc=US"
    steam_data = requests.get(STEAM_ENDPOINT).json()
    
    for game in steam_data["items"]:
        if str(game["type"]) != "app":
            continue
        
        games.append({
        "game_name": game["name"],
        "game_id": game["id"],
        "image_link": game["tiny_image"]
    })
    
    return games

