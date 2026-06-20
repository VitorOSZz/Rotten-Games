def generate_home():
    from flask import render_template
    from .games_services.SteamWebAPI_Service import get_new_releases_games, get_game_names
    
    quantity_of_games = 5
    games = get_new_releases_games(quantity_of_games)
    print(games)
    header_images = []
    for i in range(quantity_of_games):
        from .games_services.SteamWebAPI_Service import get_header_image
        header_images.append(get_header_image(games[i]))
    
    game_names = get_game_names(games)
    return render_template(
        "home.html",
        image_card1=header_images[0], game_name1= game_names[0],
        image_card2=header_images[1], game_name2= game_names[1],
        image_card3=header_images[2], game_name3= game_names[2],
        image_card4=header_images[3], game_name4= game_names[3],
        image_card5=header_images[4], game_name5= game_names[4])

def generate_admin():
    from flask import render_template

    from myapp.supabase import supabase
    from flask import session

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", session["email"])
        .limit(1)
        .execute()
    )

    user = response.data[0]
    return render_template("admin.html", admin_name=user["name"])

def generate_game(gameId="2215200"):
    appId = gameId
    url = f"https://store.steampowered.com/api/appdetails?appids={appId}"
    
    import requests
    response = requests.get(url)
        
    game_data = response.json()[str(appId)]["data"]

    game_name = game_data["name"]
    publisher = game_data["publishers"][0]
    developer = game_data["developers"][0]
    year_release = int(game_data["release_date"]["date"][-4:])
    genre = ", ".join(
        genre["description"]
        for genre in game_data["genres"]
    )
    
    from .games_services.SteamWebAPI_Service import get_header_image
    game_image = get_header_image(appId)
    
    from flask import render_template
    return render_template(
        "game.html",
        game_name=game_name,
        publisher=publisher,
        developer=developer,
        year_release=year_release,
        game_image=game_image,
        genre=genre)