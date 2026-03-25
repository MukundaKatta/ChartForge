# Contributing to ChartForge

Thank you for your interest in contributing to ChartForge! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/ChartForge.git
   cd ChartForge
   ```
3. Install development dependencies:
   ```bash
   make dev
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests:
   ```bash
   make test
   ```
4. Run linting and formatting:
   ```bash
   make lint
   make format
   ```
5. Commit your changes with a clear message:
   ```bash
   git commit -m "feat: add your feature description"
   ```
6. Push and open a pull request

## Code Style

- Follow PEP 8 conventions
- Use Black for formatting (line length: 100)
- Use type hints for all function signatures
- Write docstrings for public methods

## Adding a New Chart Type

1. Add the chart method to `src/chartforge/core.py` in the `ChartForge` class
2. Add any SVG helper functions to `src/chartforge/utils.py`
3. Write tests in `tests/test_core.py`
4. Update the README with usage examples

## Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation changes
- `test:` — adding or updating tests
- `refactor:` — code refactoring
- `chore:` — maintenance tasks

## Reporting Issues

- Use GitHub Issues to report bugs
- Include a minimal reproduction example
- Specify your Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
