from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/bye')
def say_bye():
    return "Bye"


print(__name__)

hello_world()

# flask is a framework not a library
# frameworks are their own environment with rules you need to
# abide by.
# 
# $env:FLASK_APP = "hello.py"

if __name__ == "__main__":
    app.run()

# Running it this way actually has less steps:
# We don't need to provide $env:FLASK_APP = "hello.py"
# it will Run with normal controls

# __name__ basically is the scope of the file being run.
# __main__ basically means the current file the app code is located
# >>> note line 2 above.
# These are special attributes in python.

## If I imported the random module and printed random.__name__,
### it would print "random"

# decorators is basically a wrapper function to add a
## feature or function to an existing function.

# Type 1 Function1() and wrapper_function()
"""
def function1():
    print("something")

def wrapper_function(some_function):
    time.sleep(1)
    return wrapper_function


"""