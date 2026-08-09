---
title: "2.1. Object-Oriented Programming (OOP)"
description: "Object-Oriented Programming (OOP) is a programming paradigm that organizes code around objects rather than functions and logic. Think of it as a way to model real-world concepts in your…"
excerpt: "Object-Oriented Programming (OOP) is a programming paradigm that organizes code around objects rather than functions and logic. Think of it as a way to model real-world concepts in your…"
custom_url: object-oriented-programming
template: docs
section: "Chapter 2 · Intermediate Python"
order: 80
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: intermediate
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /blog/chapter-2-intermediate-python/
next: /blog/file-io-and-data-persistence/
tags: [python, course]
---
## What is Object-Oriented Programming?

Object-Oriented Programming (OOP) is a programming paradigm that organizes code around **objects** rather than functions and logic. Think of it as a way to model real-world concepts in your code—instead of writing a collection of separate functions that operate on data, you create self-contained units (objects) that bundle both data and the methods that work on that data.

### Why Use OOP?

Before diving into the mechanics, let's understand why OOP matters:

  1. **Organization** : Large programs become easier to manage when code is grouped into logical units
  2. **Reusability** : Once you create a class, you can use it multiple times without rewriting code
  3. **Maintainability** : Changes to one part of your code are less likely to break other parts
  4. **Modeling** : OOP naturally maps to how we think about real-world problems

Consider this procedural approach to managing a bank account:


    # Procedural approach
    account_balance = 1000
    account_owner = "Alice"

    def deposit(balance, amount):
        return balance + amount

    def withdraw(balance, amount):
        if balance >= amount:
            return balance - amount
        else:
            print("Insufficient funds")
            return balance

    # Using the functions
    account_balance = deposit(account_balance, 500)
    account_balance = withdraw(account_balance, 200)


Now compare it to an object-oriented approach:


    # Object-oriented approach
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount
            return self.balance

        def withdraw(self, amount):
            if self.balance >= amount:
                self.balance -= amount
                return self.balance
            else:
                print("Insufficient funds")
                return self.balance

    # Using the class
    alice_account = BankAccount("Alice", 1000)
    alice_account.deposit(500)
    alice_account.withdraw(200)


The OOP version bundles the data (owner, balance) with the methods that operate on it, creating a more intuitive and maintainable structure.

## Classes and Objects

### Understanding Classes

A **class** is like a blueprint or template for creating objects. It defines what attributes (data) and methods (functions) the objects will have, but doesn't create the actual object itself.


    class Dog:
        # Class attribute (shared by all instances)
        species = "Canis familiaris"

        # Constructor method
        def __init__(self, name, age, breed):
            # Instance attributes (unique to each object)
            self.name = name
            self.age = age
            self.breed = breed

        # Instance method
        def bark(self):
            return f"{self.name} says Woof!"

        def get_info(self):
            return f"{self.name} is a {self.age}-year-old {self.breed}"


### Creating Objects (Instances)

An **object** is a specific instance of a class. You can create multiple objects from the same class:


    # Creating objects
    buddy = Dog("Buddy", 3, "Golden Retriever")
    max_dog = Dog("Max", 5, "German Shepherd")

    # Using object methods
    print(buddy.bark())          # Output: Buddy says Woof!
    print(max_dog.get_info())    # Output: Max is a 5-year-old German Shepherd

    # Accessing attributes
    print(buddy.name)            # Output: Buddy
    print(Dog.species)           # Output: Canis familiaris


### The `__init__` Method

The `__init__` method is a special method called a **constructor**. It's automatically called when you create a new object and is used to initialize the object's attributes:


    class Student:
        def __init__(self, name, student_id, major):
            self.name = name
            self.student_id = student_id
            self.major = major
            self.grades = []  # Initialize empty list
            self.gpa = 0.0

        def add_grade(self, grade):
            self.grades.append(grade)
            self.calculate_gpa()

        def calculate_gpa(self):
            if self.grades:
                self.gpa = sum(self.grades) / len(self.grades)

    # Usage
    student = Student("John Doe", "12345", "Computer Science")
    student.add_grade(85)
    student.add_grade(92)
    print(f"GPA: {student.gpa}")  # Output: GPA: 88.5


## Encapsulation

**Encapsulation** is the practice of bundling data and methods together while controlling access to the internal state of an object. In Python, we use naming conventions to indicate privacy levels.

### Public, Protected, and Private Members


    class BankAccount:
        def __init__(self, owner, initial_balance=0):
            self.owner = owner              # Public attribute
            self._account_number = self._generate_account_number()  # Protected
            self.__balance = initial_balance  # Private attribute

        def _generate_account_number(self):  # Protected method
            import random
            return f"ACC{random.randint(100000, 999999)}"

        def __validate_amount(self, amount):  # Private method
            return amount > 0

        def deposit(self, amount):  # Public method
            if self.__validate_amount(amount):
                self.__balance += amount
                print(f"Deposited ${amount}. New balance: ${self.__balance}")
            else:
                print("Invalid deposit amount")

        def get_balance(self):  # Public method to access private data
            return self.__balance

        def withdraw(self, amount):
            if self.__validate_amount(amount) and amount <= self.__balance:
                self.__balance -= amount
                print(f"Withdrew ${amount}. New balance: ${self.__balance}")
            else:
                print("Invalid withdrawal")

    # Usage
    account = BankAccount("Alice", 1000)
    account.deposit(500)

    # This works - accessing public attribute
    print(account.owner)

    # This works - accessing via public method
    print(account.get_balance())

    # This would raise an AttributeError - accessing private attribute directly
    # print(account.__balance)  # AttributeError!


### Property Decorators

Python provides a more elegant way to control access using properties:


    class Temperature:
        def __init__(self, celsius=0):
            self._celsius = celsius

        @property
        def celsius(self):
            return self._celsius

        @celsius.setter
        def celsius(self, value):
            if value < -273.15:
                raise ValueError("Temperature cannot be below absolute zero")
            self._celsius = value

        @property
        def fahrenheit(self):
            return (self._celsius * 9/5) + 32

        @fahrenheit.setter
        def fahrenheit(self, value):
            self.celsius = (value - 32) * 5/9

    # Usage
    temp = Temperature(25)
    print(f"Celsius: {temp.celsius}")      # Output: Celsius: 25
    print(f"Fahrenheit: {temp.fahrenheit}") # Output: Fahrenheit: 77.0

    temp.fahrenheit = 100
    print(f"Celsius: {temp.celsius}")      # Output: Celsius: 37.77777777777778


## Inheritance

**Inheritance** allows you to create new classes based on existing ones, inheriting their attributes and methods while adding or modifying functionality.

### Basic Inheritance


    # Parent class (Base class)
    class Animal:
        def __init__(self, name, species):
            self.name = name
            self.species = species
            self.is_alive = True

        def eat(self):
            print(f"{self.name} is eating")

        def sleep(self):
            print(f"{self.name} is sleeping")

        def make_sound(self):
            print("Some generic animal sound")

    # Child class (Derived class)
    class Dog(Animal):
        def __init__(self, name, breed):
            super().__init__(name, "Canis familiaris")  # Call parent constructor
            self.breed = breed

        def make_sound(self):  # Override parent method
            print(f"{self.name} barks: Woof!")

        def fetch(self):  # New method specific to Dog
            print(f"{self.name} is fetching the ball")

    class Cat(Animal):
        def __init__(self, name, indoor=True):
            super().__init__(name, "Felis catus")
            self.indoor = indoor

        def make_sound(self):  # Override parent method
            print(f"{self.name} meows: Meow!")

        def climb(self):  # New method specific to Cat
            print(f"{self.name} is climbing")

    # Usage
    dog = Dog("Buddy", "Labrador")
    cat = Cat("Whiskers", indoor=True)

    # Inherited methods
    dog.eat()        # Output: Buddy is eating
    cat.sleep()      # Output: Whiskers is sleeping

    # Overridden methods
    dog.make_sound() # Output: Buddy barks: Woof!
    cat.make_sound() # Output: Whiskers meows: Meow!

    # New methods
    dog.fetch()      # Output: Buddy is fetching the ball
    cat.climb()      # Output: Whiskers is climbing


### Multiple Inheritance

Python supports multiple inheritance, where a class can inherit from multiple parent classes:


    class Flyable:
        def fly(self):
            print("Flying through the sky")

    class Swimmable:
        def swim(self):
            print("Swimming in water")

    class Duck(Animal, Flyable, Swimmable):
        def __init__(self, name):
            super().__init__(name, "Duck")

        def make_sound(self):
            print(f"{self.name} quacks: Quack!")

    # Usage
    duck = Duck("Donald")
    duck.eat()       # From Animal
    duck.fly()       # From Flyable
    duck.swim()      # From Swimmable
    duck.make_sound()  # Overridden method


## Polymorphism

**Polymorphism** allows objects of different classes to be treated as objects of a common base class, while still calling their specific implementations of methods.


    def animal_concert(animals):
        """Function that works with any animal object"""
        for animal in animals:
            animal.make_sound()  # Each animal makes its own sound

    # Create different animals
    animals = [
        Dog("Rex", "German Shepherd"),
        Cat("Luna", indoor=False),
        Duck("Daffy")
    ]

    # Polymorphism in action
    animal_concert(animals)
    # Output:
    # Rex barks: Woof!
    # Luna meows: Meow!
    # Daffy quacks: Quack!


### Duck Typing

Python embraces "duck typing" - if it walks like a duck and quacks like a duck, it's a duck:


    class Robot:
        def __init__(self, name):
            self.name = name

        def make_sound(self):
            print(f"{self.name} beeps: Beep beep!")

    # Even though Robot doesn't inherit from Animal,
    # it can still be used in our concert
    robot = Robot("R2D2")
    animals.append(robot)
    animal_concert(animals)  # Works perfectly!


## Magic Methods & Dunder Methods

Magic methods (also called dunder methods) are special methods with double underscores that allow your objects to integrate with Python's built-in functions and operators.

### Common Magic Methods


    class Book:
        def __init__(self, title, author, pages):
            self.title = title
            self.author = author
            self.pages = pages

        def __str__(self):
            """String representation for end users"""
            return f"{self.title} by {self.author}"

        def __repr__(self):
            """String representation for developers"""
            return f"Book('{self.title}', '{self.author}', {self.pages})"

        def __len__(self):
            """Return length when len() is called"""
            return self.pages

        def __eq__(self, other):
            """Define equality comparison"""
            if isinstance(other, Book):
                return (self.title == other.title and
                       self.author == other.author)
            return False

        def __lt__(self, other):
            """Define less-than comparison (for sorting)"""
            if isinstance(other, Book):
                return self.pages < other.pages
            return NotImplemented

        def __add__(self, other):
            """Define addition operation"""
            if isinstance(other, Book):
                combined_title = f"{self.title} & {other.title}"
                combined_author = f"{self.author} & {other.author}"
                combined_pages = self.pages + other.pages
                return Book(combined_title, combined_author, combined_pages)
            return NotImplemented

    # Usage examples
    book1 = Book("1984", "George Orwell", 328)
    book2 = Book("Animal Farm", "George Orwell", 112)

    print(book1)           # Output: 1984 by George Orwell
    print(repr(book1))     # Output: Book('1984', 'George Orwell', 328)
    print(len(book1))      # Output: 328

    # Comparison
    print(book1 == book2)  # Output: False
    print(book1 > book2)   # Output: True (328 > 112 pages)

    # Addition
    combined = book1 + book2
    print(combined)        # Output: 1984 & Animal Farm by George Orwell & George Orwell


## Practical Example: A Simple Library Management System

Let's tie everything together with a comprehensive example that demonstrates all OOP concepts:


    from datetime import datetime, timedelta
    from typing import List, Optional

    class LibraryItem:
        """Base class for all library items"""
        _next_id = 1

        def __init__(self, title: str, author: str):
            self.id = LibraryItem._next_id
            LibraryItem._next_id += 1
            self.title = title
            self.author = author
            self.is_checked_out = False
            self.due_date: Optional[datetime] = None
            self.borrower: Optional[str] = None

        def __str__(self):
            status = "Available" if not self.is_checked_out else f"Due: {self.due_date.strftime('%Y-%m-%d')}"
            return f"{self.title} by {self.author} - {status}"

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.title}', '{self.author}')"

        def check_out(self, borrower: str, days: int = 14) -> bool:
            """Check out the item"""
            if self.is_checked_out:
                return False

            self.is_checked_out = True
            self.borrower = borrower
            self.due_date = datetime.now() + timedelta(days=days)
            return True

        def return_item(self) -> bool:
            """Return the item"""
            if not self.is_checked_out:
                return False

            self.is_checked_out = False
            self.borrower = None
            self.due_date = None
            return True

        def is_overdue(self) -> bool:
            """Check if item is overdue"""
            if not self.is_checked_out or not self.due_date:
                return False
            return datetime.now() > self.due_date

    class Book(LibraryItem):
        """Book class with additional properties"""
        def __init__(self, title: str, author: str, isbn: str, pages: int):
            super().__init__(title, author)
            self.isbn = isbn
            self.pages = pages

        def check_out(self, borrower: str, days: int = 21) -> bool:
            """Books can be checked out for 21 days by default"""
            return super().check_out(borrower, days)

    class DVD(LibraryItem):
        """DVD class with shorter checkout period"""
        def __init__(self, title: str, director: str, runtime: int):
            super().__init__(title, director)  # director becomes "author"
            self.director = director
            self.runtime = runtime

        def check_out(self, borrower: str, days: int = 7) -> bool:
            """DVDs can only be checked out for 7 days"""
            return super().check_out(borrower, days)

    class Library:
        """Library management system"""
        def __init__(self, name: str):
            self.name = name
            self._items: List[LibraryItem] = []
            self._members: List[str] = []

        def add_item(self, item: LibraryItem) -> None:
            """Add an item to the library"""
            self._items.append(item)
            print(f"Added: {item}")

        def add_member(self, name: str) -> None:
            """Add a library member"""
            if name not in self._members:
                self._members.append(name)
                print(f"Added member: {name}")

        def search_by_title(self, title: str) -> List[LibraryItem]:
            """Search for items by title"""
            return [item for item in self._items
                    if title.lower() in item.title.lower()]

        def search_by_author(self, author: str) -> List[LibraryItem]:
            """Search for items by author"""
            return [item for item in self._items
                    if author.lower() in item.author.lower()]

        def check_out_item(self, item_id: int, borrower: str) -> bool:
            """Check out an item by ID"""
            if borrower not in self._members:
                print(f"Error: {borrower} is not a library member")
                return False

            item = self._find_item_by_id(item_id)
            if not item:
                print(f"Error: Item with ID {item_id} not found")
                return False

            if item.check_out(borrower):
                print(f"Checked out: {item} to {borrower}")
                return True
            else:
                print(f"Error: {item.title} is already checked out")
                return False

        def return_item(self, item_id: int) -> bool:
            """Return an item by ID"""
            item = self._find_item_by_id(item_id)
            if not item:
                print(f"Error: Item with ID {item_id} not found")
                return False

            if item.return_item():
                print(f"Returned: {item}")
                return True
            else:
                print(f"Error: {item.title} was not checked out")
                return False

        def list_overdue_items(self) -> List[LibraryItem]:
            """Get list of overdue items"""
            return [item for item in self._items if item.is_overdue()]

        def _find_item_by_id(self, item_id: int) -> Optional[LibraryItem]:
            """Private method to find item by ID"""
            for item in self._items:
                if item.id == item_id:
                    return item
            return None

        def display_catalog(self) -> None:
            """Display all items in the library"""
            print(f"\n=== {self.name} Catalog ===")
            for item in self._items:
                print(f"ID {item.id}: {item}")

    # Demo usage
    def main():
        # Create library
        library = Library("City Public Library")

        # Add items
        library.add_item(Book("1984", "George Orwell", "978-0-452-28423-4", 328))
        library.add_item(Book("To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4", 281))
        library.add_item(DVD("The Matrix", "The Wachowskis", 136))
        library.add_item(DVD("Inception", "Christopher Nolan", 148))

        # Add members
        library.add_member("Alice Johnson")
        library.add_member("Bob Smith")

        # Display catalog
        library.display_catalog()

        # Check out items
        library.check_out_item(1, "Alice Johnson")
        library.check_out_item(3, "Bob Smith")

        # Display updated catalog
        library.display_catalog()

        # Search functionality
        print("\n=== Search Results for 'Matrix' ===")
        results = library.search_by_title("Matrix")
        for item in results:
            print(f"ID {item.id}: {item}")

    if __name__ == "__main__":
        main()


This comprehensive example demonstrates:

  * **Classes and Objects** : Multiple classes with different purposes
  * **Encapsulation** : Private methods and controlled access to data
  * **Inheritance** : `Book` and `DVD` inherit from `LibraryItem`
  * **Polymorphism** : All library items can be treated uniformly in lists and methods
  * **Magic Methods** : `__str__`, `__repr__` for better object representation
  * **Real-world modeling** : The system models actual library operations

## Key Takeaways

  1. **Start Simple** : Begin with basic classes and gradually add complexity
  2. **Think in Objects** : Model real-world entities as classes with attributes and behaviors
  3. **Use Inheritance Wisely** : Inherit when there's a genuine "is-a" relationship
  4. **Embrace Encapsulation** : Hide internal details and provide clean interfaces
  5. **Leverage Polymorphism** : Write code that works with multiple types of objects
  6. **Don't Overuse** : Not everything needs to be a class—simple functions are often better for simple tasks

Object-Oriented Programming is a powerful paradigm that becomes more valuable as your programs grow in complexity. Practice these concepts with small projects, and gradually work up to larger applications where OOP's organizational benefits really shine.

Next, let's review [file I/O and data persistence](<https://python.robertdevore.com/blog/file-io-and-data-persistence>)!
