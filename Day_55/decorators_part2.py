class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False
    
def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper
    
@is_authenticated_decorator
def created_blog_post(user):
    print(f"This {user.name}'s new blog post.")

new_user = User("Robert")

# If you comment out line 19, it won't print.
new_user.is_logged_in = True

created_blog_post(new_user)

# The wrapper basically acts as a gateway to actually process
# the create blog post. The  actual argument is passing the 
# User class object into the function.
# Then the name is accessed there.