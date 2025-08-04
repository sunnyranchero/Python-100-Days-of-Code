from flask import Flask, render_template
import requests
from post import Post
from rich import print as rp

# We 1st have to compile a listing of data before starting up the server.
# This will allow a central place to go back to. I'm view this as the "database"
# Will need to learn how to make this call while the server is up.
api_endpoint = "https://api.npoint.io/c790b4d5cab58020d391"
post_objects_list = []
all_blog_posts = requests.get(api_endpoint).json()

for post_single_json in all_blog_posts:
    post_object = Post(
        id=post_single_json["id"], 
        title=post_single_json["title"],
        subtitle=post_single_json["subtitle"],
        body=post_single_json["body"]
    )
    post_objects_list.append(post_object)

app = Flask(__name__)

@app.route('/')
def render_all_posts():   
    return render_template("index.html", blog_posts=post_objects_list)

# This will accept the post number id as the arg in order to select the single post.
# The link/href will pass this argument.
@app.route('/blog/<int:post_num>')
def single_blog(post_num):
    # Declare the variable to house the post object
    selected_post_object = None
    # Cycle through each post object, the one that has the same id as the requested is sent out.
    for blog_post_object in post_objects_list:
        if blog_post_object.id == post_num:
            selected_post_object = blog_post_object
    return render_template("post.html", blog_post=selected_post_object)

if __name__ == "__main__":
    app.run(debug=True)
