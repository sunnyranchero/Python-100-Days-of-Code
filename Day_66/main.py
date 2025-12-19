from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func, select, update
import random as rand
from rich import print as rp
import os

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

if os.getcwd() != os.path.dirname(__file__):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    rp("[green]CWD was changed to the current proj scope[/green]")

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    # Alt way of creating a dict object for jsonify

    def to_dict(self, compr=False):
        dict_obj = {}
        if compr == False:
            for column in self.__table__.columns:
                # create a new dict entry
                # where the key is the name of the column
                # and the value is the value of the column
                dict_obj[column.name] = getattr(self, column.name)
            return dict_obj
        else:
            # method 2, use dict comprehension to yield the same results
            return {
                column.name: getattr(
                    self, column.name) for column in self.__table__.columns
                    }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")





# HTTP GET - Read Record ##########################

# TODO: 1. Create a "random" route that allows a GET request. (default)
# Get is the default but I want to see this written out so I remember
@app.route("/random", methods=["GET"]) 
def random():
    # Switching to the 2.0 way of doing selects
    # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-selecting-data
    max_id = db.session.query(func.max(Cafe.id)).scalar()
    rp(f"The max db id is: {max_id}")
    random_id = rand.randint(a=1, b=max_id)
    rp(f"The random ID is: {random_id}")

    select_cafe = db.session.execute(select(Cafe).where(Cafe.id == random_id))
    selected_cafe = select_cafe.scalar()
    rp(selected_cafe.name)

    # initial method.
    # if you want to disclude something, do it here.
    # you could also just run this dict logic directly in the return section.
    cafe_jsonify = {
        "cafe": {
            "can_take_calls":selected_cafe.can_take_calls,
            "coffee_price":selected_cafe.coffee_price,
            "has_sockets":selected_cafe.has_sockets,
            "has_toilet":selected_cafe.has_toilet,
            "has_wifi":selected_cafe.has_wifi,
            "id":selected_cafe.id,
            "img_url":selected_cafe.img_url,
            "location":selected_cafe.location,
            "map_url":selected_cafe.map_url,
            "name":selected_cafe.name,
            "seats":selected_cafe.seats
            }  
        }  
    
    # return jsonify(cafe_jsonify)
    # return jsonify(cafe=random_cafe.to_dict())
    jsonify_alt = {"cafe": selected_cafe.to_dict(compr=False)}
    return jsonify(jsonify_alt)

# TODO: 2 create an endpoint that returns all cafes
@app.route("/all", methods=["GET"])
def all():
    # scalars returns the connection to stream the cafe objs in (iterator)
    # scalars.all() returns all the cafe objs at 1x.
    # the only reason to use 1 over the other is memory management.
    # scalars only loads into memory what is streamed in and you
    ## may stop once a condition is met.
    # then, if you have a method on the cafe obj, you must iterate through it
    ## to access.

    db_select_all = db.session.execute(select(Cafe)).scalars().all()
    cafe_jsonify = {
        "cafe": [
            cafe_obj.to_dict(compr=True) for cafe_obj in db_select_all]
            }
    return jsonify(cafe_jsonify)

# TODO: 3 create a way to find a cafe
@app.route("/search", methods=["GET"])
def search():

    default_none = {
        "error": {
            "Not Found": "Sorry, we don't have a cafe at that location."
        }
    }

    loc = request.args.get("loc")
    if not loc:
        return jsonify(default_none)
        # if I don't do the query here, it will error when a param is 
        # not included

    result_objs = db.session.execute(
        select(Cafe).where(Cafe.location.ilike(f"%{loc}%"))
        ).scalars().all()
    
    results = {
        "cafe": [cafe_obj.to_dict(compr=False) for cafe_obj in result_objs]
        }
    
    rp( f"[green]Count returned:[/green] {len(result_objs)}")
    if results:
        return jsonify(results)
    
    return jsonify(default_none)

    


# HTTP POST - Create Record ##########################

# HTTP PUT/PATCH - Update Record ##########################

# HTTP DELETE - Delete Record ##########################


if __name__ == '__main__':
    app.run(debug=True)
