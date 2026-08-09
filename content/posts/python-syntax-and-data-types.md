---
title: "1.2. Syntax & Data Types"
description: "Master Python's basic building blocks—variables, data types, and simple operations—so you can start manipulating data with confidence."
excerpt: "Master Python's basic building blocks—variables, data types, and simple operations—so you can start manipulating data with confidence."
custom_url: python-syntax-and-data-types
template: docs
section: "Chapter 1 · Beginner Python"
order: 35
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: beginner
status: stable
version: complete course
prerequisites:
  - "Complete 1.1. Python Setup & IDEs"
previous: /blog/python-setup-and-ides/
next: /blog/syntax-and-data-types/
tags: [python, course, syntax, data-types]
---
## Overview

Master Python's basic building blocks—variables, data types, and simple operations—so you can start manipulating data with confidence. Python's beauty lies in its simplicity and readability. In this section, you'll learn how Python represents information, how to give that information useful names, and how to combine values into expressions.

By the end of this lesson, you will be able to:

- Read and write basic Python statements
- Store values in clearly named variables
- Work with strings, integers, floating-point numbers, booleans, and `None`
- Inspect and convert between common data types
- Use arithmetic, comparison, and logical operators
- Format readable output with f-strings

## Python syntax at a glance

Python uses whitespace and indentation to communicate structure. A simple statement usually occupies one line:

```python
course_name = "Complete Python Development Course"
lesson_number = 2
print(course_name, lesson_number)
```

Names are case-sensitive, so `lesson`, `Lesson`, and `LESSON` are three different variables. Choose descriptive lowercase names, separate words with underscores, and avoid Python keywords such as `class`, `for`, and `if`.

Comments begin with `#` and explain intent to future readers:

```python
# Prices are stored in US dollars.
monthly_price = 19.99
```

Good comments clarify why code exists. The code itself should make what it does easy to understand.

## Variables and assignment

A variable is a name that points to a value. Python creates the name when you assign a value with `=`:

```python
student_name = "Avery"
completed_lessons = 3
is_enrolled = True
```

Python is dynamically typed. You do not declare a variable's type before using it; Python determines the type from the assigned value. You can inspect that type with `type()`:

```python
print(type(student_name))       # <class 'str'>
print(type(completed_lessons))  # <class 'int'>
print(type(is_enrolled))        # <class 'bool'>
```

Reassignment gives an existing name a new value:

```python
completed_lessons = 3
completed_lessons = completed_lessons + 1
completed_lessons += 1
print(completed_lessons)  # 5
```

Constants are conventionally written in uppercase. Python does not prevent you from changing them, but the style signals that the value should remain stable:

```python
LESSONS_PER_CHAPTER = 5
```

## Core data types

### Integers and floating-point numbers

An `int` stores a whole number, while a `float` stores a number with a decimal component:

```python
lesson_count = 20      # int
completion = 82.5     # float
```

Python supports the arithmetic operators you would expect:

```python
print(10 + 3)   # addition: 13
print(10 - 3)   # subtraction: 7
print(10 * 3)   # multiplication: 30
print(10 / 3)   # division: 3.333...
print(10 // 3)  # floor division: 3
print(10 % 3)   # remainder: 1
print(10 ** 3)  # exponent: 1000
```

Parentheses make the intended order of operations explicit:

```python
average = (88 + 91 + 95) / 3
```

### Strings

A `str` stores text. Use matching single or double quotes:

```python
language = "Python"
message = 'Readable code matters.'
```

Strings can be combined, repeated, indexed, and sliced:

```python
full_message = language + ": " + message
banner = "=" * 20
first_letter = language[0]     # P
short_name = language[:3]      # Pyt
```

F-strings are the clearest way to insert values into text:

```python
name = "Avery"
lessons = 4
print(f"{name} has completed {lessons} lessons.")
```

Useful string methods return transformed values:

```python
raw_name = "  robert devore  "
clean_name = raw_name.strip().title()
print(clean_name)  # Robert Devore
```

Strings are immutable, which means their individual characters cannot be changed in place. Methods such as `.strip()` and `.title()` create new strings.

### Booleans

A `bool` is either `True` or `False`. Booleans often come from comparisons:

```python
score = 92
passed = score >= 70
perfect = score == 100
print(passed)   # True
print(perfect)  # False
```

Comparison operators include `==`, `!=`, `<`, `<=`, `>`, and `>=`. Combine conditions with `and`, `or`, and `not`:

```python
has_account = True
email_verified = False
can_continue = has_account and email_verified
needs_verification = has_account and not email_verified
```

### None

`None` represents the intentional absence of a value:

```python
middle_name = None

if middle_name is None:
    print("No middle name provided")
```

Use `is None` and `is not None` when checking for this special value.

## Type conversion

Programs often receive values as strings, especially from `input()`. Convert them before doing numeric work:

```python
age_text = "34"
age = int(age_text)
next_year = age + 1
print(next_year)  # 35
```

Common conversion functions include `int()`, `float()`, `str()`, and `bool()`:

```python
quantity = int("5")
price = float("12.50")
summary = str(quantity) + " items"
```

Invalid conversions raise an error. For example, `int("five")` cannot produce a number. Later lessons show how to handle that failure gracefully.

## Input and output

The `input()` function pauses the program and returns what the user typed as a string:

```python
name = input("What is your name? ")
year_text = input("What year were you born? ")
year = int(year_text)

print(f"Welcome, {name}! You entered {year}.")
```

Clear prompts and formatted output make even a small command-line program easier to use.

## A small practice program

Combine variables, conversion, arithmetic, and f-strings in a simple bill calculator:

```python
item_name = input("Item name: ")
unit_price = float(input("Unit price: "))
quantity = int(input("Quantity: "))
tax_rate = 0.06

subtotal = unit_price * quantity
tax = subtotal * tax_rate
total = subtotal + tax

print("\nOrder summary")
print("-" * 24)
print(f"Item: {item_name}")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax: ${tax:.2f}")
print(f"Total: ${total:.2f}")
```

The `:.2f` format specifier displays a floating-point number with two decimal places. Try changing the quantity, price, or tax rate and predict the result before you run the program.

## Common beginner mistakes

- Using `=` when you mean `==`. Assignment stores a value; equality compares two values.
- Mixing strings and numbers without conversion. `"5" + "2"` produces `"52"`, while `5 + 2` produces `7`.
- Misspelling a variable name or changing its capitalization.
- Forgetting that `input()` always returns a string.
- Naming a variable `str`, `list`, or `type`, which hides a useful built-in name.
- Assuming floating-point arithmetic is perfectly exact. Values such as `0.1 + 0.2` may contain tiny representation differences.

## Practice exercises

1. Create variables for your name, favorite number, and whether you have used Python before. Print one formatted sentence containing all three values.
2. Ask for a temperature in Celsius and convert it to Fahrenheit with `(celsius * 9 / 5) + 32`.
3. Ask for the width and height of a rectangle, then print its area and perimeter.
4. Store a sentence and print its length, uppercase form, and first ten characters.
5. Build a tip calculator that accepts a bill amount and percentage, then prints the tip and final total.

You now have the vocabulary every Python program depends on: names, values, types, expressions, input, and output. Next, you will use those values to make decisions and repeat work with conditionals and loops.
