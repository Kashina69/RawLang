from . import generator
# import generator
import re

def tokenizer(english_code):
    # Split the input string into lines
    lines = english_code.strip().split('\n')
    
    # Regular expression to split on any whitespace
    token_pattern = re.compile(r'\s+')
    
    # List to hold the tokenized lines
    tokenized_lines = []
    
    for line in lines:
        # Remove comments (assuming comments start with #)
        # line = re.split(r'#', line)[0].strip()
        
        # Split line into tokens based on whitespace
        tokens = token_pattern.split(line)
        
        # Remove empty tokens
        tokens = [token for token in tokens if token]
        
        # Add list of tokens to tokenized_lines
        tokenized_lines.append(tokens)
    
    return tokenized_lines


def convert_line_to_code(line):
    if not line:  # Check if the line is empty
        return ""

    # Check the first token to determine the type of operation
    operation = line[0].lower()

    # Depending on the operation, generate corresponding Python code
    if operation == "make":
        if line[1] in ["list", "array", "arr", "lst"]:
            return generator.make_array(line[2:])
        elif line[1] == "set":
            return generator.make_set(line[2:])
        elif line[1] == "tuple":
            return generator.make_tuple(line[2:])
        elif line[1] in ["dictionary", "dict", "object", "obj"]:
            return generator.make_object(line[2:])
        else:
            return generator.make_variable(line[1:])

    elif operation == "create":
        if line[1].lower() in ["function", "def", "func", "fun"]:
            return generator.make_function(line[2:])
        else:
            return "Invalid function creation syntax"

    elif operation == "call":
    # Check if "with" and "arguments" are in the expected positions
        if len(line) < 5 or line[2].lower() != "with" or line[3].lower() not in ["args", "arg", "argument", "arguments"]:
            return f"Syntax error in call statement: {' '.join(line)}"
        else:
            return f"{line[1]}({', '.join(line[4:])})"


    elif operation in ["print", "prints"]:
        arguments = ' '.join(line[1:])
        return f'print({arguments})'

    elif operation == "check":
        if line[1].lower() == "if":
            condition = ' '.join(line[2:])
        else:
            condition = ' '.join(line[1:])
        return f'if {condition}:'

    elif operation in ["else", "otherwise"]:
        if len(line) > 1 and line[1].lower() == "check":
            if len(line) > 2 and line[2].lower() == "if":
                condition = ' '.join(line[3:])
                return f'elif {condition}:'
            else:
                condition = ' '.join(line[2:])
                return f'elif {condition}:'
        if len(line) > 1 and line[1].lower() == "if":
            condition = ' '.join(line[2:])
            return f'elif {condition}:'
        else:
            return 'else:'

    elif operation == "loop":
        loop_variable = line[1]
        range_start = line[3]
        range_end = line[5]
        return f'for {loop_variable} in range({range_start}, {range_end}):'

    elif operation == "return":
        return f'return {" ".join(line[1:])}'

    elif operation[0] == "#":
        return f'# {' '.join(line[1:])}'

    else:
        return f"What the hell you wrote {line[0]}"

    # Ensure function always returns a string
    return ""

def generate_python_code(english_code):
    # Ensure `generated_code` is initialized
    generated_code = "" 
    tokenized_code = tokenizer(english_code)
    indent_level = 0

    for line in tokenized_code:
        generated_line = convert_line_to_code(line)
        if line == []:
            indent_level = 0
        # Adjust indent level based on the operation
        if generated_line.endswith(":"):
            generated_code += '    ' * indent_level + generated_line + '\n'
            indent_level += 1
        elif generated_line == 'else:':
            indent_level -= 1
            generated_code += '    ' * indent_level + generated_line + '\n'
            indent_level += 1
        elif generated_line.startswith("return"):
            generated_code += '    ' * indent_level + generated_line + '\n'
            indent_level -= 1
        else:
            generated_code += '    ' * indent_level + generated_line + '\n'
    # print(generated_code)
    return generated_code

# Example usage
english_code = """
# Variable assignment
make variableName = 5
make variableName2 = 10
make variableName3 = 15

make set setName = prince rawat ji 69 @ 
make list listName = prince rawat ji 69 @ 
make tuple tupleName = prince rawat ji 69 @ 

make object people = name prince lastname rawat class 12

loop list from 1 to 20
print "Hello niggas"

# Taking input with a message
make userInput which takes input with message "Enter your name:"
make userNumber which takes number input with message "Give number:"

# Function definition
create func calculate with parameters x y z which 
    prints x + y + z
    prints x - y - z
    prints x * y * z
    prints x / y / z
    prints x % y % z
    prints x ** y ** z
    prints x // y // z
    return "all good"

# Function call
call calculate with arguments variableName variableName2 variableName3

# Conditional statements
check if variableName == 5
    print "variableName is 5"

otherwise check if variableName2 == 10
    print "variableName2 is 10"

otherwise if variableName3 == 15
    print "variableName3 is 15"
    
otherwise
    print "None of the conditions are met"

# this is a buttifyl comment  
"""
generate_python_code(english_code)