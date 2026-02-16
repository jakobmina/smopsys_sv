# Installation Guide

## From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/bimotype-ternary.git
cd bimotype-ternary

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or install with PSimon support
pip install -e ".[psimon]"

# Or install everything
pip install -e ".[all]"
```

## From PyPI (When Published)

```bash
# Basic installation
pip install bimotype-ternary

# With development tools
pip install bimotype-ternary[dev]

# With PSimon integration
pip install bimotype-ternary[psimon]

# Full installation
pip install bimotype-ternary[all]
```

## Building from Source

```bash
# Install build dependencies
pip install build

# Build the package
python -m build

# This creates:
# - dist/bimotype_ternary-1.0.0.tar.gz
# - dist/bimotype_ternary-1.0.0-py3-none-any.whl
```

## Verification

```bash
# Test the installation
python -c "from bimotype_ternary import TernaryBiMoTypeEncoder; print('✓ Installation successful')"

# Run the demo
bimotype-demo

# Or run tests
pytest bimotype_ternary/tests/ -v
```

## Requirements

- Python >= 3.8
- NumPy >= 1.20.0

### Optional Dependencies

- **Development**: pytest, pytest-cov, black, ruff
- **PSimon Integration**: psimon-h7 >= 2.0.0

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the correct directory:

```bash
# If installed in editable mode, you can import from anywhere
cd ~
python -c "from bimotype_ternary import TernaryBiMoTypeEncoder"

# If running from source without installation
cd /path/to/bimotype-ternary
python -c "import sys; sys.path.insert(0, '.'); from bimotype_ternary import TernaryBiMoTypeEncoder"
```

### PSimon Not Found

The PSimon library is optional. If not installed, the framework will use a stub implementation:

```
[WARNING] PSimon library not found. Install with: pip install psimon-h7
[INFO] Using stub implementation for demonstration
```

To install PSimon:

```bash
pip install psimon-h7
```
