def get_MostPlayed_games(how_many_games: int):
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"

    import requests
    response = requests.get(url)
    data = response.json()

    top_games = data["response"]["ranks"][:how_many_games]
    
    appIDs = []
    for i in range(how_many_games):
        appIDs.append(str(top_games[i]["appid"]))
    
    return appIDs

def get_new_releases_games(how_many_games: int):
    import requests
    featured = requests.get("https://store.steampowered.com/api/featuredcategories").json()
    
    new_releases = featured["new_releases"]["items"][:how_many_games]
    games_id = []
    for game in new_releases:
        games_id.append(str(game["id"]))
    return games_id

# Tirar esse get header images e botar a logica no generate_pages

def get_header_image(steam_id: str):
    url = f"https://steamcdn-a.akamaihd.net/steam/apps/{steam_id}/library_600x900_2x.jpg"
    
    import requests

    response = requests.head(url)
    print(response.status_code)
    if response.status_code == 200:
        return url
    else:
        url = f"https://store.steampowered.com/api/appdetails?appids={steam_id}"
        
        response = requests.get(url)
        data = response.json()[str(steam_id)]["data"]
        header_image = data["header_image"]
        return header_image

def get_game_names(appIds: list[str]):
    
    
    names = []
    for i in range(len(appIds)):
        url = f"https://store.steampowered.com/api/appdetails?appids={appIds[i]}"
        
        import requests
        response = requests.get(url)
        data = response.json()
        
        names.append(data[appIds[i]]["data"]["name"])
    
    return names