# .github/scripts/print_pr_details.py
from github import Github
import os

# Initialize the GitHub client
token = os.getenv('GITHUB_TOKEN')
g = Github(token)

# Get repository information from environment variables
repo_name = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('GITHUB_REF').split('/')[-2]  # Extract PR number from GitHub ref

# Access the repository and pull request
repo = g.get_repo(repo_name)
pr = repo.get_pull(int(pr_number))

# Print PR metadata
print("Pull Request Details:")
print(f"Title: {pr.title}")
print(f"Description: {pr.body}")
print(f"Author: {pr.user.login}")
print(f"Created at: {pr.created_at}")
print(f"PR State: {pr.state}")
print(f"PR Number: {pr.number}")
print(f"URL: {pr.html_url}")
print(f"Commits in PR: {pr.commits}")
print(f"Latest Commit SHA: {pr.head.sha}")
print(f"{pr.get_commits()[-1]=}")

last_commit = pr.get_commits()[-1]

# Print list of files changed in the PR
print("\nFiles Changed in this PR:")
for file in pr.get_files():
    print(f"Filename: {file.filename}")
    print(f"Status: {file.status}")
    print(f"Additions: {file.additions}")
    print(f"Deletions: {file.deletions}")
    print(f"Changes: {file.changes}")

    # Print the diff for this file (patch content)
    if file.patch:
        print("\nDiff:")
        print(f"{file.patch=}")  # This is the actual diff, similar to GitHub UI
    else:
        print("\nNo diff available for this file.")

    print("=" * 40)

    comment = pr.create_comment(
        body=f"This file is: {file.filename}\n",
        commit_id=last_commit,
        path=file.filename,
        position=0
    )
