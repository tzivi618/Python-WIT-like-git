# WIT – A Simple Version Control System

This project is a simplified Git-like version control system implemented in Python.  
It supports basic operations like `init`, `add`, `commit`, `log`, `status`, `checkout`, and `push`.

---

##  Features

- Initialize a Wit repository anywhere on your machine.
- Stage individual files or all files in the current folder.
- Commit changes with messages.
- View commit logs.
- Check repository status.
- Restore previous versions.
- Push to a centralized backup (to be implemented in server).

---

##  Installation & Setup

### 1. Clone the project
Download or clone this repository to your local machine.

### 2. Create a `.bat` shortcut for command-line usage  
Create a file named `wit.bat` with the following content (adjust the path if needed):

```
@echo off
python C:\Users\user1\Desktop\pythonProject\wit.py %*
```

Make sure the path to your actual `wit.py` file is correct.

### 3. Add Python and the `.bat` file to system PATH

In your Windows environment variables (`System Properties > Environment Variables`), add the following paths to the `PATH` variable:

- `C:\Users\user1\Desktop\pythonProject\.venv\Scripts`
- The folder where your `wit.bat` file is saved.

This allows you to run `wit` from any command prompt window.

---

##  Usage

Use the following commands from your terminal:

```bash
wit init               # Initialize a .wit folder
wit add <file>         # Stage a specific file
wit add .              # Stage all files in the current directory
wit commit -m "msg"    # Commit with message
wit log                # Show all commits
wit status             # Show repo status
wit checkout <hash>    # Restore files from a commit
wit push               # Push current commit to server (if implemented)
```

---

##  Notes

- The `.wit` folder is created in the current directory when running `wit init`.
- Commits are stored in the `.wit/committed` directory.
- Staged files are in `.wit/staging`.
- All commit metadata is stored in a local `data.csv` file inside `.wit`.

---

##  Example

```bash
wit init
wit add my_script.py
wit commit -m "Initial commit with basic script"
wit log
```

---

##  Technologies

- Python 3.x
- Standard libraries only (no external DB or dependencies)
- Click – for CLI interface

---

##  License

This project is part of a student final project and is not intended for production use.
