
# LLM-Powered Code Review for GitHub PRs

This project is a Python-based tool that leverages a Language Model (LLM) to perform code reviews on GitHub Pull Requests (PRs) and post comments directly to the PR using the GitHub API.

## Features

- Analyze code changes in a GitHub PR using an LLM.
- Automatically generate review comments based on analysis.
- Post comments directly to the PR using the GitHub API.

## Prerequisites

- Python 3.7 or higher
- Access to a Language Model API (e.g., OpenAI GPT)
- GitHub Personal Access Token with `repo` permissions for accessing and commenting on PRs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/llm-code-review.git
   cd llm-code-review
   
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```