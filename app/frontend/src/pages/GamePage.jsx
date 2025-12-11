import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import BoardGrid from "../components/BoardGrid";
import { useGameSocket } from "../hooks/useGameSocket";

const GamePage = () => {
  const { roomId } = useParams();
  const nav = useNavigate();
  const { username } = useAuth();

  const { connected, currentTurn, winner, boards, sendMove } =
    useGameSocket(roomId, username);

  const myBoard = boards?.self || null;
  const enemyBoard = boards?.opponent || null;

  // ✅ Redirect to lobby 4s after winner appears
  useEffect(() => {
    if (winner) {
      const timer = setTimeout(() => {
        nav("/lobby");
      }, 4000);

      return () => clearTimeout(timer);
    }
  }, [winner, nav]);

  function handleEnemyClick(row, col) {
    if (currentTurn !== username) {
      console.log("Not your turn!");
      return;
    }
    sendMove(row, col);
  }

  return (
    <div className="page">
      <h2>Game – Room {roomId}</h2>

      <p className="muted">
        You are <strong>{username}</strong> |{" "}
        {connected ? "WS connected" : "Connecting..."}
      </p>

      <p className="muted">
        Current turn: <strong>{currentTurn || "..."}</strong>
        {winner && (
          <>
            {" | "}Winner: <strong>{winner}</strong>
          </>
        )}
      </p>

      <div className="boards-layout">
        <BoardGrid title="Your Board" grid={myBoard} fogOfWar={false} />

        <BoardGrid
          title="Enemy Board"
          grid={enemyBoard}
          fogOfWar={true}
          onCellClick={handleEnemyClick}
        />

        {winner && (
          <div className="winner-popup">
            🎉 <strong>{winner}</strong> has won the game!
            <br />
            Returning to lobby...
          </div>
        )}
      </div>
    </div>
  );
};

export default GamePage;
