# wit — Simple Local Version Control

**`wit`** is a lightweight, Git-inspired version control system implemented in Python.  
It supports basic versioning features and stores all commit data locally in CSV format.

---

##  Features

- Initialize a repository with `wit init`
- Add individual files or all files using `wit add <filename>` or `wit add .`
- Commit staged files with `wit commit -m "your message"`
- View commit history with `wit log`
- Check for changes with `wit status`
- Switch to previous versions using `wit checkout <commit_hash>`
- All commits are saved to a local `data.csv` inside `.wit`

---

##  Setup Instructions

### 1. Clone the project folder  
Example:
```
C:\Users\user1\Desktop\pythonProject
```

### 2. Create a `.bat` launcher

Create a file named `wit.bat` with the following content:

```
@echo off
python C:\Users\user1\Desktop\pythonProject\wit.py %*
```

Make sure `wit.py` exists in that location.

### 3. Add the `.bat` location to your system PATH

- Open **Environment Variables** → edit the `Path` variable  
- Add:
```
C:\Users\user1\Desktop\pythonProject
```

Now you can run `wit` from any terminal window.

---

##  Directory Structure (After `wit init`)

When you initialize a repository in any folder, a `.wit` folder will be created in that folder:

```
.wit/
├── committed/
├── staging/
└── data.csv
```

> This structure is created inside the folder where you ran `wit init`.

---

##  Usage Example

```
wit init
wit add .
wit commit -m "Initial commit"
wit status
wit log
wit checkout abc123def4
```

---

##  Notes

- The `.wit` folder is local to the directory where `wit init` was executed.
- No external database is used — data is stored locally in `data.csv`.
- Only top-level file tracking is currently supported (not recursive in folders).

---

##  Requirements

- Python 3.9+
- Click library (`pip install click`)

---

##  License

MIT License.
