---
title: "3.2. Generators, Decorators and Context Managers"
description: "These three features represent some of Python's most powerful and \"Pythonic\" constructs. They allow you to write cleaner, more efficient, and more maintainable code by managing state,…"
excerpt: "These three features represent some of Python's most powerful and \"Pythonic\" constructs. They allow you to write cleaner, more efficient, and more maintainable code by managing state,…"
custom_url: generators-decorators-and-context-managers
template: docs
section: "Chapter 3 · Advanced Python"
order: 150
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: advanced
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /blog/advanced-data-structures-and-algorithms/
next: /blog/concurrency-and-parallelism/
tags: [python, course]
---
## Overview

These three features represent some of Python's most powerful and "Pythonic" constructs. They allow you to write cleaner, more efficient, and more maintainable code by managing state, resources, and behaviors with minimal boilerplate. Mastering these tools will elevate your Python code from functional to elegant and professional.

## Generators & Iterators

### Understanding Iterators

Before diving into generators, let's understand what an iterator is. An iterator is an object that implements the iterator protocol, which consists of the `__iter__()` and `__next__()` methods. When you use a `for` loop, Python automatically calls these methods behind the scenes.

```python
# Example: Manual iteration
my_list = [1, 2, 3, 4, 5]
iterator = iter(my_list)

print(next(iterator))  # Output: 1
print(next(iterator))  # Output: 2
print(next(iterator))  # Output: 3
```

### Introduction to Generators

Generators are a special type of iterator that are defined using functions with the `yield` keyword instead of `return`. They're incredibly memory-efficient because they generate values on-demand rather than storing them all in memory at once.

```text
def simple_generator():
    yield 1
    yield 2
    yield 3

# Using the generator
gen = simple_generator()
for value in gen:
    print(value)
# Output: 1, 2, 3
```

### Why Generators Matter

Consider the difference between these two approaches:

```text
# Memory-intensive approach
def get_squares_list(n):
    return [x**2 for x in range(n)]

# Memory-efficient approach
def get_squares_generator(n):
    for x in range(n):
        yield x**2

# With a large number, the list approach uses massive memory
large_squares_list = get_squares_list(1000000)  # Uses ~8MB of memory

# The generator approach uses minimal memory
large_squares_gen = get_squares_generator(1000000)  # Uses ~96 bytes
```

### Practical Generator Examples

Here's a more practical example - reading large files:

```python
def read_large_file(file_path):
    """Generator that reads a file line by line without loading it entirely into memory"""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Usage
for line in read_large_file('huge_data.txt'):
    process_line(line)  # Process each line individually
```

Another useful pattern is the infinite sequence generator:

```python
def fibonacci():
    """Infinite Fibonacci sequence generator"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Usage
fib = fibonacci()
first_10_fibs = [next(fib) for _ in range(10)]
print(first_10_fibs)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## Generator Expressions & Comprehensions

Generator expressions provide a concise way to create generators, similar to list comprehensions but with parentheses instead of square brackets:

```python
# List comprehension (creates entire list in memory)
squares_list = [x**2 for x in range(10)]

# Generator expression (creates generator object)
squares_gen = (x**2 for x in range(10))

print(type(squares_list))  # <class 'list'>
print(type(squares_gen))   # <class 'generator'>
```

### Practical Generator Expression Examples

```python
# Processing large datasets efficiently
def process_large_dataset(data_source):
    # Filter and transform data without loading everything into memory
    filtered_data = (
        transform(item)
        for item in data_source
        if is_valid(item)
    )
    return filtered_data

# Chaining generator expressions
numbers = range(1000000)
even_squares = (x**2 for x in numbers if x % 2 == 0)
large_even_squares = (x for x in even_squares if x > 1000)

# Only compute values as needed
for value in large_even_squares:
    if value > 10000:
        break
    print(value)
```

## Decorators

Decorators are a powerful feature that allows you to modify or enhance functions without changing their code. They're essentially functions that take another function as an argument and return a modified version of that function.

### Basic Decorator Syntax

```javascript
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# This is equivalent to:
# say_hello = my_decorator(say_hello)

say_hello()
# Output:
# Something is happening before the function is called.
# Hello!
# Something is happening after the function is called.
```

### Decorators with Arguments

To handle functions with arguments, use `*args` and `**kwargs`:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

result = add(3, 5)
# Output:
# Calling add with args: (3, 5), kwargs: {}
# add returned: 8
```

### Practical Decorator Examples

#### Timing Decorator

```javascript
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return "Done!"

slow_function()  # Output: slow_function took 1.0041 seconds
```

#### Caching Decorator

```text
from functools import wraps

def cache_decorator(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from arguments
        key = str(args) + str(sorted(kwargs.items()))

        if key in cache:
            print(f"Cache hit for {func.__name__}")
            return cache[key]

        print(f"Cache miss for {func.__name__}")
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper

@cache_decorator
def expensive_calculation(n):
    time.sleep(1)  # Simulate expensive operation
    return n ** 2

print(expensive_calculation(5))  # Cache miss, takes 1 second
print(expensive_calculation(5))  # Cache hit, instant
```

#### Authentication Decorator

```python
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In a real app, this would check session, JWT, etc.
        user_authenticated = check_user_auth()

        if not user_authenticated:
            raise PermissionError("Authentication required")

        return func(*args, **kwargs)
    return wrapper

@require_auth
def sensitive_operation():
    return "Sensitive data accessed"
```

## Chaining Decorators

You can apply multiple decorators to a single function. They're applied from bottom to top:

```python
def bold(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<b>{result}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<i>{result}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))  # Output: <b><i>Hello, World!</i></b>

# This is equivalent to:
# greet = bold(italic(greet))
```

### Practical Decorator Chaining

```javascript
@timing_decorator
@cache_decorator
@require_auth
def complex_calculation(data):
    # Some expensive authenticated operation
    return sum(x**2 for x in data)

# This function is now:
# - Protected by authentication
# - Cached for performance
# - Timed for monitoring
```

## Context Managers & the `with` Statement

Context managers provide a clean way to manage resources like files, network connections, or locks. They ensure that setup and cleanup code is executed properly, even if an error occurs.

### Basic Context Manager Usage

```python
# Without context manager (prone to errors)
file = open('data.txt', 'r')
data = file.read()
file.close()  # What if an error occurs before this line?

# With context manager (guaranteed cleanup)
with open('data.txt', 'r') as file:
    data = file.read()
# File is automatically closed here, even if an error occurs
```

### Multiple Context Managers

```python
# Managing multiple resources
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    data = infile.read()
    processed_data = process(data)
    outfile.write(processed_data)
# Both files are automatically closed
```

### Context Managers for Non-File Resources

```python
import threading

# Thread lock context manager
lock = threading.Lock()

with lock:
    # Critical section - only one thread can execute this
    shared_resource += 1
# Lock is automatically released
```

## Writing Custom Context Managers

### Class-Based Context Managers

To create a context manager using a class, implement `__enter__` and `__exit__` methods:

```sql
class DatabaseConnection:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = None

    def __enter__(self):
        print(f"Connecting to {self.database_url}")
        self.connection = connect_to_database(self.database_url)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            if exc_type is not None:
                print(f"Error occurred: {exc_value}")
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
            print("Database connection closed")
        return False  # Don't suppress exceptions

# Usage
with DatabaseConnection("postgresql://localhost/mydb") as db:
    db.execute("INSERT INTO users (name) VALUES ('John')")
    # Connection is automatically managed
```

### Function-Based Context Managers with `contextlib`

The `contextlib` module provides a simpler way to create context managers:

```python
from contextlib import contextmanager
import os

@contextmanager
def change_directory(path):
    old_path = os.getcwd()
    try:
        os.chdir(path)
        yield path  # This is what gets returned by 'as'
    finally:
        os.chdir(old_path)

# Usage
with change_directory('/tmp'):
    print(os.getcwd())  # /tmp
    # Do work in /tmp
print(os.getcwd())  # Back to original directory
```

### Advanced Context Manager Example

Here's a more sophisticated example that manages a temporary environment:

```python
from contextlib import contextmanager
import os
import tempfile
import shutil

@contextmanager
def temporary_environment(env_vars=None):
    """Context manager that creates a temporary directory and sets environment variables"""
    # Setup
    temp_dir = tempfile.mkdtemp()
    old_env = os.environ.copy()
    old_cwd = os.getcwd()

    try:
        # Set new environment variables
        if env_vars:
            os.environ.update(env_vars)

        # Change to temp directory
        os.chdir(temp_dir)

        yield temp_dir

    finally:
        # Cleanup
        os.chdir(old_cwd)
        os.environ.clear()
        os.environ.update(old_env)
        shutil.rmtree(temp_dir)

# Usage
with temporary_environment({'DEBUG': 'True', 'ENV': 'test'}) as temp_path:
    print(f"Working in: {temp_path}")
    print(f"DEBUG env var: {os.environ.get('DEBUG')}")
    # Create temporary files, run tests, etc.
# Everything is cleaned up automatically
```

## Putting It All Together

Here's a comprehensive example that combines generators, decorators, and context managers:

```javascript
from contextlib import contextmanager
from functools import wraps
import time
import logging

# Decorator for logging function calls
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} completed")
        return result
    return wrapper

# Context manager for timing operations
@contextmanager
def timing_context(operation_name):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        logging.info(f"{operation_name} took {end_time - start_time:.4f} seconds")

# Generator for processing large datasets
@log_calls
def process_large_dataset(data_source):
    """Generator that processes data in chunks"""
    for chunk in data_source:
        with timing_context(f"Processing chunk of size {len(chunk)}"):
            # Process each item in the chunk
            for item in chunk:
                if validate_item(item):
                    yield transform_item(item)

# Usage
def main():
    large_dataset = get_data_chunks()  # Returns chunks of data

    with timing_context("Full dataset processing"):
        processed_items = process_large_dataset(large_dataset)

        # Only process items as needed (lazy evaluation)
        for item in processed_items:
            if item.priority > 5:
                handle_high_priority_item(item)
```

## Best Practices and Tips

  1. **Use`functools.wraps`** in decorators to preserve original function metadata
  2. **Generators are memory-efficient** \- use them for large datasets or infinite sequences
  3. **Context managers ensure cleanup** \- always use them for resource management
  4. **Chain decorators thoughtfully** \- consider the order of application
  5. **Generator expressions are powerful** \- use them for data processing pipelines
  6. **Custom context managers** should handle exceptions gracefully
  7. **Document your decorators** \- make it clear what they do and any side effects

These advanced Python features will help you write more professional, efficient, and maintainable code. They're the hallmarks of experienced Python developers and are essential for building robust applications.

Now, you're ready to learn about [concurrency and parallelism](<https://python.robertdevore.com/blog/concurrency-and-parallelism>)!
