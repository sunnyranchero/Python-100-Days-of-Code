from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os # needed to set the cwd correctly in my setup.
from rich import print as rp

os.chdir(os.path.dirname(__file__))
app = Flask(__name__)

# This is set to pass because nothing more has to be altered...
# ...It simply inherits.
# First we need to initialize the db
# the SQLAlchemy class will be the constructor.
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///d63-combined-collection.db"
db.init_app(app)

# Now the db can be interacted with.

# define the table
class BooksCollection(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    rating: Mapped[float]

    def __repr__(self):
        return f"Book: {self.title}"
    
# Create the table if it does not already exist.
with app.app_context():
    db.create_all()

all_books = []

def refresh_listing():
    """Create a reusable way to refresh the current lsting."""
    with app.app_context():
        select_all_results = db.session.execute(db.select(BooksCollection))
        book_objects = select_all_results.scalars()
        for book_obj in book_objects:
            temp_dict = {}
            temp_dict["title"] = book_obj.title
            temp_dict["author"] = book_obj.author
            temp_dict["rating"] = book_obj.rating
            rp(temp_dict)

            all_books.append(temp_dict)

refresh_listing()
# exit()

@app.route('/')
def home():

    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
# GET is so the user can be served the form
# POST is so we can submit the form with the inputted data.
def add():
    # Set up my data and update the flask route
    if request.method == "POST":
        new_book = {
            "title":request.form.get(key="title"),
            "author":request.form.get(key="author"),
            "rating":request.form.get(key="rating"),
        }
        rp(new_book)
        all_books.append(new_book)
        
        return redirect(url_for('home'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

