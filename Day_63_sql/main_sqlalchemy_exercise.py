from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os
from rich import print as rp

os.chdir(os.path.dirname(__file__))

#### adding a dynamic way to turn on/off the inserts


delete_all = True #fixed, used for rerun cleanup experimenting.
create = True
read = True
update = True
delete = True



# First we need to initialize the db
# the SQLAlchemy class will be the constructor.
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# "Once constructed, the db object gives you access to 
# the db.Model class to define models, and the db.session to execute queries."
# https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/

# Configure the extension
# The next step is to connect the extension to your Flask app. 
# The only required Flask app config is the SQLALCHEMY_DATABASE_URI key. 
# That is a connection string that tells SQLAlchemy what database to connect to.

# Create the flask app
app = Flask(__name__)

# config SQLite DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# init the app with the extension
db.init_app(app)

# Subclass db.Model to define a model class. 
# The model will generate a table name by converting the 
# CamelCase class name to snake_case.
# -- so here that means User is the table name converted to user.
# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     username: Mapped[str] = mapped_column(unique=True)
#     email: Mapped[str]

class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    rating: Mapped[float]

    # Optional dunder method to produce a string rep of the created object
    # If I used the auto complete, this is literally what creates the...
    ## X object at 0x{some memory location number}
    # def __repr__(self):
    #     return super().__repr__()
    
    # This will force custom output such as the book object's attr title
    # __repr__ is the fallback if __str__ is not set.
    def __repr__(self):
        return f"Book {self.title}"
    
# with app.app_context():
#     db.create_all()
    
# as long as the db.init_app(app) is called, this should work.
# The idea being to make this self cleaning by changing the bool settings above.

if delete_all:
    with app.app_context():
        num_deleted = db.session.query(Books).delete()
        # db.session.execute(db.drop_all()) # Does not work here
        db.session.commit()

if create:
    # After all models and tables are defined, call SQLAlchemy.create_all() to 
    # create the table schema in the database. 
    # This requires an application context. 
    # Since you’re not in a request at this point, create one manually.

    with app.app_context():
        db.create_all()

    # create_all does not update tables if they are already in the database. 
    # If you change a model’s columns, use a migration library like Alembic with 
    # Flask-Alembic or Flask-Migrate to generate migrations that 
    # update the database schema.

    # Within a Flask view or CLI command, you can use db.session 
    # to execute queries and modify model data.

    # Create a record within the tables above.

    ## activate/open the app context like when we interact with a file.
    with app.app_context():
        new_book = Books(title="Harry Potter", author="J. K. Rowling",
                        rating=9.3)
        print("Adding the new book...")
        db.session.add(new_book)
        print("Committing the new book.")
        db.session.commit()

    with app.app_context():
        new_book = Books(title="Harry Potter123123", author="J. K. Rowling",
                        rating=9.3)
        print("Adding the new book...")
        db.session.add(new_book)
        print("Committing the new book.")
        db.session.commit()

    # with app.app_context():
    #     new_entry = Users(username="testing", email="something@test.com")
    #     print("adding the new user")
    #     db.session.add(new_entry)
    #     print("Committing the new user.")
    #     db.session.commit()
        



    ## None of this is needed because we are not doing the entry from the website
    ## We are basically just leveraging the sqlalchemy with flask behind the scenes.

    # @app.route("/users")
    # def user_list():
    #     users = db.session.execute(
    #         db.select(User).order_by(User.username)).scalars()
    #     return render_template("user/list.html", users=users)

    # @app.route("/users/create", methods=["GET", "POST"])
    # def user_create():
    #     if request.method == "POST":
    #         user = User(
    #             username=request.form["username"],
    #             email=request.form["email"],
    #         )
    #         db.session.add(user)
    #         db.session.commit()
    #         return redirect(url_for("user_detail", id=user.id))

    #     return render_template("user/create.html")

    # @app.route("/user/<int:id>")
    # def user_detail(id):
    #     user = db.get_or_404(User, id)
    #     return render_template("user/detail.html", user=user)

    # @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
    # def user_delete(id):
    #     user = db.get_or_404(User, id)

    #     if request.method == "POST":
    #         db.session.delete(user)
    #         db.session.commit()
    #         return redirect(url_for("user_list"))

#     return render_template("user/delete.html", user=user)
if read:
# #### to read the database:
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars()
        rp(all_books.all())

    with app.app_context():
        book = db.session.execute(
            db.select(Books).where(Books.title == "Harry Potter")).scalar()
        rp(book)

if update:
    book_id = 1
    with app.app_context():
        book_to_update = db.session.execute(db.select(Books).where(
            Books.id == book_id)).scalar()
        # we can also do book_update = db.get_or_404(Books, book_id)
        book_to_update.title = "Harry Potter and the Goblet of Fire"
        db.session.commit()

if delete:
    # before the delete
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars()
        rp(all_books.all())

    book_id = 2
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Books).where(
            Books.id == book_id)).scalar()
        # or book_to_delete = db.get_or_404(Books, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()

    # after the delete
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars()
        rp(all_books.all())


if __name__ == '__main__':
    app.run(
        debug=True, use_reloader=False
        )