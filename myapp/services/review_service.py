def post_review(gameId):
    from flask import request, session, redirect, url_for
    
    if not "email" in session:
        return "Try login again"
    
    creator = session["email"]
    role = session["role"]
    review_text = request.form["text_review"]
    playtime_hours = request.form["played_time"]
    main_point = request.form["main_point"]
    score = request.form["grade"]
    
    from ..supabase import supabase
    from .general_functions import normalize
    supabase.table("reviews").insert({
        "creator": creator,
        "role": role,
        "game_id": normalize(gameId),
        "review_text": review_text,
        "playtime_hours": playtime_hours,
        "main_point": main_point,
        "score": int(score)
    }).execute()
    
    return redirect(url_for("main.games", gameId=gameId))

def get_reviews(gameId: str):
    from ..supabase import supabase
    
    response = supabase.table("reviews").select("*").eq("game_id", gameId).limit(10).execute()
    
    if not response.data:
        return ""
    
    data = response.data
    reviews = []
    for dataDB in data:
        review = {
            "creator": dataDB["creator"],
            "role": dataDB["role"],
            "review_text": dataDB["review_text"],
            "playtime_hours": dataDB["playtime_hours"],
            "score": dataDB["score"]}
        reviews.append(review)
    
    return reviews

def reviews_formated(gameId: str):
    
    text = ""
    
    reviews = get_reviews(gameId)
    
    from ..supabase import supabase
    
    for review in reviews:
        response = supabase.table("users").select("name", "role").eq("email", review["creator"]).limit(1).execute()
        user_name = response.data[0]["name"]
        score = int(review["score"])
        user_text = review["review_text"]
        
        if review["role"] == "user":
            if score <= 3:
                image_link = "../static/img/grades/30_Total.png"
            elif score <= 5:
                image_link = "../static/img/grades/50_Total.png"
            elif score <= 8:
                image_link = "../static/img/grades/80_Total.png"
            else:
                image_link = "../static/img/grades/80_Total.png"
        if review["role"] == "specialist":
            if score <= 3:
                image_link = "../static/img/grades/30_Critics.png"
            elif score <= 5:
                image_link = "../static/img/grades/50_Critics.png"
            elif score <= 8:
                image_link = "../static/img/grades/80_Critics.png"
            else:
                image_link = "../static/img/grades/100_Critics.png"
        
        text +=f'<div class="review"><div class="top"><div class="name"><h1>{user_name}</h1></div><div class="grade"><img src="{image_link}"><h1>{score}/10</h1></div></div><div class="content"><p>{user_text}</p></div></div>\n'
    
    return text

def review_script_bar(gameId: str):
    from ..supabase import supabase
    from .general_functions import normalize

    response = (
        supabase.table("reviews")
        .select("playtime_hours")
        .eq("game_id", normalize(gameId))
        .execute()
    )

    buckets = {
        "0-2h": 0,
        "2-5h": 0,
        "5-10h": 0,
        "10-100h": 0,
        "100-300h": 0,
        "300h+": 0
    }

    for review in response.data:
        hours = review["playtime_hours"]

        if hours < 2: buckets["0-2h"] += 1
        elif hours < 5: buckets["2-5h"] += 1
        elif hours < 10: buckets["5-10h"] += 1
        elif hours < 100: buckets["10-100h"] += 1
        elif hours < 300: buckets["100-300h"] += 1
        else: buckets["300h+"] += 1

    x = f"""
    {{
        x: {list(buckets.keys())},
        y: {list(buckets.values())},
        type: 'bar'
    }}
    """

    return f"""
    var data = [{x}];
    Plotly.newPlot('chart_1', data);
    """

def get_review_percent(gameId):
    from ..supabase import supabase
    
    response = supabase.table("reviews").select("playtime_hours", "main_point").eq("game_id", gameId).execute()
    
    if not response.data:
        return [0, 0, 0, 0, 0]
    data = response.data
    
    
    total = 0
    
    graphics, story, multiplayer, playability, none = 0, 0, 0, 0, 0
    
    for review in data:
        total += 1
        match review["main_point"]:
            case "Graphics": graphics += 1
            case "Story": story += 1
            case "Multiplayer": multiplayer += 1
            case "Playability": playability += 1
            case "None": none += 1
            
    number = [
        int((graphics/total) * 100),
        int((story/total) * 100),
        int((multiplayer/total) * 100),
        int((playability/total) * 100),
        int((none/total) * 100)]
    
    return number

def review_script_pie(gameId: str):
    
    values = get_review_percent(gameId)
    
    if values == [0, 0, 0, 0, 0]:
        return ""
    x = f"""
    {{
        values: {values},
        labels: ['Graphics', 'Story', 'Multiplayer', 'Playability', 'None'],
        type: 'pie'
    }}
    """

    data = x

    layout = """
    {
        height: 400,
        width: 500
    }
        """
    

    text = f"""
    var data = [{data}];
    
    var layout = {layout};
    
    Plotly.newPlot('chart_2', data, layout);"""
    
    return text

def average_score(gameId: str, role: str):
    from ..supabase import supabase
    from .general_functions import normalize
    response = supabase.table("reviews").select("score").eq("game_id", normalize(gameId)).eq("role", role).execute()
    
    #print(f"\ndata: {response.data}\n")
    data = response.data
    
    if not data:
        return 0
    
    total_score = 0
    for review in data:
        total_score += review["score"]
    
    average = int(total_score * 10 / len(data))
    return average