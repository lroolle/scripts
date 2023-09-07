import requests
import json
import getpass
import argparse


DEFAULT_REPOS = [
    # Python
    "npm-x",
    "npmweb-x",
    "npm-package",
    "npm-contrib-x",
    "smartprobe-x",
    "smartprobe-package",
    # Go
    "npmweb-go",
    "npm-query",
    # Rust
    "npm-dataflow",
    # Other
    "npm-extensions",
]


def create_branch(
    base_url, project_key, repo_slug, base_branch, new_branch, username, password
):
    """Create a branch in a Bitbucket repository using the REST API."""

    endpoint = f"{base_url}/rest/branch-utils/1.0/projects/{project_key}/repos/{repo_slug}/branches"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "name": new_branch,
        "startPoint": f"refs/heads/{base_branch}",
        "message": f"Creating branch {new_branch}",
    }

    response = requests.post(
        endpoint, headers=headers, data=json.dumps(data), auth=(username, password)
    )

    if response.status_code == 201:
        print(f"✅ {repo_slug}: {new_branch}")
    else:
        error_msg = json.loads(response.text).get("errors", [{}])[0].get("message", "")
        print(f"❌ {repo_slug}: {error_msg}")


def main():
    """Main function to handle user input and branch creation."""

    parser = argparse.ArgumentParser(
        description="Create branches in Bitbucket repositories."
    )

    parser.add_argument(
        "--base",
        required=True,
        help="The base branch from which the new branch will be created.",
    )
    parser.add_argument(
        "--target", required=True, help="The name of the new branch to be created."
    )
    parser.add_argument("--username", required=True, help="Your Bitbucket username.")
    parser.add_argument(
        "--repos",
        nargs="*",
        default=DEFAULT_REPOS,
        help="List of repositories to create the branch in. E.g., --repos repo1 repo2 repo3",
    )
    parser.add_argument(
        "--base-url",
        required=True,
        help="The base URL of the Bitbucket server. E.g., https://git.dev.com",
    )
    parser.add_argument(
        "--project",
        required=True,
        help="The project key for the repositories. E.g., NPM",
    )

    args = parser.parse_args()

    password = getpass.getpass(
        f"Enter password for {args.username} (input will be hidden): "
    )

    print(
        f"Initializing branch '{args.target}' from base '{args.base}' in repositories:"
    )
    for repo_slug in args.repos:
        create_branch(
            args.base_url,
            args.project,
            repo_slug,
            args.base,
            args.target,
            args.username,
            password,
        )


if __name__ == "__main__":
    main()
