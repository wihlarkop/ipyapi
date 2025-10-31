# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated CI/CD.

## Workflows

### 1. Test (`test.yml`)

**Triggers:** Push to main/develop, Pull Requests

**What it does:**
- Runs tests on multiple Python versions (3.9, 3.10, 3.11, 3.12, 3.13)
- Tests on multiple OS (Ubuntu, Windows, macOS)
- Generates coverage reports
- Uploads coverage to Codecov
- Tests package build and installation

**Status Badge:**
```markdown
[![Tests](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml)
```

### 2. Code Quality (`lint.yml`)

**Triggers:** Push to main/develop, Pull Requests

**What it does:**
- Runs ruff linter to check code quality
- Checks code formatting with ruff
- Runs mypy for type checking

**Status Badge:**
```markdown
[![Code Quality](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml)
```

### 3. Publish to PyPI (`publish.yml`)

**Triggers:**
- New GitHub Release
- Manual trigger (workflow_dispatch)

**What it does:**
- Runs full test suite
- Builds the package
- Validates the distribution
- Publishes to PyPI

**Status Badge:**
```markdown
[![Publish](https://github.com/wihlarkop/ipyapi/actions/workflows/publish.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/publish.yml)
```

## Setup Instructions

### 1. Configure PyPI Publishing

**Option A: API Token (Simpler)**

1. Generate a PyPI API token:
   - Go to https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Name: `ipyapi-github-actions`
   - Scope: "Entire account" (or specific to project after first publish)
   - Copy the token (starts with `pypi-...`)

2. Add token to GitHub Secrets:
   - Go to repository Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click "Add secret"

**Option B: Trusted Publishing (More Secure)**

1. Configure on PyPI:
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new publisher
   - Owner: `wihlarkop`
   - Repository: `ipyapi`
   - Workflow: `publish.yml`
   - Environment: leave empty

2. Update `publish.yml`:
   - Remove the `password` line
   - The workflow will use OpenID Connect for authentication

### 2. Configure Codecov (Optional)

1. Go to https://codecov.io/
2. Sign in with GitHub
3. Add your repository
4. Copy the upload token
5. Add to GitHub Secrets:
   - Name: `CODECOV_TOKEN`
   - Value: Your Codecov token

### 3. Enable GitHub Actions

GitHub Actions should be enabled by default, but verify:
1. Go to repository Settings > Actions > General
2. Ensure "Allow all actions and reusable workflows" is selected

## Publishing a New Release

### Manual Process

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.0.1"  # Increment version
   ```

2. **Commit and push changes:**
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 1.0.1"
   git push
   ```

3. **Create and push a tag:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

4. **Create a GitHub Release:**
   - Go to repository > Releases > "Create a new release"
   - Choose tag: `v1.0.1`
   - Release title: `v1.0.1`
   - Description: Add changelog/release notes
   - Click "Publish release"

5. **GitHub Actions will automatically:**
   - Run all tests
   - Build the package
   - Publish to PyPI

### Automated with GitHub CLI

```bash
# Update version in pyproject.toml first, then:
VERSION="1.0.1"

# Commit changes
git add pyproject.toml
git commit -m "Bump version to ${VERSION}"
git push

# Create tag
git tag "v${VERSION}"
git push origin "v${VERSION}"

# Create release (requires GitHub CLI)
gh release create "v${VERSION}" \
  --title "v${VERSION}" \
  --notes "Release notes here"
```

## Local Testing

Test workflows locally with [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
choco install act-cli  # Windows

# Run test workflow
act pull_request -W .github/workflows/test.yml

# Run lint workflow
act pull_request -W .github/workflows/lint.yml
```

## Troubleshooting

### Workflow fails on "Publish to PyPI"

**Issue:** `403 Forbidden` error

**Solution:**
- Verify `PYPI_API_TOKEN` secret is set correctly
- Check token permissions on PyPI
- Ensure token hasn't expired

---

**Issue:** `File already exists` error

**Solution:**
- You cannot re-upload the same version to PyPI
- Increment version number in `pyproject.toml`
- Create a new release

### Tests fail unexpectedly

**Issue:** Tests pass locally but fail in CI

**Solution:**
- Check Python version compatibility
- Verify all dependencies are in `pyproject.toml`
- Check for environment-specific issues (file paths, OS differences)
- Review GitHub Actions logs for detailed errors

### Coverage upload fails

**Issue:** Codecov upload fails

**Solution:**
- Verify `CODECOV_TOKEN` is set (if using private repo)
- Check Codecov service status
- The workflow is set to `fail_ci_if_error: false`, so this won't block CI

## Adding Status Badges to README

Add these to your `README.md`:

```markdown
[![Tests](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml)
[![Code Quality](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml)
[![PyPI version](https://badge.fury.io/py/ipyapi.svg)](https://badge.fury.io/py/ipyapi)
[![Python versions](https://img.shields.io/pypi/pyversions/ipyapi.svg)](https://pypi.org/project/ipyapi/)
[![codecov](https://codecov.io/gh/wihlarkop/ipyapi/branch/main/graph/badge.svg)](https://codecov.io/gh/wihlarkop/ipyapi)
```

## Monitoring

- **GitHub Actions:** Monitor runs at `https://github.com/wihlarkop/ipyapi/actions`
- **PyPI:** Check package page at `https://pypi.org/project/ipyapi/`
- **Codecov:** View coverage at `https://codecov.io/gh/wihlarkop/ipyapi`
