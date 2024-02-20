import sys
import os

def generate_code(english_code):
    generated_code = ""
    
    
    return generated_code

def main():
    # Check if filename is provided as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python mycode.py <filename>")
        return
    
    input_filename = sys.argv[1]


    try:
        # Read English code from file
        with open(input_filename, 'r') as file:
            file_content_lowercase_as_list = [line.strip().lower() for line in file.readlines()]
            language = ""
            first_line = file_content_lowercase_as_list[0]
            if first_line.split()[0] == "language":
                if first_line.split()[-1] == "python":
                    language = "python"
                elif first_line.split()[-1] == "javascript":
                    language = "javascript"
                elif first_line.split()[-1] == "golang":
                    language = "golang"
                elif first_line.split()[-1] == "rust":
                    language = "rust"
            else:
                print("Broo at least tell the language")
                print("This is how to do it")
                print("Write:")
                print("language should be python or javascript or go or rust")
                print("On the top of the file")
                return 


            print("Programming language set to:", language)
                
            english_code = file.read()
            print(english_code)
        # Generate code
        generated_code = generate_code(english_code)

        # Create a directory to store generated code if it doesn't exist
        output_directory = "generated_code"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Write generated code to a new file
        file_extension = ""
        if language == "python": file_extension = "py"
        if language == "javascript": file_extension = "js"
        if language == "golang": file_extension = "go"
        if language == "rust": file_extension = "rs"
        output_filename = os.path.join(output_directory, input_filename.rstrip('txt') + file_extension)
        with open(output_filename, 'w') as file:
            file.write(generated_code)

        print("Code generated successfully and saved in", output_filename)

    except FileNotFoundError:
        print("File not found:", input_filename)

if __name__ == "__main__":
    main()
