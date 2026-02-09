# Contributing to audio-tools

Thank you for considering contributing to audio-tools! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/audio-tools.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Linux)
sudo apt-get install portaudio19-dev espeak espeak-ng

# Run tests
python tests/test_audio_tools.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and simple

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Add integration tests for major features

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Update documentation as needed
- Add tests for new functionality
- Ensure all tests pass
- Write clear commit messages

## Reporting Bugs

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or stack traces

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Clearly describe the feature
- Explain why it would be useful
- Provide examples if possible

## Questions?

Feel free to open an issue for any questions or concerns.
