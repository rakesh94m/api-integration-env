import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from engine import MockDatabase

app = FastAPI()
db = MockDatabase()

# Task definitions
TASKS = {
    "fetch_user": {
        "docs_snippet": "Task: Fetch the details of user with ID 1 using GET /users/1",
        "answer_endpoint": "/users/1",
        "answer_method": "GET"
    },
    "create_order": {
        "docs_snippet": "Task: Create an order for user_id=1 with item='laptop' using POST /orders",
        "answer_endpoint": "/orders",
        "answer_method": "POST",
        "answer_payload": {"user_id": 1, "item": "laptop"}
    },
    "debug_api": {
        "docs_snippet": "Task: The /status endpoint is returning errors. Call GET /status to check it.",
        "answer_endpoint": "/status",
        "answer_method": "GET"
    }
}

# Session state
session = {"task": None, "steps": 0, "done": False}

class Action(BaseModel):
    method: str
    endpoint: str
    payload: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "OpenEnv API Integration Environment"}

@app.post("/reset")
async def reset(body: Optional[Dict[str, Any]] = None):
    task_name = (body or {}).get("task", "fetch_user")
    if task_name not in TASKS:
        task_name = "fetch_user"
    
    session["task"] = task_name
    session["steps"] = 0
    session["done"] = False
    db.__init__()  # reset db state
    
    task = TASKS[task_name]
    return {
        "observation": {
            "docs_snippet": task["docs_snippet"],
            "last_response": None,
            "done": False
        }
    }

@app.post("/step")
async def step(action: Action):
    task_name = session.get("task", "fetch_user")
    task = TASKS.get(task_name, TASKS["fetch_user"])
    session["steps"] += 1
    
    reward = 0.0
    done = False
    response_data = {"error": "Unknown endpoint"}

    # Route the action
    if action.method == "GET" and action.endpoint == "/users/1":
        response_data = db.get_user(1)
        if task_name == "fetch_user":
            reward = 1.0
            done = True
        else:
            reward = 0.1  # partial credit for exploring

    elif action.method == "GET" and action.endpoint.startswith("/users/"):
        uid = int(action.endpoint.split("/")[-1]) if action.endpoint.split("/")[-1].isdigit() else -1
        response_data = db.get_user(uid)
        reward = 0.3

    elif action.method == "POST" and action.endpoint == "/orders":
        if action.payload:
            response_data, status = db.create_order(action.payload)
            if task_name == "create_order" and status == 201:
                reward = 1.0
                done = True
            elif status == 201:
                reward = 0.5
            else:
                reward = 0.0
        else:
            response_data = {"error": "No payload"}
            reward = 0.0

    elif action.method == "GET" and action.endpoint == "/status":
        response_data = {"status": "degraded", "error_rate": 0.15}
        if task_name == "debug_api":
            reward = 1.0
            done = True
        else:
            reward = 0.2

    # Cap at 5 steps
    if session["steps"] >= 5:
        done = True

    session["done"] = done

    return {
        "observation": {
            "docs_snippet": task["docs_snippet"],
            "last_response": response_data,
            "done": done
        },
        "reward": reward,
        "done": done,
        "info": {"steps": session["steps"]}
    }

@app.get("/state")
async def state():
    return {"session": session}

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
