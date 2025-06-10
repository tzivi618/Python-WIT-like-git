import os,requests,pandas

from FileManager import copy_file, delete_file, list_files_in_folder, create_new_file_in_folder, \
    create_new_folder_in_path, is_empty_folder, write_to_data_csv, read_1_row_from_data_csv, print_all_data_csv, \
    is_empty_data_csv, last_hash_code_data_csv, is_valid_path, is_file_open
from Commit import Commit

IGNORED_FILES = {"desktop.ini", "Thumbs.db", "ehthumbs.db", ".DS_Store"}
IGNORED_FOLDERS = {".git", ".wit"}
IGNORED_PREFIXES = {"~$"}
IGNORED_EXTENSIONS = {".tmp", ".lnk"}
URL='http://localhost:8000'
def should_ignore(name):
    if name in IGNORED_FILES or name in IGNORED_FOLDERS:
        return True
    if any(name.startswith(prefix) for prefix in IGNORED_PREFIXES):
        return True
    if any(name.endswith(ext) for ext in IGNORED_EXTENSIONS):
        return True
    return False

def wit_subfolder(path, subfolder):
    return os.path.join(path, ".wit", subfolder)

def require_init(func):
    def wrapper(path, *args, **kwargs):
        if did_not_already_init(path):
            return
        return func(path, *args, **kwargs)
    return wrapper

def did_not_already_init(path):
    if not os.path.exists(wit_subfolder(path, "")):
        print("fatal: not a wit repository (or any of the parent directories): .wit")
        return True
    return False

def init_repo(path):
    try:
        create_new_folder_in_path(os.path.join(path, ".wit"))
        create_new_folder_in_path(wit_subfolder(path, "committed"))
        create_new_folder_in_path(wit_subfolder(path, "staging"))
        print(f"Initialized empty Wit repository in {path}/.wit/")
    except FileExistsError:
        print(f"Reinitialized existing Wit repository in {path}.wit\\")


@require_init
def add_repo(path, file_name):
    if should_ignore(file_name):
        print(f"Skipping ignored file or folder: {file_name}")
        return
    file_path = os.path.join(path, file_name)
    staging_path = wit_subfolder(path, "staging")
    if os.path.exists(file_path):
        copy_file(file_path, staging_path)
        print(f"{file_name} file added successfully")
    else:
        print(f"fatal: pathspec '${file_name}' did not match any files")

@require_init
def add_all_repo(path):
    staging_path = wit_subfolder(path, "staging")
    for file_name in list_files_in_folder(path):
        if should_ignore(file_name):
            continue
        copy_file(os.path.join(path, file_name), staging_path)
        print(f"{file_name} file added successfully")

@require_init
def commit_repo(path, message):
    wit_path = wit_subfolder(path, "")
    staging_path = wit_subfolder(path, "staging")
    committed_path = wit_subfolder(path, "committed")
    data_csv_path = os.path.join(wit_path, "data.csv")

    if is_empty_folder(staging_path):
        print("There is no need to commit until you have made an addition.")
        return

    commit = Commit(message)

    if is_file_open(data_csv_path):
        print("Cannot commit because data.csv is open.")
        return

    if os.path.exists(data_csv_path) and os.path.getsize(data_csv_path) > 0:
        names = pandas.read_csv(data_csv_path).iloc[:, 1]
        if message in names.values:
            print(f"A commit with that name already exists {wit_path}")
            return

    try:
        create_new_folder_in_path(os.path.join(committed_path, commit.hash_code))
    except FileExistsError:
        print(f"A commit with that name already exists {wit_path}")
        return

    if os.path.exists(data_csv_path):
        last_hash = last_hash_code_data_csv(path)
        if last_hash is not None:
            copy_from_path = os.path.join(committed_path, last_hash)
        else:
            copy_from_path = path
    else:
        copy_from_path = path

    all_file_to_copy = list_files_in_folder(copy_from_path)
    list_files_in_stage = list_files_in_folder(staging_path)

    if all_file_to_copy is not None:
        for f in all_file_to_copy:
            if f not in list_files_in_stage and not should_ignore(f):
                copy_file(os.path.join(copy_from_path, f), os.path.join(committed_path, commit.hash_code))

    for file in list_files_in_stage:
        if should_ignore(file):
            continue
        copy_file(os.path.join(staging_path, file), os.path.join(committed_path, commit.hash_code))
        delete_file(os.path.join(staging_path, file))

    write_to_data_csv(path, commit)
    print(
        f"{len(list_files_in_stage)} file changed, {len(all_file_to_copy) - len(list_files_in_stage)} insertions(+), \n create new commit.\n id: {commit.hash_code}  {list_files_in_stage}")

@require_init
def log_repo(path):
    print_all_data_csv(path)

@require_init
def status_repo(path):
    staging_path = wit_subfolder(path, "staging")
    if is_empty_folder(staging_path):
        print("No need to commit")
        return
    print("A commit is required.")

@require_init
def checkout_repo(path, version_hash_code):
    committed_version_path = os.path.join(wit_subfolder(path, "committed"), version_hash_code)
    if not is_valid_path(committed_version_path):
        print(f"error: path spec $'{version_hash_code}' did not match any file(s) known to wit")
        return
    files = list_files_in_folder(committed_version_path)
    for f in files:
        if should_ignore(f):
            continue
        copy_file(os.path.join(committed_version_path, f), path)
    print(f"Note: switching to {version_hash_code}.")

"""def push_repo(path):
    staging_path = wit_subfolder(path, "staging")
    if not is_empty_folder(staging_path):
        print("You must commit before pushing.")
        return

    last_hash = last_hash_code_data_csv(path)
    if not last_hash:
        print("No commits to push.")
        return

    committed_path = os.path.join(wit_subfolder(path, "committed"), last_hash)
    files = list_files_in_folder(committed_path)
    files_data = {}
    for f in files:
        with open(os.path.join(committed_path, f), "rb") as file:
            files_data[f] = file.read()

    # שליחת alert
    response_alert = requests.post(f"{URL}/alerts", files=files_data)
    print("Alert response:", response_alert.text)

    # שליחת analyze
    response_analyze = requests.post(f"{URL}/analyze", files=files_data)
    print("Analyze response:", response_analyze.text)
"""

def push_repo(path):
    staging_path = wit_subfolder(path, "staging")
    if not is_empty_folder(staging_path):
        print("You must commit before pushing.")
        return

    last_hash = last_hash_code_data_csv(path)
    if not last_hash:
        print("No commits to push.")
        return

    committed_path = os.path.join(wit_subfolder(path, "committed"), last_hash)
    files = list_files_in_folder(committed_path)
    files_data = []
    for f in files:
        files_data.append(('files', (f, open(os.path.join(committed_path, f), 'rb'))))

    # Send to /alerts
    response_alerts = requests.post(f"{URL}/alerts", files=files_data)
    print("Alerts response:", response_alerts.text)

    # Send to /analyze
    response_analyze = requests.post(f"{URL}/analyze", files=files_data)
    print("Analyze response:", response_analyze.text)

    # Close all file handles
    for _, (_, file_obj) in files_data:
        file_obj.close()