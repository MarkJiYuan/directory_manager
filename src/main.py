import json
import os
import logging

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
structure_path = os.path.join(root_path, 'structure.json')


dir_create_count = 0
file_create_count = 0


def read_structure(path=structure_path):
    with open(path, "r") as f:
        structure = json.loads(f.read())
    return structure

def mkdir(path):
    global dir_create_count
    path = path.strip()
    path = path.rstrip("/")

    if not os.path.exists(path):
        os.makedirs(path)
        dir_create_count += 1

def mkfile(filepath):
    global file_create_count
    if not os.path.exists(filepath):
        os.system(f"touch {filepath}")
        file_create_count += 1

def generate_files(files, path):
    if isinstance(files, list):
        for file in files:
            file_name = file["file_name"]
            mkfile(os.path.join(*path, file_name))
    elif isinstance(files, dict):
        var_range = files["var_range"]
        file_format = files["file_format"]
        for var in range(var_range[0], var_range[1]):
            mkfile(os.path.join(*path, file_format.format(var)))

def recurse(structure, path):
    directory_name = structure["directory_name"]
    path.append(directory_name)
    mkdir(os.path.join(*path))

    sub_directory = structure.get("sub_directory")
    if sub_directory:
        if isinstance(sub_directory, list):
            for sub_structure in sub_directory:
                recurse(sub_structure, path)
        elif isinstance(sub_directory, dict):
            var_range = sub_directory["var_range"]
            directory_format = sub_directory["directory_format"]
            for var in range(var_range[0], var_range[1]):
                mkdir(os.path.join(*path, directory_format.format(var)))

    files = structure.get("files")
    if files:
        generate_files(files, path)

    path.pop(-1)



if __name__ == '__main__':
    basepath = input("Enter absolute path or using default relative path to create directories:\n")
    directory_name = input("Enter root directory name otherwise use default 'course_name:\n")

    structure = read_structure()
    if directory_name:
        structure["directory_name"] = directory_name
    recurse(structure, [basepath])

    print("*"*25)
    print(f"Directory Created: {dir_create_count}")
    print(f"File Created: {file_create_count}\n")






