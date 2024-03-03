import sys
import os
from code_generators.python.python_code_generator import generate_python_code
from code_generators.javascript.javascript_code_generator import generate_javascript_code
from code_generators.go_lang.go_lang_code_generator import generate_golang_code
from code_generators.rust.rust_code_generator import generate_rust_code


def checkProgrammingLanguage(first_line):
    words = first_line.lower().split()
    if words[0] == "language":
        lang = words[-1]
        if lang in ["python", "javascript", "golang", "rust"]:
            return lang
    print("Broo at least tell the language")
    print("This is how to do it")
    print("Write:")
    print("language should be python or javascript or go or rust")
    print("On the top of the file")
    return None
            
def code_generator(language, english_code):
    code_generator_dict = {
        "python": generate_python_code(english_code),
        "javascript": generate_javascript_code(english_code),
        "golang": generate_golang_code(english_code),
        "rust": generate_rust_code(english_code)
    }
    return code_generator_dict[language]
    
def check_file_extension(language):
    file_extension_dict ={
        "python": "py",
        "javascript": "js",
        "golang": "go",
        "rust": "rs"
    }
    return file_extension_dict[language]

def write_in_file(generated_code,file_extension,input_filename):
# Create a directory to store generated code if it doesn't exist
        output_directory = "generated_code"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

# Split the input filename and extension
        filename, _ = os.path.splitext(input_filename)
# Concatenate the output filename with the proper file extension
        output_filename = os.path.join(output_directory, filename + "." + file_extension)
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
        with open(input_filename, 'r') as file:
# check programming language
            first_line = file.readline()
            language = checkProgrammingLanguage(first_line)
            if language:
                print("Programming language set to:", language)
# read english code
                english_code = file.read()
                generated_code = code_generator(language, english_code)
                file_extension = check_file_extension(language)
# write code in file 
                write_in_file(generated_code, file_extension, input_filename)
            else:
                return
    except FileNotFoundError:
        print("File not found:", input_filename)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()


