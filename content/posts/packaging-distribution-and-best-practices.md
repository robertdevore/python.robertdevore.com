---
title: "3.5. Packaging, Distribution, and Best Practices"
description: "Package, test, document, and publish reusable Python projects with pyproject.toml, build tools, PyPI, CI, linting, and type checks."
excerpt: "Package, test, document, and publish reusable Python projects with pyproject.toml, build tools, PyPI, CI, linting, and type checks."
custom_url: packaging-distribution-and-best-practices
template: docs
section: "Chapter 3 · Advanced Python"
order: 180
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: advanced
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /course/building-and-consuming-apis/
next: /course/course-conclusion-from-python-novice-to-professional-developer/
tags: [python, course]
---
## Overview:

Transform your Python scripts into professional, reusable packages that others can install with `pip`. Learn industry-standard practices for code organization, documentation, testing, and distribution that will make your projects maintainable, scalable, and production-ready.

* * *

## **Project Structure: Building for Scale**

A well-organized project structure is the foundation of maintainable Python code. Here's the recommended structure for a Python package:

```text
my_awesome_package/
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.py (optional, for backwards compatibility)
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── conf.py
│   └── index.rst
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── src/
│   └── my_awesome_package/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── cli.py
└── examples/
    └── basic_usage.py
```

**Key principles:**

  * **Use`src/` layout**: Prevents accidental imports during development and testing
  * **Separate concerns** : Keep source code, tests, docs, and examples in distinct directories
  * **Include metadata files** : README, LICENSE, and configuration files at the root
  * **Version control integration** : Include `.gitignore` and CI/CD configurations

## **Modern Package Configuration with pyproject.toml**

The `pyproject.toml` file is the modern standard for Python project configuration, replacing the older `setup.py` approach:

```toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-awesome-package"
version = "1.0.0"
description = "A comprehensive utility package for data processing"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
keywords = ["data", "processing", "utilities"]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "pandas>=1.5.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
    "mypy>=0.991",
    "pre-commit>=2.20.0",
]
docs = [
    "sphinx>=5.0.0",
    "sphinx-rtd-theme>=1.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/my-awesome-package"
Documentation = "https://my-awesome-package.readthedocs.io/"
Repository = "https://github.com/yourusername/my-awesome-package.git"
"Bug Tracker" = "https://github.com/yourusername/my-awesome-package/issues"

[project.scripts]
my-tool = "my_awesome_package.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

## **Writing Effective Documentation**

### **README.md: Your Package's Front Door**

A compelling README should include:

```python
# My Awesome Package

[![PyPI version](https://badge.fury.io/py/my-awesome-package.svg)](https://badge.fury.io/py/my-awesome-package)
[![Python Support](https://img.shields.io/pypi/pyversions/my-awesome-package.svg)](https://pypi.org/project/my-awesome-package/)
[![Tests](https://github.com/yourusername/my-awesome-package/workflows/Tests/badge.svg)](https://github.com/yourusername/my-awesome-package/actions)

A comprehensive utility package for data processing with a clean, intuitive API.

## Features

- ✨ Fast data processing with pandas backend
- 🔧 Command-line interface for batch operations
- 📊 Built-in visualization tools
- 🚀 Async support for large datasets

## Quick Start

```python

from my_awesome_package import DataProcessor

processor = DataProcessor()
result = processor.clean_data("data.csv")
print(f"Processed {len(result)} records")

```
## Installation


```bash

pip install my-awesome-package

```
For development features:


```bash

pip install my-awesome-package[dev]

```
## Documentation

Full documentation is available at [my-awesome-package.readthedocs.io](<https://my-awesome-package.readthedocs.io/>).

## Contributing

We welcome contributions! Please see our [Contributing Guide](<CONTRIBUTING.md>) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](<LICENSE>) file for details.


```python

### **API Documentation with Docstrings**

Use comprehensive docstrings following the Google or NumPy style:

```python
def process_data(data: pd.DataFrame,
                 method: str = "standard",
                 **kwargs) -> pd.DataFrame:
    """Process DataFrame using specified method.

    Args:
        data: Input DataFrame to process
        method: Processing method ('standard', 'advanced', 'custom')
        **kwargs: Additional arguments passed to processing method

    Returns:
        Processed DataFrame with cleaned data

    Raises:
        ValueError: If method is not supported
        ProcessingError: If data processing fails

    Example:
        >>> import pandas as pd
        >>> from my_awesome_package import process_data
        >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        >>> result = process_data(df, method='standard')
        >>> print(result.shape)
        (3, 2)
    """
```

## **Semantic Versioning: Communicating Changes**

Follow [Semantic Versioning](<https://semver.org/>) (SemVer) with the format `MAJOR.MINOR.PATCH`:

  * **MAJOR** : Breaking changes that require user code modifications
  * **MINOR** : New features that are backwards compatible
  * **PATCH** : Bug fixes and minor improvements

```python
# src/my_awesome_package/__init__.py
__version__ = "1.2.3"

# Automated version management with setuptools_scm
from importlib.metadata import version
__version__ = version("my_awesome_package")
```

For automated versioning based on git tags:

```python
[tool.setuptools_scm]
write_to = "src/my_awesome_package/_version.py"
```

## **Building and Publishing to PyPI**

### **Building Your Package**

```python
# Install build tools
pip install build twine

# Build the package
python -m build

# This creates:
# dist/my_awesome_package-1.0.0-py3-none-any.whl
# dist/my_awesome_package-1.0.0.tar.gz
```

### **Publishing Process**

  1. **Test on TestPyPI first:**

```python
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ my-awesome-package
```

  2. **Publish to PyPI:**

```python
# Upload to PyPI
python -m twine upload dist/*
```

  3. **Automate with GitHub Actions:**

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## **Code Quality and Style**

### **Formatting with Black**

Black provides opinionated, consistent code formatting:

```python
# Install black
pip install black

# Format all Python files
black src/ tests/

# Check without modifying
black --check src/ tests/
```

### **Linting with Flake8**

```python
# Install flake8 with plugins
pip install flake8 flake8-docstrings flake8-import-order

# Create .flake8 configuration
echo "[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,docs/,build/,dist/" > .flake8

# Run linting
flake8 src/ tests/
```

### **Pre-commit Hooks**

Automate code quality checks:

```python
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
```

Install and activate:

```bash
pip install pre-commit
pre-commit install
```

## **Type Checking with MyPy**

Add type hints and static analysis:

```python
from typing import List, Optional, Union, Dict, Any
import pandas as pd

def analyze_data(
    data: pd.DataFrame,
    columns: List[str],
    method: str = "mean",
    options: Optional[Dict[str, Any]] = None
) -> Union[pd.Series, pd.DataFrame]:
    """Analyze specified columns using given method."""
    if options is None:
        options = {}

    if method == "mean":
        return data[columns].mean()
    elif method == "describe":
        return data[columns].describe()
    else:
        raise ValueError(f"Unknown method: {method}")
```

MyPy configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
```

## **Comprehensive Testing Strategy**

### **Test Structure and Organization**

```python
# tests/test_core.py
import pytest
import pandas as pd
from my_awesome_package.core import DataProcessor, ProcessingError

class TestDataProcessor:

    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'A': [1, 2, 3, None, 5],
            'B': ['a', 'b', 'c', 'd', 'e']
        })

    @pytest.fixture
    def processor(self):
        return DataProcessor()

    def test_basic_processing(self, processor, sample_data):
        result = processor.process(sample_data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4  # Null row removed

    def test_invalid_method_raises_error(self, processor, sample_data):
        with pytest.raises(ProcessingError, match="Unknown method"):
            processor.process(sample_data, method="invalid")

    @pytest.mark.parametrize("method,expected_cols", [
        ("standard", 2),
        ("advanced", 3),
    ])
    def test_different_methods(self, processor, sample_data, method, expected_cols):
        result = processor.process(sample_data, method=method)
        assert len(result.columns) == expected_cols
```

### **Test Configuration**

```python
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

## **Continuous Integration with GitHub Actions**

```yaml
# .github/workflows/ci.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Lint with flake8
      run: flake8 src/ tests/

    - name: Check formatting with black
      run: black --check src/ tests/

    - name: Type check with mypy
      run: mypy src/

    - name: Test with pytest
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## **Managing Updates and Deprecations**

### **Deprecation Warnings**

```python
import warnings
from typing import Any

def old_function(data: Any) -> Any:
    """Legacy function - use new_function instead."""
    warnings.warn(
        "old_function is deprecated and will be removed in v2.0.0. "
        "Use new_function instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function(data)
```

### **Changelog Management**

Maintain a `CHANGELOG.md` following [Keep a Changelog](<https://keepachangelog.com/>):

```python
# Changelog

## [Unreleased]
### Added
- New data validation features

## [1.2.0] - 2023-12-01
### Added
- Async processing support
- New CLI commands

### Changed
- Improved error messages
- Updated dependencies

### Deprecated
- `old_function()` will be removed in v2.0.0

### Fixed
- Memory leak in large dataset processing

## [1.1.0] - 2023-11-15
### Added
- Type hints for all public APIs
```

## **Best Practices Summary**

  1. **Follow PEP 8 and use automated formatters** for consistent code style
  2. **Write comprehensive tests** with good coverage (aim for >90%)
  3. **Use type hints** for better IDE support and error detection
  4. **Document your API** with clear docstrings and examples
  5. **Version semantically** and maintain a changelog
  6. **Automate quality checks** with pre-commit hooks and CI/CD
  7. **Structure projects consistently** using established patterns
  8. **Handle deprecations gracefully** with proper warnings and migration paths

By following these practices, your Python packages will be professional, maintainable, and ready for production use. Remember that great software is not just about functionality—it's about creating a positive experience for developers who use and contribute to your code.

YOU DID IT! Now let's go over the [course conclusion](<https://python.robertdevore.com/course/course-conclusion-from-python-novice-to-professional-developer>) to see what's next!
