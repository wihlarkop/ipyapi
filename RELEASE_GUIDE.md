# Complete Release Guide

This guide shows how to release a new version to **both GitHub and PyPI** simultaneously using GitHub Actions automation.

## Prerequisites (One-Time Setup)

### 1. Configure PyPI API Token

1. **Generate Token on PyPI:**
   - Visit: https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Token name: `ipyapi-github-actions`
   - Scope: "Entire account" (initially, then project-specific after first release)
   - Click "Add token"
   - **Copy the token** (starts with `pypi-...`)

2. **Add Token to GitHub Secrets:**
   - Go to: https://github.com/wihlarkop/ipyapi/settings/secrets/actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Secret: Paste your PyPI token
   - Click "Add secret"

### 2. Push Your Code to GitHub

```bash
# If not already pushed
git add .
git commit -m "Initial commit: Ready for v0.1.0 release"
git branch -M main
git push -u origin main
```

## Release Process

### Step 1: Prepare the Release

```bash
# 1. Make sure you're on the main branch and up to date
git checkout main
git pull

# 2. Run tests to ensure everything works
uv run pytest

# 3. Build locally to verify (optional but recommended)
uv build
```

### Step 2: Update Version Numbers

Update version in **3 places**:

**A. `pyproject.toml`:**
```toml
[project]
name = "ipyapi"
version = "0.1.0"  # Change this
```

**B. `ipyapi/__init__.py`:**
```python
__version__ = "0.1.0"  # Change this
```

**C. `CHANGELOG.md`:**
```markdown
## [0.1.0] - 2025-11-01

### Added
- Initial release
- Complete sync and async clients
- [list your changes here]
```

### Step 3: Commit Version Changes

```bash
# Add the changed files
git add pyproject.toml ipyapi/__init__.py CHANGELOG.md

# Commit with a clear message
git commit -m "Release v0.1.0"

# Push to GitHub
git push
```

### Step 4: Create and Push Git Tag

```bash
# Create an annotated tag
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push the tag to GitHub
git push origin v0.1.0
```

### Step 5: Create GitHub Release

**Option A: Using GitHub Web Interface (Easier)**

1. Go to: https://github.com/wihlarkop/ipyapi/releases
2. Click **"Draft a new release"**
3. Fill in the form:
   - **Choose a tag:** Select `v0.1.0` (the tag you just pushed)
   - **Release title:** `v0.1.0 - Initial Release`
   - **Description:** Use your changelog content:
     ```markdown
     ## Initial Release

     First public release of ipyapi - a modern Python client for ipapi.co

     ### Features
     - Complete synchronous and asynchronous clients
     - Support for all ipapi.co endpoints
     - Comprehensive error handling
     - Full type hints
     - 94% test coverage

     ### Installation
     ```bash
     pip install ipyapi
     ```

     ### Quick Start
     ```python
     from ipyapi import IPyAPI

     with IPyAPI() as client:
         location = client.get_location("8.8.8.8")
         print(f"{location.city}, {location.country_name}")
     ```

     See [README](https://github.com/wihlarkop/ipyapi#readme) for full documentation.
     ```
4. Click **"Publish release"**

**Option B: Using GitHub CLI (Faster)**

```bash
# Install GitHub CLI if needed: https://cli.github.com/

# Create release from CHANGELOG
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Release" \
  --notes "$(cat <<'EOF'
## Initial Release

First public release of ipyapi - a modern Python client for ipapi.co

### Features
- Complete synchronous and asynchronous clients
- Support for all ipapi.co endpoints
- Comprehensive error handling
- Full type hints
- 94% test coverage

### Installation
\`\`\`bash
pip install ipyapi
\`\`\`

### Quick Start
\`\`\`python
from ipyapi import IPyAPI

with IPyAPI() as client:
    location = client.get_location("8.8.8.8")
    print(f"{location.city}, {location.country_name}")
\`\`\`

See [README](https://github.com/wihlarkop/ipyapi#readme) for full documentation.
EOF
)"
```

### Step 6: Automation Takes Over!

**What happens automatically:**

1. ✅ GitHub Actions detects the new release
2. ✅ Runs the "Publish to PyPI" workflow
3. ✅ Installs dependencies
4. ✅ Runs full test suite
5. ✅ Builds the package (`.tar.gz` and `.whl`)
6. ✅ Validates the distribution
7. ✅ Publishes to PyPI automatically

**Monitor the process:**
- Go to: https://github.com/wihlarkop/ipyapi/actions
- Watch the "Publish to PyPI" workflow
- Takes ~2-3 minutes

### Step 7: Verify the Release

**A. Check PyPI:**
```bash
# Wait 1-2 minutes for PyPI to process
# Then visit: https://pypi.org/project/ipyapi/

# Or check via CLI
pip index versions ipyapi
```

**B. Test Installation:**
```bash
# Create a fresh environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from PyPI
pip install ipyapi

# Test it works
python -c "from ipyapi import IPyAPI; print('✓ Installation successful!')"
python -c "from ipyapi import __version__; print(f'Version: {__version__}')"
```

## Complete Release Script

For convenience, here's a complete script:

```bash
#!/bin/bash
# release.sh - Complete release script

set -e  # Exit on error

# Configuration
VERSION="0.1.0"

echo "🚀 Starting release process for v${VERSION}"

# Step 1: Verify we're on main and up to date
echo "📋 Checking branch..."
git checkout main
git pull

# Step 2: Run tests
echo "🧪 Running tests..."
uv run pytest

# Step 3: Build to verify
echo "📦 Building package..."
uv build

# Step 4: Update version numbers (manual step reminder)
echo "⚠️  MANUAL STEP: Update version in:"
echo "   - pyproject.toml"
echo "   - ipyapi/__init__.py"
echo "   - CHANGELOG.md"
read -p "Press Enter when done..."

# Step 5: Commit changes
echo "💾 Committing version changes..."
git add pyproject.toml ipyapi/__init__.py CHANGELOG.md
git commit -m "Release v${VERSION}"
git push

# Step 6: Create and push tag
echo "🏷️  Creating tag..."
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
git push origin "v${VERSION}"

# Step 7: Create GitHub release
echo "🎉 Creating GitHub release..."
gh release create "v${VERSION}" \
  --title "v${VERSION}" \
  --notes-file CHANGELOG.md

echo "✅ Release process initiated!"
echo "📊 Monitor progress: https://github.com/wihlarkop/ipyapi/actions"
echo "📦 Check PyPI in ~3 minutes: https://pypi.org/project/ipyapi/"
```

**To use the script:**
```bash
# Make it executable
chmod +x release.sh

# Run it
./release.sh
```

## Subsequent Releases

For future releases (0.1.1, 0.2.0, etc.):

```bash
# 1. Update version numbers (pyproject.toml, __init__.py, CHANGELOG.md)
VERSION="0.1.1"

# 2. Commit and tag
git add .
git commit -m "Release v${VERSION}"
git push
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
git push origin "v${VERSION}"

# 3. Create GitHub release
gh release create "v${VERSION}" \
  --title "v${VERSION}" \
  --notes "See CHANGELOG.md for details"

# 4. Done! Automation handles the rest
```

## Troubleshooting

### Issue: Workflow fails with "403 Forbidden"

**Cause:** PyPI token is invalid or expired

**Solution:**
1. Generate a new token on PyPI
2. Update the `PYPI_API_TOKEN` secret in GitHub
3. Re-run the workflow or create a new patch release

### Issue: "Package already exists" error

**Cause:** You're trying to publish the same version twice

**Solution:**
- You cannot re-upload the same version to PyPI
- Increment the version (e.g., 0.1.0 -> 0.1.1)
- Create a new release

### Issue: Tests pass locally but fail in CI

**Cause:** Environment differences

**Solution:**
1. Check GitHub Actions logs for details
2. Fix the issue
3. Commit the fix
4. Delete the release and tag:
   ```bash
   gh release delete v0.1.0 --yes
   git tag -d v0.1.0
   git push origin :v0.1.0
   ```
5. Increment to next patch version (0.1.0 -> 0.1.1)
6. Try again

### Issue: Forgot to update version number

**Solution:**
1. If not yet published to PyPI:
   - Delete the GitHub release and tag
   - Update version numbers
   - Re-release
2. If already published to PyPI:
   - Cannot change it
   - Release next patch version with fix

## Quick Reference

```bash
# Complete release in one go (after updating versions)
VERSION="0.1.0"
git add . && git commit -m "Release v${VERSION}"
git push && git tag -a "v${VERSION}" -m "Release ${VERSION}"
git push origin "v${VERSION}"
gh release create "v${VERSION}" --title "v${VERSION}" --notes-file CHANGELOG.md
```

## Checklist

Before each release:

- [ ] All tests pass: `uv run pytest`
- [ ] Version updated in `pyproject.toml`
- [ ] Version updated in `ipyapi/__init__.py`
- [ ] CHANGELOG.md updated
- [ ] Changes committed: `git commit -m "Release vX.Y.Z"`
- [ ] Changes pushed: `git push`
- [ ] Tag created: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Tag pushed: `git push origin vX.Y.Z`
- [ ] GitHub Release created
- [ ] Monitor Actions: https://github.com/wihlarkop/ipyapi/actions
- [ ] Verify on PyPI: https://pypi.org/project/ipyapi/
- [ ] Test installation: `pip install ipyapi`

## Summary

The release process is **automated** once you create a GitHub Release:

1. **You do:** Update versions → Commit → Tag → Create GitHub Release
2. **GitHub Actions does:** Test → Build → Publish to PyPI
3. **Result:** Available on both GitHub and PyPI! 🎉

The key is creating a **GitHub Release** with a version tag - this triggers the automation that publishes to PyPI.
