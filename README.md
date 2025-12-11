🎯 Mini Battleship – Distributed Two-Person Game System

A distributed Battleship game implemented using three microservices and two client platforms (CLI + Web).
Supports real-time gameplay via WebSockets, service-to-service communication via HTTP REST, and a clean microservice architecture.

🚀 1. Project Overview

This system allows two players to:

Register/login using simple usernames

Create and join multiplayer game rooms

Start a Battleship match between two players

Play turns in real-time using WebSockets

See personal board + fog-of-war enemy board

Receive instant updates for hits, misses, sunk ships, and winner

The project includes:

3 backend microservices (Python + FastAPI)

1 CLI client

1 Web client (React + WebSocket)

🧱 2. Architecture & Technologies
Backend Microservices (Python + FastAPI)
Service	Purpose	Communication
User Service	Username registration & login	REST
Room Service	Create/join rooms, start games, calls Game Service	REST
Game Rules Service	Battleship logic, turn system, hit/miss, WebSocket updates	REST + WebSocket
Clients
Client	Tech	Description
CLI Client	Python, aiohttp	Text-based game interface
Web Client	React (Vite), WebSocket	Visual boards + real-time gameplay
📡 3. API Documentation
## User Service (http://localhost:8001
)
POST /register

Registers a new username.

{ "username": "luke" }

POST /login

Login using username.

{ "username": "luke" }

GET /users

Returns all registered usernames.

## Room Service (http://localhost:8003
)
POST /create_room
{
  "room_id": "01",
  "host_player": "luke"
}

POST /join_room

Second player joins room.

GET /list_rooms

Shows all rooms with host/guest/status.

POST /start_game/{room_id}?username=HOST

Triggers game creation in the Game Service.

Room Service → Game Service:

POST http://localhost:8002/game/create

## Game Rules Service (http://localhost:8002
)
POST /game/create

Creates a Battleship match.

GET /list_games

Returns active games (used by CLI health-check).

## WebSocket API

Used for all gameplay communication.

Connect:
ws://localhost:8002/ws/{room_id}?player={username}

Client → Server
Make a move
{
  "action": "move",
  "player_name": "luke",
  "row": 3,
  "col": 5,
  "room_id": "01"
}

Server → Client Events
connected
{
  "event": "connected",
  "game_id": "01",
  "current_turn": "luke",
  "boards": { "self": [...], "opponent": [...] }
}

game_created

Sent when game starts.

move_made
{
  "event": "move_made",
  "by": "luke",
  "row": 3,
  "col": 5,
  "result": "hit",
  "current_turn": "bob",
  "winner": null,
  "boards": { "self": [...], "opponent": [...] }
}

winner

winner field becomes the winning username.

🔗 4. Service-to-Service Communication

Room Service → Game Rules Service

POST http://localhost:8002/game/create


This fulfills the requirement to demonstrate backend microservice communication.

🕹 5. How to Run the Project
Start Backend Services (3 terminals)
Terminal 1 — User Service
uvicorn app.user.user_service:app --reload --port 8001

Terminal 2 — Room Service
uvicorn app.room.room_service:app --reload --port 8003

Terminal 3 — Game Rules Service
uvicorn app.game.services.game_service:app --reload --port 8002

Start Web Client
cd app/frontend
npm install
npm run dev

Start CLI Client
python -m app.cli.cli_client

🎮 6. Gameplay Flow

Users register/login

Host creates a room

Guest joins the room

Host starts game (Room Service → Game Service)

Both players connect via WebSocket

Game Service sends each player:

Their own board

Fog-of-war enemy board

Players shoot turn by turn

Winner is broadcast to both clients

Web client shows animated winner popup

🏁 7. Features Implemented

✔ 3 fully isolated microservices
✔ Real-time WebSocket gameplay
✔ CLI client
✔ Web client with interactive grid
✔ Turn-based game engine
✔ Fog-of-war opponent board
✔ Ship placement, hit/miss, sinking, win detection
✔ Room creation + joining
✔ Service-to-service HTTP communication
✔ CORS configured for browser
✔ Production-ready code structure
