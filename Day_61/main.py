from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class MyForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")



app = Flask(__name__)
# This is the line that will create the secret key for the CRSF protection
app.secret_key = "some random string."

# I chose bs5 because the version was not specified in the assignment.
bootstrap = Bootstrap5(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = MyForm()
    if form.validate_on_submit():
        
        # Storing the input values so they can be used later for auth.
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            # Skipping this for now so we can just flash a message.

            # flash(message="Login successful!", category="success")
            return render_template("success2.html")
        else:
            return render_template("denied2.html")
    return render_template("login.html", form=form)


# @app.route("/success")
# def success():
#     return render_template("success.html")

# @app.route("/denied")
# def denied():
#     return render_template("denied.html")

if __name__ == '__main__':
    app.run(debug=True)
