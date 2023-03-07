"""Test entities."""
from unittest.mock import patch

import pytest

from open_dev.src.open_dev_repo import OpenDevRepo, RepoStatus


@pytest.fixture(name='repo')
def repo_fixure():
    """Create a openDev repo."""
    with patch('open_dev.src.open_dev_repo.OpenDevRepo.branch', "main"):
        yield OpenDevRepo()


# @pytest.mark.skip()
def test_inits_repo(repo):
    """Creates the repo."""
    print(repo)


def test_gets_repo(repo):
    """Repo object retrieves the current head."""
    assert isinstance(repo.current_head, str)


@pytest.mark.skip()
def test_status(repo):
    """Repo object retrieves the current status."""
    assert isinstance(repo.status, RepoStatus)
