# Contributing to Hymnary Discord Bot

Thank you for your interest in contributing to the Hymnary Discord Bot! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Hymnary-Discord-Bot.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Set up your development environment (see below)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A Discord Bot Token for testing

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your DISCORD_TOKEN and optionally GUILD_ID
```

### Running Tests

```bash
python test_bot.py
```

This will run the test suite and verify that the core functionality works.

### Running the Bot Locally

```bash
python bot.py
```

The bot will:
1. Connect to Discord
2. Download and cache sitemap files (first run only)
3. Register the `/find` command
4. Be ready to respond to commands

## Code Style

### Python Style Guide

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Use type hints where appropriate

### Documentation

- Update README.md if you add new features
- Add docstrings to new functions and classes
- Update USAGE.md for user-facing changes
- Comment complex logic

## Making Changes

### Before You Start

1. Check existing issues to see if your feature/bug is already being worked on
2. Create a new issue describing what you plan to work on
3. Wait for feedback before starting major changes

### Code Changes

1. Make your changes in your feature branch
2. Test your changes thoroughly
3. Ensure code passes syntax checks: `python -m py_compile *.py`
4. Run the test suite: `python test_bot.py`
5. Update documentation as needed

### Commit Messages

Write clear, descriptive commit messages:

```
Add support for tune sitemaps in search

- Parse tune sitemap files in addition to text sitemaps
- Update search to include tunes
- Add tests for tune searching
```

## Pull Request Process

1. Update README.md with details of changes if applicable
2. Update USAGE.md if you've changed user-facing functionality
3. Ensure all tests pass
4. Create a pull request with a clear description of your changes
5. Reference any related issues in your PR description

### PR Description Template

```markdown
## Description
Brief description of what this PR does

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How you tested these changes

## Related Issues
Fixes #123
```

## Feature Requests

### Good Feature Ideas

- Improved search algorithms
- Additional Discord commands
- Better error handling
- Performance improvements
- Support for other Hymnary.org data types

### How to Suggest Features

1. Open a GitHub issue
2. Use the "Feature Request" template
3. Describe the feature clearly
4. Explain why it would be useful
5. Consider implementation challenges

## Bug Reports

### Before Reporting

1. Check if the bug has already been reported
2. Try to reproduce the bug consistently
3. Gather relevant information (logs, screenshots, etc.)

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- discord.py version:
- Operating System:

## Logs
Relevant error messages or logs
```

## Code Review Process

### What We Look For

- Code quality and readability
- Proper error handling
- Security considerations
- Performance implications
- Test coverage
- Documentation completeness

### Review Timeline

- Small changes: 1-3 days
- Medium changes: 3-7 days
- Large changes: 1-2 weeks

## Security

### Reporting Security Issues

**Do not** open public issues for security vulnerabilities.

Instead:
1. Email the maintainers directly
2. Provide details about the vulnerability
3. Wait for a response before disclosing publicly

### Security Best Practices

- Never commit sensitive data (tokens, passwords, etc.)
- Use environment variables for configuration
- Validate user input
- Be cautious with regex (avoid ReDoS vulnerabilities)
- Keep dependencies up to date

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Look through closed issues
3. Open a new issue with the "question" label
4. Join our Discord server (if available)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Thank You!

Your contributions make this project better. Thank you for taking the time to contribute! 🎵
