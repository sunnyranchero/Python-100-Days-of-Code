from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp
import csv
import os

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
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

"""This regex pattern:

^ asserts the start of the string.
(0?[1-9]|1[0-2]) matches hours from 01 to 12 (with optional leading zero for single-digit hours).
: matches the literal colon.
[0-5][0-9] matches valid minutes from 00 to 59.
\s? allows for zero or one whitespace character between the time and AM/PM.
(?:AM|PM|am|pm) is a non-capturing group matching the AM or PM indicator in any case.
$ asserts the end of the string."""

def update_csv():
    pass


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name',
                        validators=[DataRequired()])
    # Adding different fields into the base form
    cafe_location = StringField('Cafe Location on Google(URL)',
                                 validators=[DataRequired(), URL(message="This needs to be a valid URL.")] )
    opening_time = StringField('Opening Time e.g. 8AM',
                                validators=[DataRequired(), Regexp(
                                    regex=r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(?:AM|PM|am|pm)$",
                                    message="Please enter a valid time in HH:MM AM/PM format"
                                )])
    closing_time = StringField('Closing Time e.g. 5:30PM',
                               validators=[DataRequired(), Regexp(
                                    regex=r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(?:AM|PM|am|pm)$",
                                    message="Please enter a valid time in HH:MM AM/PM format"
                                )])
    coffee_rating = SelectField('Coffee Rating',
                                validators=[DataRequired()],
                                choices=(['✘'] + ['☕️' * i for i in range(1, 6)]))
    wifi_strength_rating = SelectField('Wifi Strength Rating',
                                       validators=[DataRequired()],
                                       choices=(['✘'] + ['💪' * i for i in range(1, 6)]))
    power_outlet_rating = SelectField('Power Outlet Rating',
                                       validators=[DataRequired()],
                                       choices=(['✘'] + ['🔌' * i for i in range(1, 6)]))

    # The submit is from the original.
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        # print(form)
        return redirect(url_for('add_cafe'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    print(os.getcwd())
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # I ran into an issue where the cwd was causing issues with
    # accessing the cwd/pwd for this project because of how I have it
    # being run. The solution is to change the dir to the executing script.
    os.chdir(os.path.dirname(__file__))
    with open('./cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)
    # print(f"This is the file that is run: {__file__}")
    # print(f"This is the dirname: {os.path.dirname(__file__)}")
    # print(f"This is the pwd: {os.getcwd()}")
    # return render_template('cafes.html')


if __name__ == '__main__':
    app.run(debug=True)

# TODO: Get the PWD correct to identify the file I am updating. 
# Then call that function within the submit section
# Also, make a normalize time function.