"""Main module."""

import enum
from dataclasses import dataclass
from pathlib import Path

from git import Repo


class RepoStatus(enum.Enum):
    """Represets repository statuses."""

    LOCAL_DIRTY = enum.auto()
    LOCAL_AHEAD = enum.auto()
    REMOTE_AHEAD = enum.auto()
    SYNCED = enum.auto()
    WARNING = enum.auto()
    UNKNOWN = enum.auto()


@dataclass
class OpenDevRepo:
    """Class for Repos."""

    name: str = "open-dev"
    project_slug: str = "open_dev"
    cli_name = "o-dev"
    remote_path: str = "git@github.com:8ball030/open_dev.git"
    description: str = "A collection of tooling to enable open source development."
    local_path: Path = Path(".")
    detached: bool = False

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
        try:
            return self.git_repo.active_branch.name
        except TypeError:
            self.detached = True
            return self.current_head

    @property
    def status(self) -> RepoStatus:
        """Returns the current head."""
        num_ahead, num_behind = self.difference_to_target
        if self.git_repo.is_dirty():
            return RepoStatus.LOCAL_DIRTY
        elif not num_ahead and not num_behind:
            return RepoStatus.SYNCED
        elif num_ahead and not num_behind:
            return RepoStatus.LOCAL_AHEAD
        elif not num_ahead and num_behind:
            return RepoStatus.REMOTE_AHEAD
        elif num_ahead and num_behind:
            return RepoStatus.WARNING
        return RepoStatus.UNKNOWN

    @property
    def difference_to_target(self):
        """Checks the difference between current branch and remote."""
        target_branch = self.branch
        if self.detached:
            target_branch = "main"
        commits_diff = self.git_repo.git.rev_list('--left-right', '--count', f'{target_branch}@{{u}}')
        num_ahead, num_behind = commits_diff.split('\t')
        return int(num_ahead), int(num_behind)

    def __str__(self) -> str:
        return f"OpenDevRepo({self.remote_path})"

    def __repr__(self) -> str:
        return str(self)
