"""Test entities."""
from open_dev.src.open_dev_repo import OpenDevRepo, RepoStatus
import pytest
from unittest.mock import patch


@pytest.fixture()
def open_dev_repo():
    with patch('open_dev.src.open_dev_repo.OpenDevRepo.branch', "main"):
        yield OpenDevRepo()

# @pytest.mark.skip()
def test_inits_repo(open_dev_repo):
    """Creates the repo."""


def test_gets_repo(open_dev_repo):
    """Repo object retrieves the current head."""
    assert isinstance(open_dev_repo.current_head, str)


@pytest.mark.skip()
def test_status(open_dev_repo):
    """Repo object retrieves the current head."""
    with patch('git.cmd', (1,2)):
        assert isinstance(open_dev_repo.status, RepoStatus)
