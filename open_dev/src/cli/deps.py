"""Dependency Management for open dev."""
import rich_click as click


@click.group()
def deps():
    """Manage Dependencies."""
    click.echo('Lets sort out those dependencies.')


@click.command()
def install():
    """Synchronise dependencies."""
    click.echo(
        """
    Install dependencies with deps with
    ```bash
    pip install -e . --user
    ````
    """
    )


deps.add_command(install)
