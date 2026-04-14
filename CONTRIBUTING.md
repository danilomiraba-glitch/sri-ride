# Contributing

Thanks for contributing.

## Development setup

1. Create an environment.
2. Install project in editable mode.
3. Run tests before opening a PR.

Example with uv:

```bash
uv venv
uv pip install -e ".[dev]"
uv run pytest
```

## Pull request guidelines

1. Keep changes focused and minimal.
2. Add or update tests when behavior changes.
3. Update `CHANGELOG.md` for user-facing changes.

