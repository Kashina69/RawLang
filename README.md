# RawLang
RawLang is a user-friendly compiler that translates literal English to programming languages like Python, Javascript, GoLang, Rust code. With RawLang, you can write code using familiar English words and phrases.
 
-----
You work on Building Logic and writing English paragraphs for the coding part RawLang takes care of it; no Vim needed for ultimate productivity.

## Features
- Write code using English-like syntax
- Write continuous paragraphs without the need for indentation or code formatting.
- No need to strain your fingers by typing random symbols; at most, use one full stop per paragraph.
- Suitable for Rapid prototyping, scripting, automation, and educational purposes
- Write in different programming languages

## Getting Started
To get started with RawLang, simply clone the repository and follow the instructions.

```
C:\RawLang>python main.py {file location}
For example:
C:\RawLang>python main.py ./codeDir/english_code.txt

```

## Example 
Write something like this in your 'english_code.txt' file:
``` RawLang
Language should be python

make name and age with values "RawLang" 19.
create function calculate with parameters x , y and z which assign x + y - z to result then return result
create function print_message with parameters name and age which prints "Hello" + name
print "Your age is " age
assign "RawLang" to name  
assign value to variable age as 2
call function print_message with arguments name and age 
call function calculate with arguments 2 3 4 
```

```
Must write Language should be languageName on the top of the file 
```

## Output in python
You will get the output in a newly generated directory in the 'RawLang' folder named 'generated_code' and the file name will be the same as the code.txt with the appropriate extension of the language you have written in the top of the file.

```py
name = "RawLang"
age = 19
def calculate(x, y, z):
    sum = x + y - z
    return sum

def print_message(name, age):
    print("Hello" + name)
    print("Your age is " + age)

name = "RawLang"
age = 2

print_message(name, age)
calculate(2, 3, 4)


```
## Language syntax and keywords
[Docs](https://github.com/Kashina69/RawLang/blob/main/Syntax%20and%20keywords.md)

## Languages available now 
- Python
- Javascript
- Golang
- Rust

## Contributing
Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests to help RawLang improve.
Plzz don't contribute in readme.md its already good 

## License
This project is licensed under the MIT License.

## Developer 
Prince Rawat AKA Kashina 
