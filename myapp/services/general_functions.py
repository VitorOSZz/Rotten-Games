def normalize(text):
    import unicodedata
    import re

    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text

def get_respective_image(score, role):
    image_link = ""
    if role == "user":
        if score <= 3:
            image_link = "../static/img/grades/30_Total.png"
        elif score <= 5:
            image_link = "../static/img/grades/50_Total.png"
        elif score <= 8:
            image_link = "../static/img/grades/80_Total.png"
        else:
            image_link = "../static/img/grades/80_Total.png"
    if role == "specialist":
        if score <= 3:
            image_link = "../static/img/grades/30_Critics.png"
        elif score <= 5:
            image_link = "../static/img/grades/50_Critics.png"
        elif score <= 8:
            image_link = "../static/img/grades/80_Critics.png"
        else:
            image_link = "../static/img/grades/100_Critics.png"
    return image_link