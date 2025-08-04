def logging_decorator(function):
    def wrapper(*args):
        
        # Extract the function name
        function_name = function.__name__
    
        print(f"You called {function_name}{args}")
        
        # Run the function here
        result = function(*args)

        print(f"It returned: {result}")

        # Return the result back to the function
        return result
    
    return wrapper       


# TODO: Use the decorator 👇
@logging_decorator
def a_function(*args):
    return sum(args)

a_function(1,2,3)