from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="User Service")

# Enable CORS so React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for registered usernames
users = set()

class UserRequest(BaseModel):
    username: str

@app.post("/register")
def register_user(req: UserRequest):
    """Register a new username. Fails if username already exists."""
    if req.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users.add(req.username)
    return {"message": f"User '{req.username}' registered successfully"}

@app.post("/login")
def login_user(req: UserRequest):
    """Login using an existing username. Fails if username not found."""
    if req.username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"Welcome back, {req.username}!"}

@app.get("/users")
def list_users():
    """Get a list of all registered usernames."""
    return {"registered_users": list(users)}
