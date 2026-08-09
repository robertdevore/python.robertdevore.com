---
title: "2.2. File I/O & Data Persistence"
description: "Learn to read from and write to files, handle different formats, and make your programs interact with real data that survives after your script ends."
excerpt: "Learn to read from and write to files, handle different formats, and make your programs interact with real data that survives after your script ends."
custom_url: file-io-and-data-persistence
template: docs
section: "Chapter 2 · Intermediate Python"
order: 90
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: intermediate
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /course/object-oriented-programming/
next: /course/virtual-environments-and-package-management/
tags: [python, course]
---
## Overview

Learn to read from and write to files, handle different formats, and make your programs interact with real data that survives after your script ends.

* * *

## Introduction

Data persistence is crucial for any real-world application. Whether you're building a web scraper that saves results, a game that stores high scores, or a data analysis tool that processes CSV files, you need to know how to work with files effectively.

In this chapter, you'll master Python's file handling capabilities, from basic text operations to working with structured data formats like CSV and JSON. You'll also learn how to handle file paths safely across different operating systems and implement robust error handling to prevent crashes when files are missing or inaccessible.

* * *

## Working with Text Files

### Basic File Operations

Python's built-in `open()` function is your gateway to file operations. It returns a file object that you can use to read from or write to files.

```python
# Basic file reading
file = open('example.txt', 'r')
content = file.read()
print(content)
file.close()
```

However, manually managing file closing is error-prone. If an exception occurs before `close()`, the file remains open. The recommended approach uses the `with` statement:

```python
# Proper file handling with context manager
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# File is automatically closed when exiting the 'with' block
```

### File Modes

Understanding file modes is essential for proper file operations:

  * `'r'` \- Read mode (default)
  * `'w'` \- Write mode (overwrites existing content)
  * `'a'` \- Append mode (adds to end of file)
  * `'x'` \- Exclusive creation (fails if file exists)
  * `'b'` \- Binary mode (e.g., `'rb'`, `'wb'`)
  * `'t'` \- Text mode (default)

```python
# Writing to a file
with open('output.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('This is line 2.\n')

# Appending to a file
with open('output.txt', 'a') as file:
    file.write('This line is appended.\n')
```

### Reading Methods

Python offers several methods for reading file content:

```python
# Read entire file as a string
with open('data.txt', 'r') as file:
    content = file.read()

# Read file line by line
with open('data.txt', 'r') as file:
    for line in file:
        print(line.strip())  # strip() removes newline characters

# Read all lines into a list
with open('data.txt', 'r') as file:
    lines = file.readlines()

# Read one line at a time
with open('data.txt', 'r') as file:
    first_line = file.readline()
    second_line = file.readline()
```

### Practical Example: Log File Processor

```python
def process_log_file(filename):
    """Process a log file and extract error messages."""
    errors = []

    with open(filename, 'r') as file:
        for line_num, line in enumerate(file, 1):
            if 'ERROR' in line:
                errors.append({
                    'line_number': line_num,
                    'message': line.strip(),
                    'timestamp': line.split()[0] if line.split() else 'Unknown'
                })

    return errors

# Usage
error_list = process_log_file('application.log')
for error in error_list:
    print(f"Line {error['line_number']}: {error['message']}")
```

* * *

## Handling CSV Files

CSV (Comma-Separated Values) files are ubiquitous in data processing. Python's `csv` module provides powerful tools for reading and writing CSV data.

### Reading CSV Files

```python
import csv

# Basic CSV reading
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)  # Each row is a list of strings

# Reading with headers
def read_csv_with_headers(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = []
        for row in csv_reader:
            data.append(dict(row))  # Each row is a dictionary
        return data

# Example usage
employee_data = read_csv_with_headers('employees.csv')
for employee in employee_data:
    print(f"{employee['Name']}: {employee['Department']}")
```

### Writing CSV Files

```python
import csv

# Writing basic CSV
data = [
    ['Name', 'Age', 'City'],
    ['Alice', '25', 'New York'],
    ['Bob', '30', 'San Francisco'],
    ['Charlie', '35', 'Chicago']
]

with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

# Writing with DictWriter
employees = [
    {'Name': 'Alice', 'Age': 25, 'Department': 'Engineering'},
    {'Name': 'Bob', 'Age': 30, 'Department': 'Marketing'},
    {'Name': 'Charlie', 'Age': 35, 'Department': 'Sales'}
]

with open('employees_output.csv', 'w', newline='') as file:
    fieldnames = ['Name', 'Age', 'Department']
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

    csv_writer.writeheader()  # Write column headers
    csv_writer.writerows(employees)
```

### Advanced CSV Operations

```python
import csv

def analyze_sales_data(filename):
    """Analyze sales data from CSV file."""
    total_sales = 0
    product_sales = {}

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # Convert string to float for calculations
            amount = float(row['Amount'])
            product = row['Product']

            total_sales += amount

            if product in product_sales:
                product_sales[product] += amount
            else:
                product_sales[product] = amount

    return {
        'total_sales': total_sales,
        'product_breakdown': product_sales,
        'top_product': max(product_sales.items(), key=lambda x: x[1])
    }

# Custom CSV dialect for unusual formats
csv.register_dialect('custom', delimiter=';', quotechar='"',
                     doublequote=True, skipinitialspace=True)

with open('european_data.csv', 'r') as file:
    csv_reader = csv.reader(file, dialect='custom')
    for row in csv_reader:
        print(row)
```

* * *

## Reading and Writing JSON

JSON (JavaScript Object Notation) is the standard format for APIs and configuration files. Python's `json` module makes working with JSON data straightforward.

### Basic JSON Operations

```javascript
import json

# Reading JSON from file
with open('config.json', 'r') as file:
    config = json.load(file)
    print(config['database']['host'])

# Writing JSON to file
data = {
    'users': [
        {'name': 'Alice', 'email': 'alice@example.com', 'active': True},
        {'name': 'Bob', 'email': 'bob@example.com', 'active': False}
    ],
    'settings': {
        'theme': 'dark',
        'notifications': True,
        'max_connections': 100
    }
}

with open('users.json', 'w') as file:
    json.dump(data, file, indent=2)  # indent for pretty formatting
```

### JSON String Operations

```python
import json

# Convert Python object to JSON string
python_dict = {'name': 'Alice', 'age': 30, 'skills': ['Python', 'SQL']}
json_string = json.dumps(python_dict, indent=2)
print(json_string)

# Convert JSON string to Python object
json_data = '{"name": "Bob", "age": 25, "active": true}'
python_obj = json.loads(json_data)
print(python_obj['name'])  # Output: Bob
```

### Handling Complex JSON Data

```text
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Data with datetime objects
log_entry = {
    'timestamp': datetime.now(),
    'level': 'INFO',
    'message': 'Application started',
    'user_data': {
        'user_id': 12345,
        'session_start': datetime.now()
    }
}

# Save with custom encoder
with open('log.json', 'w') as file:
    json.dump(log_entry, file, cls=DateTimeEncoder, indent=2)

def load_json_with_error_handling(filename):
    """Load JSON file with comprehensive error handling."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filename}: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error reading {filename}: {e}")
        return {}
```

### Practical Example: Configuration Manager

```python
import json
import os

class ConfigManager:
    """Manage application configuration with JSON files."""

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Invalid configuration file. Using defaults.")
                return self.get_default_config()
        else:
            config = self.get_default_config()
            self.save_config(config)
            return config

    def get_default_config(self):
        """Return default configuration."""
        return {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'myapp'
            },
            'logging': {
                'level': 'INFO',
                'file': 'app.log'
            },
            'features': {
                'email_notifications': True,
                'auto_backup': False
            }
        }

    def save_config(self, config=None):
        """Save configuration to file."""
        config = config or self.config
        with open(self.config_file, 'w') as file:
            json.dump(config, file, indent=2)

    def get(self, key_path, default=None):
        """Get configuration value using dot notation."""
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path, value):
        """Set configuration value using dot notation."""
        keys = key_path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value
        self.save_config()

# Usage
config = ConfigManager()
print(config.get('database.host'))  # localhost
config.set('database.host', '192.168.1.100')
print(config.get('database.host'))  # 192.168.1.100
```

* * *

## File Paths & OS Operations

Working with file paths correctly is crucial for cross-platform compatibility. Python provides several modules for path manipulation.

### Using os.path

```python
import os

# Path operations
current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'data', 'input.txt')
print(f"File path: {file_path}")

# Path information
print(f"Directory: {os.path.dirname(file_path)}")
print(f"Filename: {os.path.basename(file_path)}")
print(f"Extension: {os.path.splitext(file_path)[1]}")

# Check file/directory existence
if os.path.exists(file_path):
    print("File exists")
    print(f"Size: {os.path.getsize(file_path)} bytes")
    print(f"Is file: {os.path.isfile(file_path)}")
    print(f"Is directory: {os.path.isdir(file_path)}")
```

### Modern Path Handling with pathlib

```python
from pathlib import Path

# Modern path operations
current_dir = Path.cwd()
data_dir = current_dir / 'data'
file_path = data_dir / 'input.txt'

print(f"File path: {file_path}")
print(f"Parent directory: {file_path.parent}")
print(f"Filename: {file_path.name}")
print(f"Extension: {file_path.suffix}")

# Check existence and properties
if file_path.exists():
    print(f"Size: {file_path.stat().st_size} bytes")
    print(f"Is file: {file_path.is_file()}")
    print(f"Is directory: {file_path.is_dir()}")

# Create directories
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)  # Create if doesn't exist

# List directory contents
for item in data_dir.iterdir():
    if item.is_file():
        print(f"File: {item.name}")
    elif item.is_dir():
        print(f"Directory: {item.name}")
```

### Cross-Platform File Operations

```python
import os
import shutil
from pathlib import Path

def safe_file_operations():
    """Demonstrate safe, cross-platform file operations."""

    # Create directory structure
    base_dir = Path('project_data')
    subdirs = ['input', 'output', 'temp']

    for subdir in subdirs:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)

    # Copy files safely
    source_file = Path('important_data.txt')
    if source_file.exists():
        destination = base_dir / 'input' / source_file.name
        shutil.copy2(source_file, destination)  # Preserves metadata
        print(f"Copied {source_file} to {destination}")

    # Move files
    temp_file = base_dir / 'temp' / 'temporary.txt'
    if temp_file.exists():
        final_location = base_dir / 'output' / 'final.txt'
        shutil.move(str(temp_file), str(final_location))

    # Remove files and directories
    temp_dir = base_dir / 'temp'
    if temp_dir.exists():
        shutil.rmtree(temp_dir)  # Remove directory and contents

def find_files_by_extension(directory, extension):
    """Find all files with specific extension in directory."""
    directory = Path(directory)
    pattern = f"*.{extension}"
    return list(directory.rglob(pattern))  # Recursive search

# Usage
python_files = find_files_by_extension('.', 'py')
for file in python_files:
    print(file)
```

* * *

## Error Handling with Files

Robust file handling requires anticipating and handling various error conditions.

### Common File Errors

```python
import os
import json

def safe_file_reader(filename):
    """Read file with comprehensive error handling."""
    try:
        with open(filename, 'r') as file:
            return file.read()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    except PermissionError:
        print(f"Error: Permission denied accessing '{filename}'.")
        return None

    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return None

    except Exception as e:
        print(f"Unexpected error reading '{filename}': {e}")
        return None

def safe_json_processor(filename):
    """Process JSON file with error handling."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

        # Process the data
        if 'users' in data:
            for user in data['users']:
                if 'email' not in user:
                    print(f"Warning: User {user.get('name', 'Unknown')} missing email")

        return data

    except FileNotFoundError:
        print(f"Configuration file '{filename}' not found. Creating default.")
        default_config = {'users': [], 'settings': {}}

        try:
            with open(filename, 'w') as file:
                json.dump(default_config, file, indent=2)
            return default_config
        except IOError as e:
            print(f"Could not create default config: {e}")
            return {}

    except json.JSONDecodeError as e:
        print(f"Invalid JSON in '{filename}': {e}")
        print(f"Error at line {e.lineno}, column {e.colno}")
        return {}

    except Exception as e:
        print(f"Unexpected error processing '{filename}': {e}")
        return {}
```

### Validation and Backup Strategies

```python
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

class SafeFileManager:
    """Manage files with backup and validation."""

    def __init__(self, backup_dir='backups'):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def calculate_checksum(self, filepath):
        """Calculate MD5 checksum of file."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except IOError:
            return None

    def backup_file(self, filepath):
        """Create timestamped backup of file."""
        filepath = Path(filepath)
        if not filepath.exists():
            return False

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
        backup_path = self.backup_dir / backup_name

        try:
            shutil.copy2(filepath, backup_path)
            return backup_path
        except IOError as e:
            print(f"Backup failed: {e}")
            return False

    def safe_write(self, filepath, content, backup=True):
        """Write content to file with backup and validation."""
        filepath = Path(filepath)

        # Create backup if file exists
        if backup and filepath.exists():
            backup_path = self.backup_file(filepath)
            if not backup_path:
                return False

        # Write to temporary file first
        temp_path = filepath.with_suffix(filepath.suffix + '.tmp')

        try:
            with open(temp_path, 'w') as file:
                file.write(content)

            # Verify write was successful
            if temp_path.exists() and temp_path.stat().st_size > 0:
                # Replace original file
                shutil.move(str(temp_path), str(filepath))
                return True
            else:
                temp_path.unlink(missing_ok=True)  # Clean up
                return False

        except IOError as e:
            print(f"Write failed: {e}")
            temp_path.unlink(missing_ok=True)  # Clean up
            return False

# Usage
file_manager = SafeFileManager()
success = file_manager.safe_write('important.txt', 'Critical data here')
if success:
    print("File written successfully with backup")
```

* * *

## Best Practices and Summary

### Key Takeaways

  1. **Always use context managers (`with` statements)** for file operations to ensure proper cleanup
  2. **Handle errors explicitly** \- don't let file operations crash your program
  3. **Use`pathlib` for modern path handling** \- it's cleaner and more readable than `os.path`
  4. **Choose the right format** : text files for simple data, CSV for tabular data, JSON for structured data
  5. **Validate and backup important data** before modifying files
  6. **Use appropriate file modes** and understand the difference between text and binary modes

### Common Patterns

```python
# Pattern 1: Safe file processing
def process_data_file(input_file, output_file):
    """Safe pattern for file processing."""
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                processed_line = line.strip().upper()
                outfile.write(processed_line + '\n')
        return True
    except Exception as e:
        print(f"Processing failed: {e}")
        return False

# Pattern 2: Configuration management
def load_config(config_file='config.json', defaults=None):
    """Load configuration with defaults."""
    defaults = defaults or {}

    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return {**defaults, **config}  # Merge with defaults
    except (FileNotFoundError, json.JSONDecodeError):
        return defaults

# Pattern 3: Data export
def export_data(data, filename, format='json'):
    """Export data in multiple formats."""
    try:
        if format == 'json':
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
        elif format == 'csv' and isinstance(data, list):
            with open(filename, 'w', newline='') as file:
                if data and isinstance(data[0], dict):
                    writer = csv.DictWriter(file, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        return True
    except Exception as e:
        print(f"Export failed: {e}")
        return False
```

By mastering these file I/O concepts, you'll be able to build applications that persist data reliably, handle various file formats, and gracefully recover from file-related errors. This foundation is essential for any serious Python development work.

Next, let's cover [virtual environments and package management](<https://python.robertdevore.com/course/virtual-environments-and-package-management>)!
