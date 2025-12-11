# app/game/services/game_service.py
import asyncio
from typing import Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.game.game_manager import GameManager

app = FastAPI(title="Battleship Game Service")

# --------------------------------------
# CORS for frontend
# --------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# room_id -> GameManager
games: Dict[str, GameManager] = {}

# room_id -> { websocket: player_name }
ws_clients: Dict[str, Dict[WebSocket, str]] = {}


# Safe sender to avoid crashes
async def safe_send(ws: WebSocket, payload):
    try:
        await ws.send_json(payload)
    except Exception:
        pass


# --------------------------------------
# Utility: Fog-of-war
# --------------------------------------
def serialize_boards(game: GameManager, player: str):
    opponent = game.get_opponent(player)

    own = game.boards[player].grid
    opp_real = game.boards[opponent].grid

    opp_view = [
        [c if c in ("X", "M") else "~" for c in row]
        for row in opp_real
    ]

    return {"self": own, "opponent": opp_view}


# --------------------------------------
# REST: Create a new game
# --------------------------------------
class CreateGame(BaseModel):
    player1: str
    player2: str
    room_id: Optional[str] = None


@app.post("/game/create")
async def create_game(req: CreateGame):
    """
    RoomService calls this endpoint when the host starts the game.
    Both players may already be connected via WS.
    """
    room_id = req.room_id or f"game_{len(games)+1}"

    gm = GameManager(req.player1, req.player2)
    games[room_id] = gm

    # IMPORTANT:
    # Notify all connected clients that the game has really started
    if room_id in ws_clients:
        for ws, player in ws_clients[room_id].items():
            await safe_send(ws, {
                "event": "game_created",
                "game_id": room_id,
                "players": gm.players,
                "current_turn": gm.current_turn,
                "boards": serialize_boards(gm, player)
            })

    return {"message": "game_created", "room_id": room_id}


# --------------------------------------
# WEBSOCKET HANDLING
# --------------------------------------
@app.websocket("/ws/{room_id}")
async def ws_endpoint(ws: WebSocket, room_id: str, player: str = Query(...)):
    await ws.accept()

    # register connection
    ws_clients.setdefault(room_id, {})[ws] = player

    gm = games.get(room_id)

    # CASE 1: Game already created → send actual game state
    if gm:
        await safe_send(ws, {
            "event": "connected",
            "game_id": room_id,
            "current_turn": gm.current_turn,
            "boards": serialize_boards(gm, player)
        })

    # CASE 2: Game NOT started yet → wait for /game/create
    else:
        await safe_send(ws, {
            "event": "connected",
            "message": "waiting_for_game"
        })

    try:
        while True:
            raw = await ws.receive_json()

            if raw.get("action") == "move":
                p = raw["player_name"]
                row = raw["row"]
                col = raw["col"]

                gm = games.get(room_id)
                if not gm:
                    continue

                result = gm.make_move(p, row, col)

                # broadcast updated boards
                for client_ws, pname in ws_clients[room_id].items():
                    await safe_send(client_ws, {
                        "event": "move_made",
                        "game_id": room_id,
                        "by": p,
                        "row": row,
                        "col": col,
                        "result": result,
                        "current_turn": gm.current_turn,
                        "winner": gm.winner,
                        "boards": serialize_boards(gm, pname)
                    })

    except WebSocketDisconnect:
        pass
    finally:
        ws_clients[room_id].pop(ws, None)


# List games (CLI uses this)
@app.get("/list_games")
async def list_games():
    return {"active_games": list(games.keys())}
