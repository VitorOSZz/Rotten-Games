def post_review():
    return True
def try_post_review(gameId):
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
    
    supabase.table("reviews").insert({
        "creator": creator,
        "role": role,
        "game_id": gameId,
        "review_text": review_text,
        "playtime_hours": playtime_hours,
        "main_point": main_point,
        "score": score
    }).execute()
    
    return redirect(url_for("main.games", gameId=gameId))