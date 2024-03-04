import ply.lex as lex

# Define token names
tokens = (
    'NEWLINE',
    'INDENT',
    'FULL_STOP',
    'STRING'
)

# Regular expression rules for simple tokens
t_NEWLINE = r'\n'
t_INDENT = r'\n\t+'
t_FULL_STOP = r'\.'
t_STRING = r'[^\n\.]+'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def tokenizer(input_string):
    lexer.input(input_string)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        tokens.append(tok.value)
    return tokens

# Example usage
input_string = """make variableName = 5, variableName2 = 10 and variableName3 = 15
make variableName, variableName2 and variableName3 = 5, 10 and 15
make variableName, variableName2 and variableName3 with values 5, 10 and 15
make variableName which takes input 
make variableName which takes number input with message "Give number "

create (function or fun or func) functionName with parameters parameter1, parameter2 and parameter3 which 
    prints parameter1 + parameter2 + parameter3
    prints parameter1 - parameter2 - parameter3
    prints parameter1 * parameter2 * parameter3
    prints parameter1 / parameter2 / parameter3
    prints parameter1 % parameter2 % parameter3
    prints parameter1 ** parameter2 ** parameter3
    prints parameter1 // parameter2 // parameter3
    return "all good"
"""
print(tokenizer(input_string))

for block in tokenizer(input_string):
    # print(block ,end="")
    with open("output.txt", "a") as file:
        file.write(str(block))

