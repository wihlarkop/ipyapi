# Versioning Guide for IPyAPI

This guide explains how to version the ipyapi package following best practices.

## Current Status

**Current Version:** `0.1.0` (Alpha)

Starting with `0.1.0` allows flexibility for API changes before committing to a stable 1.0.0 release.

## Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH` (e.g., `0.1.0`, `1.2.3`)

### Version Components

```
0.1.0
│ │ │
│ │ └─── PATCH: Bug fixes (backward compatible)
│ └───── MINOR: New features (backward compatible)
└─────── MAJOR: Breaking changes (incompatible API changes)
```

## Version 0.x.x (Pre-1.0)

### During 0.x.x Development

- **0.1.0** - Initial release
- **0.1.1** - Bug fixes
- **0.2.0** - New features (may include small breaking changes)
- **0.3.0** - More features
- **1.0.0** - First stable release

**Important:** In 0.x.x versions, you can make breaking changes in MINOR versions. This is acceptable before 1.0.0.

### Examples for 0.x.x

```python
# Version 0.1.0 -> 0.1.1 (Bug fix)
- Fixed: Rate limit error handling
- Fixed: Type hints for optional parameters

# Version 0.1.1 -> 0.2.0 (New features)
- Added: Retry mechanism with exponential backoff
- Added: Request timeout configuration
- Changed: Default timeout from 10s to 30s (minor breaking change)

# Version 0.2.0 -> 0.3.0 (More features)
- Added: Response caching support
- Added: Batch IP lookup method
- Changed: Client initialization parameters (minor breaking change)

# Version 0.3.0 -> 1.0.0 (Stable release)
- Stable API, no breaking changes
- Production ready
- Committed to strict SemVer from now on
```

## Version 1.x.x+ (Stable)

### After 1.0.0 Release

Once you reach 1.0.0, **strict SemVer applies:**

```python
# Version 1.0.0 -> 1.0.1 (Patch)
- Fixed: Memory leak in async client
- Fixed: Error handling for edge cases

# Version 1.0.1 -> 1.1.0 (Minor)
- Added: New convenience method get_coordinates()
- Added: Support for proxy configuration
- Deprecated: Old method names (but still work)

# Version 1.1.0 -> 2.0.0 (Major - Breaking!)
- Removed: Deprecated methods
- Changed: Client initialization requires API key
- Changed: Method signatures
```

## When to Increment Each Version

### PATCH (0.1.0 -> 0.1.1)

Increment for bug fixes only:
- ✅ Fixed incorrect error handling
- ✅ Fixed memory leaks
- ✅ Fixed documentation errors
- ✅ Fixed type hints
- ❌ No new features
- ❌ No API changes

### MINOR (0.1.0 -> 0.2.0)

Increment for new features:
- ✅ New methods added
- ✅ New optional parameters
- ✅ Deprecating old methods (but still work)
- ✅ Performance improvements
- ✅ In 0.x: Small breaking changes OK
- ❌ In 1.x+: Must be backward compatible

### MAJOR (0.9.0 -> 1.0.0 or 1.5.0 -> 2.0.0)

Increment for breaking changes:
- ✅ Removed methods
- ✅ Changed method signatures
- ✅ Changed behavior of existing methods
- ✅ Removed deprecated features
- ✅ 0.x -> 1.0.0: First stable release

## Practical Examples for IPyAPI

### Example 1: Adding a Bug Fix

```bash
# Current: 0.1.0
# Fix: Timeout error handling

# Update version
version = "0.1.1"

# Changelog
## [0.1.1] - 2025-11-05
### Fixed
- Fixed timeout handling in async client
- Fixed type hints for get_location method
```

### Example 2: Adding New Features

```bash
# Current: 0.1.1
# New: Retry mechanism and caching

# Update version
version = "0.2.0"

# Changelog
## [0.2.0] - 2025-11-10
### Added
- Retry mechanism with exponential backoff
- Response caching with TTL
- New method: get_multiple_locations()
```

### Example 3: Reaching Stable Release

```bash
# Current: 0.3.5
# Ready for production

# Update version
version = "1.0.0"

# Changelog
## [1.0.0] - 2025-12-01
### Changed
- First stable release
- API is now stable and will follow strict SemVer
- All features tested in production environments
```

### Example 4: Breaking Changes

```bash
# Current: 1.5.2
# Breaking: Require API key for all requests

# Update version
version = "2.0.0"

# Changelog
## [2.0.0] - 2026-01-15
### Changed (BREAKING)
- Client now requires api_key parameter
- Removed deprecated get_ip_info() method
- Changed return type of get_location() to always return IPLocation object
```

## Release Checklist

Before bumping version:

- [ ] Update `pyproject.toml` version
- [ ] Update `ipyapi/__init__.py` __version__
- [ ] Update `CHANGELOG.md` with changes
- [ ] Run all tests: `uv run pytest`
- [ ] Build package: `uv build`
- [ ] Commit changes: `git commit -m "Bump version to X.Y.Z"`
- [ ] Create tag: `git tag vX.Y.Z`
- [ ] Push: `git push && git push --tags`
- [ ] Create GitHub Release
- [ ] Verify PyPI publication

## Version Workflow

```bash
# 1. Decide version increment
VERSION="0.2.0"  # or 0.1.1, 1.0.0, etc.

# 2. Update version in files
# - pyproject.toml
# - ipyapi/__init__.py
# - CHANGELOG.md

# 3. Commit and tag
git add .
git commit -m "Bump version to ${VERSION}"
git push
git tag "v${VERSION}"
git push origin "v${VERSION}"

# 4. Create GitHub Release
gh release create "v${VERSION}" \
  --title "v${VERSION}" \
  --notes-file CHANGELOG.md
```

## Common Questions

### Q: When should I release 1.0.0?

**A:** Release 1.0.0 when:
- API is stable and won't change
- Thoroughly tested in real projects
- Used in production by others
- Confident in the design
- Ready to commit to strict SemVer

For ipyapi: After 3-6 months of 0.x releases with user feedback.

### Q: Can I skip versions?

**A:** Yes! You can go from 0.1.5 directly to 0.3.0 if you have significant changes, or straight to 1.0.0 if ready.

### Q: What if I accidentally publish wrong version?

**A:** You cannot unpublish from PyPI! If it's a critical issue:
- Immediately release a new patch version fixing it
- Mark the bad version in PyPI as "yanked" (users can still install but not by default)

### Q: Should I use pre-release versions?

**A:** For testing, you can use:
- `0.1.0a1` - Alpha 1
- `0.1.0b1` - Beta 1
- `0.1.0rc1` - Release Candidate 1

For ipyapi: Not necessary for 0.x versions.

## Development Status Classifiers

Update in `pyproject.toml`:

```toml
# Current (0.1.0)
"Development Status :: 3 - Alpha"

# After significant testing (0.5.0+)
"Development Status :: 4 - Beta"

# After 1.0.0
"Development Status :: 5 - Production/Stable"

# If widely used and mature (2.0.0+)
"Development Status :: 6 - Mature"
```

## Resources

- [Semantic Versioning 2.0.0](https://semver.org/)
- [PEP 440](https://peps.python.org/pep-0440/) - Python version scheme
- [Keep a Changelog](https://keepachangelog.com/)
- [Calendar Versioning](https://calver.org/) - Alternative to SemVer

## Summary for IPyAPI

**Current Strategy:**
1. Start at `0.1.0` (Alpha) ✅
2. Iterate with 0.x versions, gathering feedback
3. Stabilize API over 3-6 months
4. Release `1.0.0` when confident
5. Follow strict SemVer after 1.0.0

This approach gives you flexibility while showing users your commitment to eventually providing a stable API.
