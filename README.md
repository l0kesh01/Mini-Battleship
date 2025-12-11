🎯 **Mini Battleship – Distributed Two-Person Game System**
===========================================================

A distributed Battleship game implemented using **three microservices** and **two client platforms (CLI + Web)**.Supports **real-time gameplay via WebSockets**, **service-to-service REST communication**, and a clean **microservice architecture**.

🚀 **1\. Project Overview**
===========================

This system allows two players to:

*   Register/login using usernames
    
*   Create and join multiplayer rooms
    
*   Start a Battleship match
    
*   Play turn-based gameplay in real-time using WebSockets
    
*   See personal board + fog-of-war enemy board
    
*   Receive instant updates (hit, miss, sunk, winner)
    

### **Includes:**

*   ✅ **3 backend microservices (Python + FastAPI)**
    
*   ✅ **CLI client (Python)**
    
*   ✅ **Web client (React + WebSocket)**
    

🧱 **2\. Architecture & Technologies**
======================================

### **Microservices (Python + FastAPI)**

| Service | Description | Protocol |
|--------|-------------|----------|
| **User Service** | Username registration + login | REST |
| **Room Service** | Room creation, join, start game | REST → Game Service |
| **Game Rules Service** | Battleship engine, turn logic, live events | REST + WebSocket |

---

### **Clients**

| Client | Tech | Purpose |
|--------|------|---------|
| **CLI Client** | Python, aiohttp | Terminal gameplay |
| **Web Client** | React + Vite + WebSocket | Visual game board |

---
📡 **3\. API Documentation**
============================

**User Service**
----------------

> http://localhost:8001

### **POST /register**

Register a username.

`   { "username": "luke" }   `

### **POST /login**

Login using username.

`   { "username": "luke" }   `

### **GET /users**

List all registered users.

**Room Service**
----------------

> http://localhost:8003

### **POST /create\_room**

`   {    "room_id": "01",    "host_player": "luke"  }   `

### **POST /join\_room**

Guest joins a room.

### **GET /list\_rooms**

Returns all rooms with host / guest / status.

### **POST /start\_game/{room\_id}?username=HOST**

Triggers game creation.

Room Service → Game Service:

`   POST http://localhost:8002/game/create   `

**Game Rules Service**
----------------------

> http://localhost:8002

### **POST /game/create**

Create a Battleship match.

### **GET /list\_games**

Required for CLI service health-check.

🔌 **WebSocket API**
====================

### **Connect:**

`   ws://localhost:8002/ws/{room_id}?player={username}   `

**Client → Server**
-------------------

### **Make a move**

`   {    "action": "move",    "player_name": "luke",    "row": 3,    "col": 5,    "room_id": "01"  }   `

**Server → Client Events**
--------------------------

### **connected**

`   {    "event": "connected",    "game_id": "01",    "current_turn": "luke",    "boards": { "self": [...], "opponent": [...] }  }   `

### **game\_created**

Sent when game starts.

### **move\_made**

`   {    "event": "move_made",    "by": "luke",    "row": 3,    "col": 5,    "result": "hit",    "current_turn": "bob",    "winner": null,    "boards": { "self": [...], "opponent": [...] }  }   `

### **winner**

Winner field appears when game ends.

🔗 **4\. Service-to-Service Communication**
===========================================

Room Service → Game Rules Service:

`   POST http://localhost:8002/game/create   `

This satisfies the requirement for **microservice interaction via REST**.

🕹 **5\. How to Run the Project**
=================================

**Start Backend Services (3 terminals)**
----------------------------------------

### **Terminal 1 — User Service**

`   uvicorn app.user.user_service:app --reload --port 8001   `

### **Terminal 2 — Room Service**

`   uvicorn app.room.room_service:app --reload --port 8003   `

### **Terminal 3 — Game Rules Service**

`   uvicorn app.game.services.game_service:app --reload --port 8002   `

**Start Web Client**
--------------------

`   cd app/frontend  npm install  npm run dev   `

**Start CLI Client**
--------------------

`   python -m app.cli.cli_client   `

🎮 **6\. Gameplay Flow**
========================

1.  User registers/logs in
    
2.  Host creates room
    
3.  Guest joins room
    
4.  Host starts game
    
5.  Both players connect via WebSocket
    
6.  Game Service sends:
    
    *   Player’s own board
        
    *   Fog-of-war enemy board
        
7.  Turn-based shots
    
8.  Hit, miss, sunk ship logs
    
9.  Winner event broadcast
    
10.  Web client shows winner popup
    

🏁 **7\. Features Implemented**
===============================

*   ✔ Three isolated microservices
    
*   ✔ Real-time WebSocket gameplay
    
*   ✔ CLI client
    
*   ✔ Web client UI
    
*   ✔ Turn-based game engine
    
*   ✔ Fog-of-war enemy board
    
*   ✔ Automatic ship placement
    
*   ✔ Hit/miss/sunk/winner logic
    
*   ✔ Service-to-service REST calls
    
*   ✔ CORS-enabled backend
