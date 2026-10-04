import re

def parse_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
        
        print("Lines that start with 'a':")
        for line in lines:
            if re.match(r'^a', line):
                print(line)
        print("-")
        
        print("Lines that end with 'b':")
        for line in lines:
            if re.search(r'b$', line):
                print(line)
        print("-")
        
        print("Lines that contain an underscore:")
        for line in lines:
            if re.search(r'_', line):
                print(line)
        print("-")
        
        print("Lines that contain an uppercase letter:")
        for line in lines:
            if re.search(r'[A-Z]', line):
                print(line)
        print("-")
        
        print("Replacing space, comma, dot with colon:")
        for line in lines:
            print(re.sub(r'[ ,.]', ':', line))
        print("-")
        
        print("Snake case to Camel case:")
        for line in lines:
            print(''.join(word.title() if i > 0 else word for i, word in enumerate(re.split(r'_', line))))
        print("-")
        
        print("Inserting spaces before capital letters:")
        for line in lines:
            print(re.sub(r'(?<!^)([A-Z])', r' \1', line))
        print("-")
        
        print("Camel case to snake case:")
        for line in lines:
            print(re.sub(r'(?<!^)(?=[A-Z])', '_', line).lower())
        print("-")

# Example usage
parse_text_file("C:/Users/Admin/AppData/Roaming/git/labs/lab5/row.txt")
