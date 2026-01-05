from flask import (
    Flask, render_template, request, url_for, 
    redirect, flash, send_from_directory)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, func, select, update
from flask_login import (
    UserMixin, login_user, LoginManager, 
    login_required, current_user, logout_user)
# These are 2 packages that I prefer to use.
import os
from rich import print as rp

# Adding the lines to force this program to run in the scope of this proj.
# This is due to how I chose to set this program up.
cwd = os.getcwd()
proj_dir = os.path.dirname(__file__)

if cwd != proj_dir:
    os.chdir(proj_dir)
    rp("[red]Changed the cwd to use this proj dir.[/red]")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE

class Base(DeclarativeBase):
    # Create a child class that inherits from the declarative meta class init.
    # sets us up to have a register for all future classes inheriting from this
    # child class.
    pass

# This is creating the database also called users.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB

# this creates a child class that represents the User table metadata 
# from the db.
# the metaclass from the parent adds the entry back to the Base in the model.
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer,
                                     primary_key=True,
                                     autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

####################### Proj logic goes here ###########################

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """Register the user if one does not exist."""

    if request.method == "POST":
        # Get the username from the form.
        form_name = request.form["name"]
        form_email = request.form["email"]
        form_password = generate_password_hash(
            request.form["password"],
            method="pbkdf2:sha256",
            salt_length=8)
                                               
        
        rp(f"{form_name} | {form_email} | {form_password}")

        # confirm the email does not exist by counting
        count_query = select(
            func.count()).select_from(User).where(User.email==form_email)
        
        email_count = db.session.execute(count_query).scalar()

        rp(f"[blue]Email exist check:[/blue][green]{email_count}[/green]")

        if email_count == 0:
            new_user = User(
                email=form_email,
                password=form_password,
                name=form_name
            )
            db.session.add(new_user)
            db.session.commit()
            
            return render_template("secrets.html", user_name=form_name)
        
        else:
            return render_template("register.html", user_taken=True)

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory("static", 
                               "files/cheat_sheet.pdf",
                               as_attachment=False,
                               mimetype='application/pdf')


if __name__ == "__main__":
    app.run(debug=True)
