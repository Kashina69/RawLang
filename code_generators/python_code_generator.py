def generate_python_code(english_code):
    for index, line in enumerate(english_code):
        if index == 1 :
            return
        words_list = line.split()
        for index, word in enumerate(words_list):
            if word == "make":
                if words_list[index + 1] == "list": write_list_code(words_list,index)
                print("make")
            if word == "create":
                if words_list[index + 1] == "function" or words_list[index + 1] == "fun" or words_list[index + 1] == "func": write_function_code(words_list,index)
    
    
# chat gpt write list code function 
    
def write_list_code(words_list, make_index):
    list_generated_code = ""
    list_name = words_list[make_index + 2]

    # Check if "with" is present in the words_list
    if "with" not in words_list:
        print(f"Write 'with' after 'create list {list_name}'")
        return

    # Concatenate list name from words after "create list" until "with"
    for i in range(make_index + 2, words_list.index("with")):
        list_name = list_name + "_" + words_list[i]

    # Check if "value" or "values" is present after "with"
    if words_list[words_list.index("with") + 1].lower() in ["value", "values"]:
        # Find the values to be added to the list
        values_index = words_list.index("with") + 2
        values = words_list[values_index:]

        # Check for presence of "and" and ensure it's the second last value
        if "and" in values and values[-2] == "and":
            # Extract values to be added to the list
            values_to_add = values[:-2] 
            values_to_add.append(values[-1])
            # Process values_to_add as needed
            print("Values to add:", values_to_add)
        else:
            print("Error: Expected 'and' as the second last word after 'value(s)'")
    else:
        print(f"Write 'value' or 'values' after 'with' in 'create list {list_name} with'")

    

def write_function_code(words_list, create_index):
    generate_code = ""
    function_name = words_list[create_index + 2]

    # Check if "with" is present
    if "with" not in words_list:
        print(f"Write 'with' after 'create function {function_name}'")
        return

    # Construct function name considering possible spaces
    for i in range(create_index + 2, words_list.index("with")):
        function_name = function_name + "_" + words_list[i]

    # Check if "parameters" or "parameter" is present after "with"
    if words_list[words_list.index("with") + 1].lower() not in ["parameters", "parameter"]:
        print(f"Write 'parameters' after 'with' in 'create function {function_name} with'")
        return

    # Extract parameters
    parameters = []
    for i in range(words_list.index("parameter") + 1, len(words_list)):
        if words_list[i] == "with":
            break
        parameters.append(words_list[i])

    # Construct function definition
    generate_code += f"def {function_name}("
    generate_code += ", ".join(parameters)
    generate_code += "):\n"
    generate_code += "    # Your code here\n"

    # Check if there's a condition after "which"
    if "which" in words_list and words_list.index("which") + 1 < len(words_list):
        if words_list[words_list.index("which") + 1] == "check":
            # Run function to generate condition code
            generate_code += generate_condition_code(words_list, words_list.index("which") + 1)

    return generate_code

def generate_condition_code(words_list, index):
    # Your logic for generating condition code here
    pass
