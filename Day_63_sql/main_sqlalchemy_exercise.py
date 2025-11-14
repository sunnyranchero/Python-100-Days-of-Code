from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os

os.chdir(os.path.dirname(__file__))

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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# init the app with the extension
db.init_app(app)

# Subclass db.Model to define a model class. 
# The model will generate a table name by converting the 
# CamelCase class name to snake_case.
# -- so here that means User is the table name converted to user.
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]

class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    rating: Mapped[float]

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

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)