import time

# Functions inputs/functionality/output
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

# These functions are considered 1st class objects, can be passed around as
# arguments.
# ex: int/string/float etc.

# wrapper function example

def calculate(calc_function, n1, n2):
    return calc_function(n1, n2)

result = calculate(multiply, 2, 3)
print(result)

result2 = calculate(add, 2, 3)
print(result2)

# nested functions

def outer_function():
    print("I'm outer")

    # The scope here, this is only accessible within outer function.
    # a name error will happen if you try to run outside this outer function.
    def nested_function():
        print("I'm inner")
    
    nested_function()

outer_function()

# Functions can be returned from other functions.

def outer_function2():
    print("I'm outer")

    # The scope here, this is only accessible within outer function.
    # a name error will happen if you try to run outside this outer function.
    def nested_function():
        print("I'm inner")
    
    # get rid of (), means we are no longer activating it
    return nested_function

# this will print I'm outer
inner_function = outer_function2()

# can trigger outer function, we can also trigger inner fuction

# This will trigger, I'm inner

inner_function()
    
# decorator functions

def decorator_function(function):
    def wrapper_function():
        function()
    return wrapper_function

# an example

def say_hello():
    time.sleep(2)
    print("hello")

say_hello()

# if I wanted a delay on all lines.
# we could technically add functionality to these functions.
# we could add the delay in the wrapper funciont

def delay_decorator(function):
    def wrapper_function():
        time.sleep(1)
        # do something before
        function()
        # could run it 2x if you wanted
        # do something after
    return wrapper_function

@delay_decorator
def say_bye():
    print("bye")

@delay_decorator
def say_greeting():
    print("how are you?")

say_bye()

# a decorator function is just a wrapper function
# that accepts a function
# and wraps some functionality around it.

# The @asdfasdf syntax is called syntactic sugar.
# It just makes it easier to write an alt line of code.

# We could just call the functions instead, assign output to variable,
# Then call the variable with the ().
# basically in reduces the typing down to just putting the @asdfa
# above the function you want to pass into it.

