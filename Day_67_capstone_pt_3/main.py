from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, select, update, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os
from rich import print as rp

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Ensure this is running in the intended directory.
cwd = os.getcwd()
proj_dir = os.path.dirname(__file__)

if cwd != proj_dir:
    os.chdir(proj_dir)
    rp("Changed the directory to the project directory.")

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # This grabs all post objects from the db and converts them to a list
    # of objects. I added the descending order so new posts will be on top.
    all_posts_scalar_obj = db.session.execute(select(
        BlogPost).order_by(desc(BlogPost.id))).scalars().all()
    posts = [post for post in all_posts_scalar_obj]

    return render_template("index.html", all_posts=posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    # I opted to change the endpoint instead of passing the param using:
    #   ?Post_id=n
    # This way I can force it to contain an integer.
    # I also kept both ways to query the db. 
    # I kept the 404 method for simplicity.

    # requested_post = db.session.execute(
    #     select(BlogPost).where(BlogPost.id == post_id)).scalar()
    
    requested_post = db.get_or_404(entity=BlogPost, ident=post_id)
    
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
