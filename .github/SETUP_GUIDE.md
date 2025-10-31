# GitHub Actions Setup Guide

Follow these steps to configure automated publishing for your ipyapi package.

## Step 1: Push to GitHub

If you haven't already, push your code to GitHub:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete ipyapi library with CI/CD"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/wihlarkop/ipyapi.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Configure PyPI API Token

### Generate PyPI Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/token/)
2. Click **"Add API token"**
3. Fill in:
   - **Token name:** `ipyapi-github-actions`
   - **Scope:** Select "Entire account" (or project-specific after first publish)
4. Click **"Add token"**
5. **Important:** Copy the token immediately (starts with `pypi-...`)
   - You won't be able to see it again!

### Add Token to GitHub Secrets

1. Go to your repository on GitHub: `https://github.com/wihlarkop/ipyapi`
2. Click **Settings** (top navigation)
3. In the left sidebar, click **Secrets and variables** > **Actions**
4. Click **"New repository secret"**
5. Fill in:
   - **Name:** `PYPI_API_TOKEN`
   - **Secret:** Paste your PyPI token
6. Click **"Add secret"**

## Step 3: Test GitHub Actions

### Trigger Test Workflow

The test workflow runs automatically on push/PR. To manually test:

```bash
# Make a small change
echo "# Testing CI" >> README.md

# Commit and push
git add README.md
git commit -m "Test CI workflows"
git push
```

Check the Actions tab: `https://github.com/wihlarkop/ipyapi/actions`

You should see the **Tests** and **Code Quality** workflows running.

## Step 4: Make Your First Release

### Update Version

Edit `pyproject.toml`:

```toml
[project]
name = "ipyapi"
version = "1.0.0"  # Your first release version
```

### Create Release

```bash
# Commit version change
git add pyproject.toml
git commit -m "Release v1.0.0"
git push

# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

### Create GitHub Release

**Option A: Using GitHub Web Interface**

1. Go to `https://github.com/wihlarkop/ipyapi/releases`
2. Click **"Create a new release"**
3. Fill in:
   - **Choose a tag:** Select `v1.0.0`
   - **Release title:** `v1.0.0`
   - **Description:** Write your release notes, for example:

     ```markdown
     ## Initial Release

     First stable release of ipyapi - a modern Python client for ipapi.co

     ### Features
     - Complete API coverage for ipapi.co
     - Both sync and async clients
     - Comprehensive error handling
     - Full type hints
     - 94% test coverage

     ### Installation
     ```bash
     pip install ipyapi
     ```
     ```

4. Click **"Publish release"**

**Option B: Using GitHub CLI**

```bash
# Install GitHub CLI if needed: https://cli.github.com/

gh release create v1.0.0 \
  --title "v1.0.0 - Initial Release" \
  --notes "First stable release with complete API coverage"
```

### Monitor the Release

1. Go to Actions tab: `https://github.com/wihlarkop/ipyapi/actions`
2. You'll see the **"Publish to PyPI"** workflow running
3. Wait for it to complete (usually 2-3 minutes)
4. Check PyPI: `https://pypi.org/project/ipyapi/`

## Step 5: Verify Installation

Once published, test the installation:

```bash
# Create a fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # or `test_env\Scripts\activate` on Windows

# Install from PyPI
pip install ipyapi

# Test import
python -c "from ipyapi import IPyAPI; print('Success!')"
```

## Troubleshooting

### Workflow fails with "403 Forbidden"

**Problem:** PyPI API token is invalid or not set correctly

**Solution:**
1. Verify the secret name is exactly `PYPI_API_TOKEN`
2. Generate a new token on PyPI
3. Update the GitHub secret with the new token

### Workflow fails with "Package already exists"

**Problem:** Version number hasn't been incremented

**Solution:**
1. Update version in `pyproject.toml`
2. Commit and create a new release with new version

### Tests fail in CI but pass locally

**Problem:** Environment differences

**Solution:**
1. Check the GitHub Actions logs for details
2. Ensure all dependencies are in `pyproject.toml`
3. Test with the same Python version as CI

## Optional: Codecov Integration

For code coverage reports:

1. Sign up at [codecov.io](https://codecov.io/)
2. Add your repository
3. Get your upload token
4. Add to GitHub Secrets as `CODECOV_TOKEN`

## Next Steps

After successful setup:

1. **Add badges to README** - They're already there!
2. **Set up branch protection** - Require tests to pass before merging
3. **Enable Dependabot** - Automatic dependency updates
4. **Add CHANGELOG.md** - Track changes between versions

## Future Releases

For subsequent releases:

1. Make your changes
2. Update version in `pyproject.toml`
3. Commit: `git commit -m "Release vX.Y.Z"`
4. Tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
5. Create GitHub Release
6. Automation handles the rest!

## Getting Help

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **PyPI Publishing Guide:** https://packaging.python.org/en/latest/tutorials/packaging-projects/
- **UV Documentation:** https://docs.astral.sh/uv/

---

**Need help?** Open an issue at `https://github.com/wihlarkop/ipyapi/issues`
