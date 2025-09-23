from flask import Flask, render_template
import requests
from rich import print as rp

app = Flask(__name__)

API_ENDPOINT = "https://api.npoint.io/cadbb639003d1baeeaf6"
full_json_content = requests.get(API_ENDPOINT).json()
# rp(full_json_content)


@app.route("/")
def home():
    return render_template("index.html", all_posts_json = full_json_content)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in full_json_content:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)



# Place this line at the bottom in order to run this directly

if __name__ == "__main__":
    app.run(debug=True)