"""
display detailed info about errors occuring in a function
"""

def print_error(err, function, error_type=None):
    print("*"*20)
    print("Error in function: ", function)
    if error_type is not None:
        print("Error Type: ", error_type)
    print("Error message: ",err)

