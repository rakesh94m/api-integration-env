from pydantic import BaseModel
from typing import Optional, Dict, Any

class Observation(BaseModel):
    docs_snippet: str      # Instructions for the AI
    last_response: Any     # What the "server" said back
    done: bool             # Is the task finished?

class Action(BaseModel):
    method: str            # "GET" or "POST"
    endpoint: str          # e.g., "/users"
    payload: Optional[Dict[str, Any]] = None