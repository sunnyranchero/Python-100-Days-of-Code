from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
# from wtforms.validators import DataRequired


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
    email = StringField('email')
    password = StringField('password')

app = Flask(__name__)
# This is the line that will create the secret key for the CRSF protection
app.secret_key = "some random string."


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    form = MyForm()
    # if form.validate_on_submit():
    #     return redirect('/success')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
