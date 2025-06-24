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