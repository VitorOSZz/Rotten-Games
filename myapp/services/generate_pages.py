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
    
    try:
        import requests
        response = requests.get(url)
        game_data = response.json()[str(appId)]["data"]

        if game_data is None:
            raise ValueError("Steam returned None")
        
        game_name = game_data["name"]
        publisher = game_data["publishers"][0]
        developer = game_data["developers"][0]
        year_release = int(game_data["release_date"]["date"][-4:])
        genre = ", ".join(
            genre["description"]
            for genre in game_data["genres"]
    )
        
    except Exception:
        from ..supabase import supabase
        from .general_functions import normalize
        response = supabase.table("games").select("*").eq("name_normalized", normalize(gameId)).limit(1).execute()
        
        print(f"GAME: {response.data}")
        if not response.data:
            return "Error"
        
        data = response.data[0]
        game_name = data["game_name"]
        publisher = data["publisher"]
        developer = data["developer"]
        year_release = data["year_release"]
        genre = data["genre"]
    
    
    from .games_services.SteamWebAPI_Service import get_header_image
    game_image = get_header_image(appId)
    
    review_link = f"{gameId}/review"
    
    from .review_service import get_reviews, reviews_formated
    get_reviews(gameId)
    reviews = reviews_formated(gameId)
    from .review_service import review_script_bar, review_script_pie
    
    from flask import render_template
    from .review_service import average_score
    from .general_functions import get_respective_image
    
    critic_average_score = average_score(gameId, "specialist")
    user_average_score = average_score(gameId, "user")
    return render_template(
        "game.html",
        game_name=game_name,
        publisher=publisher,
        developer=developer,
        year_release=year_release,
        game_image=game_image,
        genre=genre,
        review_link=review_link,
        reviews = reviews,
        script1=review_script_bar(gameId),
        script2=review_script_pie(gameId),
        user_average=user_average_score,
        critic_average=critic_average_score,
        critic_rate=get_respective_image(critic_average_score, "specialist"),
        user_rate=get_respective_image(user_average_score, "user")
        )

def generate_search_page(games):    
    
    txt = ""
    for game in games:
        
        #if game[]
        gameId = game["game_id"]
        game_name = game["game_name"]
        image_link = game["image_link"]
        
        txt += f'<a href="/games/{gameId}"><div class="game_card"><h3>{game_name}</h3><img src="{image_link}" alt=""></div></a>'
    from flask import render_template, render_template_string
    #return render_template_string(txt)
    return render_template("list_games.html", list=txt)

def generate_game_review(gameId: str):
    from flask import render_template, session
    from .games_services.SteamWebAPI_Service import get_header_image
    

    if "email" in session:
        if session["role"] == "user" or session["role"] == "specialist":
            game_image = get_header_image(gameId)
            return render_template("review.html", game_image=game_image, form_action=f"/games/{gameId}/review")
        else:
            return "admins can't post a review"
    
    return "Error, try login again"