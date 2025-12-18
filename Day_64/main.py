from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, exists, func, select, update
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length
import requests
import os
import json
from rich import print as rp

# Define a form to use in the sql code (this was from a few lessons back)

class EditMovieForm(FlaskForm):
    movie_rating = DecimalField('Rating out of 10 (7, 5.5, 6.3)', 
                                places=1,
                                validators=[DataRequired(), 
                                            NumberRange(min=0, max=10)])
    new_review = StringField('Your Review',
                             validators=[DataRequired(), Length(max=100)])
    submit_btn = SubmitField('Submit')

class AddMovieForm(FlaskForm):
    movie_title = StringField('Movie Title',
                              validators=[DataRequired()])
    submit_btn = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
# API Access is located here: https://www.themoviedb.org/settings/api

# CREATE DB

## Create the basis for the new database
class Base(DeclarativeBase):
    pass
## Define what is now needed to interact with the database
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///d64_movies.db"
db.init_app(app)

# CREATE TABLE
class MoviesDb(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Not making this unique: Total Recall being 2 dif movies w/ same title
    title: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    ranking: Mapped[int] = mapped_column(nullable=True)
    review: Mapped[str] = mapped_column(nullable=True)
    img_url: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        """If you try to print the object: 
        \n- This is what is printed instead of the obj address."""
        return f"Movie obj: {id} - {self.title}"
    
# Create the database object if it does not already exist.
# Then create the table if it does not already exist.
# Yes, it does check whether or not the obj exists already.
with app.app_context():
    db.create_all()

def query_movie_db(type:str, search_term:str) -> dict:
    """This is used to query the movies database\n
    This yields a dict containing the info required."""
        
    api_file_path = os.path.abspath("./.api_creds.json")
    with open(api_file_path, "r") as f:
        api_data = json.load(f)
 
    if type == "auth":
        header = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_data["api_read_access_token"]}"
        }
        url = api_data["url_auth"]

        response = requests.get(url, headers=header)
        response_dict = json.loads(response.text)

        rp(response_dict)
        if response_dict["success"] != True:
            rp("[red]Auth was unsuccessful[/red]")
            return None

        rp("[green]Auth successful[/green]")
        return response_dict
    elif type == "search":
        url = api_data["url_movie_search"]

        response = requests.get(url, params={
            "api_key": api_data["api_key"],
            "query": search_term
            })
        rp(f"Request response code: {response.status_code}")
        if response.status_code != 200:
            rp("[red]Auth was unsuccessful[/red]")
            return None

        rp("[green]Auth successful[/green]")
        
        return response.json()["results"]
    
    elif type == "add_selected":
        url = str(api_data["url_add_selected"]).replace("{movie_id}",
                                                         search_term)
        response = requests.get(url,
                                 params={"api_key": api_data["api_key"]})
        rp(f"Request response code: {response.status_code}")

        if response.status_code != 200:
            rp("[red]Auth was unsuccessful[/red]")
            return None

        rp("[green]Auth successful[/green]")
        
        return response.json()
           
# Add Movie
def add_movie(new_movie_obj):
    """Reusable function to create the movie if 1 does not exist\n
    takes in an object"""
    field_check_title = new_movie_obj.title
    field_check_year = new_movie_obj.year
    field_check_img_url = new_movie_obj.img_url
    # Step 1 - check if the database exists,
    ## This should return True if there are rows that exist.
    
    row_exists = db.session.query(
        exists().where(
            (MoviesDb.title == field_check_title) &
            (MoviesDb.year == field_check_year) &
            (MoviesDb.img_url == field_check_img_url)
        )
    ).scalar()
    
    # Step 2 - if not, then create
    if not row_exists:
            db.session.add(new_movie_obj)
            db.session.commit()
            rp(f"[green]Added a new movie:[/green] {field_check_title}")
    else:
        rp(f"[blue]New movie exists:[/blue] {field_check_title}")

def select_all() -> list[MoviesDb] :
    """Retrieve a list of all movies from the database"""
    
    select_query = db.session.execute(
        db.select(MoviesDb).order_by(MoviesDb.ranking.desc()))
    
    # Actually a ScalarResult obj. This is streamed into the variable
    # Technically I should import the ScalarResult obj so I can 
    # add a Type output correctly.
    
    movie_obj_list = select_query.scalars() 

    return movie_obj_list

def update_ranking():

    row_num = func.row_number().over(
        order_by=MoviesDb.rating.desc()).label("rn")
    subquery = select(MoviesDb.id, row_num).subquery()

    update_stmt = update(MoviesDb).where(
        MoviesDb.id == subquery.c.id).values(ranking=subquery.c.rn)

    db.session.execute(update_stmt)
    db.session.commit()
  
# Movie 1 info:
new_movie_1 = MoviesDb(
    title="Phone Booth",
    year=2002,
    description="""Publicist Stuart Shepard finds himself trapped in a phone 
    booth, pinned down by an extortionist's sniper rifle. Unable to leave or 
    receive outside help, Stuart's negotiation with the caller leads to a 
    jaw-dropping climax.""",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)

# Movie 2 info:
new_movie_2 = MoviesDb(
    title="Avatar The Way of Water",
    year=2022,
    description="""Set more than a decade after the events of the first film, 
    learn the story of the Sully family (Jake, Neytiri, and their kids), the 
    trouble that follows them, the lengths they go to keep each other safe, 
    the battles they fight to stay alive, and the tragedies they endure.""",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)


# Due to my setup, make sure our CWD is the current dir
if os.getcwd() != os.path.dirname(__file__):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    print("Cwd was changed to the current file dir __file__")

with app.app_context():
    # Adding the creation here seems to keep triggering the insert
    # Keeping the insertion in the home page to limit recalls.
    # Nice to have: Maybe add an endpoint called "starter" to perform that insert.
    add_movie(new_movie_1)
    add_movie(new_movie_2)


###################### BEGIN FLASK CALLS AND ROUTES HERE #######################
@app.route("/")
def home():
    # If a database function that I made above is called within
    # an endpoint, I do not need the app.app_context() block.
    # The endpoints run within the correct context by default.
    # This makes the inclusion of these lines redundant.
    # Also, the only time to include the app.app_context() block is  
    # outside an endpoint like where create_all() is. 

    # Triggering the add function so there is always test data.
    update_ranking()
    movie_list = select_all()

    return render_template("index.html", movie_list=movie_list)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditMovieForm()
    id = request.args.get("id")
    movie_query = db.session.execute(db.select(MoviesDb).where(MoviesDb.id==id))
    scalar_result = movie_query.scalar()

    # if request.method == "POST":
    #     print("hello")
    if form.validate_on_submit():
        # rp(form.movie_rating.data)
        # rp(form.new_review.data)
        scalar_result.rating = form.movie_rating.data
        scalar_result.review = form.new_review.data
        db.session.commit()      

        return redirect(url_for("home"))

    return render_template("edit.html", movie=scalar_result, form=form)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    id = request.args.get("id")
    # This is coded to work by grabbing by PK.
    selected_movie = db.get_or_404(MoviesDb, id)
    db.session.delete(selected_movie)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddMovieForm()

    if add_form.validate_on_submit():
        rp(add_form.movie_title.data)
        data = query_movie_db(type="search",
                        search_term=add_form.movie_title.data)
        
        # return redirect(url_for("select", query_data = data))
        return render_template("select.html", query_data = data)      


    return render_template("add.html", form=add_form)

@app.route("/find", methods=["GET", "POST"])
def find():
    id = request.args.get("id")
    movie = query_movie_db(
        type="add_selected",
        search_term=id
    )

    rp(movie)
    new_movie = MoviesDb(
        title=movie["title"],
        year=str(movie["release_date"]).split("-")[0],
        description=movie["overview"],
        # rating=5.5,
        # ranking=5.5,
        # review="",
        img_url=f'https://image.tmdb.org/t/p/w500/{str(movie["poster_path"])}'      
    )

    add_movie(new_movie)
    id = db.session.query(func.max(MoviesDb.id)).scalar()

    return redirect(url_for("edit", id=id))

if __name__ == '__main__':
    app.run(debug=True)
