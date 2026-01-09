# Advanced Features

## Table of Contents
- [Background Tasks](#background-tasks)
- [WebSockets](#websockets)
- [Middleware](#middleware)
- [Lifespan Events](#lifespan-events)
- [Streaming Responses](#streaming-responses)
- [Server-Sent Events](#server-sent-events)

## Background Tasks

### Basic Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

def send_email(email: str, subject: str, body: str):
    # Simulated email sending
    import time
    time.sleep(2)  # Simulate slow operation
    print(f"Email sent to {email}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!", "Thanks for signing up")
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification will be sent"}
```

### Dependency with Background Tasks

```python
from fastapi import Depends, BackgroundTasks

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"Query received: {q}")
    return q

@app.get("/items/")
async def read_items(q: str = Depends(get_query)):
    return {"q": q}
```

### Async Background Tasks

```python
import asyncio

async def async_send_email(email: str, message: str):
    await asyncio.sleep(2)  # Simulate async operation
    print(f"Async email sent to {email}")

@app.post("/async-notification/")
async def send_async_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(async_send_email, email, "Hello!")
    return {"message": "Will be sent"}
```

## WebSockets

### Basic WebSocket

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### WebSocket with JSON

```python
@app.websocket("/ws/json")
async def websocket_json(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            response = {"received": data, "status": "ok"}
            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass
```

### Connection Manager (Chat/Broadcast)

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    await manager.broadcast(f"{client_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} left the chat")
```

### WebSocket with Authentication

```python
from fastapi import Query, WebSocket, WebSocketDisconnect, status

async def get_token(websocket: WebSocket, token: str = Query(...)):
    if token != "valid-token":  # Replace with real auth
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    return token

@app.websocket("/ws/secure")
async def secure_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    # Validate token
    if not validate_token(token):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Authenticated: {data}")
    except WebSocketDisconnect:
        pass
```

## Middleware

### Custom Middleware

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(TimingMiddleware)
```

### Request Logging Middleware

```python
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)
```

### Pure ASGI Middleware (Better Performance)

```python
from starlette.types import ASGIApp, Receive, Scope, Send

class PureASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            # Add custom header
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.append((b"x-custom-header", b"value"))
                    message["headers"] = headers
                await send(message)
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)

app.add_middleware(PureASGIMiddleware)
```

### Common Middleware Stack

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# Order matters: last added = first executed
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

## Lifespan Events

### Modern Lifespan (Recommended)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Shared resources
db_pool = None
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global db_pool, redis_client
    db_pool = await create_db_pool()
    redis_client = await create_redis_client()
    print("Application started")

    yield  # Application runs here

    # Shutdown
    await db_pool.close()
    await redis_client.close()
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)
```

### State Management

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Store shared state
    app.state.db_pool = await create_db_pool()
    app.state.settings = load_settings()
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(request: Request):
    # Access state via request
    pool = request.app.state.db_pool
    return {"pool_size": pool.size}
```

## Streaming Responses

### Stream File Download

```python
from fastapi.responses import StreamingResponse
import io

@app.get("/download")
async def download_file():
    def generate():
        for i in range(100):
            yield f"Line {i}\n"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=data.txt"}
    )
```

### Stream Large File

```python
from pathlib import Path

@app.get("/download/{filename}")
async def download_large_file(filename: str):
    file_path = Path(f"files/{filename}")

    def iterfile():
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # 1MB chunks
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

### Async Generator Streaming

```python
import asyncio

async def slow_data_generator():
    for i in range(10):
        await asyncio.sleep(1)
        yield f"data: {i}\n\n"

@app.get("/stream")
async def stream_data():
    return StreamingResponse(
        slow_data_generator(),
        media_type="text/event-stream"
    )
```

## Server-Sent Events

### Basic SSE

```python
from fastapi.responses import StreamingResponse
import asyncio
import json

async def event_generator():
    while True:
        await asyncio.sleep(1)
        data = {"time": str(datetime.now()), "value": random.randint(1, 100)}
        yield f"data: {json.dumps(data)}\n\n"

@app.get("/events")
async def sse_endpoint():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

### SSE with Event Types

```python
async def typed_event_generator():
    yield "event: connected\ndata: {\"status\": \"ok\"}\n\n"

    counter = 0
    while True:
        await asyncio.sleep(2)
        counter += 1
        yield f"event: update\ndata: {{\"count\": {counter}}}\n\n"

        if counter % 5 == 0:
            yield f"event: milestone\ndata: {{\"milestone\": {counter}}}\n\n"

@app.get("/typed-events")
async def typed_sse():
    return StreamingResponse(
        typed_event_generator(),
        media_type="text/event-stream"
    )
```

### Client-Side SSE (JavaScript)

```javascript
// Frontend code
const eventSource = new EventSource('/events');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

eventSource.addEventListener('update', (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
});

eventSource.onerror = () => {
    console.log('Connection error');
    eventSource.close();
};
```
