"""Console script for open_dev."""
import textwrap

import rich_click as click

from open_dev.constants import HEADER
from open_dev.src.cli.deps import deps
from open_dev.src.cli.repo import repo
from open_dev.src.cli.test import test

click.rich_click.USE_MARKDOWN = True

click.echo(textwrap.dedent(HEADER))


@click.group()
def main():
    """Oh dev tooling to speed up development."""


for group in [repo, deps, test]:
    main.add_command(group)
if __name__ == '__main__':
    main()
