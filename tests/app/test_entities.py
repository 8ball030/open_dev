"""Test entities."""
from open_dev.src.open_dev_repo import OpenDevRepo, RepoStatus


def test_inits_repo():
    """Creates the repo."""
    OpenDevRepo()


def test_gets_repo():
    """Repo object retrieves the current head."""
    repo = OpenDevRepo()
    assert isinstance(repo.current_head, str)

def test_status():
    """Repo object retrieves the current head."""
    repo = OpenDevRepo()
    assert isinstance(repo.status, RepoStatus)
