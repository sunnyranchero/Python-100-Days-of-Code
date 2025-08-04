from flask import Flask
app = Flask(__name__)

def make_bold(function):
    def wrapper_function():
        raw_output = function()
        return f'<b> {raw_output} </b>'
    return wrapper_function

def make_emphasis(function):
    def wrapper_function():
        raw_output = function()
        return f'<em> {raw_output} </em>'
    return wrapper_function

def make_underline(function):
    def wrapper_function():
        raw_output = function()
        return f'<u> {raw_output} </u>'
    return wrapper_function

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hthome')
def hello_world2():
    return '<h1 style="text-align: center"> Hello, World! </h1>' \
    '<p> this is a paragraph </p>' \
    '<img src="https://w.wallhaven.cc/full/7p/wallhaven-7prdye.jpg" width="400px"> '

@app.route('/bye')
def bye():
    return 'bye'

# Now add more decorators
@app.route('/bye2')
@make_bold
@make_emphasis
@make_underline
def bye2():
    return 'bye'

# what if we wanted to greet out user

@app.route('/username/<name>')
def greet(name):
    return f'Hello {name}'

# allows us to read in a file path.
# I wonder if we could include a separate variable after this.
@app.route('/userpath/<path:mytest>/<extra>')
def pathtest(mytest, extra):
    return f"My path is {mytest}, and this is extra: {extra}"

# The debug allows for developement without having to reload the server.
if __name__ == '__main__':
    app.run(debug=True)