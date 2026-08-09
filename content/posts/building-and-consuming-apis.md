---
title: "3.4. Building and Consuming APIs"
description: "APIs (Application Programming Interfaces) are the backbone of modern software development, enabling applications to communicate with each other over the internet. In this chapter, you'll…"
excerpt: "APIs (Application Programming Interfaces) are the backbone of modern software development, enabling applications to communicate with each other over the internet. In this chapter, you'll…"
custom_url: building-and-consuming-apis
template: docs
section: "Chapter 3 · Advanced Python"
order: 170
date: 2025-06-17
author: Robert DeVore
audience: Python learners
difficulty: advanced
status: stable
version: complete course
prerequisites:
  - "Complete the previous lesson in the course path"
previous: /blog/concurrency-and-parallelism/
next: /blog/packaging-distribution-and-best-practices/
tags: [python, course]
---
## Overview

APIs (Application Programming Interfaces) are the backbone of modern software development, enabling applications to communicate with each other over the internet. In this chapter, you'll master both sides of API development: building robust REST APIs using Flask and FastAPI, and consuming external APIs to integrate powerful third-party services into your applications.

* * *

## What is an API?

An **API (Application Programming Interface)** is a set of rules and protocols that allows different software applications to communicate with each other. Think of it as a waiter in a restaurant—you (the client) don't need to know how the kitchen works, but you can order food through the waiter (API), who communicates your request to the kitchen (server) and brings back your meal (response).

**REST (Representational State Transfer)** is an architectural style for designing networked applications. RESTful APIs use standard HTTP methods and are stateless, meaning each request contains all the information needed to process it.

### Key REST Principles:

  * **Stateless** : Each request is independent
  * **Resource-based** : URLs represent resources (e.g., `/users/123`)
  * **HTTP Methods** : Use standard verbs (GET, POST, PUT, DELETE)
  * **JSON** : Commonly used data format for requests and responses

* * *

## HTTP Methods & Status Codes

Understanding HTTP methods and status codes is crucial for API development:

### HTTP Methods:

  * **GET** : Retrieve data (e.g., get user information)
  * **POST** : Create new resources (e.g., create a new user)
  * **PUT** : Update entire resources (e.g., update all user fields)
  * **PATCH** : Partially update resources (e.g., update user's email only)
  * **DELETE** : Remove resources (e.g., delete a user)

### Common Status Codes:

  * **200 OK** : Request successful
  * **201 Created** : Resource created successfully
  * **400 Bad Request** : Invalid request data
  * **401 Unauthorized** : Authentication required
  * **403 Forbidden** : Access denied
  * **404 Not Found** : Resource doesn't exist
  * **500 Internal Server Error** : Server error

* * *

## Creating a Simple REST API with Flask

Flask is a lightweight, flexible web framework perfect for building APIs. Let's create a Todo API to demonstrate core concepts.

### Setting Up Flask

First, install Flask in your virtual environment:

```bash
pip install flask flask-cors
```

### Basic Flask API Structure

```python
# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# In-memory data store (use a database in production)
todos = []

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify({
        'todos': todos,
        'count': len(todos)
    })

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()

    # Basic validation
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    todo = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.utcnow().isoformat()
    }

    todos.append(todo)
    return jsonify(todo), 201

@app.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo)

@app.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Update fields
    todo['title'] = data.get('title', todo['title'])
    todo['description'] = data.get('description', todo['description'])
    todo['completed'] = data.get('completed', todo['completed'])

    return jsonify(todo)

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Run your API:

```python
python app.py
```

Test it with curl or a tool like Postman:

```python
# Create a todo
curl -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask APIs", "description": "Build awesome APIs"}'

# Get all todos
curl http://localhost:5000/todos
```

* * *

## Introduction to FastAPI

FastAPI is a modern, high-performance web framework that automatically generates API documentation and provides excellent type safety. It's built on Python 3.6+ type hints.

### Setting Up FastAPI

```bash
pip install fastapi uvicorn python-multipart
```

### FastAPI Todo API

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime

class TodoResponse(BaseModel):
    todos: List[Todo]
    count: int

# In-memory storage
todos_db = []

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

@app.get("/todos", response_model=TodoResponse)
async def get_todos():
    """Get all todos"""
    return TodoResponse(todos=todos_db, count=len(todos_db))

@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo_data: TodoCreate):
    """Create a new todo"""
    todo = Todo(
        id=str(uuid.uuid4()),
        title=todo_data.title,
        description=todo_data.description or "",
        completed=False,
        created_at=datetime.utcnow()
    )
    todos_db.append(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    """Get a specific todo by ID"""
    todo = next((t for t in todos_db if t.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    """Update a todo"""
    todo = next((t for t in todos_db if t.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update only provided fields
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed

    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo"""
    global todos_db
    original_count = len(todos_db)
    todos_db = [t for t in todos_db if t.id != todo_id]

    if len(todos_db) == original_count:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

FastAPI automatically generates interactive documentation at `http://localhost:8000/docs`.

* * *

## Data Validation & Serialization

### Flask with Marshmallow

For Flask, use Marshmallow for data validation:

```bash
pip install marshmallow



from marshmallow import Schema, fields, validate, ValidationError

class TodoSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

@app.route('/todos', methods=['POST'])
def create_todo():
    try:
        data = todo_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Create todo with validated data
    # ... rest of the logic
```

### FastAPI with Pydantic

FastAPI uses Pydantic models (shown earlier) for automatic validation:

```python
from pydantic import BaseModel, Field, validator

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

* * *

## Authentication & Security

### API Key Authentication

```python
# Flask example
from functools import wraps

API_KEYS = {'your-secret-key': 'user1'}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key not in API_KEYS:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/todos', methods=['POST'])
@require_api_key
def create_todo():
    # Protected endpoint
    pass
```

### JWT Authentication (FastAPI)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/todos", response_model=Todo)
async def create_todo(todo_data: TodoCreate, user=Depends(verify_token)):
    # Protected endpoint
    pass
```

* * *

## Consuming APIs with Python

Use the `requests` library to consume external APIs:

```bash
pip install requests
```

### Basic API Client

```python
import requests
from typing import Dict, List, Optional

class TodoAPIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'X-API-Key': api_key})

    def get_todos(self) -> List[Dict]:
        """Get all todos"""
        response = self.session.get(f"{self.base_url}/todos")
        response.raise_for_status()
        return response.json()['todos']

    def create_todo(self, title: str, description: str = "") -> Dict:
        """Create a new todo"""
        data = {'title': title, 'description': description}
        response = self.session.post(f"{self.base_url}/todos", json=data)
        response.raise_for_status()
        return response.json()

    def update_todo(self, todo_id: str, **kwargs) -> Dict:
        """Update a todo"""
        response = self.session.put(f"{self.base_url}/todos/{todo_id}", json=kwargs)
        response.raise_for_status()
        return response.json()

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo"""
        response = self.session.delete(f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return True

# Usage example
client = TodoAPIClient("http://localhost:8000")

# Create a todo
new_todo = client.create_todo("Learn API consumption", "Master REST APIs")
print(f"Created todo: {new_todo['id']}")

# Get all todos
todos = client.get_todos()
print(f"Total todos: {len(todos)}")

# Update todo
updated = client.update_todo(new_todo['id'], completed=True)
print(f"Todo completed: {updated['completed']}")
```

### Async API Client

For high-performance applications, use `httpx` for async requests:

```javascript
pip install httpx



import httpx
import asyncio
from typing import List, Dict

class AsyncTodoClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    async def get_todos(self) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/todos")
            response.raise_for_status()
            return response.json()['todos']

    async def create_multiple_todos(self, todos: List[Dict]) -> List[Dict]:
        """Create multiple todos concurrently"""
        async with httpx.AsyncClient() as client:
            tasks = [
                client.post(f"{self.base_url}/todos", json=todo)
                for todo in todos
            ]
            responses = await asyncio.gather(*tasks)
            return [r.json() for r in responses]

# Usage
async def main():
    client = AsyncTodoClient("http://localhost:8000")

    # Create multiple todos concurrently
    todos_to_create = [
        {"title": "Task 1", "description": "First task"},
        {"title": "Task 2", "description": "Second task"},
        {"title": "Task 3", "description": "Third task"},
    ]

    created_todos = await client.create_multiple_todos(todos_to_create)
    print(f"Created {len(created_todos)} todos")

# Run async function
asyncio.run(main())
```

* * *

## Practical Example: Weather API Integration

Let's build a weather service that consumes the OpenWeatherMap API:

```python
import requests
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class WeatherData:
    city: str
    temperature: float
    description: str
    humidity: int
    feels_like: float

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_weather(self, city: str, units: str = "metric") -> Optional[WeatherData]:
        """Get current weather for a city"""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                city=data['name'],
                temperature=data['main']['temp'],
                description=data['weather'][0]['description'],
                humidity=data['main']['humidity'],
                feels_like=data['main']['feels_like']
            )
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

# Flask integration
@app.route('/weather/<city>')
def get_weather(city):
    weather_service = WeatherService(os.getenv('OPENWEATHER_API_KEY'))
    weather = weather_service.get_weather(city)

    if not weather:
        return jsonify({'error': 'Weather data not available'}), 404

    return jsonify({
        'city': weather.city,
        'temperature': weather.temperature,
        'description': weather.description,
        'humidity': weather.humidity,
        'feels_like': weather.feels_like
    })
```

* * *

## API Documentation

### FastAPI Auto-Documentation

FastAPI automatically generates OpenAPI (Swagger) documentation. Enhance it with detailed descriptions:

```python
@app.post(
    "/todos",
    response_model=Todo,
    status_code=201,
    summary="Create a new todo",
    description="Create a new todo item with title and optional description",
    response_description="The created todo item"
)
async def create_todo(todo_data: TodoCreate):
    """
    Create a new todo with the following information:

    - **title**: The todo title (required, 1-100 characters)
    - **description**: Optional description (max 500 characters)
    """
    # Implementation here
```

### Flask Documentation with Flask-RESTX

```bash
pip install flask-restx



from flask_restx import Api, Resource, fields

api = Api(app, doc='/docs/')

todo_model = api.model('Todo', {
    'id': fields.String(description='Todo ID'),
    'title': fields.String(required=True, description='Todo title'),
    'description': fields.String(description='Todo description'),
    'completed': fields.Boolean(description='Completion status')
})

@api.route('/todos')
class TodoList(Resource):
    @api.doc('list_todos')
    @api.marshal_list_with(todo_model)
    def get(self):
        """Get all todos"""
        return todos

    @api.doc('create_todo')
    @api.expect(todo_model)
    @api.marshal_with(todo_model, code=201)
    def post(self):
        """Create a new todo"""
        # Implementation here
```

* * *

## Best Practices & Error Handling

### Robust Error Handling

```python
from flask import Flask
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'error': 'Validation failed', 'details': error.messages}), 400
```

### Rate Limiting

```bash
pip install flask-limiter



from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/todos', methods=['POST'])
@limiter.limit("10 per minute")
def create_todo():
    # Implementation here
```

### API Versioning

```python
# URL versioning
@app.route('/api/v1/todos')
def get_todos_v1():
    pass

@app.route('/api/v2/todos')
def get_todos_v2():
    pass

# Header versioning
@app.before_request
def check_api_version():
    version = request.headers.get('API-Version', 'v1')
    if version not in ['v1', 'v2']:
        return jsonify({'error': 'Unsupported API version'}), 400
```

This comprehensive guide covers both building and consuming APIs with Python, providing you with the knowledge to create robust, scalable web services and integrate with external APIs effectively. Remember to always validate input data, handle errors gracefully, and document your APIs thoroughly for better developer experience.

Now, let's review [packaging distribution and best practices](<https://python.robertdevore.com/blog/packaging-distribution-and-best-practices>).
