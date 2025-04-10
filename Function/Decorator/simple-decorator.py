def timer(func):
    def inner():
        print('time started')
        print(func())
        print('time ended')
    return inner

# timer()()

@timer
def get_factorial():
    print(f"Factorial start now")
    return 10

get_factorial()

## decorator is like auto callable-- when i call the get factorial function and its have a decorator. so its calling function is the parameter of the decorator

