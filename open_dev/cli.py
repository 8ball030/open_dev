"""Console script for open_dev."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("open_dev")
    click.echo("=" * len("open_dev"))
    click.echo("A collection of tooling to enable open source development.")


if __name__ == "__main__":
    main()  # pragma: no cover
