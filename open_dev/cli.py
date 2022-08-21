"""Console script for open_dev."""
import subprocess
import textwrap
import time

import rich_click as click
from rich.progress import track

from open_dev.constants import HEADER
from open_dev.src.open_dev_repo import OpenDevRepo

click.rich_click.USE_MARKDOWN = True


def execute(cmd):
    """Executes a command."""
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def fstr(string):
    """Formatr strings from the interface."""
    return string.split(" ")


@click.group()
def repo():
    """Tooling to enable devs to buidl quick."""


@click.command()
def create():
    """Creates a new repository."""
    click.echo('Hello there')


@click.command()
def info():
    """Retrieves infromation about the current repo."""

    current_repo = OpenDevRepo()
    repo_info = textwrap.dedent(
        f"""
    Currently managing:

        name: \t\t{current_repo.name}
        hash: \t\t{current_repo.current_head[:8]}
        branch: \t\t{current_repo.branch}
        status: \t\t{current_repo.status}


    """
    )
    click.echo(repo_info)


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
    click.echo('Starting Tests.')
    for _ in track(range(20), description="Processing..."):
        time.sleep(0.05)
    click.echo(
        'Success!',
        color="green",
    )


@click.group()
def tasks():
    """Manage Tasks."""


@click.command()
def install():
    """Synchronise dependencies."""
    click.echo(
        """
    Installing dependencies with deps with
    ```bash
    pip install -e . --user
    ````
    """
    )
    cmds = ["pipenv run pip install poetry", "pipenv run poetry install", "pipenv run pip install ."]
    for i in cmds:
        cmd = fstr(i)
        for path in execute(cmd):
            print(path, end="")


click.echo(textwrap.dedent(HEADER))


@click.group()
def main():
    """Oh dev tooling to speed up development."""


deps.add_command(install)
repo.add_command(create)
repo.add_command(info)
test.add_command(run_all)

for group in [repo, deps, test]:
    main.add_command(group)


if __name__ == '__main__':
    main()
