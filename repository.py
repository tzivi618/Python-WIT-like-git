# import os,requests,pandas,io
# from file_manager import create_new_folder_in_path,copy_file,delete_file,is_empty_folder,list_files_in_folder
# from commit import Commit
# from commit_data_service import get_last_commit_hash_from_server
#
# IGNORED_FILES = {"desktop.ini", "Thumbs.db", "ehthumbs.db", ".DS_Store"}
# IGNORED_FOLDERS = {".git", ".wit"}
# IGNORED_PREFIXES = {"~$"}
# IGNORED_EXTENSIONS = {".tmp", ".lnk"}
#
# URL='http://localhost:8000'
#
# #Used
# def should_ignore(name):
#     """
#     Returns True if the file or folder name should be ignored by the repository.
#     """
#     if name in IGNORED_FILES or name in IGNORED_FOLDERS:
#         return True
#     if any(name.startswith(prefix) for prefix in IGNORED_PREFIXES):
#         return True
#     if any(name.endswith(ext) for ext in IGNORED_EXTENSIONS):
#         return True
#     return False
#
# #Used
# def wit_subfolder(path, subfolder=""):
#     """
#     Returns the path to a subfolder inside the .wit directory.
#     If no subfolder is provided, returns the path to .wit itself.
#     """
#     if subfolder:
#         return os.path.join(path, ".wit", subfolder)
#     return os.path.join(path, ".wit")
#
# #Used
# def require_init(func):
#     """
#     Decorator that runs the function only if the repository is initialized.
#     """
#     def wrapper(path, *args, **kwargs):
#         if did_not_already_init(path):
#             return
#         return func(path, *args, **kwargs)
#     return wrapper
#
# #Used
# def did_not_already_init(path):
#     """
#     Returns True if the .wit repository is not initialized at the given path.
#     Prints an error message if the .wit directory is missing.
#     """
#     if not os.path.exists(wit_subfolder(path, "")):
#         print("fatal: not a wit repository (or any of the parent directories): .wit")
#         return True
#     return False
#
# #Used
# def init_repo(path):
#     """
#     Initializes a new Wit repository at the given path, creating required subfolders.
#     """
#     try:
#         create_new_folder_in_path(wit_subfolder(path))
#         create_new_folder_in_path(wit_subfolder(path, "committed"))
#         create_new_folder_in_path(wit_subfolder(path, "staging"))
#         print(f"Initialized empty Wit repository in {path}/.wit/")
#     except FileExistsError:
#         print(f"Reinitialized existing Wit repository in {path}.wit\\")
#
# #Used
# @require_init
# def add_repo(path, file_name):
#     """
#     Adds a file to the staging area if it exists and is not ignored.
#     """
#     if should_ignore(file_name):
#         return
#     file_path = os.path.join(path, file_name)
#     staging_path = wit_subfolder(path, "staging")
#     if os.path.exists(file_path):
#         copy_file(file_path, staging_path)
#         print(f"{file_name} file added successfully")
#     else:
#         print(f"fatal: pathspec '${file_name}' did not match any files")
# #Used
# @require_init
# def add_all_repo(path):
#     """
#     Adds all non-ignored files in the given path to the staging area.
#     """
#     staging_path = wit_subfolder(path, "staging")
#     for file_name in list_files_in_folder(path):
#         if should_ignore(file_name):
#             continue
#         copy_file(os.path.join(path, file_name), staging_path)
#         print(f"{file_name} file added successfully")
#
#
# @require_init
# def commit_repo(path, message):
#     wit_path = wit_subfolder(path, "")
#     staging_path = wit_subfolder(path, "staging")
#     committed_path = wit_subfolder(path, "committed")
#
#     if is_empty_folder(staging_path):
#         print("There is no need to commit until you have made an addition.")
#         return
#
#     commit = Commit(message)
#
#
#     create_new_folder_in_path(os.path.join(committed_path, commit.hash_code))
#
#     last_hash = get_last_commit_hash_from_server()
#     if last_hash is not None:
#         copy_from_path = os.path.join(committed_path, last_hash)
#     else:
#         copy_from_path = path
#
#     all_file_to_copy = list_files_in_folder(copy_from_path)
#     list_files_in_stage = list_files_in_folder(staging_path)
#
#     if all_file_to_copy is not None:
#         for f in all_file_to_copy:
#             if f not in list_files_in_stage and not should_ignore(f):
#                 copy_file(os.path.join(copy_from_path, f), os.path.join(committed_path, commit.hash_code))
#
#     for file in list_files_in_stage:
#         if should_ignore(file):
#             continue
#         copy_file(os.path.join(staging_path, file), os.path.join(committed_path, commit.hash_code))
#         delete_file(os.path.join(staging_path, file))
#     commit_data = {
#         "hash_code": commit.hash_code,
#         "message": commit.message,
#         "timestamp": commit.timestamp  # Add this property to your Commit class if missing
#     }
#     try:
#         response = requests.post(f"{URL}/commits", json=commit_data)
#         if response.status_code == 200:
#             print(f"{len(list_files_in_stage)} file changed, {len(all_file_to_copy) - len(list_files_in_stage)} insertions(+), \n create new commit.\n id: {commit.hash_code}  {list_files_in_stage}")
#         else:
#             print(f"שגיאה בשמירת הקומיט ב־DB: {response.text}")
#     except Exception as e:
#             print(f"שגיאה בשמירת הקומיט ב־DB: {e}")
#
# @require_init
# def log_repo(path):
#     print_all_data_csv(path)
#
# @require_init
# def status_repo(path):
#     staging_path = wit_subfolder(path, "staging")
#     if is_empty_folder(staging_path):
#         print("No need to commit")
#         return
#     print("A commit is required.")
#
# @require_init
# def checkout_repo(path, version_hash_code):
#     committed_version_path = os.path.join(wit_subfolder(path, "committed"), version_hash_code)
#     if not is_valid_path(committed_version_path):
#         print(f"error: path spec $'{version_hash_code}' did not match any file(s) known to wit")
#         return
#     files = list_files_in_folder(committed_version_path)
#     for f in files:
#         if should_ignore(f):
#             continue
#         copy_file(os.path.join(committed_version_path, f), path)
#     print(f"Note: switching to {version_hash_code}.")
#
#
# import io
# @require_init
# def push_repo(path):
#     staging_path = wit_subfolder(path, "staging")
#     if not is_empty_folder(staging_path):
#         print("You must commit before pushing.")
#         return
#
#     last_hash = last_hash_code_data_csv(path)
#     if not last_hash:
#         print("No commits to push.")
#         return
#
#     committed_path = os.path.join(wit_subfolder(path, "committed"), last_hash)
#     files = list_files_in_folder(committed_path)
#     file_blobs = []
#     for f in files:
#         file_path = os.path.join(committed_path, f)
#         with open(file_path, 'rb') as file_obj:
#             content = file_obj.read()
#             file_blobs.append((f, content))
#
#     def make_files_data():
#         data = [('files', (f, io.BytesIO(content))) for f, content in file_blobs]
#         data.append(('project_root', (None, str(path))))
#         return data
#
#     # Send to /alerts
#     response_alerts = requests.post(f"{URL}/alerts", files=make_files_data())
#     print("Alerts response:", response_alerts.text)
#
#     # Send to /analyze (with new BytesIO objects)
#     response_analyze = requests.post(f"{URL}/analyze", files=make_files_data())
#     print("Analyze response:", response_analyze.text)


# @require_init
# def commit_repo(path, message):
#     """
#     Creates a new commit with staged files.
#     """
#     staging_path = wit_subfolder(path, "staging")
#     committed_path = wit_subfolder(path, "committed")
#
#     if is_empty_folder(staging_path):
#         print("There is no need to commit until you have made an addition.")
#         return
#
#     commit_mgr = CommitManager(path)
#     commit = commit_mgr.save(message)
#
#     commit_folder = os.path.join(committed_path, commit.hash_code)
#     create_new_folder_in_path(commit_folder)
#
#     for file_name in list_files_in_folder(staging_path):
#         if should_ignore(file_name):
#             continue
#         copy_file(os.path.join(staging_path, file_name), os.path.join(commit_folder, file_name))
#         delete_file(os.path.join(staging_path, file_name))
#
#     print(f"Created new commit {commit.hash_code}")
# @require_init
# def status_repo(path):
#     """
#     Prints the repository status.
#     """
#     staging_path = wit_subfolder(path, "staging")
#     if is_empty_folder(staging_path):
#         print("No need to commit")
#     else:
#         print("A commit is required.")

# repository.py
import os
from functools import wraps
from file_manager import (
    should_ignore,
    is_valid_path,
    create_new_folder_in_path,
    copy_file,
    delete_file,
    is_empty_folder,
    list_files_in_folder,
    wit_subfolder
)
from commit_manager_csv import CommitManager


def require_init(func):
    """
    Decorator that runs the function only if the repository is initialized.
    """
    @wraps(func)
    def wrapper(path, *args, **kwargs):
        if not os.path.exists(wit_subfolder(path)):
            print("fatal: not a wit repository (or any of the parent directories): .wit")
            return
        return func(path, *args, **kwargs)
    return wrapper


def init_repo(path):
    """
    Initializes a new Wit repository at the given path, creating required subfolders.
    """
    wit_path = wit_subfolder(path)
    committed = wit_subfolder(path, "committed")
    staging = wit_subfolder(path, "staging")
    try:
        create_new_folder_in_path(wit_path)
        create_new_folder_in_path(committed)
        create_new_folder_in_path(staging)
        print(f"Initialized empty Wit repository in {wit_path}/")
    except FileExistsError:
        print(f"Reinitialized existing Wit repository in {wit_path}/")


@require_init
def add_repo(path, file_name):
    """
    Adds a file to the staging area if it exists and is not ignored.
    """
    if should_ignore(file_name):
        return
    file_path = os.path.join(path, file_name)
    staging_path = wit_subfolder(path, "staging")
    if is_valid_path(file_path):
        copy_file(file_path, os.path.join(staging_path, file_name))
        print(f"{file_name} file added successfully")
    else:
        print(f"fatal: pathspec '{file_name}' did not match any files")


@require_init
def add_all_repo(path):
    """
    Adds all non-ignored files in the given path to the staging area.
    """
    staging_path = wit_subfolder(path, "staging")
    for file_name in list_files_in_folder(path):
        if should_ignore(file_name):
            continue
        copy_file(os.path.join(path, file_name), os.path.join(staging_path, file_name))
        print(f"{file_name} file added successfully")


@require_init
def commit_repo(path, message):
    """
    Creates a new commit with staged files and prints a detailed summary.
    """
    staging_path = wit_subfolder(path, "staging")
    committed_path = wit_subfolder(path, "committed")

    if is_empty_folder(staging_path):
        print("There is no need to commit until you have made an addition.")
        return

    commit_mgr = CommitManager(path)
    last_hash = commit_mgr.get_last_hash()
    commit = commit_mgr.save(message)
    commit_folder = os.path.join(committed_path, commit.hash_code)
    create_new_folder_in_path(commit_folder)

    # Read existing files from last commit (if any)
    prev_files = set()
    if last_hash:
        prev_commit_path = os.path.join(committed_path, last_hash)
        prev_files = set(list_files_in_folder(prev_commit_path))

    # Process staged files
    staged_files = list_files_in_folder(staging_path)
    new_files = []
    for file_name in staged_files:
        if should_ignore(file_name):
            continue
        src = os.path.join(staging_path, file_name)
        dst = os.path.join(commit_folder, file_name)
        copy_file(src, dst)
        delete_file(src)
        if file_name not in prev_files:
            new_files.append(file_name)

    # Summary output like Git
    print(f"[master {commit.hash_code}] {message}")
    print(f"{len(staged_files)} file(s) changed, {len(new_files)} insertions(+)")
    for file_name in staged_files:
        print(f" create mode 100644 {file_name}")


@require_init
def log_repo(path):
    """
    Prints all commits.
    """
    commit_mgr = CommitManager(path)
    commit_mgr.print_all()


@require_init
def status_repo(path):
    """
    Prints the repository status, similar to 'git status'.
    Shows staged files, modified files, and untracked files.
    """
    staging_path = wit_subfolder(path, "staging")
    committed_path = wit_subfolder(path, "committed")

    commit_mgr = CommitManager(path)
    last_commit = commit_mgr.get_last_commit()

    staged_files = set(list_files_in_folder(staging_path))
    committed_files = set()
    if last_commit:
        last_commit_path = os.path.join(committed_path, last_commit.hash_code)
        if is_valid_path(last_commit_path):
            committed_files = set(list_files_in_folder(last_commit_path))

    working_dir_files = {
        f for f in list_files_in_folder(path)
        if not should_ignore(f)
    }

    print("=== Status ===")

    # Staged files
    if staged_files:
        print("\nStaged files:")
        for f in sorted(staged_files):
            print(f"  {f}")
    else:
        print("\nNo files staged for commit.")

    # Modified files (in staging but different from last commit)
    modified_files = staged_files & committed_files
    if modified_files:
        print("\nModified files:")
        for f in sorted(modified_files):
            print(f"  {f}")

    # Untracked files
    untracked_files = working_dir_files - staged_files - committed_files
    if untracked_files:
        print("\nUntracked files:")
        for f in sorted(untracked_files):
            print(f"  {f}")



@require_init
def checkout_repo(path, version_hash_code):
    """
    Restores files from the given commit hash to the working directory.
    """
    committed_version_path = os.path.join(wit_subfolder(path, "committed"), version_hash_code)
    if not is_valid_path(committed_version_path):
        print(f"error: path spec '{version_hash_code}' did not match any file(s) known to wit")
        return
    for file_name in list_files_in_folder(committed_version_path):
        if should_ignore(file_name):
            continue
        copy_file(os.path.join(committed_version_path, file_name), os.path.join(path, file_name))
    print(f"Note: switching to {version_hash_code}.")

def push_repo(path):
    pass