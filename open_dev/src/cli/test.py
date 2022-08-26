"""Test module."""
import time

import rich_click as click
from rich.progress import track


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


test.add_command(run_all)
