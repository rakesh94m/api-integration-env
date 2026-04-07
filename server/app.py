import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

app = FastAPI()

class Action(BaseModel):
    method: str
    endpoint: str
    payload: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "OpenEnv API is Running"}

@app.post("/reset")
async def reset():
    return {"observation": {"docs_snippet": "Task: Fetch User 1", "last_response": None, "done": False}}

@app.post("/step")
async def step(action: Action):
    return {
        "observation": {"docs_snippet": "Task updated", "last_response": {"id": 1, "name": "Alice"}, "done": True},
        "reward": 1.0,
        "done": True,
        "info": {}
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
