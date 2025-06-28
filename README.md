# WIT – A Simple Version Control System

This project is a Git-like version control system developed in Python.  
Supports basic commands: `init`, `add`, `commit`, `log`, `status`, `checkout`, `push`, and also `analyze` for temporary analysis.

---

##  Main Features
- Create a new Wit repository in any folder.
- Staging of individual files or all files in the folder.
- Create commits with messages.
- View commit history.
- Check repository status.
- Restore previous versions.
- Send code to the server with `push`.
- Temporary code analysis with `analyze`.
- Save graphs and analysis results in the `results` folder.
---

##  Installation & Setup

### 1. Clone the project
Clone or download the repository to your local machine.

### 2. Create a `.bat` file for command shortcuts
Create a file named `wit.bat` with the following content (adjust the path):

```bat
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
wit init               # Create a .wit folder for version control
wit add <file>         # Add a file to staging
wit add .              # Add all files in the current folder
wit commit -m "msg"    # Create a commit with message
wit log                # View commit history
wit status             # Check repository status
wit checkout <hash>    # Restore files from a specific commit
wit push               # Send the latest commit to the server for analysis and graph generation
wit analyze            # Temporary analysis only (without commit)
```

---

##  Notes

- The  `.wit` older is created on the first run of `wit init`.
- Commits are stored in `.wit/committed`.
- Files waiting to be committed are in `.wit/staging`.
- All commit metadata is saved locally in the `data.csv` file inside `.wit`.
- Graphs and analysis results are saved in the `results` folder

---

##  Example

```bash
wit init
wit add my_script.py
wit commit -m "Initial commit with script"
wit log
wit push
```

---

##  Technologies

- Python 3.x
- Click – for CLI interface

---

##  License

This project was built for study and demo purposes only and is not recommended for production use.

---

##  See also
https://github.com/tzivi618/wit-server-py

