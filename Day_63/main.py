from flask import Flask, render_template, request, redirect, url_for
from rich import print as rp

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

all_books = []


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
    app.run(debug=True)

