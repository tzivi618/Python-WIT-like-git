import os
import io
import requests
from requests.exceptions import RequestException, HTTPError
from functools import wraps
from file_manager import (
    should_ignore, is_valid_path, create_new_folder_in_path,
    copy_file, is_empty_folder, list_all_files_recursively,
    delete_empty_folders, wit_subfolder, _clear_working_directory,
    clear_all_file_and_directory
)
from commit_manager_csv import CommitManager

URL = "http://localhost:8000"

def require_init(func):
    """Decorator to ensure the path is a Wit repository before running the function."""
    @wraps(func)
    def wrapper(path, *args, **kwargs):
        if not os.path.exists(wit_subfolder(path)):
            print("fatal: not a wit repository (or any of the parent directories): .wit")
            return
        return func(path, *args, **kwargs)
    return wrapper

def init_repo(path):
    """Initialize a new Wit repository with required folders."""
    create_new_folder_in_path(wit_subfolder(path))
    create_new_folder_in_path(wit_subfolder(path, "committed"))
    create_new_folder_in_path(wit_subfolder(path, "staging"))
    print(f"Initialized empty Wit repository in {wit_subfolder(path)}/")

def _copy_to_staging(path, rel_path, staging_path):
    """Copy a file to the staging area."""
    src = os.path.join(path, rel_path)
    dest = os.path.join(staging_path, rel_path)
    copy_file(src, dest)
    print(f"Added: {rel_path}")

@require_init
def add_repo(path, name):
    """Add a specific file or directory to staging."""
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
            for file in files:
                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, path)
                if not should_ignore(abs_file_path):
                    _copy_to_staging(path, rel_path, staging_path)

@require_init
def add_all_repo(path):
    """Add all non-ignored files in the working directory to staging."""
    staging_path = wit_subfolder(path, "staging")
    files = list_all_files_recursively(path, include_wit=False)
    for rel_path in files:
        _copy_to_staging(path, rel_path, staging_path)

def _move_staged_files_to_commit(staging_path, commit_folder, prev_files):
    """Move staged files to a commit folder and return info on changes."""
    staged_files = list_all_files_recursively(staging_path, include_wit=True)
    new_files = []
    for rel_path in staged_files:
        src = os.path.join(staging_path, rel_path)
        dst = os.path.join(commit_folder, rel_path)
        copy_file(src, dst)
        if rel_path not in prev_files:
            new_files.append(rel_path)
    delete_empty_folders(staging_path)
    return staged_files, new_files

@require_init
def commit_repo(path, message):
    """Create a new commit from staged files with a message."""
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
        prev_files = set(list_all_files_recursively(prev_commit_path, include_wit=True))

    staged_files, new_files = _move_staged_files_to_commit(staging_path, commit_folder, prev_files)
    clear_all_file_and_directory(staging_path)

    print(f"[master {commit.hash_code}] {message}")
    print(f"{len(staged_files)} file(s) changed, {len(new_files)} insertions(+)")
    for file_name in staged_files:
        print(f" create mode 100644 {file_name}")

@require_init
def log_repo(path):
    """Print all previous commits."""
    CommitManager(path).print_all()

def _get_committed_files(committed_path, last_commit):
    """Get all committed files from the last commit."""
    if not last_commit:
        return set()
    last_commit_path = os.path.join(committed_path, last_commit.hash_code)
    if not is_valid_path(last_commit_path):
        return set()
    return set(list_all_files_recursively(last_commit_path, include_wit=True))

def _get_working_directory_files(path):
    """Get all current files in the working directory."""
    return {f for f in list_all_files_recursively(path, include_wit=False) if not should_ignore(f)}

def _print_staged_files(staged_files):
    """Print staged files for user reference."""
    if staged_files:
        print("\nStaged files:")
        for f in sorted(staged_files):
            print(f"  {f}")
    else:
        print("\nNo files staged for commit.")

def _print_untracked_files(working_files, staged_files, committed_files):
    """Print files that are not tracked by the system."""
    untracked = working_files - staged_files - committed_files
    if untracked:
        print("\nUntracked files:")
        for f in sorted(untracked):
            print(f"  {f}")

@require_init
def status_repo(path):
    """Show the status of files in the repository."""
    staging_path = wit_subfolder(path, "staging")
    committed_path = wit_subfolder(path, "committed")
    commit_mgr = CommitManager(path)
    last_commit = commit_mgr.get_last_commit()
    staged_files = set(list_all_files_recursively(staging_path, include_wit=True))
    committed_files = _get_committed_files(committed_path, last_commit)
    working_dir_files = _get_working_directory_files(path)
    print("=== Status ===")
    _print_staged_files(staged_files)
    _print_untracked_files(working_dir_files, staged_files, committed_files)

@require_init
def checkout_repo(path, version_hash_code):
    """Restore all files to a specific commit version."""
    committed_version_path = os.path.join(wit_subfolder(path, "committed"), version_hash_code)
    if not is_valid_path(committed_version_path):
        print(f"error: path spec '{version_hash_code}' did not match any file(s) known to wit")
        return
    committed_files = list_all_files_recursively(committed_version_path, include_wit=True)
    _clear_working_directory(path, set(committed_files))
    for rel_path in committed_files:
        if should_ignore(rel_path):
            continue
        src = os.path.join(committed_version_path, rel_path)
        dst = os.path.join(path, rel_path)
        copy_file(src, dst)
    print(f"Note: switching to {version_hash_code}.")

def send_file_to_server(files_data, server_url):
    """Send files to a server for analysis or alerts."""
    try:
        response = requests.post(server_url, files=files_data)
        response.raise_for_status()
        return response
    except HTTPError as e:
        return e.response
    except RequestException as e:
        print(f"[Error] Network error: {e}")
        return None

@require_init
def push_repo(path):
    """Send committed Python files to the server for analysis."""
    staging_path = wit_subfolder(path, "staging")
    last_hash = CommitManager(path).get_last_hash()
    if not is_empty_folder(staging_path) or not last_hash:
        print("You must commit before pushing.")
        return

    committed_path = os.path.join(wit_subfolder(path, "committed"), last_hash)
    files = [
        f for f in list_all_files_recursively(committed_path, include_wit=True, include_graphs=True)
        if f.endswith(".py")
    ]
    file_blobs = []
    for f in files:
        file_path = os.path.join(committed_path, f)
        with open(file_path, 'rb') as file_obj:
            content = file_obj.read()
            file_blobs.append((f, content))

    if not file_blobs:
        print("[Notice] No Python files to analyze. Push aborted.")
        return

    def make_files_data():
        data = [('files', (f, io.BytesIO(content))) for f, content in file_blobs]
        data.append(('project_root', (None, str(path))))
        return data

    response = send_file_to_server(make_files_data(), URL + "/alerts")
    if response is None:
        print("[Error] No response received from server.")
        return

    try:
        json_response = response.json()
    except Exception:
        print("[Error] Server returned invalid JSON.")
        print(response.text)
        return

    status = json_response.get("status")
    errors = json_response.get("errors", [])

    if status == "failed":
        print("[Error] No Python files were processed successfully.")
        for err in errors:
            print(f" - {err['file']}: {err['error']}")
    elif status == "partial":
        print("[Partial Success] Some files processed successfully.")
        for err in errors:
            print(f" - {err['file']}: {err['error']}")
        print(json_response["message"])
    elif status == "success":
        print("[Success] All files processed successfully.")
        print(json_response["message"])
    else:
        print("[Warning] Unknown response status from server.")
        print(json_response)

@require_init
def analyze_only(path):
    """Send all .py files in working directory for static analysis only."""
    files = list_all_files_recursively(path, include_wit=False, include_graphs=False)
    file_blobs = []
    for f in files:
        if not f.endswith(".py"):
            continue
        file_path = os.path.join(path, f)
        with open(file_path, 'rb') as file_obj:
            content = file_obj.read()
            file_blobs.append((f, content))

    if not file_blobs:
        print("[Notice] No Python files to analyze. Analyze aborted.")
        return

    def make_files_data():
        data = [('files', (f, io.BytesIO(content))) for f, content in file_blobs]
        data.append(('project_root', (None, str(path))))
        return data

    response = send_file_to_server(make_files_data(), URL + "/analyze")
    if response is None:
        print("[Error] No response received from server.")
        return

    try:
        json_response = response.json()
    except Exception:
        print("[Error] Server returned invalid JSON.")
        print(response.text)
        return

    status = json_response.get("status")
    errors = json_response.get("errors", [])

    if status == "failed":
        print("[Error] No Python files were analyzed.")
        for err in errors:
            print(f" - {err['file']}: {err['error']}")
    elif status == "partial":
        print("[Partial Success] Some files analyzed successfully.")
        for err in errors:
            print(f" - {err['file']}: {err['error']}")
        print(json_response["message"])
    elif status == "success":
        print("[Success] All files analyzed successfully.")
        print(json_response["message"])
    else:
        print("[Warning] Unknown response status from server.")
        print(json_response)
