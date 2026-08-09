---
title: "1.5. Basic Error Handling"
description: "Prepare for inevitable mistakes - catch, handle, and recover from errors so your scripts don't just crash at the first sign of trouble."
excerpt: "Prepare for inevitable mistakes - catch, handle, and recover from errors so your scripts don't just crash at the first sign of trouble."
custom_url: basic-error-handling
template: docs
section: "Chapter 1 · Beginner Python"
order: 60
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: beginner
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /blog/functions-and-modules/
next: /blog/chapter-2-intermediate-python/
tags: [python, course]
---
## Overview

Prepare for inevitable mistakes - catch, handle, and recover from errors so your scripts don't just crash at the first sign of trouble.

* * *

## Introduction: Why Error Handling Matters

Picture this: You've just written your first Python program to calculate grades for your class. You're excited to show it off, but the moment someone enters "ABC" instead of a number, your program crashes with a scary red error message. Your user stares at the screen, confused and frustrated.

This is exactly why error handling is one of the most important skills you'll learn as a programmer. Errors aren't just inevitable—they're actually valuable information that can help you build better, more robust programs.

In this chapter, we'll transform you from someone who fears error messages into someone who confidently handles them, creating programs that gracefully recover from problems instead of crashing.

* * *

## What are Errors and Exceptions?

Before we dive into handling errors, let's understand what they actually are. In Python, there are two main types of problems you'll encounter:

### Syntax Errors

**Syntax errors** occur when Python can't understand your code because it doesn't follow Python's grammar rules. These happen before your program even starts running.

```python
# Syntax Error - Missing closing parenthesis
print("Hello World"

# Syntax Error - Missing colon after if statement
if x == 5
    print("x is 5")

# Syntax Error - Incorrect indentation
def my_function():
print("This won't work")
```

When you have a syntax error, Python won't even try to run your program. It'll point out exactly where the problem is, and you'll need to fix it before proceeding.

### Runtime Exceptions

**Exceptions** (also called runtime errors) occur while your program is running. Your code is syntactically correct, but something goes wrong during execution.

```python
# This code looks fine, but will crash if user enters "hello"
age = int(input("Enter your age: "))
print(f"You are {age} years old")

# This will crash if the file doesn't exist
file = open("nonexistent.txt", "r")

# This will crash if we try to divide by zero
result = 10 / 0
```

The key difference: syntax errors prevent your program from starting, while exceptions crash your program while it's running. We can't prevent all exceptions, but we can handle them gracefully.

* * *

## Understanding Common Beginner Errors

Let's look at the most common exceptions you'll encounter as a beginner, with examples of when they occur:

### ValueError

Occurs when a function receives an argument of the right type but with an inappropriate value.

```python
# Trying to convert a non-numeric string to integer
number = int("hello")  # ValueError: invalid literal for int()

# Trying to convert an empty string
number = int("")  # ValueError: invalid literal for int()

# Math operations with inappropriate values
import math
result = math.sqrt(-1)  # ValueError: math domain error
```

### TypeError

Happens when an operation is performed on an inappropriate type.

```python
# Trying to add a string and integer
result = "5" + 3  # TypeError: can only concatenate str to str

# Calling a non-callable object
x = 5
x()  # TypeError: 'int' object is not callable

# Using wrong number of arguments
def greet(name):
    return f"Hello, {name}"

greet()  # TypeError: greet() missing 1 required positional argument
```

### NameError

Occurs when trying to use a variable that hasn't been defined.

```python
# Using a variable before defining it
print(my_variable)  # NameError: name 'my_variable' is not defined

# Typo in variable name
my_name = "Alice"
print(my_nme)  # NameError: name 'my_nme' is not defined
```

### IndexError

Happens when trying to access a list item that doesn't exist.

```python
numbers = [1, 2, 3]
print(numbers[5])  # IndexError: list index out of range

# Empty list
empty_list = []
print(empty_list[0])  # IndexError: list index out of range
```

### KeyError

Occurs when trying to access a dictionary key that doesn't exist.

```python
student = {"name": "Alice", "age": 20}
print(student["grade"])  # KeyError: 'grade'
```

### FileNotFoundError

Happens when trying to open a file that doesn't exist.

```python
# Trying to open a non-existent file
with open("missing_file.txt", "r") as file:
    content = file.read()  # FileNotFoundError
```

* * *

## Introduction to try and except Blocks

Now that we understand what exceptions are, let's learn how to handle them gracefully using `try` and `except` blocks.

### Basic try/except Structure

The basic structure looks like this:

```text
try:
    # Code that might cause an error
    risky_code_here()
except:
    # Code that runs if an error occurs
    print("Something went wrong!")
```

Let's see this in action:

```python
try:
    age = int(input("Enter your age: "))
    print(f"You are {age} years old")
except:
    print("Please enter a valid number for your age.")
```

Now, instead of crashing when someone enters "twenty-five", your program politely asks for a valid number.

### Catching Specific Exceptions

While catching all exceptions works, it's better practice to catch specific ones:

```python
try:
    age = int(input("Enter your age: "))
    print(f"You are {age} years old")
except ValueError:
    print("Please enter a valid number for your age.")
```

This approach is better because:

  1. It's more precise about what we're handling
  2. It won't accidentally hide other unexpected errors
  3. It makes our code more readable and maintainable

### Handling Multiple Exception Types

You can handle different types of exceptions differently:

```python
try:
    filename = input("Enter filename: ")
    with open(filename, "r") as file:
        content = file.read()
        lines = int(input("How many lines to show? "))
        print("\n".join(content.split("\n")[:lines]))

except FileNotFoundError:
    print("Sorry, that file doesn't exist.")
except ValueError:
    print("Please enter a valid number for lines.")
except PermissionError:
    print("You don't have permission to read that file.")
```

### The else Clause

The `else` clause runs only if no exception occurred:

```python
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("That's not a valid number!")
else:
    print(f"Great! You entered {number}")
    print(f"Its square is {number ** 2}")
```

### The finally Clause

The `finally` clause always runs, whether an exception occurred or not:

```python
try:
    file = open("data.txt", "r")
    data = file.read()
    process_data(data)
except FileNotFoundError:
    print("File not found!")
finally:
    # This always runs
    if 'file' in locals():
        file.close()
    print("Cleanup completed")
```

* * *

## Practical Examples and Patterns

### Safe User Input

Here's a robust way to get numeric input from users:

```python
def get_positive_integer(prompt):
    """Get a positive integer from user with error handling."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")

# Usage
age = get_positive_integer("Enter your age: ")
print(f"You are {age} years old")
```

### Safe File Operations

```python
def read_file_safely(filename):
    """Read a file with proper error handling."""
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Usage
content = read_file_safely("my_document.txt")
if content:
    print("File contents:")
    print(content)
else:
    print("Could not read the file.")
```

### Calculator with Error Handling

```python
def safe_calculator():
    """A simple calculator with comprehensive error handling."""
    print("Simple Calculator")
    print("Enter 'quit' to exit")

    while True:
        try:
            # Get the operation
            operation = input("\nEnter operation (+, -, *, /) or 'quit': ").strip()

            if operation.lower() == 'quit':
                print("Thanks for using the calculator!")
                break

            if operation not in ['+', '-', '*', '/']:
                print("Invalid operation. Please use +, -, *, or /")
                continue

            # Get the numbers
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            # Perform calculation
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    print("Error: Cannot divide by zero!")
                    continue
                result = num1 / num2

            print(f"Result: {num1} {operation} {num2} = {result}")

        except ValueError:
            print("Error: Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\nCalculator interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Run the calculator
safe_calculator()
```

* * *

## Printing Helpful Error Messages

Good error messages help users understand what went wrong and how to fix it. Here are some guidelines:

### Be Specific and Clear

❌ Bad:

```python
except:
    print("Error!")
```

✅ Good:

```python
except ValueError:
    print("Please enter a number, not text or symbols.")
```

### Provide Context

❌ Bad:

```python
except FileNotFoundError:
    print("File not found.")
```

✅ Good:

```python
except FileNotFoundError:
    print(f"Error: Could not find the file '{filename}'.")
    print("Please check the filename and try again.")
```

### Suggest Solutions

❌ Bad:

```python
except ZeroDivisionError:
    print("Cannot divide by zero.")
```

✅ Good:

```python
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")
    print("Please enter a non-zero number for the divisor.")
```

* * *

## Learning from Tracebacks

When an exception occurs and isn't caught, Python shows a **traceback** —a detailed error report. Learning to read these is crucial for debugging.

Here's a typical traceback:

```python
Traceback (most recent call last):
  File "calculator.py", line 15, in <module>
    result = divide_numbers(10, 0)
  File "calculator.py", line 8, in divide_numbers
    return a / b
ZeroDivisionError: division by zero
```

Reading from bottom to top:

  1. **Exception type and message** : `ZeroDivisionError: division by zero`
  2. **Where it occurred** : Line 8 in the `divide_numbers` function
  3. **How we got there** : Called from line 15 in the main program

### Using Tracebacks to Debug

```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

def main():
    scores = []  # Empty list!
    average = calculate_average(scores)
    print(f"Average score: {average}")

main()
```

This produces:

```python
Traceback (most recent call last):
  File "grades.py", line 9, in main
    average = calculate_average(scores)
  File "grades.py", line 4, in calculate_average
    return total / count
ZeroDivisionError: division by zero
```

The traceback tells us:

  * The error is a division by zero
  * It happened in `calculate_average` when we tried to divide by `count`
  * `count` must be zero, meaning our list is empty
  * We called this function from `main()` with an empty list

* * *

## Best Practices for Error Handling

### 1\. Be Specific with Exception Types

```python
# Don't catch everything
try:
    value = int(user_input)
except:  # Too broad!
    print("Error occurred")

# Catch specific exceptions
try:
    value = int(user_input)
except ValueError:  # Specific and clear
    print("Please enter a valid integer")
```

### 2\. Don't Ignore Exceptions

```python
# Don't do this
try:
    risky_operation()
except:
    pass  # Silent failure is dangerous!

# Do this instead
try:
    risky_operation()
except SpecificError as e:
    print(f"Warning: Operation failed - {e}")
    # Handle appropriately
```

### 3\. Use Exception Information

```python
try:
    with open(filename, 'r') as file:
        data = file.read()
except FileNotFoundError as e:
    print(f"Could not open file: {e}")
    print(f"Please check if '{filename}' exists")
```

### 4\. Keep try Blocks Small

```python
# Don't wrap too much code
try:
    # 50 lines of code here - too much!
except ValueError:
    pass

# Keep it focused
try:
    user_age = int(input("Enter age: "))
except ValueError:
    print("Please enter a valid age")

# Then continue with other operations
```

* * *

## Putting It All Together: A Complete Example

Let's create a simple grade management system that demonstrates all these concepts:

```python
def get_student_grades():
    """Collect and manage student grades with comprehensive error handling."""
    grades = []

    print("Grade Management System")
    print("Enter grades one by one. Type 'done' when finished.")
    print("Valid grades are between 0 and 100.")

    while True:
        try:
            user_input = input("\nEnter a grade (or 'done'): ").strip()

            # Check if user wants to finish
            if user_input.lower() == 'done':
                break

            # Try to convert to float
            grade = float(user_input)

            # Validate grade range
            if grade < 0 or grade > 100:
                print("Error: Grade must be between 0 and 100.")
                continue

            grades.append(grade)
            print(f"Added grade: {grade}")

        except ValueError:
            print("Error: Please enter a valid number or 'done'.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            return None

    # Calculate statistics if we have grades
    if not grades:
        print("No grades entered.")
        return None

    try:
        average = sum(grades) / len(grades)
        highest = max(grades)
        lowest = min(grades)

        print(f"\nGrade Statistics:")
        print(f"Number of grades: {len(grades)}")
        print(f"Average: {average:.2f}")
        print(f"Highest: {highest}")
        print(f"Lowest: {lowest}")

        return grades

    except Exception as e:
        print(f"Error calculating statistics: {e}")
        return grades

# Run the program
if __name__ == "__main__":
    student_grades = get_student_grades()
```

* * *

## Conclusion

Error handling is your safety net as a programmer. It transforms your programs from fragile scripts that crash at the first sign of trouble into robust applications that can handle real-world conditions gracefully.

Key takeaways from this chapter:

  1. **Understand the difference** between syntax errors (which prevent your program from running) and exceptions (which occur during execution)

  2. **Use try/except blocks** to catch and handle specific exceptions rather than letting your program crash

  3. **Be specific** with exception types—catch `ValueError` instead of using a bare `except`

  4. **Provide helpful error messages** that explain what went wrong and how to fix it

  5. **Learn to read tracebacks** —they're your best debugging tool

  6. **Keep error handling focused** —don't wrap too much code in try blocks

Remember, good error handling isn't just about preventing crashes—it's about creating a better experience for anyone using your programs. When errors are handled well, users feel confident and can easily recover from mistakes.

As you continue your Python journey, you'll encounter more complex error scenarios, but the fundamentals you've learned here will serve you well. Every professional Python developer relies on these same concepts to build reliable, user-friendly applications.

In [Chapter 2](<https://python.robertdevore.com/blog/chapter-2-intermediate-python>), we'll move on to Intermediate Python concepts, where you'll learn about Object-Oriented Programming and start building more sophisticated programs that benefit greatly from the solid error handling foundation you've just built.
