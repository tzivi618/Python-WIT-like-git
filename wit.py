"""
Command Line Interface for Wit - a minimal version control system.
Provides commands similar to Git: init, add, commit, status, log, checkout, push, analyze.
"""

import click
from repository import (
    init_repo, add_repo, commit_repo, log_repo,
    status_repo, checkout_repo, push_repo, add_all_repo, analyze_only
)
from pathlib import Path

@click.group()
def cli():
    """
    Entry point for the Wit CLI commands.
    """
    pass

@cli.command()
def init():
    """
    Initialize a new Wit repository in the current directory.
    """
    path = Path.cwd()
    init_repo(path)

@cli.command()
@click.argument('file_name')
def add(file_name):
    """
    Add a file or folder to the staging area.
    Use '.' to add all files.
    """
    path = Path.cwd()
    if file_name == '.':
        add_all_repo(path)
    else:
        add_repo(path, file_name)

@cli.command()
@click.option('-m', '--message', required=True, help='Commit message')
def commit(message):
    """
    Create a new commit with staged changes and a commit message.
    """
    path = Path.cwd()
    commit_repo(path, message)

@cli.command()
def status():
    """
    Show the current status of the working directory and staging area.
    """
    path = Path.cwd()
    status_repo(path)

@cli.command()
def log():
    """
    Display the commit history of the repository.
    """
    path = Path.cwd()
    log_repo(path)

@cli.command()
@click.argument('version_hash_code')
def checkout(version_hash_code):
    """
    Restore files in the working directory to a specific commit version.
    """
    path = Path.cwd()
    checkout_repo(path, version_hash_code)

@cli.command()
def push():
    """
    Push committed code to an external server for code analysis.
    """
    path = Path.cwd()
    push_repo(path)

@cli.command()
def analyze():
    """
    Analyze Python files in the working directory using an external server.
    """
    path = Path.cwd()
    analyze_only(path)

if __name__ == '__main__':
    cli()
