---
title: "1.1. Python Setup & IDEs"
description: "Welcome to your Python journey! Before we dive into writing code, we need to set up your development environment properly. Think of this as preparing your workspace—just like a carpenter…"
excerpt: "Welcome to your Python journey! Before we dive into writing code, we need to set up your development environment properly. Think of this as preparing your workspace—just like a carpenter…"
custom_url: python-setup-and-ides
template: docs
section: "Chapter 1 · Beginner Python"
order: 30
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: beginner
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /course/chapter-1-beginner-python/
next: /course/python-syntax-and-data-types/
tags: [python, course]
---
## Overview

Welcome to your Python journey! Before we dive into writing code, we need to set up your development environment properly. Think of this as preparing your workspace—just like a carpenter needs the right tools and a clean workbench, you need Python installed and a good code editor to write, run, and debug your programs effectively.

In this chapter, you'll learn how to:

  * Install Python on your computer (Windows, macOS, or Linux)
  * Choose and set up an appropriate IDE or code editor
  * Write and run your first Python script
  * Navigate the command line basics you'll need
  * Troubleshoot common setup issues

By the end of this section, you'll have a fully functional Python development environment and the confidence to start coding immediately.

## Installing Python

Python is free and available for all major operating systems. Let's walk through the installation process for each platform.

### Windows Installation

**Step 1: Download Python**

  1. Visit the official Python website: [python.org](<https://python.org>)
  2. Click "Downloads" and then "Download Python 3.x.x" (where x.x represents the latest version)
  3. The website automatically detects your operating system and suggests the right version

**Step 2: Run the Installer**

  1. Once downloaded, run the installer file (usually named `python-3.x.x-amd64.exe`)
  2. **Important** : Check the box "Add Python to PATH" at the bottom of the installer window
  3. Click "Install Now" for a standard installation, or "Customize installation" if you want specific options
  4. Wait for the installation to complete

**Step 3: Verify Installation**

  1. Open Command Prompt (press `Windows + R`, type `cmd`, press Enter)
  2. Type `python --version` and press Enter
  3. You should see something like `Python 3.11.5` displayed

### macOS Installation

**Method 1: Official Installer (Recommended for Beginners)**

  1. Visit [python.org](<https://python.org>) and download the macOS installer
  2. Run the downloaded `.pkg` file
  3. Follow the installation wizard (default settings are usually fine)
  4. Open Terminal (Applications → Utilities → Terminal)
  5. Type `python3 --version` to verify installation

**Method 2: Using Homebrew (For Advanced Users)** If you have Homebrew installed:

```bash
brew install python
```

**Note** : macOS comes with Python 2.7 pre-installed, but you want Python 3.x for modern development. Always use `python3` command on macOS.

### Linux Installation

Most Linux distributions come with Python pre-installed, but it might be an older version.

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install python3 python3-pip
```

**CentOS/RHEL/Fedora:**

```bash
sudo dnf install python3 python3-pip
```

**Verify installation:**

```python
python3 --version
```

### Python Version Considerations

  * **Use Python 3.8 or newer** : Python 2 is deprecated and no longer supported
  * **Latest stable version** : Generally recommended unless you have specific compatibility requirements
  * **Long-term support** : Python 3.8, 3.9, and 3.10 have extended support periods

## Choosing an IDE or Editor

An Integrated Development Environment (IDE) or code editor is where you'll write your Python code. Here are the most popular options for beginners:

### Visual Studio Code (VS Code) - **Recommended for Beginners**

**Why VS Code?**

  * Free and open-source
  * Excellent Python support with extensions
  * Great balance of features and simplicity
  * Large community and extensive documentation
  * Works on Windows, macOS, and Linux

**Installation:**

  1. Download from [code.visualstudio.com](<https://code.visualstudio.com>)
  2. Install the Python extension by Microsoft
  3. Install the Python Indent extension for better code formatting

**Setting up VS Code for Python:**

  1. Open VS Code
  2. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
  3. Search for "Python" and install the official Microsoft Python extension
  4. Optionally install "Python Indent" and "Python Docstring Generator"

### PyCharm Community Edition

**Why PyCharm?**

  * Professional IDE specifically designed for Python
  * Excellent debugging capabilities
  * Built-in terminal and version control
  * Great for larger projects

**Installation:**

  1. Download from [jetbrains.com/pycharm](<https://www.jetbrains.com/pycharm/>)
  2. Choose Community Edition (free)
  3. Follow the installation wizard

### Thonny - **Best for Absolute Beginners**

**Why Thonny?**

  * Designed specifically for Python beginners
  * Simple, clean interface
  * Built-in Python interpreter
  * Excellent for learning and understanding code execution

**Installation:**

  1. Download from [thonny.org](<https://thonny.org>)
  2. Install and run—it comes with Python built-in!

### Other Popular Options

  * **IDLE** : Comes with Python installation, very basic but sufficient for simple scripts
  * **Sublime Text** : Fast and lightweight, good for experienced users
  * **Atom** : Hackable text editor (note: GitHub has sunset Atom as of 2022)
  * **Vim/Neovim** : For advanced users who prefer terminal-based editing

### Making Your Choice

For beginners, I recommend this progression:

  1. **Start with Thonny** if you're completely new to programming
  2. **Move to VS Code** as you become more comfortable
  3. **Consider PyCharm** when working on larger projects

## First Script: "Hello, World!"

Now let's write your first Python program! This is a tradition in programming—every programmer's first program displays "Hello, World!" on the screen.

### Using Your Chosen Editor

**Step 1: Create a New File**

  1. Open your chosen editor (VS Code, PyCharm, Thonny, etc.)
  2. Create a new file
  3. Save it as `hello.py` (the `.py` extension tells the computer this is a Python file)

**Step 2: Write Your First Code** Type the following code exactly as shown:

```python
print("Hello, World!")
```

**Step 3: Run Your Program**

**In VS Code:**

  1. Open the terminal (Terminal → New Terminal)
  2. Type `python hello.py` (or `python3 hello.py` on macOS/Linux)
  3. Press Enter

**In PyCharm:**

  1. Right-click on your file and select "Run 'hello'"
  2. Or press Ctrl+Shift+F10 (Cmd+Shift+R on macOS)

**In Thonny:**

  1. Click the green "Run" button or press F5

**Expected Output:**

```text
Hello, World!
```

Congratulations! You've just written and executed your first Python program!

### Understanding Your First Program

Let's break down what happened:

  * `print()` is a **function** that displays text on the screen
  * `"Hello, World!"` is a **string** (text data) enclosed in quotation marks
  * The parentheses `()` are required to call the function
  * Python executes the code line by line, from top to bottom

### Experiment with Variations

Try modifying your program:

```python
print("Hello, World!")
print("Welcome to Python programming!")
print("My name is", "Python Student")
```

Or with variables:

```python
name = "Python Student"
print("Hello, my name is", name)
```

## Command Line Basics

The command line (also called terminal, command prompt, or shell) is a text-based interface for interacting with your computer. While modern computers rely heavily on graphical interfaces, the command line remains essential for programming.

### Opening the Command Line

**Windows:**

  * Press `Windows + R`, type `cmd`, press Enter
  * Or search for "Command Prompt" in the Start menu

**macOS:**

  * Press `Cmd + Space`, type "Terminal", press Enter
  * Or go to Applications → Utilities → Terminal

**Linux:**

  * Press `Ctrl + Alt + T`
  * Or search for "Terminal" in your applications

### Essential Commands

Here are the most important commands you'll need:

**Navigation:**

```python
# See your current location
pwd                    # "print working directory"

# List files and folders
ls                     # macOS/Linux
dir                    # Windows

# Change directory
cd Desktop            # Go to Desktop folder
cd ..                 # Go up one level
cd /                  # Go to root directory (macOS/Linux)
cd \                  # Go to root directory (Windows)
```

**File Operations:**

```python
# Create a new directory
mkdir my_python_projects

# Create a new file (macOS/Linux)
touch hello.py

# Create a new file (Windows)
type nul > hello.py
```

**Running Python:**

```python
# Run a Python file
python hello.py        # Windows
python3 hello.py       # macOS/Linux

# Start interactive Python
python                 # Windows
python3                # macOS/Linux

# Exit interactive Python
exit()
```

### Interactive Python Shell

The Python shell (REPL - Read-Eval-Print Loop) lets you type Python code and see results immediately:

```bash
$ python3
Python 3.11.5 (main, Aug 24 2023, 15:18:16)
>>> print("Hello from the shell!")
Hello from the shell!
>>> 2 + 3
5
>>> name = "Python"
>>> print(f"I'm learning {name}!")
I'm learning Python!
>>> exit()
```

This is excellent for testing small pieces of code and learning Python interactively.

## Troubleshooting Setup Issues

Even with careful installation, you might encounter some common issues. Here are solutions to the most frequent problems:

### Problem 1: "python is not recognized" or "command not found"

**Symptoms:**

  * Typing `python` in the command line gives an error
  * Error message: "'python' is not recognized as an internal or external command"

**Solution:** This means Python is not in your system's PATH.

**Windows:**

  1. Search for "Environment Variables" in Start menu
  2. Click "Edit the system environment variables"
  3. Click "Environment Variables"
  4. Under "System Variables," find "Path" and click "Edit"
  5. Click "New" and add the Python installation directory (usually `C:\Python3x\` and `C:\Python3x\Scripts\`)
  6. Click OK and restart your command prompt

**macOS/Linux:** Add this line to your `.bashrc` or `.zshrc` file:

```bash
export PATH="/usr/local/bin/python3:$PATH"
```

### Problem 2: Multiple Python Versions

**Symptoms:**

  * `python --version` shows Python 2.7
  * Confusion about which Python is running

**Solution:** Use specific version commands:

```python
python3 --version    # For Python 3
python2 --version    # For Python 2 (if installed)
```

Always use `python3` for your development work.

### Problem 3: Permission Errors

**Symptoms:**

  * "Permission denied" when installing packages
  * Cannot write to certain directories

**Solution:** **Windows:** Run Command Prompt as Administrator** macOS/Linux:** Use `sudo` carefully:

```bash
sudo python3 -m pip install package_name
```

Better solution: Use virtual environments (covered in later chapters).

### Problem 4: IDE Not Recognizing Python

**Symptoms:**

  * VS Code or PyCharm shows "Python interpreter not found"
  * Syntax highlighting not working

**Solution:** **VS Code:**

  1. Press `Ctrl+Shift+P` (Cmd+Shift+P on macOS)
  2. Type "Python: Select Interpreter"
  3. Choose the correct Python installation

**PyCharm:**

  1. Go to File → Settings → Project → Python Interpreter
  2. Click the gear icon and "Add"
  3. Select your Python installation

### Problem 5: Firewall or Antivirus Blocking

**Symptoms:**

  * Installation fails or is very slow
  * Cannot download packages later

**Solution:**

  1. Temporarily disable antivirus during installation
  2. Add Python to your antivirus exceptions
  3. Check if corporate firewall is blocking downloads

### Getting Help

When you encounter issues:

  1. **Read error messages carefully** \- they often contain the solution
  2. **Check the official Python documentation** at [docs.python.org](<https://docs.python.org>)
  3. **Search Stack Overflow** \- most Python questions have been asked before
  4. **Use Python's built-in help** : Type `help()` in the Python shell
  5. **Ask for help** on Python communities like Reddit's r/learnpython

## Verifying Your Setup

Before moving on, let's make sure everything is working correctly:

### Checklist

  1. **Python Installation:**

```python
    python --version        # Should show Python 3.8+
python3 --version       # On macOS/Linux
```

  2. **Package Manager (pip):**

```bash
    pip --version           # Should show pip version
pip3 --version          # On macOS/Linux
```

  3. **Your Editor:**

```python
 * Can create and save `.py` files
 * Syntax highlighting works
 * Can run Python scripts
```

  4. **Command Line:**

```python
 * Can navigate directories
 * Can run Python files
 * Can access interactive Python shell
```

### Final Test Script

Create a file called `test_setup.py` and add this code:

```python
import sys
import os

print("Python Setup Test")
print("=" * 20)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Platform: {sys.platform}")
print("=" * 20)
print("Setup test completed successfully!")
```

Run this script. If it executes without errors and shows your Python version information, your setup is complete!

## Next Steps

Congratulations! You now have a fully functional Python development environment. Here's what you've accomplished:

  * ✅ Installed Python on your system
  * ✅ Chose and configured a code editor
  * ✅ Written and run your first Python program
  * ✅ Learned essential command line skills
  * ✅ Troubleshooted common setup issues

In the next section ([1.2 Syntax & Data Types](<https://python.robertdevore.com/course/syntax-and-data-types>)), you'll start learning Python's core language features. You'll discover how to work with different types of data, create variables, and write more complex programs.

**Recommended Practice:**

  * Experiment with the `print()` function
  * Try running Python in interactive mode
  * Create a few more simple `.py` files
  * Get comfortable with your chosen editor's features

Remember: every expert programmer started exactly where you are now. The key is consistent practice and patience with yourself as you learn. You've taken the most important step—you're ready to code!
