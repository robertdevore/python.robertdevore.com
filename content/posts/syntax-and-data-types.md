---
title: "1.3. Control Flow (If, For, While)"
description: "Control flow is what makes your programs truly intelligent. Instead of just executing line by line from top to bottom, you'll learn to make your code make decisions, repeat actions, and…"
excerpt: "Control flow is what makes your programs truly intelligent. Instead of just executing line by line from top to bottom, you'll learn to make your code make decisions, repeat actions, and…"
custom_url: syntax-and-data-types
template: docs
section: "Chapter 1 · Beginner Python"
order: 40
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: beginner
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /blog/python-syntax-and-data-types/
next: /blog/functions-and-modules/
tags: [python, course]
---
## Overview

Control flow is what makes your programs truly intelligent. Instead of just executing line by line from top to bottom, you'll learn to make your code make decisions, repeat actions, and respond dynamically to different situations. This is where your programs start to feel alive—they can think, choose, and adapt based on the data they encounter.

In this chapter, you'll master the fundamental building blocks that let you control the flow of execution in your Python programs: conditional statements (`if`, `elif`, `else`) and loops (`for` and `while`). By the end, you'll be able to build programs that can handle user input intelligently, process collections of data, and solve real-world problems through logical decision-making.

* * *

## **if, elif, else Statements: Making Decisions**

Every program needs to make decisions. Should we display a welcome message or an error? Is the user old enough to access this content? Has the player won the game? Python's conditional statements let your code choose different paths based on the conditions you specify.

### **Basic if Statements**

The simplest form of decision-making is the `if` statement. It evaluates a condition and only executes the code inside if that condition is `True`.

```python
age = 18

if age >= 18:
    print("You are eligible to vote!")
    print("Welcome to the voting system.")
```

The basic structure is:

  * `if` keyword followed by a condition
  * A colon (`:`) to end the condition line
  * Indented code block that executes when the condition is `True`

**Important:** Python uses indentation (spaces or tabs) to define code blocks. Everything indented at the same level after the `if` statement belongs to that conditional block.

### **Adding else for Alternative Actions**

What if you want to do something different when the condition is `False`? That's where `else` comes in:

```python
age = 16

if age >= 18:
    print("You are eligible to vote!")
else:
    print("You are not old enough to vote yet.")
    print(f"You can vote in {18 - age} years.")
```

This creates a clear fork in your program's logic—one path for when the condition is true, another for when it's false.

### **Multiple Conditions with elif**

Real life rarely involves just two choices. The `elif` (else if) statement lets you check multiple conditions in sequence:

```python
score = 85

if score >= 90:
    grade = "A"
    print("Excellent work!")
elif score >= 80:
    grade = "B"
    print("Good job!")
elif score >= 70:
    grade = "C"
    print("Satisfactory.")
elif score >= 60:
    grade = "D"
    print("You passed, but consider studying more.")
else:
    grade = "F"
    print("Unfortunately, you failed. Don't give up!")

print(f"Your grade is: {grade}")
```

Python evaluates these conditions from top to bottom and stops at the first `True` condition. This means order matters! If you put the `score >= 60` condition first, a score of 85 would trigger that condition instead of the more specific `score >= 80`.

### **Practical Example: A Simple Calculator Menu**

Let's build something useful—a calculator that asks the user what operation they want to perform:

```python
print("Simple Calculator")
print("Choose an operation:")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")

choice = input("Enter your choice (1-4): ")

if choice == "1":
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
elif choice == "2":
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = num1 - num2
    print(f"{num1} - {num2} = {result}")
elif choice == "3":
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")
elif choice == "4":
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    if num2 != 0:
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
    else:
        print("Error: Cannot divide by zero!")
else:
    print("Invalid choice. Please run the program again.")
```

Notice how we nested another `if` statement inside the division case to check for division by zero—this shows how conditional statements can be combined to handle complex logic.

* * *

## **Comparison & Logical Operators: Building Smart Conditions**

To make good decisions, your programs need to compare values and combine multiple conditions. Python provides powerful operators for these tasks.

### **Comparison Operators**

These operators compare two values and return either `True` or `False`:

Operator | Meaning | Example | Result
---|---|---|---
`==` | Equal to | `5 == 5` | `True`
`!=` | Not equal to | `5 != 3` | `True`
`<` | Less than | `3 < 5` | `True`
`>` | Greater than | `5 > 3` | `True`
`<=` | Less than or equal | `3 <= 3` | `True`
`>=` | Greater than or equal | `5 >= 3` | `True`

```python
# Comparing numbers
temperature = 72
print(temperature > 70)  # True
print(temperature == 72)  # True

# Comparing strings
name = "Alice"
print(name == "alice")  # False (case-sensitive!)
print(name.lower() == "alice")  # True

# Comparing with user input
user_age = int(input("Enter your age: "))
if user_age >= 21:
    print("You can legally drink alcohol in the US.")
```

### **Logical Operators: Combining Conditions**

Sometimes you need to check multiple conditions at once. Logical operators let you combine conditions:

  * `and`: Both conditions must be `True`
  * `or`: At least one condition must be `True`
  * `not`: Flips `True` to `False` and vice versa

```python
# Using 'and' - both conditions must be true
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can rent a car!")
else:
    print("Sorry, you cannot rent a car.")

# Using 'or' - at least one condition must be true
day = "Saturday"
is_holiday = False

if day == "Saturday" or day == "Sunday" or is_holiday:
    print("No work today!")
else:
    print("It's a workday.")

# Using 'not' - reverses the boolean value
is_raining = False

if not is_raining:
    print("Great weather for a walk!")
else:
    print("Better stay inside.")
```

### **Complex Logical Expressions**

You can combine multiple operators, but use parentheses to make your logic clear:

```python
# A more complex example: movie theater admission
age = 16
has_parent = True
movie_rating = "R"

if (age >= 17) or (age >= 13 and has_parent and movie_rating != "NC-17"):
    print("You can watch this movie!")
else:
    print("Sorry, you cannot watch this movie.")
```

* * *

## **for Loops: Repeating Actions with Collections**

Imagine you need to print numbers 1 through 10, or process every item in a shopping list. Writing individual lines for each item would be tedious and impractical. Loops solve this by letting you repeat code automatically.

### **Basic for Loop Structure**

The `for` loop iterates over a sequence (like a list, string, or range):

```python
fruits = ["apple", "banana", "cherry", "date"]

for fruit in fruits:
    print(f"I like {fruit}s!")
```

Output:

```text
I like apples!
I like bananas!
I like cherrys!
I like dates!
```

### **Using range() for Number Sequences**

The `range()` function generates sequences of numbers, perfect for counting loops:

```python
# Print numbers 0 through 4
for i in range(5):
    print(f"Count: {i}")

# Print numbers 1 through 5
for i in range(1, 6):
    print(f"Count: {i}")

# Print even numbers from 2 to 10
for i in range(2, 11, 2):
    print(f"Even number: {i}")
```

The `range()` function takes up to three parameters:

  * `range(stop)`: Numbers from 0 to stop-1
  * `range(start, stop)`: Numbers from start to stop-1
  * `range(start, stop, step)`: Numbers from start to stop-1, incrementing by step

### **Looping Through Strings**

Strings are sequences too, so you can loop through each character:

```python
word = "Python"

for letter in word:
    print(f"Letter: {letter}")
```

### **Practical Example: Grade Calculator**

Let's build a program that calculates the average grade from a list of test scores:

```python
# List of test scores
scores = [85, 92, 78, 96, 88]
total = 0

print("Individual scores:")
for score in scores:
    print(f"Score: {score}")
    total += score  # Add each score to the total

average = total / len(scores)
print(f"\nTotal points: {total}")
print(f"Number of tests: {len(scores)}")
print(f"Average grade: {average:.1f}")

# Determine letter grade
if average >= 90:
    letter_grade = "A"
elif average >= 80:
    letter_grade = "B"
elif average >= 70:
    letter_grade = "C"
elif average >= 60:
    letter_grade = "D"
else:
    letter_grade = "F"

print(f"Letter grade: {letter_grade}")
```

### **Nested Loops**

You can put loops inside other loops to handle more complex data structures:

```python
# Multiplication table
print("Multiplication Table (1-5):")
print("   ", end="")
for i in range(1, 6):
    print(f"{i:4}", end="")
print()  # New line

for i in range(1, 6):
    print(f"{i}: ", end="")
    for j in range(1, 6):
        result = i * j
        print(f"{result:4}", end="")
    print()  # New line after each row
```

* * *

## **while Loops: Repeating Until a Condition Changes**

While `for` loops are great when you know how many times to repeat something, `while` loops are perfect when you need to keep going until some condition changes. They're especially useful for user input validation, game loops, and processing data of unknown size.

### **Basic while Loop Structure**

A `while` loop continues executing as long as its condition remains `True`:

```python
count = 1

while count <= 5:
    print(f"Count is: {count}")
    count += 1  # Important: change the condition variable!

print("Loop finished!")
```

**Critical Warning:** Always make sure your `while` loop condition will eventually become `False`, or you'll create an infinite loop that runs forever!

### **User Input Validation**

One of the most practical uses for `while` loops is ensuring users provide valid input:

```python
# Keep asking until we get a valid age
while True:
    try:
        age = int(input("Please enter your age: "))
        if age < 0:
            print("Age cannot be negative. Please try again.")
        elif age > 150:
            print("That seems unrealistic. Please try again.")
        else:
            break  # Exit the loop - we got valid input!
    except ValueError:
        print("Please enter a valid number.")

print(f"Thank you! Your age is {age}.")
```

### **Practical Example: Number Guessing Game**

Let's create an interactive guessing game that demonstrates `while` loops in action:

```python
import random

# Generate a random number between 1 and 100
secret_number = random.randint(1, 100)
guesses = 0
max_guesses = 7

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print(f"You have {max_guesses} guesses to find it!")

while guesses < max_guesses:
    try:
        guess = int(input(f"\nGuess #{guesses + 1}: Enter your guess: "))
        guesses += 1

        if guess == secret_number:
            print(f"🎉 Congratulations! You found it in {guesses} guesses!")
            break
        elif guess < secret_number:
            print("Too low! Try a higher number.")
        else:
            print("Too high! Try a lower number.")

        remaining = max_guesses - guesses
        if remaining > 0:
            print(f"You have {remaining} guesses left.")

    except ValueError:
        print("Please enter a valid number!")
        guesses -= 1  # Don't count invalid input as a guess

if guesses >= max_guesses and guess != secret_number:
    print(f"\n😞 Sorry! You've used all your guesses. The number was {secret_number}.")
```

* * *

## **Loop Control: break & continue**

Sometimes you need fine-grained control over your loops. Python provides `break` and `continue` statements to modify loop behavior.

### **break: Exiting Loops Early**

The `break` statement immediately exits the current loop:

```python
# Find the first number divisible by 7
numbers = [12, 15, 21, 28, 33, 42]

for num in numbers:
    if num % 7 == 0:
        print(f"Found first number divisible by 7: {num}")
        break
    print(f"{num} is not divisible by 7")
```

### **continue: Skipping to the Next Iteration**

The `continue` statement skips the rest of the current iteration and jumps to the next one:

```python
# Print only positive numbers
numbers = [1, -2, 3, -4, 5, -6, 7]

print("Positive numbers only:")
for num in numbers:
    if num < 0:
        continue  # Skip negative numbers
    print(num)
```

### **Practical Example: Menu System**

Here's a complete example that combines everything we've learned—a restaurant ordering system:

```python
def display_menu():
    print("\n🍽️  RESTAURANT MENU")
    print("1. Pizza - $12.99")
    print("2. Burger - $8.99")
    print("3. Salad - $6.99")
    print("4. Drink - $2.99")
    print("5. View Order")
    print("6. Checkout")
    print("0. Exit")

order = []
total_cost = 0.0
menu_prices = {
    "1": ("Pizza", 12.99),
    "2": ("Burger", 8.99),
    "3": ("Salad", 6.99),
    "4": ("Drink", 2.99)
}

print("Welcome to Python Restaurant! 🐍")

while True:
    display_menu()
    choice = input("\nEnter your choice: ").strip()

    if choice == "0":
        print("Thank you for visiting Python Restaurant!")
        break

    elif choice in menu_prices:
        item_name, item_price = menu_prices[choice]
        order.append((item_name, item_price))
        total_cost += item_price
        print(f"Added {item_name} to your order!")

    elif choice == "5":
        if not order:
            print("Your order is empty.")
            continue

        print("\n📝 YOUR ORDER:")
        for i, (item, price) in enumerate(order, 1):
            print(f"{i}. {item} - ${price:.2f}")
        print(f"Total: ${total_cost:.2f}")

    elif choice == "6":
        if not order:
            print("Your order is empty. Add some items first!")
            continue

        print("\n🧾 FINAL ORDER:")
        for item, price in order:
            print(f"{item} - ${price:.2f}")

        tax = total_cost * 0.08
        final_total = total_cost + tax

        print(f"\nSubtotal: ${total_cost:.2f}")
        print(f"Tax (8%): ${tax:.2f}")
        print(f"Total: ${final_total:.2f}")

        payment = input("\nConfirm payment? (y/n): ").lower()
        if payment == "y":
            print("Payment processed! Enjoy your meal! 🎉")
            break
        else:
            print("Payment cancelled. You can modify your order.")

    else:
        print("Invalid choice. Please try again.")
```

* * *

## **Putting It All Together: Best Practices**

As you build more complex programs with control flow, keep these principles in mind:

### **1\. Keep Conditions Simple and Readable**

```python
# Good: Clear and readable
if age >= 18 and has_valid_id:
    allow_entry = True

# Avoid: Complex nested conditions
if not (age < 18 or not has_valid_id or (is_banned and not is_vip)):
    allow_entry = True
```

### **2\. Use Meaningful Variable Names**

```python
# Good: Descriptive names
for customer in customer_list:
    if customer.is_premium_member:
        apply_discount(customer)

# Avoid: Cryptic names
for c in cl:
    if c.ipm:
        ad(c)
```

### **3\. Avoid Deep Nesting**

```python
# Good: Early returns/continues to reduce nesting
for user in users:
    if not user.is_active:
        continue
    if not user.has_permission:
        continue
    process_user(user)

# Avoid: Deep nesting
for user in users:
    if user.is_active:
        if user.has_permission:
            process_user(user)
```

### **4\. Handle Edge Cases**

Always think about what could go wrong:

  * What if a list is empty?
  * What if user input is invalid?
  * What if a calculation results in division by zero?

* * *

## **Practice Exercises**

Try these exercises to reinforce your understanding:

  1. **Temperature Converter** : Write a program that converts temperatures between Celsius and Fahrenheit. Use `if` statements to handle user choice and input validation.

  2. **Password Strength Checker** : Create a program that evaluates password strength based on length, special characters, numbers, and mixed case.

  3. **Times Table Generator** : Use nested loops to create a customizable multiplication table.

  4. **Rock, Paper, Scissors** : Build the classic game with user input, computer AI, and score tracking using while loops.

  5. **Prime Number Finder** : Write a program that finds all prime numbers up to a given number using loops and conditional logic.

Control flow is the foundation of all programming logic. Master these concepts, and you'll be able to build programs that can think, decide, and adapt—the hallmarks of intelligent software. In [the next section](<https://python.robertdevore.com/blog/functions-and-modules>), we'll learn how to organize this logic into reusable functions and modules.
