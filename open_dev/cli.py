"""Console script for open_dev."""

import click

description ="A collection of tooling to enable open source development."

@click.command()
def main():
    """Main entrypoint."""
    click.echo("open_dev")
    click.echo("=" * len("open_dev"))
    click.echo(description)
    click.echo("*" * len(description))


if __name__ == "__main__":
    main()  # pragma: no cover
