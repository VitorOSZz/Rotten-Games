def get_MostPlayed_games():
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"

    import requests
    response = requests.get(url)
    data = response.json()

    top_games = data["response"]["ranks"][:5]
    
    appIDs = []
    for i in range(5):
        appIDs.append(str(top_games[i]["appid"]))
    
    return appIDs

def get_header_images(appIds: list[str]):
    
    header_images = []
    for i in range(5):
        image = f"https://steamcdn-a.akamaihd.net/steam/apps/{appIds[i]}/library_600x900_2x.jpg"
        
        header_images.append(image)
    
    return header_images

def get_game_names(appIds: list[str]):
    
    
    names = []
    for i in range(len(appIds)):
        url = f"https://store.steampowered.com/api/appdetails?appids={appIds[i]}"
        
        import requests
        response = requests.get(url)
        data = response.json()
        
        names.append(data[appIds[i]]["data"]["name"])
    
    return names