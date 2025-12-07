from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os # needed to set the cwd correctly in my setup.
from rich import print as rp

os.chdir(os.path.dirname(__file__))
app = Flask(__name__)
##############################################################
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
############################################################

all_books = []

def truncate_table():
    """This will truncate the existing table to restart it."""
    with app.app_context():
        record_count_truncated = db.session.query(BooksCollection).delete()
        rp(f"Total records deleted: {record_count_truncated}")
        db.session.commit()

def set_testing_data():
    """This will insert testing data during the project dev"""
    with app.app_context():
        test_book1 = BooksCollection(title="TestTitle1",
                                     author="TestAuthor1",
                                     rating=99.1)
        test_book2 = BooksCollection(title="TestTitle2",
                                     author="TestAuthor2",
                                     rating=99.2)
        test_book3 = BooksCollection(title="TestTitle3",
                                     author="TestAuthor3",
                                     rating=99.3)
        db.session.add_all([test_book1, test_book2, test_book3])
        db.session.commit()
        rp("Records added : 3")

def refresh_listing():
    """Create a reusable way to refresh the current lsting."""
    with app.app_context():
        all_books.clear()
        select_all_results = db.session.execute(db.select(BooksCollection))
        book_objects = select_all_results.scalars()
        for book_obj in book_objects:
            temp_dict = {}
            temp_dict["id"] = book_obj.id
            temp_dict["title"] = book_obj.title
            temp_dict["author"] = book_obj.author
            temp_dict["rating"] = book_obj.rating
            rp(temp_dict)

            all_books.append(temp_dict)

def insert_new_book(title:str, author:str, rating:float):
    """Generate a reusable process for adding new book entries. """
    with app.app_context():
        new_book = BooksCollection(title=title,
                                   author=author,
                                   rating=rating)
        rp("Adding a new book...")
        db.session.add(new_book)
        db.session.commit()

def update_entry(book_title_orig:str, field_to_update:str, value):
    """send a dict of {"author":"value, "title":"value", "rating":value}"""
    # Convert the book title to the id
    # Then do the update off the id which is the PK.
    # Title is unique so either could technically work here. 
    # I simply prefer using the pk
    db_obj = db.session.execute(
        db.select(BooksCollection).where(BooksCollection.title==book_title_orig)
    ).scalar()
    if db_obj is not None:
        with app.app_context():
            book_update = db.session.execute(
                db.select(BooksCollection).where(BooksCollection.id==db_obj.id)
            ).scalar()
            if field_to_update.lower() == "author":
                book_update.author = value
                rp("Update completed")
            elif field_to_update.lower() == "title":
                book_update.title = value
                rp("Update completed")
            elif field_to_update.lower() == "rating":
                book_update.rating = value
                rp("Update completed")
            else:
                rp(f"{field_to_update} is not a valid value.")
                rp(f"Please select: author, title, or rating.")



# exit()

@app.route('/')
def home():
    # Refresh the listing upon going to the home page.
    refresh_listing()
    return render_template("index.html", books=all_books)

@app.route("/edit/<book_id>", methods=["GET", "POST"])
def edit(book_id):
    # This part allows for retrieval of the book id from the home page.
    # book_id = request.args.get("book_id")

    # Placing this here creates the object instance.
    # it can be used to change the value in the database.

    if request.method == "POST":
        # print(f"The book ID2 is: {book_id}")
        book_to_update = db.get_or_404(BooksCollection, book_id)
        print(f"The book ID is: {book_to_update.id}")
        # print(f"rating print test2: {book.rating}")
        # Get the new rating from the input form
        try:
            new_rating = float(request.form["rating"])
        except ValueError as e:
            print(f"The float conversion was invalid\nRedirecting home...")
            return redirect(url_for("home"))
        # Assign the new rating into the database.
        book_to_update.rating = new_rating
        db.session.commit()

        print(f"The new rating is: {new_rating}")
        return redirect(url_for("home"))   
    
    book = db.get_or_404(BooksCollection, book_id)
    print(f"GET: The book ID is: {book_id}")
    print(f"GET: rating print test: {book.rating}")
    return render_template("update_rating.html", book=book)


@app.route("/add", methods=["GET", "POST"])
# GET is so the user can be served the form
# POST is so we can submit the form with the inputted data.
def add():
    # Set up my data and update the flask route
    if request.method == "POST":
        if request.form.get(key="type").lower() == "add":
            new_book = {
                "title":request.form.get(key="title"),
                "author":request.form.get(key="author"),
                "rating":request.form.get(key="rating"),
            }
            rp(new_book)
            # all_books.append(new_book)
            # Update the db to reflect the new add.
            insert_new_book(title=new_book["title"],
                            author=new_book["author"],
                            rating=new_book["rating"])
            
            return redirect(url_for('home'))
        
        elif request.form.get(key="type").lower() == "update":
            # TODO: make this function by getting the info from the form.
            ## Or just make a drop down of all the available titles.
            update_entry(book_title_orig="test2", field_to_update="", value="")

            return redirect(url_for('home'))
        
        elif request.form.get(key="type") == "delete":
            if request.form.get(key="title").lower() == "!reset!":
                truncate_table()
                set_testing_data()

                return redirect(url_for('home'))


    return render_template("add.html")

@app.route("/delete/<book_id>", methods=["GET", "POST"])
def delete(book_id):
    book = db.get_or_404(BooksCollection, book_id)
    db.session.delete(book)
    db.session.commit()
    
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

