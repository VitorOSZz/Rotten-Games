def generate_home():
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