from flask import Flask, render_template
import random
from datetime import datetime as dt

# Just adding the next phase to this one.
import requests

app = Flask(__name__)



# stopped at 3:54 of video 397.

def get_gender(name):
    """Guess which gender a name is."""
    # https://genderize.io/documentation
    gender_endpoint = "https://api.genderize.io?name="
    """
    sample response:
    Response
    {
        "count": 1094417,
        "name": "peter",
        "gender": "male",
        "probability": 1
    }
    """
    response_raw = requests.get(f"{gender_endpoint}{name}")
    response_json = response_raw.json()
    return response_json["gender"]


def get_age(name):
    """Guess what age a person is based on their name."""
    # https://agify.io/documentation#basic-usage
    age_endpoint = "https://api.agify.io?name="

    """
    sample response:
    Response
    {
        "count": 298219,
        "name": "michael",
        "age": 62
    }
    """

    response_raw = requests.get(f"{age_endpoint}{name}")
    response_json = response_raw.json()
    return response_json["age"]

@app.route("/")
def home():
    random_number = random.randint(1, 10)
    # current_year = dt.strftime(dt.today(), "%Y")
    current_year = dt.today().year
    # I can add as many keyword args as I need after the initial template
    # **context == **kwargs
    # use the param within the context with the keyword.
    # Then refer to this back in the html
    return render_template("index.html", num=random_number, cur_year=current_year)

@app.route("/r/<name>")
def req_ex(name:str):
    username = name.capitalize()
    gender_guess = get_gender(name=name)
    age_guess = get_age(name=name)
    return render_template("index_req.html", name=username, gender_guess=gender_guess, age_guess=age_guess)

@app.route("/blog1")
def blog1():
    # url_endpoint = "https://www.npoint.io/docs/c790b4d5cab58020d391"
    api_endpoint = "https://api.npoint.io/c790b4d5cab58020d391"
    full_content = requests.get(api_endpoint).json()
    return render_template("blog1.html", all_blog_posts = full_content)

@app.route("/blog2")
def blog2():
    api_endpoint = "https://api.npoint.io/c790b4d5cab58020d391"
    full_content = requests.get(api_endpoint).json()
    return render_template("blog2.html", all_blog_posts = full_content)

if __name__ == "__main__":
    app.run(debug=True)