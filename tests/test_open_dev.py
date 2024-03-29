#!/usr/bin/env python
"""Tests for `open_dev` package."""

import pytest
from click.testing import CliRunner

from open_dev import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    import requests
    return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    """


def test_content(response):  # pylint: disable=W0621
    """
    Sample pytest test function with the pytest fixture as an argument.
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    """
    del response


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0


def test_commit_group():
    """Test the commit group."""
    runner = CliRunner()
    result = runner.invoke(cli.commit, ['--help'])
    assert result.exit_code == 0, result.output
