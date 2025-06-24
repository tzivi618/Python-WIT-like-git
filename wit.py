import click

from repository import init_repo, add_repo, commit_repo, log_repo, status_repo, checkout_repo,push_repo, add_all_repo

from pathlib import Path


@click.group()
def cli():
    pass


@cli.command()
def init():
    path = Path.cwd()
    print(path)
    init_repo(path)


@cli.command()
@click.argument('file_name')
def add(file_name):
    path = Path.cwd()
    if file_name == '.':
        add_all_repo(path)
    else:
        add_repo(path, file_name)

@cli.command()
@click.option('-m', '--message', required=True, help='Commit message')
def commit(message):
    path = Path.cwd()
    commit_repo(path, message)



@cli.command()
def status():
    path = Path.cwd()
    status_repo(path)


@cli.command()
def log():
    path = Path.cwd()
    log_repo(path)


@cli.command()
@click.argument('version_hash_code')
def checkout(version_hash_code):
    path = Path.cwd()
    checkout_repo(path, version_hash_code)

@cli.command()
def push():
    path=Path.cwd()
    push_repo(path)


if __name__ == '__main__':
    cli()
