from myapp.supabase import supabase
from myapp.extensions import bcrypt

def find_user_by_email(email): 
    response = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    return response

def register_user(email, password):
    existing_user = find_user_by_email(email).data
    
    if len(existing_user) > 0:
        raise ValueError("Email already exists")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        supabase.table("users").insert({
            "email": email, 
            "password_hash": hashed_password, 
            "role": "user"}).execute()
        return True