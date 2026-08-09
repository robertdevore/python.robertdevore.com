---
title: "3.3. Concurrency & Parallelism"
description: "Modern applications demand speed and responsiveness. Users expect web pages to load quickly, data processing to happen in real-time, and interfaces to remain interactive even during…"
excerpt: "Modern applications demand speed and responsiveness. Users expect web pages to load quickly, data processing to happen in real-time, and interfaces to remain interactive even during…"
custom_url: concurrency-and-parallelism
template: docs
section: "Chapter 3 · Advanced Python"
order: 160
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: advanced
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /course/generators-decorators-and-context-managers/
next: /course/building-and-consuming-apis/
tags: [python, course]
---
## Overview

Modern applications demand speed and responsiveness. Users expect web pages to load quickly, data processing to happen in real-time, and interfaces to remain interactive even during heavy computations. The key to achieving this lies in understanding and implementing **concurrency** and **parallelism** —two fundamental approaches to running multiple operations simultaneously.

In this chapter, you'll master Python's powerful concurrency and parallelism tools: threading for I/O-bound tasks, multiprocessing for CPU-intensive work, and async programming for handling thousands of concurrent operations efficiently. By the end, you'll know exactly when and how to apply each approach to make your applications faster, more responsive, and capable of handling real-world scale.

* * *

## **Concurrency vs. Parallelism Explained**

Before diving into implementation, it's crucial to understand the fundamental difference between concurrency and parallelism—concepts that are often confused but serve different purposes.

### **Concurrency: Dealing with Many Things at Once**

Concurrency is about **structure** —organizing your program to handle multiple tasks by rapidly switching between them. Think of a single chef in a kitchen managing multiple dishes: they start the pasta water, while it heats they chop vegetables, then check the pasta, season the sauce, and so on. Only one task happens at any instant, but by intelligent task switching, multiple dishes progress simultaneously.

```python
import time
import threading

def cook_pasta():
    print("Starting pasta water...")
    time.sleep(2)  # Water heating
    print("Adding pasta...")
    time.sleep(5)  # Cooking time
    print("Pasta ready!")

def prepare_sauce():
    print("Chopping vegetables...")
    time.sleep(3)  # Prep time
    print("Cooking sauce...")
    time.sleep(4)  # Sauce cooking
    print("Sauce ready!")

# Sequential approach - takes 14 seconds total
start_time = time.time()
cook_pasta()
prepare_sauce()
print(f"Sequential cooking took {time.time() - start_time:.1f} seconds")
```

### **Parallelism: Doing Many Things at Once**

Parallelism is about **execution** —literally performing multiple operations simultaneously using multiple processing units. This is like having two chefs working in parallel kitchens, each preparing different dishes at exactly the same time.

```python
import multiprocessing
import time

def cpu_intensive_task(n):
    """Simulate CPU-bound work"""
    result = 0
    for i in range(n * 1000000):
        result += i * i
    return result

# Sequential execution
start_time = time.time()
results = [cpu_intensive_task(100), cpu_intensive_task(100), cpu_intensive_task(100)]
sequential_time = time.time() - start_time

# Parallel execution
start_time = time.time()
with multiprocessing.Pool() as pool:
    results = pool.map(cpu_intensive_task, [100, 100, 100])
parallel_time = time.time() - start_time

print(f"Sequential: {sequential_time:.2f}s")
print(f"Parallel: {parallel_time:.2f}s")
print(f"Speedup: {sequential_time/parallel_time:.1f}x")
```

### **When to Use Each Approach**

**Use Concurrency (Threading/Async) for I/O-bound tasks:**

  * Web scraping and API calls
  * File operations and database queries
  * Network requests and socket programming
  * User interface responsiveness

**Use Parallelism (Multiprocessing) for CPU-bound tasks:**

  * Mathematical computations
  * Image/video processing
  * Data analysis and machine learning
  * Cryptographic operations

* * *

## **Threading with the`threading` Module**

Python's `threading` module enables concurrent execution within a single process, making it perfect for I/O-bound operations where your program spends time waiting for external resources.

### **Basic Threading Concepts**

```python
import threading
import time
import requests

def download_url(url, name):
    """Download content from a URL"""
    print(f"Starting download: {name}")
    start_time = time.time()

    response = requests.get(url)
    download_time = time.time() - start_time

    print(f"Finished {name}: {len(response.content)} bytes in {download_time:.2f}s")
    return len(response.content)

# List of URLs to download
urls = [
    ("https://httpbin.org/delay/1", "Site 1"),
    ("https://httpbin.org/delay/2", "Site 2"),
    ("https://httpbin.org/delay/1", "Site 3"),
]

# Sequential downloads
print("=== Sequential Downloads ===")
start_time = time.time()
for url, name in urls:
    download_url(url, name)
sequential_time = time.time() - start_time

# Concurrent downloads with threading
print("\n=== Concurrent Downloads ===")
start_time = time.time()
threads = []

for url, name in urls:
    thread = threading.Thread(target=download_url, args=(url, name))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

concurrent_time = time.time() - start_time

print(f"\nSequential time: {sequential_time:.2f}s")
print(f"Concurrent time: {concurrent_time:.2f}s")
print(f"Speedup: {sequential_time/concurrent_time:.1f}x")
```

### **Thread Safety and Synchronization**

When multiple threads access shared data, you need synchronization mechanisms to prevent race conditions:

```python
import threading
import time
import random

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = threading.Lock()  # Thread-safe locking

    def deposit(self, amount):
        with self.lock:  # Acquire lock before modifying balance
            current_balance = self.balance
            time.sleep(0.001)  # Simulate processing time
            self.balance = current_balance + amount
            print(f"Deposited ${amount}, Balance: ${self.balance}")

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                current_balance = self.balance
                time.sleep(0.001)  # Simulate processing time
                self.balance = current_balance - amount
                print(f"Withdrew ${amount}, Balance: ${self.balance}")
                return True
            else:
                print(f"Insufficient funds for ${amount}")
                return False

# Demonstrate thread safety
account = BankAccount(1000)

def random_transactions(account, num_transactions):
    for _ in range(num_transactions):
        if random.choice([True, False]):
            account.deposit(random.randint(10, 100))
        else:
            account.withdraw(random.randint(10, 100))

# Create multiple threads performing transactions
threads = []
for i in range(3):
    thread = threading.Thread(target=random_transactions, args=(account, 5))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Final balance: ${account.balance}")
```

### **Producer-Consumer Pattern with Queue**

The `queue` module provides thread-safe data structures perfect for coordinating work between threads:

```python
import threading
import queue
import time
import random

def producer(q, name, num_items):
    """Produce items and put them in the queue"""
    for i in range(num_items):
        item = f"{name}-item-{i}"
        q.put(item)
        print(f"Producer {name} created: {item}")
        time.sleep(random.uniform(0.1, 0.5))

    # Signal completion
    q.put(None)
    print(f"Producer {name} finished")

def consumer(q, name):
    """Consume items from the queue"""
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break

        print(f"Consumer {name} processing: {item}")
        time.sleep(random.uniform(0.2, 0.8))  # Simulate processing
        q.task_done()

    print(f"Consumer {name} finished")

# Create a thread-safe queue
work_queue = queue.Queue()

# Start producers and consumers
producers = []
consumers = []

# Create producer threads
for i in range(2):
    p = threading.Thread(target=producer, args=(work_queue, f"P{i}", 5))
    producers.append(p)
    p.start()

# Create consumer threads
for i in range(3):
    c = threading.Thread(target=consumer, args=(work_queue, f"C{i}"))
    consumers.append(c)
    c.start()

# Wait for all producers to finish
for p in producers:
    p.join()

# Signal consumers to stop
for _ in consumers:
    work_queue.put(None)

# Wait for all consumers to finish
for c in consumers:
    c.join()

print("All work completed!")
```

* * *

## **Multiprocessing with the`multiprocessing` Module**

When you need true parallelism for CPU-intensive tasks, multiprocessing creates separate Python processes that can run simultaneously on multiple CPU cores.

### **Basic Process Creation**

```python
import multiprocessing
import time
import os

def cpu_intensive_function(n, name):
    """CPU-bound task that benefits from parallel execution"""
    print(f"Process {name} (PID: {os.getpid()}) starting calculation...")

    # Simulate intensive computation
    result = 0
    for i in range(n):
        result += i ** 2

    print(f"Process {name} completed: {result}")
    return result

if __name__ == "__main__":
    # Sequential execution
    print("=== Sequential Execution ===")
    start_time = time.time()
    results = []
    for i in range(4):
        result = cpu_intensive_function(1000000, f"Sequential-{i}")
        results.append(result)
    sequential_time = time.time() - start_time

    # Parallel execution
    print("\n=== Parallel Execution ===")
    start_time = time.time()

    processes = []
    for i in range(4):
        p = multiprocessing.Process(
            target=cpu_intensive_function,
            args=(1000000, f"Parallel-{i}")
        )
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    parallel_time = time.time() - start_time

    print(f"\nSequential time: {sequential_time:.2f}s")
    print(f"Parallel time: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time/parallel_time:.1f}x")
```

### **Process Pools for Scalable Parallel Processing**

Process pools manage worker processes automatically, making parallel programming much simpler:

```python
import multiprocessing
import time
import math

def is_prime(n):
    """Check if a number is prime (CPU-intensive)"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def find_primes_in_range(start, end):
    """Find all prime numbers in a given range"""
    primes = []
    for num in range(start, end):
        if is_prime(num):
            primes.append(num)
    return primes

if __name__ == "__main__":
    # Define ranges to check for primes
    ranges = [(1000, 2000), (2000, 3000), (3000, 4000), (4000, 5000)]

    # Sequential processing
    print("=== Sequential Prime Finding ===")
    start_time = time.time()
    all_primes = []
    for start, end in ranges:
        primes = find_primes_in_range(start, end)
        all_primes.extend(primes)
    sequential_time = time.time() - start_time

    # Parallel processing with Pool
    print("=== Parallel Prime Finding ===")
    start_time = time.time()

    with multiprocessing.Pool() as pool:
        # Use starmap to pass multiple arguments to each worker
        results = pool.starmap(find_primes_in_range, ranges)
        # Flatten the results
        parallel_primes = [prime for sublist in results for prime in sublist]

    parallel_time = time.time() - start_time

    print(f"Found {len(all_primes)} primes")
    print(f"Sequential time: {sequential_time:.2f}s")
    print(f"Parallel time: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time/parallel_time:.1f}x")
```

### **Inter-Process Communication**

Processes don't share memory by default, so you need special mechanisms for communication:

```python
import multiprocessing
import time
import random

def worker_with_queue(work_queue, result_queue, worker_id):
    """Worker process that processes items from a queue"""
    while True:
        try:
            # Get work item with timeout
            item = work_queue.get(timeout=1)
            if item is None:  # Poison pill to stop worker
                break

            # Simulate work
            result = item ** 2
            time.sleep(random.uniform(0.1, 0.3))

            # Send result back
            result_queue.put((worker_id, item, result))
            print(f"Worker {worker_id}: {item}² = {result}")

        except:
            break  # Timeout or error, exit worker

def monitor_results(result_queue, expected_results):
    """Monitor and collect results from workers"""
    results = []
    while len(results) < expected_results:
        try:
            result = result_queue.get(timeout=5)
            results.append(result)
        except:
            break
    return results

if __name__ == "__main__":
    # Create queues for communication
    work_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Add work items
    work_items = list(range(1, 21))  # Numbers 1-20
    for item in work_items:
        work_queue.put(item)

    # Start worker processes
    num_workers = 4
    workers = []

    for i in range(num_workers):
        p = multiprocessing.Process(
            target=worker_with_queue,
            args=(work_queue, result_queue, i)
        )
        workers.append(p)
        p.start()

    # Monitor results in main process
    results = monitor_results(result_queue, len(work_items))

    # Signal workers to stop
    for _ in range(num_workers):
        work_queue.put(None)  # Poison pill

    # Wait for workers to finish
    for p in workers:
        p.join()

    # Display results
    print(f"\nCollected {len(results)} results:")
    for worker_id, original, squared in sorted(results, key=lambda x: x[1]):
        print(f"Worker {worker_id}: {original}² = {squared}")
```

* * *

## **Async Programming with`asyncio`**

Async programming shines when dealing with I/O-bound operations, allowing you to handle thousands of concurrent operations efficiently without the overhead of threads or processes.

### **Understanding Async/Await**

```javascript
import asyncio
import aiohttp
import time

async def fetch_url(session, url, name):
    """Asynchronously fetch content from a URL"""
    print(f"Starting fetch: {name}")
    start_time = time.time()

    async with session.get(url) as response:
        content = await response.text()
        fetch_time = time.time() - start_time

        print(f"Finished {name}: {len(content)} chars in {fetch_time:.2f}s")
        return len(content)

async def main():
    # URLs to fetch
    urls = [
        ("https://httpbin.org/delay/1", "Site 1"),
        ("https://httpbin.org/delay/2", "Site 2"),
        ("https://httpbin.org/delay/1", "Site 3"),
        ("https://httpbin.org/delay/3", "Site 4"),
    ]

    # Create a session for connection pooling
    async with aiohttp.ClientSession() as session:
        start_time = time.time()

        # Create tasks for concurrent execution
        tasks = [fetch_url(session, url, name) for url, name in urls]

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)

        total_time = time.time() - start_time
        print(f"\nTotal time: {total_time:.2f}s")
        print(f"Total content: {sum(results)} characters")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```

### **Async Context Managers and Iterators**

```python
import asyncio
import aiofiles
import json

class AsyncDataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.file = await aiofiles.open(self.filename, 'w')
        print(f"Opened file: {self.filename}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.file:
            await self.file.close()
            print(f"Closed file: {self.filename}")

    async def process_data(self, data):
        """Process and write data asynchronously"""
        json_data = json.dumps(data) + '\n'
        await self.file.write(json_data)
        await asyncio.sleep(0.1)  # Simulate processing time

async def generate_data():
    """Async generator that yields data"""
    for i in range(10):
        await asyncio.sleep(0.1)  # Simulate data generation delay
        yield {"id": i, "value": i ** 2, "timestamp": time.time()}

async def process_stream():
    """Process streaming data asynchronously"""
    async with AsyncDataProcessor("async_data.json") as processor:
        async for data in generate_data():
            print(f"Processing: {data}")
            await processor.process_data(data)

if __name__ == "__main__":
    asyncio.run(process_stream())
```

* * *

## **Common Pitfalls & The Global Interpreter Lock (GIL)**

### **Understanding the GIL**

Python's Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously. This means:

  * **Threading doesn't provide true parallelism for CPU-bound tasks**
  * **Threading is excellent for I/O-bound tasks** (GIL is released during I/O operations)
  * **Multiprocessing bypasses the GIL** by using separate processes

```python
import threading
import multiprocessing
import time

def cpu_bound_task(n):
    """CPU-intensive task affected by GIL"""
    count = 0
    for i in range(n):
        count += i * i
    return count

def demonstrate_gil_impact():
    n = 5000000

    # Single-threaded baseline
    start_time = time.time()
    result = cpu_bound_task(n)
    single_time = time.time() - start_time

    # Multi-threaded (limited by GIL)
    start_time = time.time()
    threads = []
    for _ in range(2):
        t = threading.Thread(target=cpu_bound_task, args=(n//2,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    thread_time = time.time() - start_time

    # Multi-process (bypasses GIL)
    start_time = time.time()
    with multiprocessing.Pool(2) as pool:
        pool.map(cpu_bound_task, [n//2, n//2])
    process_time = time.time() - start_time

    print(f"Single-threaded: {single_time:.2f}s")
    print(f"Multi-threaded: {thread_time:.2f}s (Speedup: {single_time/thread_time:.1f}x)")
    print(f"Multi-process: {process_time:.2f}s (Speedup: {single_time/process_time:.1f}x)")

if __name__ == "__main__":
    demonstrate_gil_impact()
```

### **Common Pitfalls and Solutions**

  1. **Race Conditions** : Always use locks for shared mutable state
  2. **Deadlocks** : Avoid circular lock dependencies
  3. **Resource Leaks** : Use context managers and proper cleanup
  4. **Overhead** : Don't use concurrency for trivial tasks

* * *

## **Practical Project: Async Web Scraper**

Let's build a comprehensive web scraper that demonstrates real-world async programming:

```python
import asyncio
import aiohttp
import aiofiles
import time
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import List, Set
import json

@dataclass
class ScrapedPage:
    url: str
    title: str
    links: List[str]
    status_code: int
    content_length: int
    load_time: float

class AsyncWebScraper:
    def __init__(self, max_concurrent=10, delay=1.0):
        self.max_concurrent = max_concurrent
        self.delay = delay
        self.session = None
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def scrape_page(self, url: str) -> ScrapedPage:
        """Scrape a single page"""
        async with self.semaphore:  # Limit concurrent requests
            start_time = time.time()

            try:
                async with self.session.get(url) as response:
                    content = await response.text()
                    load_time = time.time() - start_time

                    # Extract title (simplified)
                    title = "No Title"
                    if "<title>" in content:
                        start = content.find("<title>") + 7
                        end = content.find("</title>", start)
                        if end > start:
                            title = content[start:end].strip()

                    # Extract links (simplified)
                    links = []
                    import re
                    link_pattern = r'<a\s+href=["\']([^"\']+)["\']'
                    for match in re.finditer(link_pattern, content):
                        link = urljoin(url, match.group(1))
                        links.append(link)

                    page = ScrapedPage(
                        url=url,
                        title=title,
                        links=links[:10],  # Limit to first 10 links
                        status_code=response.status,
                        content_length=len(content),
                        load_time=load_time
                    )

                    print(f"Scraped: {url} ({response.status}) - {title}")
                    await asyncio.sleep(self.delay)  # Rate limiting
                    return page

            except Exception as e:
                print(f"Error scraping {url}: {e}")
                return ScrapedPage(url, "Error", [], 0, 0, 0)

    async def scrape_multiple(self, urls: List[str]) -> List[ScrapedPage]:
        """Scrape multiple pages concurrently"""
        tasks = [self.scrape_page(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def save_results(self, pages: List[ScrapedPage], filename: str):
        """Save results to JSON file"""
        data = []
        for page in pages:
            if isinstance(page, ScrapedPage):
                data.append({
                    'url': page.url,
                    'title': page.title,
                    'links_count': len(page.links),
                    'status_code': page.status_code,
                    'content_length': page.content_length,
                    'load_time': page.load_time
                })

        async with aiofiles.open(filename, 'w') as f:
            await f.write(json.dumps(data, indent=2))

        print(f"Results saved to {filename}")

async def main():
    """Main scraping function"""
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
    ]

    start_time = time.time()

    async with AsyncWebScraper(max_concurrent=3, delay=0.5) as scraper:
        print(f"Starting to scrape {len(urls)} URLs...")
        pages = await scraper.scrape_multiple(urls)
        await scraper.save_results(pages, "scraping_results.json")

    total_time = time.time() - start_time
    successful_pages = sum(1 for p in pages if isinstance(p, ScrapedPage) and p.status_code == 200)

    print(f"\nScraping completed in {total_time:.2f} seconds")
    print(f"Successfully scraped {successful_pages}/{len(urls)} pages")
    print(f"Average time per page: {total_time/len(urls):.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
```

## **Conclusion**

Mastering concurrency and parallelism is essential for building modern, efficient Python applications. Remember these key principles:

  * **Use threading for I/O-bound tasks** where you're waiting for external resources
  * **Use multiprocessing for CPU-bound tasks** that can benefit from parallel execution
  * **Use async/await for handling many concurrent I/O operations** efficiently
  * **Always consider the GIL's impact** when choosing between threading and multiprocessing
  * **Implement proper error handling and resource management** in concurrent code

The techniques you've learned here form the foundation for building scalable, responsive applications that can handle real-world performance demands. Practice with different scenarios, measure performance improvements, and always profile your code to ensure your concurrency choices are actually improving performance rather than adding unnecessary complexity.

Now, let's dive into [building and consuming API's](<https://python.robertdevore.com/course/building-and-consuming-apis>)!
