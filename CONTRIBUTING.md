<!-- omit in toc -->
# Contributing to itscalledsoccer

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The ASA community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Tweet about it
> - Refer this project in your project's README
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
    - [Environment Setup](#environment-setup)
      - [Install Python](#install-python)
      - [Install git](#install-git)
      - [Create and checkout a branch](#create-and-checkout-a-branch)
      - [Create and activate a virtual environment](#create-and-activate-a-virtual-environment)
      - [Install development dependencies](#install-development-dependencies)
    - [Make your changes](#make-your-changes)
      - [Linting and formatting](#linting-and-formatting)
      - [Testing](#testing)
    - [Open a pull request](#open-a-pull-request)
  - [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://american-soccer-analysis.github.io/itscalledsoccer/).

Before you ask a question, it is best to search for existing [Issues](https://github.com/American-Soccer-Analysis/itscalledsoccer/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/American-Soccer-Analysis/itscalledsoccer/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions, depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://american-soccer-analysis.github.io/itscalledsoccer/). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/American-Soccer-Analysis/itscalledsoccerissues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be submitted [here](https://github.com/American-Soccer-Analysis/itscalledsoccer/security/advisories/new).

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Bug Report](https://github.com/American-Soccer-Analysis/itscalledsoccer/issues/new?assignees=&labels=bug&projects=&template=bug-report.yml&title=%5BBug%5D%3A+%3Ctitle%3E).
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps. Bugs without reproduction steps will not be addressed until they are provided.
- If the team is able to reproduce the issue, the issue will be left to be [implemented by someone](#your-first-code-contribution).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for `itscalledsoccer`, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://american-soccer-analysis.github.io/itscalledsoccer/) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/American-Soccer-Analysis/itscalledsoccer/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/American-Soccer-Analysis/itscalledsoccer/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- **Explain why this enhancement would be useful** to most `itscalledsoccer` users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

Include the above information in a new [Feature Request](https://github.com/American-Soccer-Analysis/itscalledsoccer/issues/new?assignees=&labels=feature-request&projects=&template=feature-request.yml&title=%5BFeature+Request%5D%3A+%3Ctitle%3E).

### Your First Code Contribution

#### Environment Setup

The first thing you'll want to do is [fork](https://github.com/American-Soccer-Analysis/itscalledsoccer/fork) the repository and then clone it down to the machine you're working on via SSH or HTTPS.

```sh
# SSH
git clone git@github.com:American-Soccer-Analysis/itscalledsoccer.git
# HTTPS
git clone https://github.com/American-Soccer-Analysis/itscalledsoccer.git
```

##### Install Python

Once the repository is successfully cloned, make sure you have Python 3 installed on your system. To check that it's installed correctly, you can run:

```sh
python --version
# Or:
python3 --version
# On Windows (cmd.exe, with the Python Launcher for Windows):
py --version
```

If you don't have Python already installed, you can download it [here](https://www.python.org/downloads/).

##### Install git

You'll also need [git](https://git-scm.com/) installed. If you don't have it installed, it can be downloaded [here](https://git-scm.com/downloads). To make sure it's installed correctly, you can run:

```sh
git -v
```

##### Create and checkout a branch

You'll want to create a branch for your changes. You can do that via the `git` command.

```sh
cd itscalledsoccer
git branch BRANCH_NAME
git checkout BRANCH_NAME
```

##### Create and activate a virtual environment

You'll want to create a Python virtual environment, which isolates installed dependencies from other projects, to install the dependencies for `itscalledsoccer`

```sh
python3 -m venv venv
# Mac/Linux
. venv/bin/activate
# Windows
venv/Scripts/activate
```

For more information, see the [venv documentation](https://docs.python.org/3/library/venv.html).

##### Install development dependencies

The following command will install the appropriate dependencies in the virtual environment you just created.

```sh
pip install ".[test]"
```

#### Make your changes

With the dependencies installed, you're now ready to make your changes. All of the logic for `itscalledsoccer` exists in `client.py`, so this is probably the only Python file you'll need to change. When you're finished with your changes, make sure the new code compiles correctly, all the lint and unit tests pass and you've made any necessary updates to the [documentation](#improving-the-documentation).

##### Linting and formatting

`itscalledsoccer` uses [mypy](https://www.mypy-lang.org/) for static type checking.

```sh
mypy itscalledsoccer
```


`itscalledsoccer` uses [ruff](https://docs.astral.sh/ruff/) for formatting. 

```sh
ruff check itscalledsoccer
ruff format itscalledsoccer
```

##### Testing

`itscalledsoccer` uses [pytest](https://docs.pytest.org/en/8.2.x/#) for testing. To run the test suite, run `pytest` from the root directory of the repository.

```sh
pytest
```

Whenever you add or modify code, you should ensure that your changes have test coverage. To create a test coverage report, run the below command. 

```sh
pytest --cov=itscalledsoccer --cov-report=html
```
Open htmlcov/index.html in a browser and review the generated coverage report.


#### Open a pull request

Once the tests are in good shape and the code has been linted and formatted, you're ready to open a pull request (PR). The [GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) provide great instructions on how to do just that.

Once the PR is open, one of the `itscalledsoccer` maintainers will approve the CI workflow run if needed and review the code.

### Improving The Documentation

We use [`Material for MkDocs`](https://squidfunk.github.io/mkdocs-material/) to generate our [documentation site](https://american-soccer-analysis.github.io/itscalledsoccer/). All of our documentation lives in the `docs` folder except for the documentation that is automatically generated from the docstrings by [`mkdocstrings`](https://mkdocstrings.github.io/). Our docstrings follow the [Google styleguide](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings).

## Styleguides

### Commit Messages

We aim to follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for our commit messages.

<!-- omit in toc -->
## Attribution

This guide is based on the **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!
