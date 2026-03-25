import os
import sys
from typing import Callable

from code_generators.go_lang.go_lang_code_generator import generate_golang_code
from code_generators.javascript.javascript_code_generator import generate_javascript_code
from code_generators.python.python_code_generator import generate_python_code
from code_generators.rust.rust_code_generator import generate_rust_code


SUPPORTED_LANGUAGES = {
    "python": ("py", generate_python_code),
    "javascript": ("js", generate_javascript_code),
    "golang": ("go", generate_golang_code),
    "rust": ("rs", generate_rust_code),
}


def check_programming_language(first_line: str) -> str | None:
    words = first_line.lower().split()
    if len(words) >= 2 and words[0] == "language":
        lang = words[-1]
        if lang in SUPPORTED_LANGUAGES:
            return lang
    print("Language not set correctly.")
    print("Use one of these headers at the top of your .rl file:")
    print("language should be python | javascript | golang | rust")
    return None


def generate_code(language: str, english_code: str) -> str:
    _, generator = SUPPORTED_LANGUAGES[language]
    return generator(english_code)


def write_in_file(generated_code: str, file_extension: str, input_filename: str) -> str:
    output_directory = "generated_code"
    os.makedirs(output_directory, exist_ok=True)

    filename = os.path.splitext(os.path.basename(input_filename))[0]
    output_filename = os.path.join(output_directory, f"{filename}.{file_extension}")

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(generated_code)

    return output_filename


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <rawlang_file>")
        return

    input_filename = sys.argv[1]
    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            first_line = file.readline()
            language = check_programming_language(first_line)
            if not language:
                return

            english_code = file.read()
            generated_code = generate_code(language, english_code)
            file_extension, _ = SUPPORTED_LANGUAGES[language]
            output_filename = write_in_file(generated_code, file_extension, input_filename)
            print(f"Programming language set to: {language}")
            print(f"Code generated successfully and saved in {output_filename}")
    except FileNotFoundError:
        print(f"File not found: {input_filename}")
    except Exception as error:  # noqa: BLE001
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
