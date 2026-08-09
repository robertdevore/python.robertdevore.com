---
title: "2.5. Introduction to Testing"
description: "Get started with writing and running tests so your code stays reliable, refactor-safe, and bug-free as it grows."
excerpt: "Get started with writing and running tests so your code stays reliable, refactor-safe, and bug-free as it grows."
custom_url: introduction-to-testing
template: docs
section: "Chapter 2 · Intermediate Python"
order: 120
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: intermediate
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /blog/exceptions-and-robust-error-handling/
next: /blog/chapter-3-advanced-python/
tags: [python, course]
---
## Overview

Get started with writing and running tests so your code stays reliable, refactor-safe, and bug-free as it grows.

* * *

## **Why Testing Matters**

Imagine you've built a calculator app that works perfectly. A few weeks later, you add a new feature—maybe currency conversion—and suddenly your basic addition function starts giving wrong results. Without tests, you might not discover this until an angry user reports it. With tests, you'd catch the problem immediately.

**Testing is insurance for your code.** It ensures that:

  * Your functions work as expected
  * Changes don't break existing functionality
  * Edge cases are handled properly
  * Your code is reliable enough for others to use

As projects grow larger and more complex, manual testing becomes impractical. Automated tests run in seconds and give you confidence that your code works correctly, even after major changes.

* * *

## **Types of Tests**

Before diving into code, let's understand the different types of tests you'll encounter:

### **Unit Tests**

These test individual functions or methods in isolation. They're fast, focused, and make up the majority of your test suite.

```javascript
def add(a, b):
    return a + b

# Unit test for the add function
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### **Integration Tests**

These test how different parts of your system work together. For example, testing that your database layer works correctly with your business logic.

```python
def test_user_registration_flow():
    # Test that user creation, database storage, and email sending work together
    user = create_user("john@example.com", "password123")
    assert user.id is not None
    assert database.find_user(user.id) == user
    assert email_service.was_welcome_email_sent(user.email)
```

### **Functional Tests**

These test complete features from the user's perspective, often called "end-to-end" tests.

```python
def test_calculator_workflow():
    # Test the entire calculator application workflow
    calculator = Calculator()
    calculator.input("2")
    calculator.input("+")
    calculator.input("3")
    result = calculator.calculate()
    assert result == "5"
```

For now, we'll focus primarily on **unit tests** since they're the foundation of good testing practices.

* * *

## **Your First Test with unittest**

Python comes with a built-in testing framework called `unittest`. Let's start with a simple example.

Create a file called `calculator.py`:

```python
# calculator.py
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide a by b and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Now create a test file called `test_calculator.py`:

```javascript
# test_calculator.py
import unittest
from calculator import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):

    def test_add(self):
        """Test the add function with various inputs."""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(-5, -3), -8)

    def test_subtract(self):
        """Test the subtract function."""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 1), -1)
        self.assertEqual(subtract(-2, -1), -1)

    def test_multiply(self):
        """Test the multiply function."""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 100), 0)

    def test_divide(self):
        """Test the divide function."""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(7, 2), 3.5)
        self.assertEqual(divide(-6, 3), -2)

    def test_divide_by_zero(self):
        """Test that dividing by zero raises an exception."""
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
```

Run the tests from your terminal:

```python
python test_calculator.py
```

You should see output like:

```python
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

Each dot represents a passing test. If a test fails, you'll see details about what went wrong.

* * *

## **Introduction to pytest**

While `unittest` is built into Python, many developers prefer `pytest` because it's more concise and powerful. Let's rewrite our tests using pytest.

First, install pytest:

```bash
pip install pytest
```

Create a new file called `test_calculator_pytest.py`:

```javascript
# test_calculator_pytest.py
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    """Test the add function with various inputs."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-5, -3) == -8

def test_subtract():
    """Test the subtract function."""
    assert subtract(5, 3) == 2
    assert subtract(0, 1) == -1
    assert subtract(-2, -1) == -1

def test_multiply():
    """Test the multiply function."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0

def test_divide():
    """Test the divide function."""
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(-6, 3) == -2

def test_divide_by_zero():
    """Test that dividing by zero raises an exception."""
    with pytest.raises(ValueError):
        divide(10, 0)
```

Run the pytest tests:

```bash
pytest test_calculator_pytest.py
```

Notice how pytest is more concise—no need to inherit from a test class or call `unittest.main()`. Just write functions that start with `test_` and use simple `assert` statements.

* * *

## **Test Discovery and Running Tests**

Both `unittest` and `pytest` can automatically discover and run your tests.

### **unittest Discovery**

```python
# Run all tests in the current directory
python -m unittest discover

# Run tests in a specific directory
python -m unittest discover tests/

# Run a specific test file
python -m unittest test_calculator

# Run a specific test class
python -m unittest test_calculator.TestCalculator

# Run a specific test method
python -m unittest test_calculator.TestCalculator.test_add
```

### **pytest Discovery**

```python
# Run all tests (pytest automatically finds test files)
pytest

# Run tests in a specific directory
pytest tests/

# Run a specific test file
pytest test_calculator_pytest.py

# Run tests matching a pattern
pytest -k "add"

# Run with verbose output
pytest -v

# Run and show test coverage
pytest --cov=calculator
```

### **Test File Naming Conventions**

For automatic discovery to work, follow these naming conventions:

  * Test files should start with `test_` or end with `_test.py`
  * Test functions should start with `test_`
  * Test classes should start with `Test` (for unittest)

* * *

## **Understanding Assertions**

Assertions are the heart of testing—they check if your code produces the expected results.

### **unittest Assertions**

```python
import unittest

class TestAssertions(unittest.TestCase):

    def test_equality_assertions(self):
        self.assertEqual(2 + 2, 4)           # Check equality
        self.assertNotEqual(2 + 2, 5)       # Check inequality
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)  # Floating point comparison

    def test_boolean_assertions(self):
        self.assertTrue(5 > 3)               # Check if True
        self.assertFalse(5 < 3)              # Check if False

    def test_membership_assertions(self):
        self.assertIn('hello', 'hello world')        # Check membership
        self.assertNotIn('goodbye', 'hello world')   # Check non-membership

    def test_exception_assertions(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

        with self.assertRaises(ValueError) as context:
            int('not a number')
        self.assertIn('invalid literal', str(context.exception))

    def test_none_assertions(self):
        self.assertIsNone(None)              # Check if None
        self.assertIsNotNone('hello')        # Check if not None

    def test_type_assertions(self):
        self.assertIsInstance('hello', str)   # Check type
        self.assertNotIsInstance('hello', int)
```

### **pytest Assertions**

```python
import pytest

def test_equality_assertions():
    assert 2 + 2 == 4
    assert 2 + 2 != 5
    assert abs(0.1 + 0.2 - 0.3) < 1e-10  # Floating point comparison

def test_boolean_assertions():
    assert 5 > 3
    assert not (5 < 3)

def test_membership_assertions():
    assert 'hello' in 'hello world'
    assert 'goodbye' not in 'hello world'

def test_exception_assertions():
    with pytest.raises(ZeroDivisionError):
        1 / 0

    with pytest.raises(ValueError, match='invalid literal'):
        int('not a number')

def test_none_assertions():
    assert None is None
    assert 'hello' is not None

def test_type_assertions():
    assert isinstance('hello', str)
    assert not isinstance('hello', int)
```

* * *

## **Practical Testing Example: User Class**

Let's test a more realistic example. Create a `user.py` file:

```python
# user.py
class User:
    def __init__(self, username, email, age=None):
        if not username:
            raise ValueError("Username cannot be empty")
        if '@' not in email:
            raise ValueError("Invalid email format")
        if age is not None and age < 0:
            raise ValueError("Age cannot be negative")

        self.username = username
        self.email = email
        self.age = age
        self.is_active = True

    def get_display_name(self):
        if self.age:
            return f"{self.username} ({self.age})"
        return self.username

    def deactivate(self):
        self.is_active = False

    def is_adult(self):
        if self.age is None:
            return None
        return self.age >= 18
```

Now let's write comprehensive tests using pytest:

```python
# test_user.py
import pytest
from user import User

class TestUser:

    def test_user_creation_valid(self):
        """Test creating a user with valid data."""
        user = User("john_doe", "john@example.com", 25)
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.age == 25
        assert user.is_active is True

    def test_user_creation_without_age(self):
        """Test creating a user without specifying age."""
        user = User("jane", "jane@example.com")
        assert user.username == "jane"
        assert user.email == "jane@example.com"
        assert user.age is None

    def test_user_creation_invalid_username(self):
        """Test that empty username raises ValueError."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User("", "test@example.com")

    def test_user_creation_invalid_email(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            User("testuser", "invalid-email")

    def test_user_creation_negative_age(self):
        """Test that negative age raises ValueError."""
        with pytest.raises(ValueError, match="Age cannot be negative"):
            User("testuser", "test@example.com", -5)

    def test_get_display_name_with_age(self):
        """Test display name when age is provided."""
        user = User("alice", "alice@example.com", 30)
        assert user.get_display_name() == "alice (30)"

    def test_get_display_name_without_age(self):
        """Test display name when age is not provided."""
        user = User("bob", "bob@example.com")
        assert user.get_display_name() == "bob"

    def test_deactivate_user(self):
        """Test user deactivation."""
        user = User("charlie", "charlie@example.com")
        assert user.is_active is True
        user.deactivate()
        assert user.is_active is False

    def test_is_adult_with_adult_age(self):
        """Test is_adult returns True for adults."""
        user = User("adult", "adult@example.com", 21)
        assert user.is_adult() is True

    def test_is_adult_with_minor_age(self):
        """Test is_adult returns False for minors."""
        user = User("minor", "minor@example.com", 16)
        assert user.is_adult() is False

    def test_is_adult_with_no_age(self):
        """Test is_adult returns None when age is not set."""
        user = User("unknown", "unknown@example.com")
        assert user.is_adult() is None
```

Run these tests:

```bash
pytest test_user.py -v
```

* * *

## **Testing Best Practices**

### **1\. Follow the AAA Pattern**

Structure your tests with **Arrange, Act, Assert** :

```python
def test_user_display_name():
    # Arrange - Set up test data
    user = User("testuser", "test@example.com", 25)

    # Act - Execute the code being tested
    display_name = user.get_display_name()

    # Assert - Check the result
    assert display_name == "testuser (25)"
```

### **2\. Write Descriptive Test Names**

Good test names explain what is being tested and what the expected outcome is:

```python
# Bad
def test_divide():
    pass

# Good
def test_divide_returns_correct_result_for_positive_numbers():
    pass

def test_divide_raises_error_when_dividing_by_zero():
    pass
```

### **3\. Test Edge Cases**

Don't just test the happy path. Test boundary conditions and edge cases:

```python
def test_age_validation():
    # Test boundary values
    User("test", "test@example.com", 0)    # Minimum valid age
    User("test", "test@example.com", 150)  # Very high but valid age

    # Test invalid cases
    with pytest.raises(ValueError):
        User("test", "test@example.com", -1)  # Just below minimum
```

### **4\. Keep Tests Independent**

Each test should be able to run independently of others:

```python
# Bad - tests depend on each other
class TestBadUserTests:
    def test_create_user(self):
        self.user = User("test", "test@example.com")

    def test_deactivate_user(self):
        self.user.deactivate()  # Depends on previous test
        assert not self.user.is_active

# Good - each test is independent
class TestGoodUserTests:
    def test_create_user(self):
        user = User("test", "test@example.com")
        assert user.is_active

    def test_deactivate_user(self):
        user = User("test", "test@example.com")
        user.deactivate()
        assert not user.is_active
```

### **5\. Use Fixtures for Setup**

When you need the same setup for multiple tests, use fixtures (pytest) or setUp methods (unittest):

```python
# pytest fixtures
@pytest.fixture
def sample_user():
    return User("testuser", "test@example.com", 25)

def test_display_name(sample_user):
    assert sample_user.get_display_name() == "testuser (25)"

def test_is_adult(sample_user):
    assert sample_user.is_adult() is True
```

### **6\. Write Fast Tests**

Keep unit tests fast by avoiding:

  * File I/O operations
  * Network calls
  * Database operations
  * Sleep statements

If you need these, consider using mocks or moving to integration tests.

* * *

## **Running Tests Automatically**

Set up your tests to run automatically during development:

### **Using pytest-watch**

```bash
pip install pytest-watch
ptw  # Runs tests automatically when files change
```

### **Pre-commit Hooks**

Install `pre-commit` to run tests before each commit:

```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: python
        types: [python]
        pass_filenames: false
        always_run: true
```

* * *

## **Next Steps**

Now that you understand testing basics:

  1. **Practice writing tests** for your existing code
  2. **Try Test-Driven Development (TDD)** \- write tests before implementing features
  3. **Learn about mocking** for testing code with external dependencies
  4. **Explore test coverage tools** like `pytest-cov` to ensure you're testing enough
  5. **Set up continuous integration** to run tests automatically on code changes

Testing might seem like extra work initially, but it saves enormous time in the long run. As your projects grow, you'll appreciate having a safety net that catches bugs before they reach users.

Remember: **good tests are like good documentation** —they explain how your code should behave and give you confidence to make changes without fear of breaking things.

* * *

**Key Takeaways:**

  * Tests prevent bugs and make refactoring safe
  * Start with unit tests using `unittest` or `pytest`
  * Write descriptive test names and test edge cases
  * Keep tests fast, independent, and well-organized
  * Make testing part of your regular development workflow

With these fundamentals, you're ready to write reliable, maintainable Python code that you and others can trust.

Next up - [Chapter 3: Advanced Python](<https://python.robertdevore.com/blog/chapter-3-advanced-python>).
