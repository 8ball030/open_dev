"""Console script for open_dev."""
import subprocess

import rich_click as click
from rich.progress import track
import time
from open_dev.src.entities.repos import OpenDevRepo

click.rich_click.USE_MARKDOWN = True

click.echo(OpenDevRepo.name)
click.echo("=" * len(OpenDevRepo.name))
click.echo(OpenDevRepo.description)
click.echo("*" * len(OpenDevRepo.description))


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def format(string):
    return string.split(" ")

@click.group()
def repo():
    """Tooling to enable devs to buidl quick."""


@click.command()
def create():
    """Creates a new repository."""
    click.echo('Hello there')

@click.command()
def watch():
    """Creates a new repository."""
    click.echo('Hello there')

@click.group()
def deps():
    """Manage Dependencies."""
    click.echo('Lets sort out those dependencies.')

@click.group()
def test():
    """Manage Tests."""
    click.echo('Lets run some tests.')

@click.command()
def run_all():
    """Test all."""
    click.echo('Starting Tests...')
    for i in track(range(20), description="Processing..."):
        time.sleep(1)  # Simulate work being done    


@click.group()
def tasks():
    """Manage Tasks."""

@click.command()
def install():
    """Synchronise dependencies."""
    click.echo("""
    Installing dependencies with deps with
    ```bash
    pip install -e . --user
    ````
    """)
    cmds = [
        "pipenv run pip install poetry",
        "pipenv run poetry install",
        "pipenv run pip install ."
    ]
    for i in cmds:
        cmd = format(i)
        for path in execute(cmd):
            print(path, end="")



@click.group()
def main():
    """OhDev open_dev tooling to enable devs to buidl quick."""


deps.add_command(install)
repo.add_command(create)
test.add_command(run_all)

for group in [
    repo,
    deps,
    test
]:
    main.add_command(group)


if __name__ == '__main__':
    main()
