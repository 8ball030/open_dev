"""Test entities."""
from open_dev.src.open_dev_repo import OpenDevRepo, RepoStatus
import pytest


@pytest.mark.skip()
def test_inits_repo():
    """Creates the repo."""
    OpenDevRepo()


@pytest.mark.skip()
def test_gets_repo():
    """Repo object retrieves the current head."""
    repo = OpenDevRepo()
    assert isinstance(repo.current_head, str)


@pytest.mark.skip()
def test_status():
    """Repo object retrieves the current head."""
    repo = OpenDevRepo()
    assert isinstance(repo.status, RepoStatus)
