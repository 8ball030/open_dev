"""Main module."""

from dataclasses import dataclass
from pathlib import Path

import enum
from git import Repo

class RepoStatus(enum.Enum):
    LOCAL_DIRTY = enum.auto()
    LOCAL_AHEAD = enum.auto()
    REMOTE_AHEAD = enum.auto()
    SYNCED = enum.auto()

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

    @property
    def branch(self) -> str:
        """Returns the current head."""
        return self.git_repo.active_branch.name

    @property
    def status(self) -> str:
        """Returns the current head."""
        if self.git_repo.is_dirty():
            print("Dirty working tree!")
            return RepoStatus.LOCAL_DIRTY
        commits_diff = self.git_repo.git.rev_list('--left-right', '--count', f'{branch}...{branch}@{{u}}')
        num_ahead, num_behind = commits_diff.split('\t')
        print(f'num_commits_ahead: {num_ahead}')
        print(f'num_commits_behind: {num_behind}') 

    def __str__(self) -> str:
        return f"OpenDevRepo({self.remote_path})"


    def __repr__(self) -> str:
        return str(self)

        