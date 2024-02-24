import sys
import os
from code_generators.python_code_generator import generate_python_code
from code_generators.javascript_code_generator import generate_javascript_code
from code_generators.go_lang_code_generator import generate_golang_code
from code_generators.rust_code_generator import generate_rust_code

language = ""
generated_code = ""
input_filename =""
file_extension = ""
def checkProgrammingLanguage(first_line):
    if first_line.split()[0] == "language":
        if first_line.split()[-1] == "python": return "python"
        elif first_line.split()[-1] == "javascript": return "javascript"
        elif first_line.split()[-1] == "golang": return "golang"
        elif first_line.split()[-1] == "rust": return "rust"
    else:
        print("Broo at least tell the language")
        print("This is how to do it")
        print("Write:")
        print("language should be python or javascript or go or rust")
        print("On the top of the file")
        
def code_generator(language, english_code):
    if language == "python": return generate_python_code(english_code)
    if language == "javascript": return generate_javascript_code(english_code)
    if language == "golang": return generate_golang_code(english_code)
    if language == "rust": return generate_rust_code(english_code)
    
def check_file_extension(language):
    if language == "python": return "py"
    if language == "javascript": return "js"
    if language == "golang": return "go"
    if language == "rust": return "rs"
    print("check extension "+language)

def write_in_file(generated_code,file_extension):
     # Create a directory to store generated code if it doesn't exist
        output_directory = "generated_code"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        output_filename = os.path.join(output_directory, input_filename.rstrip('txt') + file_extension)
        with open(output_filename, 'w') as file:
            file.write(generated_code)

        print("Code generated successfully and saved in", output_filename)







def main():
    # Check if filename is provided as command-line argument
    if len(sys.argv) != 2:
        print("Bro atleast give a file to work on")
        return
    input_filename = sys.argv[1]

    try:
        # Read English code from file
        with open(input_filename, 'r') as file:

            # check file content convert it to linst and lowercase it 
            file_content_lowercase_as_list = [line.strip().lower() for line in file.readlines()]
            print(file_content_lowercase_as_list)
            
            # check first line and set the programming language
            first_line = file_content_lowercase_as_list[0]
            language = checkProgrammingLanguage(first_line)
            print("Programming language set to:", language)
            
            # read all english code 
            english_code = file.read()
            print(english_code)
        # Generate code
        generated_code = code_generator(language, english_code)

        file_extension = check_file_extension(language)

        print("file extension is ")
        print(file_extension)
        write_in_file(generated_code, file_extension)

    except FileNotFoundError:
        print("File not found:", input_filename)

if __name__ == "__main__":
    main()


