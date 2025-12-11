# app/cli/game_client.py
import asyncio
from aiohttp import ClientSession, WSMsgType
from typing import Optional
from .utils import print_board


GAME_WS_BASE = "ws://127.0.0.1:8002/ws"


class GameClient:
    def __init__(self, session: ClientSession, username: str):
        self.session = session
        self.username = username

        self.ws = None
        self.listener_task: Optional[asyncio.Task] = None

        self.room_id = None
        self.current_turn: Optional[str] = None
        self.winner: Optional[str] = None

        self.own_board = None
        self.opponent_view = None

        self._connected = asyncio.Event()

    # ============================
    # CONNECT / DISCONNECT
    # ============================
    async def connect(self, room_id: str):
        if self.ws:
            print("Already connected.")
            return

        self.room_id = room_id
        ws_url = f"{GAME_WS_BASE}/{room_id}?player={self.username}"

        try:
            self.ws = await self.session.ws_connect(ws_url)
        except Exception as e:
            print("WebSocket connect failed:", e)
            return

        print("🔌 Connected to game server.")
        self.listener_task = asyncio.create_task(self._listener())

        # Wait for "connected" or "game_created"
        await self._connected.wait()
        print("🕹️ Game client ready.")

    async def disconnect(self):
        if self.listener_task:
            self.listener_task.cancel()

        if self.ws:
            try:
                await self.ws.close()
            except:
                pass

        self.ws = None
        self.room_id = None
        self._connected.clear()
        print("Disconnected from game websocket.")

    # ============================
    # LISTENER LOOP
    # ============================
    async def _listener(self):
        if self.ws is None:
            print("Listener started but websocket is None!(Ignored)")
            return
        ws =self.ws
        try:
            async for msg in self.ws:
                if msg.type == WSMsgType.TEXT:
                    data = msg.json()
                    await self._handle_event(data)

                elif msg.type == WSMsgType.ERROR:
                    print("WebSocket error:", msg)
                    break

        except asyncio.CancelledError:
            return
        except Exception as e:
            print("Listener crashed:", e)
        finally:
            self._connected.clear()

    # ============================
    # EVENT HANDLER
    # ============================
    async def _handle_event(self, data: dict):
        event = data.get("event")

        # --------------------------
        # CONNECTED
        # --------------------------
        if event == "connected":
            print("ℹ️", data.get("message", "Connected."))

            if data.get("boards"):
                boards = data["boards"]
                self.own_board = boards.get("self")
                self.opponent_view = boards.get("opponent")

            self.current_turn = data.get("current_turn")
            self.winner = data.get("winner")

            print(f"Current turn: {self.current_turn}")
            if self.own_board:
                print("Your board:")
                print_board(self.own_board)

            self._connected.set()
            return

        # --------------------------
        # GAME CREATED
        # --------------------------
        if event == "game_created":
            print("🚀 Game created:", data.get("players"))
            self.current_turn = data.get("current_turn")
            print(f"Current turn: {self.current_turn}")
            return

        # --------------------------
        # MOVE MADE
        # --------------------------
        if event == "move_made":
            shooter = data["by"]
            row = data["row"]
            col = data["col"]
            result = data["result"]

            print(f"🔔 {shooter} fired at ({row},{col}) → {result}")

            self.current_turn = data.get("current_turn")
            self.winner = data.get("winner")

            # update your private board + opponent fog
            boards = data.get("boards", {})
            self.own_board = boards.get("self")
            self.opponent_view = boards.get("opponent")

            print(f"Next turn: {self.current_turn}")

            if self.own_board:
                print("\nYour board:")
                print_board(self.own_board)

            if self.opponent_view:
                print("\nOpponent (fog-of-war):")
                print_board(self.opponent_view)

            if self.winner:
                print(f"\n🏆 Winner: {self.winner}")

            return

        # --------------------------
        # ACK OR OTHER
        # --------------------------
        if event == "ack":
            return

        print("Event:", data)

    # ============================
    # SEND SHOT
    # ============================
    async def send_shot(self, row: int, col: int):
        if not self.ws:
            print("Not connected.")
            return

        if self.winner:
            print("Game finished.")
            return

        if self.current_turn and self.current_turn != self.username:
            print("❌ Not your turn.")
            return

        payload = {
            "action": "move",
            "player_name": self.username,
            "room_id": self.room_id,
            "row": row,
            "col": col
        }

        try:
            await self.ws.send_json(payload)
        except Exception as e:
            print("Failed to send move:", e)
