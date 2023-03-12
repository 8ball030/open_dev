"""Console script for open_dev."""
import logging
import os
import re
import textwrap

import openai
import rich_click as click
from rich.logging import RichHandler

from open_dev.src.open_dev_repo import OpenDevRepo


def get_logger():
    """Get the logger."""
    new_logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(message)s")

    handler = RichHandler(
        markup=False,
        rich_tracebacks=True,
        locals_max_string=None,
        locals_max_length=None,
    )
    handler.setFormatter(formatter)
    new_logger.addHandler(handler)
    return new_logger


logger = get_logger()
logger.setLevel(logging.INFO)

openai.api_key = os.environ.get("OPENAI_API_KEY")


def summarize_changes(changes, is_title=False, is_commit=False):
    """Summarise the changes"""
    added_lines = re.findall(r'\n\+(.*?)\n', changes)
    deleted_lines = re.findall(r'\n\-(.*?)\n', changes)
    added_lines = "\n".join(added_lines)
    deleted_lines = "\n".join(deleted_lines)

    added_lines = f"Added:\n{added_lines}\n\n"
    deleted_lines = f"Deleted:\n{deleted_lines}\n\n"

    prompt = "The following is a paragraph eloquently describing the changes;"

    text = f"{added_lines}{deleted_lines}\n{prompt}"

    max_token = 200

    stop = "****",
    if is_title:
        text = f"{changes}\nWhat could be the title?\n\nA:"
        max_token = 25

    if is_commit:
        text = f"{changes}\nWhat could be the commit message? \n\nA:"
        max_token = 20
        stop = "\n\n"

    # Use OpenAI's GPT-3 language model to summarize the text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text[-4096:],
        max_tokens=max_token,
        n=1,
        stop=stop,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary


def fstr(string):
    """Formatr strings from the interface."""
    return string.split(" ")


@click.group()
def repo():
    """Tooling to enable devs to buidl quick."""


@click.command()
def info():
    """Retrieves infromation about the current repo."""

    current_repo = OpenDevRepo()
    repo_info = textwrap.dedent(
        f"""
    Currently managing:

        name: \t\t{current_repo.name}
        hash: \t\t{current_repo.current_head[:8]}
        branch: \t\t{current_repo.branch}
        status: \t\t{current_repo.status}


    """
    )
    click.echo(repo_info)


@click.command()
@click.option("--target-branch", "-tb", default="main", help="The target branch to compare against.")
@click.option("--title", "-t", default=None, help="The title of the PR. If none will be autogenerated by chatgpt3.")
@click.option(
    "--description", "-d", default=None, help="The description of the PR. If none will be autogenerated by chatgpt3."
)
@click.option("--dry-run", is_flag=True, default=False, help="Simulate the commit and pr creation.")
def pull(target_branch, title, description, dry_run):
    """Creates a pull request based on a summary of changes from chatgpt."""
    current_repo = OpenDevRepo()
    changes = current_repo.changes_from_target(target_branch)
    logger.info("Detecting changes from  %s to %s", target_branch, current_repo.branch)

    if changes is not None:
        logger.info("Changes detected: %s", changes)
        logger.debug(changes)

    if description is None:
        # we try to get more summaries until the user is happy and then we create the PR
        accepted = False
        while not accepted:
            description = summarize_changes(changes)
            logger.info("Generated:\n%s", description)
            accepted = click.confirm("Is this summary acceptable?")
    if title is None:
        accepted = False
        while not accepted:
            title = summarize_changes(description, is_title=True)
            logger.info("Generated:\n%s", title)
            accepted = click.confirm("Is this title acceptable?")
    if not dry_run:
        pull_request = current_repo.create_pr(title, description, target_branch)
        logger.info("Created PR: %s", pull_request)
    else:
        logger.info("Dry run, no PR created.")


@click.command()
@click.argument("commit_type", type=click.Choice(["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]))
@click.argument("msg", type=click.STRING, nargs=-1, default=None)
def commit(commit_type, msg):
    """Check only check for changes since the last commit and commit them."""
    current_repo = OpenDevRepo()
    # if we have no message we will try to generate one

    # target_branch is the current branches latest commit
    since = current_repo.current_head
    target_branch = None
    if msg == () or msg is None:
        message = None
    # we output a nice message to the user
    logger.info("Preparing [%s] changes to %s since %s. Current msg: %s", commit_type, target_branch, since, message)
    if message is None:
        changes = current_repo.changes_since_last_commit()
        logger.info("Detecting changes from  %s ", since)

        if changes is not None:
            logger.info("Changes detected: %s", changes)
            logger.debug(changes)

        accepted = False
        while not accepted:
            description = summarize_changes(f"{changes}\nCommit type: {commit_type}", is_commit=True)
            message = f"[{commit_type}]  {description}"
            logger.info("Generated:\n%s", message)
            accepted = click.confirm("Is this commit msg acceptable?")

    logger.info("Committing [%s] changes to %s since %s. Current msg: %s", commit_type, target_branch, since, message)
    current_repo.commit(message)




@click.group()
def main():
    """Oh dev tooling to speed up development."""


repo.add_command(info)
repo.add_command(pull)

for group in [
    repo,
    commit
]:
    main.add_command(group)


if __name__ == '__main__':
    main()
