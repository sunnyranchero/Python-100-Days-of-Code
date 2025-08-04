import time
current_time = time.time()
print(current_time) # seconds since Jan 1st, 1970 

# Write your code below 👇

def speed_calc_decorator(function):
    def time_calc():
        start_time = time.time()
        function()
        end_time = time.time()
        runtime_total = end_time - start_time
        return runtime_total
    return time_calc

@speed_calc_decorator
def fast_function():
  for i in range(1000000):
    i * i
        
@speed_calc_decorator
def slow_function():
  for i in range(10000000):
    i * i

print(f"fast_function run speed: {fast_function()}")

print(f"slow_function run speed: {slow_function()}")