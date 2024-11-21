from typing import Type, List, Any

def validated_input(res_type: Type, message: str, invalid_message: str = "That object is invalid, please try again.") -> Any | None:
    '''
    A generic function to validate user input based on a data type.

    This function will catch all `ValueError`s thrown by the data type's constructor.
    This function will wait in a loop until user input is correct.

    Parameters:
        res_type (Type): Any constructor for any data type, the constructor must take one parameter.
        message (str): The message to display to the user when they input.
        invalid_message (str): The message to display when the user inputs an invalid data type.

    Returns:
        out (Any | None): Returns the user's input casted to the type specified by `res_type`.
    '''
    ok = False # Variable used to check if the data input is valid
    res = None # The result returned from the function
    while not ok: # Trap the user in a loop until a valid data type is given
        try: # Check for any errors
            # Retrieve input from the user (and display the message), then cast the result to the given data type.
            # If casting is unsuccessful a ValueError would be thrown
            res = res_type(input(message))
            ok = True # If the program gets here it means that no ValueErrors were thrown, so we can assume the casting was ok
        except ValueError:
            print(invalid_message) # If there were a value error display the user a message
    return res

def validate_list_input(list: List[str], message: str, invalid_message: str = "That object is invalid, please try again.") -> str:
    '''
    A generic function to validate an input based on values in a string list.

    This function will check if the users input is contained in the list and waits until the user enters a valid list value.

    The function will return the user's input.

    Parameters:
        list (List[str]): The list you wish to compare against.
        message (str): The message to display to the user when they input.
        invalid_message (str): The message to display when the user inputs an object that's not in the list.
    
    Returns:
        out (str): The object in the list the user choose.
    '''

    ok = False # Variable used to check if the data input is valid
    res = None # The result returned from the function
    while not ok:
        res = input(message)
        if res in list: # Check if the input is in the list
            ok = True
        else:
            print(invalid_message) # otherwise display an error message

    return res

def display_list(list: List[str]) -> str:
    out = ""
    for ele in list:
        out += f"{ele}, "
    return out

def yes_or_no_input(message):
    actions = ["yes", "no"]
    return validate_list_input(actions, f"{message}. Choose yes or no. ")