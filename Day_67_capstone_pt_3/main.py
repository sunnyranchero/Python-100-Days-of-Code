from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, select, update, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask_ckeditor.utils import cleanify
from datetime import date as dt
import os
from titlecase import titlecase
from rich import print as rp


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
ckeditor = CKEditor(app)

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

class PostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post", validators=[DataRequired()])



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
@app.route("/new-post", methods=['GET','POST'])
def add_new_post():
    form = PostForm()

    if form.validate_on_submit():
        today_date = dt.today().strftime("%B %d, %Y")
        rp(form.title.data)
        rp(form.subtitle.data)
        rp(form.author.data)
        rp(form.img_url.data)
        rp(form.body.data)
        new_post = BlogPost(
            title=titlecase(form.title.data),
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=cleanify(form.body.data),
            date=today_date
        )
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)

# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, ident=post_id)

    edit_form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body,
    )

    if edit_form.validate_on_submit():
        # perform the updates in this field.
        post.title=titlecase(edit_form.title.data)
        post.subtitle=edit_form.subtitle.data
        post.author=edit_form.author.data
        post.img_url=edit_form.img_url.data
        post.body=cleanify(edit_form.body.data)
        # The date is untouched as specified
        # This will produce an update statement to the db
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True)

# TODO: delete_post() to remove a blog post from the database
@app.route("/delete-post/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(BlogPost, ident=post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
