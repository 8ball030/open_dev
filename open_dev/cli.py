"""Console script for open_dev."""
import subprocess

import rich_click as click
# from open_dev.src.entities.repos import OpenDevRepo

click.rich_click.USE_MARKDOWN = True


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


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


@click.command()
def install():
    """Synchronise dependencies."""
    click.echo("""
    Installing dependencies with deps with
    ```bash
    pip install -e . --user
    ````
    """)
    def format(string):
        return string.split(" ")
    cmds = [
        "pip install poetry",
    ]
    for i in cmds:
        cmd = format(i)

        for path in execute(cmd):
            print(path, end="")

    # assert '--help  Show this message and exit.' in help_result.output


@click.group()
def main():
    """Oh! dev tooling to enable devs to buidl quick."""
    # click.echo(OpenDevRepo)
    click.echo("=" * len("open_dev"))
    # click.echo(OpenDevRepo.description)
    # click.echo("*" * len(OpenDevRepo.description))


deps.add_command(install)
repo.add_command(create)

for group in [
    repo,
    deps,
]:
    main.add_command(group)


if __name__ == '__main__':
    main()
