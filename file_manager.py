import os, shutil, subprocess

IGNORED_FILES = {"desktop.ini", "Thumbs.db", "ehthumbs.db", ".DS_Store"}
IGNORED_FOLDERS = {".git", ".wit", ""}
IGNORED_PREFIXES = {"~$"}
IGNORED_EXTENSIONS = {".tmp", ".lnk"}

def should_ignore(path_or_name: str, *, allow_wit=False, allow_results=True) -> bool:
    name = os.path.basename(path_or_name).lower()
    path = path_or_name.lower()
    if not allow_wit and any(part in IGNORED_FOLDERS for part in path.split(os.sep)):
        return True
    if not allow_results and "results" in path.split(os.sep):
        return True
    return (
        name in IGNORED_FILES or
        any(name.startswith(prefix) for prefix in IGNORED_PREFIXES) or
        any(name.endswith(ext) for ext in IGNORED_EXTENSIONS)
    )

def is_valid_path(path: str) -> bool:
    return os.path.exists(path)

def ensure_parent_exists(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def create_new_folder_in_path(path: str):
    os.makedirs(path, exist_ok=True)
    try:
        subprocess.run(['attrib', '+h', path], check=True)
    except Exception:
        pass

def copy_file(source_path: str, dest_path: str):
    if is_valid_path(source_path):
        ensure_parent_exists(dest_path)
        shutil.copy2(source_path, dest_path)

def delete_file(path: str):
    if is_valid_path(path):
        os.remove(path)

def is_empty_folder(path: str) -> bool:
    return not os.listdir(path)

def list_all_files_recursively(base_path: str, *, include_wit=False, include_graphs=True):
    all_files = []
    for root, dirs, files in os.walk(base_path):
        if not include_wit and ".wit" in root.split(os.sep):
            continue
        if not include_graphs and "results" in root.split(os.sep):
            continue
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, base_path)
            if not include_wit and ".wit" in rel_path.split(os.sep):
                continue
            if not include_graphs and "results" in rel_path.split(os.sep):
                continue
            if should_ignore(file_path, allow_wit=include_wit, allow_results=include_graphs):
                continue
            all_files.append(rel_path)
    return all_files

def delete_empty_folders(path: str):
    for root, dirs, _ in os.walk(path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if is_empty_folder(dir_path):
                os.rmdir(dir_path)

def _clear_working_directory(path: str, valid_files: set):
    working_files = list_all_files_recursively(path, include_wit=False)
    for rel_path in working_files:
        if rel_path in valid_files:
            continue
        full_path = os.path.join(path, rel_path)
        if os.path.isfile(full_path):
            delete_file(full_path)

def clear_all_file_and_directory(path: str):
    if not os.path.isdir(path):
        print(f"Path '{path}' is not a valid directory.")
        return
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
        except Exception as e:
            print(f"Failed to delete {full_path}: {e}")

def wit_subfolder(path: str, subfolder="") -> str:
    return os.path.join(path, ".wit", subfolder) if subfolder else os.path.join(path, ".wit")
