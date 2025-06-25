import os, shutil, subprocess

IGNORED_FILES = {"desktop.ini", "Thumbs.db", "ehthumbs.db", ".DS_Store"}
IGNORED_FOLDERS = {".git", ".wit"}
IGNORED_PREFIXES = {"~$"}
IGNORED_EXTENSIONS = {".tmp", ".lnk"}


def should_ignore(path_or_name: str) -> bool:
    """
    Returns True if the given path or name should be ignored.
    Ignores system files, temporary files, Git/Wit folders, and others.
    """
    name = os.path.basename(path_or_name).lower()
    path = path_or_name.lower()

    return (
        name in IGNORED_FILES or
        name in IGNORED_FOLDERS or
        any(name.startswith(prefix) for prefix in IGNORED_PREFIXES) or
        any(name.endswith(ext) for ext in IGNORED_EXTENSIONS) or
        any(ignored_folder in path.split(os.sep) for ignored_folder in IGNORED_FOLDERS)
    )


def is_valid_path(path):
    """
    Returns True if the given path exists in the file system.
    """
    return os.path.exists(path)


def ensure_parent_exists(path):
    """
    Ensures the parent directory of the given path exists.
    Creates it if necessary.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def create_new_folder_in_path(path):
    """
    Creates a folder at the given path.
    On Windows, the folder is hidden using the 'attrib' command.
    """
    os.makedirs(path, exist_ok=True)
    try:
        subprocess.run(['attrib', '+h', path], check=True)
    except Exception:
        pass


def copy_file(source_path, dest_path):
    """
    Copies a file from source_path to dest_path.
    Creates parent folders if needed.
    """
    if is_valid_path(source_path):
        ensure_parent_exists(dest_path)
        shutil.copy2(source_path, dest_path)


def delete_file(path):
    """
    Deletes the file at the given path, if it exists.
    """
    if is_valid_path(path):
        os.remove(path)


def is_empty_folder(path):
    """
    Returns True if the folder at the given path is empty.
    """
    return not os.listdir(path)


def list_files_in_folder(path):
    """
    Returns a list of file names directly inside the given folder.
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def list_all_files_recursively(base_path):
    """
    Returns a list of all files inside the base path, recursively.
    Each path is returned as a relative path from base_path.
    """
    all_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_path)
            all_files.append(rel_path)
    return all_files


def delete_empty_folders(path):
    """
    Recursively deletes all empty folders under the given path.
    """
    for root, dirs, _ in os.walk(path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if is_empty_folder(dir_path):
                os.rmdir(dir_path)


def _clear_working_directory(path, valid_files):
    """
    Deletes all files in the working directory that are not part of valid_files.
    Ignores system and Wit-related files.
    """
    working_files = list_all_files_recursively(path)
    for rel_path in working_files:
        if should_ignore(rel_path) or rel_path in valid_files:
            continue
        delete_file(os.path.join(path, rel_path))


def wit_subfolder(path, subfolder=""):
    """
    Returns the path to a subfolder inside the .wit directory.
    If no subfolder is provided, returns the path to the .wit directory itself.
    """
    return os.path.join(path, ".wit", subfolder) if subfolder else os.path.join(path, ".wit")
