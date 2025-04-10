import math

def timer(func):
    def inner(*args, **kwargs):
        print('time started')
        print(args)
        result = func(*args, **kwargs)
        print(result)
        print('time ended')
    return inner

# timer()()

@timer
def get_factorial(n, m):
    print(f"Factorial start now")
    return math.factorial(n)

get_factorial(120, 10)