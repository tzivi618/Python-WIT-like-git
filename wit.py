"""
Command Line Interface for Wit - a minimal version control system.
Provides commands similar to Git: init, add, commit, status, log, checkout, push.
"""

import click
from repository import (
    init_repo, add_repo, commit_repo, log_repo,
    status_repo, checkout_repo, push_repo, add_all_repo
)
from pathlib import Path


@click.group()
def cli():
    """Main CLI entry point."""
    pass


@cli.command()
def init():
    """Initialize a new Wit repository."""
    path = Path.cwd()
    init_repo(path)


@cli.command()
@click.argument('file_name')
def add(file_name):
    """Add a file or all files (with '.') to staging area."""
    path = Path.cwd()
    if file_name == '.':
        add_all_repo(path)
    else:
        add_repo(path, file_name)


@cli.command()
@click.option('-m', '--message', required=True, help='Commit message')
def commit(message):
    """Create a commit with the staged changes."""
    path = Path.cwd()
    commit_repo(path, message)


@cli.command()
def status():
    """Show the current repository status."""
    path = Path.cwd()
    status_repo(path)


@cli.command()
def log():
    """Display commit history."""
    path = Path.cwd()
    log_repo(path)


@cli.command()
@click.argument('version_hash_code')
def checkout(version_hash_code):
    """Switch to a specific commit version."""
    path = Path.cwd()
    checkout_repo(path, version_hash_code)


@cli.command()
def push():
    """Push committed data to a remote or external server (future use)."""
    path = Path.cwd()
    push_repo(path)


if __name__ == '__main__':
    cli()
