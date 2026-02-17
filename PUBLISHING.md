# Publishing to PyPI

This document explains how to publish the `bimotype-ternary` package to PyPI.

## Prerequisites

### 1. PyPI Account Setup

1. Create accounts on:
   - [PyPI](https://pypi.org/account/register/)
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing)

2. Enable 2FA (Two-Factor Authentication) on both accounts

### 2. GitHub Trusted Publishing Setup

**Recommended Method** - No API tokens needed!

1. Go to your PyPI account settings
2. Navigate to "Publishing" → "Add a new publisher"
3. Fill in:
   - **PyPI Project Name**: `bimotype-ternary`
   - **Owner**: `jakobmina`
   - **Repository name**: `bimotype-ternary`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

4. Repeat for TestPyPI (use environment name `testpypi`)

### 3. GitHub Repository Setup

1. Go to your GitHub repository settings
2. Navigate to "Environments"
3. Create two environments:
   - `pypi` (for production releases)
   - `testpypi` (for testing)

## Publishing Methods

### Method 1: Automatic (Recommended)

**On Release Creation:**

```bash
# 1. Update version in pyproject.toml
# 2. Commit and push changes
git add pyproject.toml
git commit -m "Bump version to 1.1.0"
git push

# 3. Create a new release on GitHub
# Go to: https://github.com/yourusername/bimotype-ternary/releases/new
# - Tag: v1.1.0
# - Title: Release 1.1.0
# - Description: What's new in this release
# - Click "Publish release"

# GitHub Actions will automatically:
# - Build the package
# - Run tests
# - Publish to PyPI
```

### Method 2: Manual Trigger

**Test on TestPyPI first:**

```bash
# 1. Go to Actions tab on GitHub
# 2. Select "Publish to PyPI" workflow
# 3. Click "Run workflow"
# 4. This will publish to TestPyPI

# 5. Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ bimotype-ternary
```

### Method 3: Local Publishing (Fallback)

**If GitHub Actions fails:**

```bash
# 1. Install build tools
pip install build twine

# 2. Build the package
python -m build

# 3. Check the distribution
twine check dist/*

# 4. Upload to TestPyPI (test first!)
twine upload --repository testpypi dist/*

# 5. Test installation
pip install --index-url https://test.pypi.org/simple/ bimotype-ternary

# 6. Upload to PyPI (production)
twine upload dist/*
```

## Version Bumping

Update version in `pyproject.toml`:

```toml
[project]
name = "bimotype-ternary"
version = "1.1.0"  # Update this
```

**Semantic Versioning:**

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

## Pre-Release Checklist

- [ ] All tests passing (`pytest -v`)
- [ ] Version bumped in `pyproject.toml`
- [ ] CHANGELOG.md updated
- [ ] README.md up to date
- [ ] Documentation reviewed
- [ ] Clean build directory (`rm -rf dist/ build/ *.egg-info`)

## Troubleshooting

### "Project already exists"

If the project name is taken on PyPI, update in `pyproject.toml`:

```toml
[project]
name = "bimotype-ternary-quantum"  # Add suffix
```

### "Invalid credentials"

For trusted publishing:

1. Verify environment names match in GitHub and PyPI
2. Check workflow name is exactly `publish.yml`
3. Ensure repository name matches

For API tokens:

1. Generate new token on PyPI
2. Add to GitHub Secrets as `PYPI_API_TOKEN`
3. Update workflow to use token authentication

### "Build failed"

```bash
# Clean and rebuild locally
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
```

## Security Best Practices

1. ✅ **Use Trusted Publishing** (no tokens to manage)
2. ✅ **Enable 2FA** on PyPI account
3. ✅ **Use environment protection** in GitHub
4. ✅ **Review changes** before publishing
5. ✅ **Test on TestPyPI** first
6. ❌ **Never commit** API tokens to git

## Monitoring

After publishing:

1. Check PyPI page: <https://pypi.org/project/bimotype-ternary/>
2. Test installation: `pip install bimotype-ternary`
3. Verify all extras work:

   ```bash
   pip install bimotype-ternary[crypto]
   pip install bimotype-ternary[all]
   ```

## Resources

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [GitHub Actions for PyPI](https://github.com/marketplace/actions/pypi-publish)
