with open("englishcode.txt", 'r') as file:
        file_content_lowercase_as_list = [line.strip().lower() for line in file.readlines()]
        print(file_content_lowercase_as_list)
