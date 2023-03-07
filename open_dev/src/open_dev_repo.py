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

    def changes_from_target(self, target: str = "main") -> str:
        """Returns the changes from the target branch."""
        return self.git_repo.git.diff(f"{target}..{self.branch}")

    def __str__(self) -> str:
        return f"OpenDevRepo({self.remote_path})"

    def create_pr(self, title, description, target_branch):
        """Creates a PR on the remote"""
        remote_repo = self.git_repo.remote()
        branch = self.git_repo.active_branch

        # Create the pull request using the `git` command-line interface
        # git push the branch to the remote repository
        # git push --set-upstream origin (git rev-parse --abbrev-ref HEAD)

        self.git_repo.git.push(remote_repo.name, branch.name)
        url = remote_repo.url
        owner = url.split(":")[1].split("/")[:-1][0]
        repo = url.split(":")[1].split("/")[-1:][0].split(".git")[0]

        command = f"gh pr create -B {target_branch} -R {owner}/{repo} --fill -t '{title}' -b '{description}'"
        res = self.git_repo.git.execute(command, shell=True)
        return res

    def __repr__(self) -> str:
        return str(self)
