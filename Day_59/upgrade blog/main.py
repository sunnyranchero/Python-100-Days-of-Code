from flask import Flask, render_template
import requests
from rich import print as rp

app = Flask(__name__)

API_ENDPOINT = "https://api.npoint.io/cadbb639003d1baeeaf6"


@app.route("/")
def home():
    global API_ENDPOINT
    full_json_content = requests.get(API_ENDPOINT).json()
    rp(full_json_content)
    return render_template("index.html", all_posts_json = full_json_content)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



# Place this line at the bottom in order to run this directly

if __name__ == "__main__":
    app.run(debug=True)