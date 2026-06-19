def validate_name():
    from flask import request
    
    name = request.form["name"]
    if len(name) > 16:
        raise Exception("This name is too long")

    from re import fullmatch
    return bool(fullmatch(r"[A-Za-zÀ-ÿ]+", name))

def validate_email():
    from flask import request
    
    email = request.form["email"]
    
    from email_validator import validate_email, EmailNotValidError

    try:
        # Check that the email address is valid. Turn on check_deliverability
        # for first-time validations like on account creation pages (but not
        # login pages).
        emailinfo = validate_email(email, check_deliverability=False)

        # After this point, use only the normalized form of the email address,
        # especially before going to a database query.
        email = emailinfo.normalized

    except EmailNotValidError as e:

        # The exception message is human-readable explanation of why it's
        # not a valid (or deliverable) email address.
        raise Exception("This email is not valid.")
    
    return True

def validate_password():
    from flask import request
    
    first_password = request.form["first_password"]
    if len(first_password) >= 4 and len(first_password) <= 16:
        
        second_password = request.form["second_password"]
        
        if first_password != second_password:
            raise Exception("Passwords isn't the same.")
    else:
        raise Exception("Passwords doesn't have more than 4 characters or less than 16")