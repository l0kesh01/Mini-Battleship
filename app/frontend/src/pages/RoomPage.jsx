import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { listRooms, startGame } from "../api/roomApi";

const RoomPage = () => {
  const { roomId } = useParams();
  const { username } = useAuth();
  const nav = useNavigate();
  const [room, setRoom] = useState(null);
  const [error, setError] = useState(null);

  // -----------------------------------------
  // Load room details
  // -----------------------------------------
  async function loadRoom() {
    const { ok, data } = await listRooms();
    if (!ok) return;
    const r = data[roomId];
    setRoom(r || null);
  }

  // Redirect if no user logged in
  useEffect(() => {
    if (!username) nav("/login");
  }, [username, nav]);

  // Load once when entering page
  useEffect(() => {
    loadRoom();
  }, [roomId]);

  // -----------------------------------------
  // 🔥 POLL room state every 1 second
  // Guest will auto-detect when host starts game
  // -----------------------------------------
  useEffect(() => {
    const interval = setInterval(() => {
      loadRoom();
    }, 1000);
    return () => clearInterval(interval);
  }, [roomId]);

  // -----------------------------------------
  // 🔥 REDIRECT BOTH PLAYERS WHEN GAME STARTS
  // -----------------------------------------
  if (room && room.status === "started") {
    nav(`/game/${roomId}`);
  }

  // Host clicks start game
  async function handleStart() {
    setError(null);
    const { ok, data } = await startGame(roomId, username);
    if (!ok) {
      setError(data?.detail || "Failed to start game");
      return;
    }
    nav(`/game/${roomId}`);
  }

  // -----------------------------------------
  // Render Room UI
  // -----------------------------------------
  if (!room) {
    return (
      <div className="page">
        <h2>Room {roomId}</h2>
        <p className="muted">Room not found.</p>
        <Link to="/lobby" className="btn-secondary">
          Back to lobby
        </Link>
      </div>
    );
  }

  const isHost = room.host === username;

  return (
    <div className="page">
      <h2>Room {roomId}</h2>
      <div className="card">
        <p>
          Host: <strong>{room.host}</strong>
        </p>
        <p>
          Guest: <strong>{room.guest || "Waiting..."}</strong>
        </p>
        <p>
          Status: <strong>{room.status}</strong>
        </p>

        {error && <div className="error">{error}</div>}

        <div className="row">
          <Link to="/lobby" className="btn-secondary">
            Back
          </Link>
          <button
            className="btn-primary"
            disabled={!isHost || !room.guest}
            onClick={handleStart}
          >
            Start Game
          </button>
        </div>
      </div>
    </div>
  );
};

export default RoomPage;
