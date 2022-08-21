"""Main module."""

from dataclasses import dataclass
from pathlib import Path

from git import Repo


@dataclass
class OpenDevRepo:
    """Class for Repos."""

    name: str = "open-dev"
    project_slug: str = "open_dev"
    cli_name = "o-dev"
    remote_path: str = "git@github.com:8ball030/open_dev.git"
    description: str = "A collection of tooling to enable open source development."
    local_path: Path = Path(".")

    @property
    def git_repo(self) -> Repo:
        """Retrieve the repository."""
        assert self.local_path.exists()
        return Repo(self.local_path)

    @property
    def current_head(self) -> str:
        """Returns the current head."""
        return self.git_repo.head.object.hexsha

    def __str__(self) -> str:
        return f"OpenDevRepo({self.remote_path})"
