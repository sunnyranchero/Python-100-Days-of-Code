from flask import Flask
import random
app = Flask(__name__)

def make_h1(function):
    def wrapper():
        function_output = function()
        return f"<h1>{function_output}</h1>"
    return wrapper

def generate_random():
    r_num  = random.randint(0, 9)
    return r_num

random_number = generate_random()

# @make_h1
@app.route('/')
def home():
    return "<h1> Guess a number between 0 and 9 </h1>" \
    "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' width='400px'>"

@app.route('/<int:guess>')
def logic_the_guess(guess:int):
    print(random_number)
    if guess > random_number:
        return f"<h2 style='color:Crimson; background-color: DarkSlateGray;'>You guessed: {guess}... Too high</h2>"\
        "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif' width='400'>"
    elif guess < random_number:
        return f"<h2 style='color:DarkCyan; background-color: DarkSlateGray;'>You guessed: {guess}... Too low</h2>"\
        "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif' width='400'>"
    elif guess == random_number:
        return f"<h2 style='color:chartreuse; background-color: DarkSlateGray;'>You guessed: {guess}... Just right</h2>"\
        "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif' width='400'>"
    else:
        return f"<h2>You guessed {guess}. it doesn't look correct</h2>"
    

# Enable debugging and running the flask app from the file rather than changing env variables
if __name__ == '__main__':
    app.run(debug=True)

"""
Solution
https://gist.github.com/angelabauer/26eb9190a094761a9f49b22e8ee4c0fb

from flask import Flask
import random

random_number = random.randint(0, 9)
print(random_number)

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>"


@app.route("/<int:guess>")
def guess_number(guess):
    if guess > random_number:
        return "<h1 style='color: purple'>Too high, try again!</h1>" \
               "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'/>"

    elif guess < random_number:
        return "<h1 style='color: red'>Too low, try again!</h1>"\
               "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'/>"
    else:
        return "<h1 style='color: green'>You found me!</h1>" \
               "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>"


if __name__ == "__main__":
    app.run(debug=True)

"""

"""
This one actually has links:
from flask import Flask
from random import randint

LOWER_LIMIT = 1
UPPER_LIMIT = 12
NUMBER_TO_GUESS = randint(LOWER_LIMIT, UPPER_LIMIT)
LINK_HTML = "<br>".join([f'<a href="/{num}">Guess number {num}</a>' for num in range(LOWER_LIMIT, UPPER_LIMIT + 1)])

app = Flask(__name__)

def guess_decorator(function):
    def some_wrapper():
        return function() + "<br>" + LINK_HTML
    return some_wrapper

@app.route("/")
@guess_decorator
def guessing_game():
    return f'<h1>Try to guess a number between {LOWER_LIMIT} and {UPPER_LIMIT}!</h1><br><img src= "https://media.giphy.com/media/3GRwYzxwdceaI/giphy-downsized-large.gif" width=200>'

def win_or_lose_decorator(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs) + "<br>" + LINK_HTML
    return wrapper

@app.route('/<int:number>')
@win_or_lose_decorator
def win_or_lose(number):
    if number > NUMBER_TO_GUESS:
        return f'<h1 style="color:red">Too High! Try again!</h1><br><img src= "https://media.giphy.com/media/gyRWkLSQVqlPi/giphy.gif" width=200><br>'
    elif number == NUMBER_TO_GUESS:
        return f'<h1 style="color:green">Congratulation!</h1><br><img src= "https://media.giphy.com/media/4Iw2OzgiiTc4M/giphy.gif" width=200>'
    else:
        return f'<h1 style="color:purple">Too Low! Try again!</h1><br><img src= "https://media.giphy.com/media/dRcMsUUrnR8He/giphy.gif" width=200>'

if __name__ == "__main__":
    app.run(debug=True)

"""