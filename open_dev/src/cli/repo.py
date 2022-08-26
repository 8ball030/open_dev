"""Command group for repo."""
import textwrap

import rich_click as click

from open_dev.src.open_dev_repo import OpenDevRepo

click.rich_click.USE_MARKDOWN = True


def get_repo():
    """Returns currne working repo."""
    current_repo = OpenDevRepo()
    return current_repo


@click.group()
def repo():
    """Tooling to enable devs to buidl quick."""


@click.command()
def get():
    """Retrieves infromation about the current repo."""

    current_repo = get_repo()
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
def create():
    """Creates a new repository."""
    click.echo('Hello there')


@click.command()
def sync():
    """Synchronise a repo."""
    get_repo().sync()


repo.add_command(create)
repo.add_command(get)
repo.add_command(sync)
