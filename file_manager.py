import csv, os, shutil, subprocess
from commit import Commit
#FileManager
#Used
def require_valid_path(func):
    """
    Decorator that checks all path arguments for validity before running the function.
    Assumes all arguments named 'path', or ending with '_path', are paths.
    """
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, str) and os.path.exists(arg):
                continue
            elif isinstance(arg, str) and (arg.endswith('path') or arg == 'path'):
                if not os.path.exists(arg):
                    print(f"Invalid path: {arg}")
                    return
        for k, v in kwargs.items():
            if (k == 'path' or k.endswith('_path')) and not os.path.exists(v):
                print(f"Invalid path: {v}")
                return
        return func(*args, **kwargs)
    return wrapper

#Used
def create_new_folder_in_path(path):
    """
    Creates a new folder at the given path and sets it as hidden (Windows).
    """
    try:
        os.mkdir(path)
        subprocess.run(['attrib', '+h', path])
    except FileExistsError as e:
        raise e

#Used
@require_valid_path
def copy_file(source_path, dest_path):
    """
    Copies a file from source_path to dest_path.
    """
    shutil.copy(source_path, dest_path)

#Used
@require_valid_path
def delete_file(path):
    """
    Deletes the file at the specified path.
    """
    os.remove(path)

#Used
@require_valid_path
def is_empty_folder(path):
    """
    Returns True if the folder at the given path is empty.
    If the folder is not empty, returns False.
    """
    return not os.listdir(path)

#Used
@require_valid_path
def list_files_in_folder(path):
    """
       Returns a list of all files in the specified folder path.
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

#Not used
def is_file_open(file_path):
    try:
        with open(file_path, 'a'):
            return False
    except IOError:
        return True

def create_new_file_in_folder(folder_path, file_name):
    with open(os.path.join(folder_path, file_name), 'w') as file:
        file.write("")

def is_valid_path(path):
    return os.path.exists(path)


def wit_file_path(path, *names):
    return os.path.join(path, ".wit", *names)

def write_to_data_csv(path, commit):
    data_csv_path = wit_file_path(path, "data.csv")
    if not os.path.exists(os.path.dirname(data_csv_path)):
        print(f"The directory does not exist: {os.path.dirname(data_csv_path)}")
        return
    try:
        with open(data_csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(commit.get_list_value())
    except PermissionError as e:
        print(f"Permission denied: {e}")

def read_1_row_from_data_csv(path, hash_code):
    data_csv_path = wit_file_path(path, "data.csv")
    with open(data_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == hash_code:
                return Commit(row[1], row[0], row[2])
    return None

def print_all_data_csv(path):
    data_csv_path = wit_file_path(path, "data.csv")
    with open(data_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            c = Commit(row[1], row[0], row[2])
            print(c)

def is_empty_data_csv(path):
    data_csv_path = wit_file_path(path, "data.csv")
    return os.stat(data_csv_path).st_size == 0

def last_hash_code_data_csv(path):
    data_csv = wit_file_path(path, "data.csv")
    with open(data_csv, mode='r') as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1]
        last_value = last_line.strip().split(',')[0]
        return last_value