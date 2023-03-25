# Collaboration Guidelines

This document provides guidelines for working together using Git, Jira, and the trunk-based development approach with feature branches and pull requests.

## Table of Contents

- [Setting Up the Development Environment](#setting-up-the-development-environment)
  - [Visual Studio Code](#visual-studio-code)
  - [PyCharm](#pycharm)
- [How to Report Issues or Bugs](#how-to-report-issues-or-bugs)
- [The process for submitting pull requests](#the-process-for-submitting-pull-requests)

## Setting Up the Development Environment

We recommend using either Visual Studio Code or PyCharm as your development environment for this project. Both IDEs provide excellent support for Python and Django development, including debugging, syntax highlighting, and code navigation. Below you can find brief introductions and links to help you get started with either IDE.

### Visual Studio Code

Visual Studio Code (VSCode) is a lightweight, extensible, and open-source code editor with built-in support for a wide range of programming languages and tools. For Python and Django development, you'll want to install the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension and optionally the [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django) extension for VSCode.

For more information on setting up VSCode for Python development, refer to the [official Python tutorial for VSCode](https://code.visualstudio.com/docs/python/python-tutorial).

### PyCharm

PyCharm is a powerful, feature-rich, and dedicated IDE for Python development, created by JetBrains. It comes in two editions: Community (free and open-source) and Professional (paid, with additional features, including built-in support for Django).

To get started with Django development in PyCharm, refer to the [official PyCharm tutorial on Django](https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-django-project.html).

Choose the IDE that best fits your needs and preferences, and follow the relevant tutorial to set up your development environment.

## How to Report Issues or Bugs

If you encounter any issues or bugs during development, we use Jira to track and manage them. To report a new issue or bug, follow these steps:

1. Enter JIRA and createa a "Bug" ticket
2. Provide a clear and concise summary of the issue.
3. Add a detailed description, including steps to reproduce the problem, the expected behavior, and any relevant error messages or logs.
4. Assign the appropriate labels, components, and priority.
5. Assign the issue to a team member or leave it unassigned if you're unsure who should handle it.

Remember to keep the issue up to date by adding comments, attaching relevant files, and updating the status as needed. Collaborate with your team members to resolve the issue as efficiently as possible.

## The process for submitting pull requests

1. Familiarize yourself with basic Git commands and concepts. Here's a good starting point: [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf). Additionally, you may want to use Git UI tools like [GitExtensions](https://gitextensions.github.io/) or [SourceTree](https://www.sourcetreeapp.com/) to simplify your workflow.

2. Create a Jira ticket for each new feature, bug fix, or task you're working on. Make sure to include a clear description and acceptance criteria.

3. When starting work on a new Jira ticket, create a new feature branch in the Git repository. Use the following naming convention: `<ticket_id>-<short-description>`. For example: SWE-123-add-login-form.

4. Commit your changes to the feature branch regularly and push the branch to the remote repository. Follow a commit message convention to maintain a clean and readable commit history. Here's a good starting point: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

5. When you think your work on a feature is complete, first pull the latest changes from the `main` branch.

```bash
git checkout main
git pull
git checkout your-feature-branch
git merge main
```

6. Resolve any conflicts that may have arisen during the merge. You can find a helpful guide on [resolving merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts) in the GitHub documentation. Commit the changes after resolving the conflicts.

7. Push your feature branch to the remote repository.

```bash
git push
```

8. Create a pull request to merge your feature branch into the `main` branch. Make sure to include a link to the Jira ticket in the pull request description.

9. Assign at least two reviewer to your pull request. The reviewer should be someone who is familiar with the codebase and can provide constructive feedback.

10. When the PR has been approved by the reviewers, merge the PR and delete the feature branch.

11. If you're working on a Jira ticket that has already been assigned to someone else, create a new branch using the same naming convention as above. Then, create a pull request to merge your branch into the feature branch of the person who is already working on the ticket. Make sure to include a link to the Jira ticket in the pull request description.

12. We encourage pair programming sessions when working on complex features or when collaborating with other team members to enhance the learning experience and ensure higher code quality.
