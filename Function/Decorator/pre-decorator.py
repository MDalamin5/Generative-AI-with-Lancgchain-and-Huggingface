## function inside function

def double_func():
    print("i'm from 1's function")
    
    ## inner function
    def inner_func():
        print("I'm form inner function")
        return f"I'm a inner function"
    return inner_func ## this value from double func

print(double_func()())

## function as the input

def work(i_am_function):
    print('This is 1"s line')
    i_am_function()
    print('the last line')
    
    
def sleeping():
    print("My task is doing coding and sleeping")
    

work(sleeping)


