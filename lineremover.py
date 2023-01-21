

def delete_line(filename, string_condition):
    with open(filename, 'r', errors='ignore') as file:
        lines = file.readlines()
        print(lines[-1])

    for line in lines:
        if string_condition in line:
            line = line + "."
    with open(filename, 'w', errors='ignore') as file:
        for line in lines:
            file.write(line.replace('\n', '.\n'))

delete_filename = input("File: ")
delete_string_condition = input("Delete line if contains: ")

delete_line(delete_filename, delete_string_condition)