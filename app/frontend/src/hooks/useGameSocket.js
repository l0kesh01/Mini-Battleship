import { useEffect, useRef, useState } from "react";
import { endpoints } from "../api/client";

export function useGameSocket(roomId, username) {
  const [connected, setConnected] = useState(false);
  const [currentTurn, setCurrentTurn] = useState(null);
  const [winner, setWinner] = useState(null);
  const [boards, setBoards] = useState(null);

  const wsRef = useRef(null);

  useEffect(() => {
    if (!roomId || !username) return;

    const url = endpoints.game.wsUrl(roomId, username);
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WS OPEN");
      setConnected(true);
    };

    ws.onclose = () => {
      console.log("WS CLOSED");
      setConnected(false);
    };

    ws.onmessage = (evt) => {
      let data;
      try {
        data = JSON.parse(evt.data);
      } catch (err) {
        console.warn("Invalid WS JSON:", evt.data);
        return;
      }

      console.log("WS MESSAGE:", data);
      const event = data.event;

      // ------------------------------
      // EVENT: CONNECTED
      // ------------------------------
      if (event === "connected") {
        if (data.boards) {
          setBoards(data.boards);
        }
        setCurrentTurn(data.current_turn || null);
        return;
      }

      // ------------------------------
      // EVENT: GAME CREATED
      // (Game officially starts)
      // ------------------------------
      if (event === "game_created") {
        console.log("GAME CREATED RECEIVED");
        setBoards(data.boards || null);
        setCurrentTurn(data.current_turn || null);
        return;
      }

      // ------------------------------
      // EVENT: MOVE MADE
      // ------------------------------
      if (event === "move_made") {
        setBoards(data.boards || null);
        setCurrentTurn(data.current_turn || null);
        setWinner(data.winner || null);
        return;
      }
    };

    return () => {
      ws.close();
    };
  }, [roomId, username]);

  // -----------------------------------
  // SEND MOVE
  // -----------------------------------
  function sendMove(row, col) {
    if (!wsRef.current) return;
    wsRef.current.send(
      JSON.stringify({
        action: "move",
        player_name: username,
        row,
        col,
        room_id: roomId,
      })
    );
  }

  return {
    connected,
    currentTurn,
    winner,
    boards,
    sendMove,
  };
}
