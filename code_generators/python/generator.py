def make_array(tokens):
    # Generate code for creating an array
    variable_name = tokens[0]
    values = ', '.join(tokens[2:])  # Assuming "make x array 1 2 3"
    return f'{variable_name} = [{values}]'

def make_set(tokens):
    # Generate code for creating a set
    variable_name = tokens[0]
    values = ', '.join(tokens[2:])  # Assuming "make x set 1 2 3"
    return f'{variable_name} = {{{values}}}'

def make_tuple(tokens):
    # Generate code for creating a tuple
    variable_name = tokens[0]
    values = ', '.join(tokens[2:])  # Assuming "make x tuple 1 2 3"
    return f'{variable_name} = ({values},)'

def make_object(tokens):
     # Extract the variable name (first token)
    variable_name = tokens[0]
    
    # Initialize an empty list to hold formatted key-value pairs
    key_value_pairs = []
    
    # Iterate through the remaining tokens two at a time (key and value)
    for i in range(2, len(tokens), 2):
        key = tokens[i].rstrip(':')
        value = tokens[i + 1]

        # Check if value can be converted to an integer
        try:
            int(value)
        except ValueError:
            # If it cannot be converted, quote the value
            value = f'"{value}"'

        # Append the formatted key-value pair to the list
        key_value_pairs.append(f"'{key}': {value}")
    
    # Join all key-value pairs with commas
    key_value_pairs_str = ', '.join(key_value_pairs)
    
    # Return the formatted dictionary assignment statement
    return f'{variable_name} = {{{key_value_pairs_str}}}'

def make_variable(tokens):
    # Generate code for creating multiple variables
    code_lines = []
    i = 0
    while i < len(tokens):
        if tokens[i] == 'takes':
            variable_name = tokens[0]
            message = ' '.join(tokens[i + 5:])
            code_lines.append(f'{variable_name} = input({message})')
            break
        else:
            variable_name = tokens[i]
            if i + 2 < len(tokens) and tokens[i + 1] == '=':
                value = tokens[i + 2]
                code_lines.append(f'{variable_name} = {value}')
                i += 3
            else:
                i += 1
    return '\n'.join(code_lines)


def make_function(tokens):
    # Generate code for creating a function
    function_name = tokens[0]
    if tokens[1] == "with" and tokens[2] in ["parameters", "parms", "parm", "parameter" ]:
        parameters = ', '.join(tokens[3:])  # Assuming "create function f x y"
        return f'def {function_name}({parameters}):'
    else:
        print(f"Atleast write the code properly like create function with parameters in line \n {tokens} :")
        return ":"
