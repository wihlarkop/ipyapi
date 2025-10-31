# Publishing to PyPI

This guide explains how to publish the ipyapi package to PyPI.

## Automated Publishing (Recommended)

The project uses GitHub Actions for automated publishing. When you create a new GitHub Release, the package is automatically built, tested, and published to PyPI.

**Quick Start:**
1. Update version in `pyproject.toml`
2. Create a GitHub Release with a tag (e.g., `v1.0.1`)
3. GitHub Actions handles the rest!

See `.github/workflows/README.md` for detailed setup instructions.

## Manual Publishing (Alternative)

## Prerequisites

1. Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. Generate API tokens:
   - Go to Account Settings > API tokens
   - Create a new token for the project
   - Save the token securely (you'll only see it once)

## Testing the Build

```bash
# Build the package
uv build

# This creates files in dist/:
# - ipyapi-1.0.0.tar.gz (source distribution)
# - ipyapi-1.0.0-py3-none-any.whl (wheel)
```

## Publishing to TestPyPI (Recommended First)

```bash
# Install twine if not already installed
uv pip install twine

# Upload to TestPyPI
uv run twine upload --repository testpypi dist/*

# When prompted:
# Username: __token__
# Password: <your-testpypi-token>
```

Test the installation:

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ipyapi

# Try importing
python -c "from ipyapi import IPyAPI; print('Success!')"
```

## Publishing to PyPI (Production)

Once you've verified everything works on TestPyPI:

```bash
# Upload to PyPI
uv run twine upload dist/*

# When prompted:
# Username: __token__
# Password: <your-pypi-token>
```

## Automated Publishing with GitHub Actions (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install 3.11

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          uv pip install twine
          uv run twine upload dist/*
```

Don't forget to add your PyPI API token to GitHub Secrets:
1. Go to repository Settings > Secrets and variables > Actions
2. Add new secret: `PYPI_API_TOKEN`

## Version Bumping

Before each release, update the version in `pyproject.toml`:

```toml
[project]
name = "ipyapi"
version = "1.0.1"  # Increment this
```

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

## Checklist Before Publishing

- [ ] All tests pass: `uv run pytest`
- [ ] Version number updated in `pyproject.toml`
- [ ] CHANGELOG/release notes updated
- [ ] README is up to date
- [ ] Build succeeds: `uv build`
- [ ] Tested on TestPyPI
- [ ] Git tag created: `git tag v1.0.0 && git push --tags`

## Post-Publishing

After publishing:

1. Create a GitHub release with the same version tag
2. Update the README with the new version
3. Announce on social media/relevant communities
4. Monitor for issues and user feedback

## Useful Commands

```bash
# Clean build artifacts
rm -rf dist/ build/ *.egg-info

# Check package with twine
uv run twine check dist/*

# View package info
pip show ipyapi

# Uninstall
pip uninstall ipyapi
```

## Troubleshooting

**Error: File already exists**
- You cannot reupload the same version. Increment the version number.

**Error: Invalid credentials**
- Make sure you're using `__token__` as username
- Verify your API token is correct and has proper permissions

**Error: Package name already taken**
- Choose a different package name in `pyproject.toml`
