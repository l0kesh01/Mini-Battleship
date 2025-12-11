# app/cli/cli_client.py
import asyncio
import aiohttp
import shlex
import sys
from app.cli.utils import wait_for_service, async_input, print_board
from app.cli.game_client import GameClient

ROOM_SERVICE = "http://127.0.0.1:8003"
USER_SERVICE = "http://127.0.0.1:8001"
GAME_SERVICE = "http://127.0.0.1:8002"

HELP_TEXT = """
Available commands:
  register <username>
  login <username>
  list_users
  create_room <room_id>
  join_room <room_id>
  list_rooms
  start_game <room_id>
  connect <room_id>         # connect websocket to game
  board                     # show your board (if connected)
  shoot <row> <col>         # fire at row,col (0-based, 0..11)
  leave                     # leave current game (disconnect ws)
  help
  exit
"""

async def call_post(session, url, json):
    try:
        async with session.post(url, json=json) as r:
            return r.status, await r.json()
    except Exception as e:
        return None, {"error": str(e)}

async def call_get(session, url):
    try:
        async with session.get(url) as r:
            return r.status, await r.json()
    except Exception as e:
        return None, {"error": str(e)}


async def repl():
    print("=== Battleship CLI (command shell) ===")
    # Wait for services
    await wait_for_service(f"{ROOM_SERVICE}/list_rooms", "Room Service")
    await wait_for_service(f"{GAME_SERVICE}/list_games", "Game Service")
    await wait_for_service(f"{USER_SERVICE}/users", "User Service")

    async with aiohttp.ClientSession() as session:
        current_user = None
        gc: GameClient | None = None

        while True:
            try:
                raw = (await async_input("> ")).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                return

            if not raw:
                continue

            # simple shell parsing
            parts = shlex.split(raw)
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd == "help":
                print(HELP_TEXT)
                continue

            if cmd == "exit":
                if gc:
                    await gc.disconnect()
                print("Bye.")
                return

            # ---- registration / login ----
            if cmd == "register":
                if len(args) != 1:
                    print("Usage: register <username>")
                    continue
                u = args[0]
                status, data = await call_post(session, f"{USER_SERVICE}/register", {"username": u})
                print(data)
                if status == 200:
                    current_user = u
                    print(f"✅ Registered and logged in as {u}")
                continue

            if cmd == "login":
                if len(args) != 1:
                    print("Usage: login <username>")
                    continue
                u = args[0]
                status, data = await call_post(session, f"{USER_SERVICE}/login", {"username": u})
                print(data)
                if status == 200:
                    current_user = u
                    print(f"✅ Logged in as {u}")
                continue

            if cmd == "list_users":
                status, data = await call_get(session, f"{USER_SERVICE}/users")
                print(data)
                continue

            # ---- rooms ----
            if cmd == "create_room":
                if len(args) != 1:
                    print("Usage: create_room <room_id>")
                    continue
                if not current_user:
                    print("You must register/login first.")
                    continue
                rid = args[0]
                status, data = await call_post(session, f"{ROOM_SERVICE}/create_room", {"room_id": rid, "host_player": current_user})
                print(data)
                continue

            if cmd == "join_room":
                if len(args) != 1:
                    print("Usage: join_room <room_id>")
                    continue
                if not current_user:
                    print("You must register/login first.")
                    continue
                rid = args[0]
                status, data = await call_post(session, f"{ROOM_SERVICE}/join_room", {"room_id": rid, "guest_player": current_user})
                print(data)
                continue

            if cmd == "list_rooms":
                status, data = await call_get(session, f"{ROOM_SERVICE}/list_rooms")
                print(data)
                continue

            if cmd == "start_game":
                if len(args) != 1:
                    print("Usage: start_game <room_id>")
                    continue
                if not current_user:
                    print("You must register/login first.")
                    continue
                rid = args[0]
                # Room service expects ?username=...
                try:
                    async with session.post(f"{ROOM_SERVICE}/start_game/{rid}?username={current_user}") as r:
                        resp = await r.json()
                        print(resp)
                except Exception as e:
                    print("Start game failed:", e)
                continue

            # ---- websocket / gameplay ----
            if cmd == "connect":
                if len(args) != 1:
                    print("Usage: connect <room_id>")
                    continue
                if not current_user:
                    print("You must register/login first.")
                    continue
                rid = args[0]
                # instantiate game client if needed
                if gc:
                    await gc.disconnect()
                gc = GameClient(session, current_user)
                await gc.connect(rid)
                continue

            if cmd == "board":
                if not gc or not gc.own_board:
                    print("No board available. Connect to a game first.")
                    continue
                print_board(gc.own_board)
                continue

            if cmd == "shoot":
                if len(args) != 2:
                    print("Usage: shoot <row> <col>")
                    continue
                if not gc:
                    print("You must connect to the game first (connect <room_id>)")
                    continue
                try:
                    r = int(args[0]); c = int(args[1])
                except ValueError:
                    print("Row/col must be integers.")
                    continue
                if not (0 <= r <= 11 and 0 <= c <= 11):
                    print("Row and column must be between 0 and 11.")
                    continue
                await gc.send_shot(r, c)
                continue

            if cmd == "leave":
                if gc:
                    await gc.disconnect(); gc = None
                else:
                    print("Not in a game.")
                continue

            print("Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    asyncio.run(repl())
