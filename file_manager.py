import os, shutil, subprocess

IGNORED_FILES = {"desktop.ini", "Thumbs.db", "ehthumbs.db", ".DS_Store"}
IGNORED_FOLDERS = {".git", ".wit"}
IGNORED_PREFIXES = {"~$"}
IGNORED_EXTENSIONS = {".tmp", ".lnk"}

def should_ignore(name):
    """
    Checks if a file or folder should be ignored based on name patterns.
    """
    return (
        name in IGNORED_FILES or
        name in IGNORED_FOLDERS or
        any(name.startswith(prefix) for prefix in IGNORED_PREFIXES) or
        any(name.endswith(ext) for ext in IGNORED_EXTENSIONS)
    )

def is_valid_path(path):
    """
    Checks if the given path exists on the file system.
    """
    return os.path.exists(path)

def ensure_parent_exists(path):
    """
    Ensures the parent directory of the given path exists.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def create_new_folder_in_path(path):
    """
    Creates a new folder at the given path and hides it on Windows.
    """
    os.makedirs(path, exist_ok=True)
    try:
        subprocess.run(['attrib', '+h', path], check=True)
    except Exception:
        pass

def copy_file(source_path, dest_path):
    """
    Copies a file from source_path to dest_path.
    """
    if is_valid_path(source_path):
        ensure_parent_exists(dest_path)
        shutil.copy2(source_path, dest_path)

def delete_file(path):
    """
    Deletes the file at the given path.
    """
    if is_valid_path(path):
        os.remove(path)

def is_empty_folder(path):
    """
    Checks if the given folder is empty.
    """
    return not os.listdir(path)

def list_files_in_folder(path):
    """
    Returns a list of file names in the given folder.
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def wit_subfolder(path, subfolder=""):
    """
    Constructs a path to a subfolder inside the .wit directory.
    """
    return os.path.join(path, ".wit", subfolder) if subfolder else os.path.join(path, ".wit")
