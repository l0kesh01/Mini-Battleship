from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Room Service")

# ---------------------------
# CORS (required for frontend)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # frontend allowed
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, OPTIONS, etc
    allow_headers=["*"],
)

# ---------------------------
# Models
# ---------------------------
class CreateRoomRequest(BaseModel):
    room_id: str
    host_player: str

class JoinRoomRequest(BaseModel):
    room_id: str
    guest_player: str

# ---------------------------
# In-memory storage
# ---------------------------
rooms = {}  # room_id -> {"host": str, "guest": Optional[str], "status": str}

# ---------------------------
# Helper: check if user is registered
# ---------------------------
USER_SERVICE_URL = "http://127.0.0.1:8001"
GAME_SERVICE_URL = "http://127.0.0.1:8002"

async def is_registered(username: str) -> bool:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{USER_SERVICE_URL}/users")
            if resp.status_code == 200:
                users = resp.json().get("registered_users", [])
                return username in users
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="User service unreachable")
    return False

# ---------------------------
# Routes
# ---------------------------
@app.post("/create_room")
async def create_room(req: CreateRoomRequest):
    if not await is_registered(req.host_player):
        raise HTTPException(status_code=403, detail=f"User '{req.host_player}' is not registered")

    if req.room_id in rooms:
        raise HTTPException(status_code=400, detail="Room already exists")

    rooms[req.room_id] = {
        "host": req.host_player,
        "guest": None,
        "status": "waiting"
    }

    return {"message": f"Room '{req.room_id}' created successfully by {req.host_player}"}


@app.post("/join_room")
async def join_room(req: JoinRoomRequest):
    if not await is_registered(req.guest_player):
        raise HTTPException(status_code=403, detail=f"User '{req.guest_player}' is not registered")

    if req.room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")

    if rooms[req.room_id]["guest"]:
        raise HTTPException(status_code=400, detail="Room is already full")

    if rooms[req.room_id]["host"] == req.guest_player:
        raise HTTPException(status_code=400, detail="Cannot join your own room as guest")

    rooms[req.room_id]["guest"] = req.guest_player
    return {"message": f"{req.guest_player} joined room '{req.room_id}'"}


@app.get("/list_rooms")
def list_rooms():
    return rooms


@app.post("/start_game/{room_id}")
async def start_game(room_id: str, username: str):

    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")

    room = rooms[room_id]

    if room["host"] != username:
        raise HTTPException(status_code=403, detail="Only the host can start the game")

    if not room["guest"]:
        raise HTTPException(status_code=400, detail="Waiting for another player to join")

    if room.get("status") == "started":
        raise HTTPException(status_code=400, detail="Game already started")

    payload = {
        "player1": room["host"],
        "player2": room["guest"],
        "room_id": room_id,
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(
                f"{GAME_SERVICE_URL}/game/create",
                json=payload
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Game service unreachable: {str(e)}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to start game")

    room["status"] = "started"

    return {
        "message": f"Game started for room '{room_id}'",
        "details": response.json()
    }
