import os, shutil
from functools import wraps
from file_manager import (should_ignore, is_valid_path, create_new_folder_in_path, copy_file, delete_file,
    is_empty_folder, list_all_files_recursively, delete_empty_folders, wit_subfolder, _clear_working_directory
)
from commit_manager_csv import CommitManager

def require_init(func):
    """
      Decorator that ensures the repository is initialized before running the function.
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
    Initializes a new Wit repository by creating the .wit, committed, and staging folders.
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

def _copy_to_staging(path, rel_path, staging_path):
    """
        Copies a single file from the working directory to the staging area.
    """
    src = os.path.join(path, rel_path)
    dest = os.path.join(staging_path, rel_path)
    copy_file(src, dest)
    print(f"Added: {rel_path}")

@require_init
def add_repo(path, name):
    """
        Adds a specific file or folder (recursively) to the staging area.
    """
    full_path = os.path.join(path, name)
    staging_path = wit_subfolder(path, "staging")
    if not is_valid_path(full_path):
        print(f"fatal: pathspec '{name}' did not match any files")
        return
    if os.path.isfile(full_path):
        if not should_ignore(name):
            _copy_to_staging(path, name, staging_path)
    elif os.path.isdir(full_path):
        for root, _, files in os.walk(full_path):
            if should_ignore(root):
                continue
            for file in files:
                if should_ignore(file):
                    continue
                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, path)
                _copy_to_staging(path, rel_path, staging_path)

@require_init
def add_all_repo(path):
    """
        Adds all non-ignored files in the working directory to the staging area.
    """
    staging_path = wit_subfolder(path, "staging")
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]
        for file in files:
            src = os.path.join(root, file)
            if should_ignore(src):
                continue
            rel_path = os.path.relpath(src, path)
            _copy_to_staging(path, rel_path, staging_path)

def _move_staged_files_to_commit(staging_path, commit_folder, prev_files):
    """
        Moves all staged files to a new commit folder and returns the list of moved files.
    """
    staged_files = list_all_files_recursively(staging_path)
    new_files = []
    for rel_path in staged_files:
        if should_ignore(rel_path):
            continue
        src = os.path.join(staging_path, rel_path)
        dst = os.path.join(commit_folder, rel_path)
        copy_file(src, dst)
        delete_file(src)
        if rel_path not in prev_files:
            new_files.append(rel_path)
    delete_empty_folders(staging_path)
    return staged_files, new_files

@require_init
def commit_repo(path, message):
    """
    Saves a new commit with the staged files and prints a commit summary.
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
    prev_files = set()
    if last_hash:
        prev_commit_path = os.path.join(committed_path, last_hash)
        prev_files = set(list_all_files_recursively(prev_commit_path))
    staged_files, new_files = _move_staged_files_to_commit(staging_path, commit_folder, prev_files)
    print(f"[master {commit.hash_code}] {message}")
    print(f"{len(staged_files)} file(s) changed, {len(new_files)} insertions(+)")
    for file_name in staged_files:
        print(f" create mode 100644 {file_name}")

@require_init
def log_repo(path):
    """
    Prints a list of all previous commits in reverse chronological order.
    """
    commit_mgr = CommitManager(path)
    commit_mgr.print_all()

def _get_committed_files(committed_path, last_commit):
    """
        Returns a set of all files in the last commit.
    """
    if not last_commit:
        return set()
    last_commit_path = os.path.join(committed_path, last_commit.hash_code)
    if not is_valid_path(last_commit_path):
        return set()
    return set(list_all_files_recursively(last_commit_path))

def _get_working_directory_files(path):
    """
    Returns a set of all non-ignored files currently in the working directory.
    """
    return {
        f for f in list_all_files_recursively(path)
        if not should_ignore(f)
    }

def _print_staged_files(staged_files):
    """
    Prints the list of staged files.
    """
    if staged_files:
        print("\nStaged files:")
        for f in sorted(staged_files):
            print(f"  {f}")
    else:
        print("\nNo files staged for commit.")

def _print_untracked_files(working_files, staged_files, committed_files):
    """
    Prints the list of untracked files that are neither committed nor staged.
    """
    untracked = working_files - staged_files - committed_files
    if untracked:
        print("\nUntracked files:")
        for f in sorted(untracked):
            print(f"  {f}")

@require_init
def status_repo(path):
    """
    Displays the repository status: staged and untracked files.
    """
    staging_path = wit_subfolder(path, "staging")
    committed_path = wit_subfolder(path, "committed")

    commit_mgr = CommitManager(path)
    last_commit = commit_mgr.get_last_commit()

    staged_files = set(list_all_files_recursively(staging_path))
    committed_files = _get_committed_files(committed_path, last_commit)
    working_dir_files = _get_working_directory_files(path)

    print("=== Status ===")
    _print_staged_files(staged_files)
    _print_untracked_files(working_dir_files, staged_files, committed_files)


@require_init
def checkout_repo(path, version_hash_code):
    """
    Restores the working directory to the state of the specified commit.
    """
    committed_version_path = os.path.join(wit_subfolder(path, "committed"), version_hash_code)
    if not is_valid_path(committed_version_path):
        print(f"error: path spec '{version_hash_code}' did not match any file(s) known to wit")
        return
    committed_files = list_all_files_recursively(committed_version_path)
    _clear_working_directory(path, committed_files)
    for rel_path in committed_files:
        if should_ignore(rel_path):
            continue
        src = os.path.join(committed_version_path, rel_path)
        dst = os.path.join(path, rel_path)
        copy_file(src, dst)
    print(f"Note: switching to {version_hash_code}.")

def push_repo(path):
    pass