import React, { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";
import { listRooms, createRoom, joinRoom } from "../api/roomApi";
import { getUsers } from "../api/userApi";

const LobbyPage = () => {
  const { username } = useAuth();
  const nav = useNavigate();
  const [rooms, setRooms] = useState({});
  const [roomId, setRoomId] = useState("");
  const [users, setUsers] = useState([]);

  useEffect(() => {
    if (!username) {
      nav("/login");
    }
  }, [username, nav]);

  async function refreshRooms() {
    const { ok, data } = await listRooms();
    if (ok) setRooms(data);
  }

  async function refreshUsers() {
    const { ok, data } = await getUsers();
    if (ok) setUsers(data.registered_users || []);
  }

  useEffect(() => {
    refreshRooms();
    refreshUsers();
  }, []);

  async function handleCreate() {
    if (!roomId) return;
    await createRoom(roomId, username);
    setRoomId("");
    refreshRooms();
  }

  async function handleJoin(id) {
    await joinRoom(id, username);
    refreshRooms();
  }

  return (
    <div className="page">
      <h2>Lobby</h2>
      <p className="muted">Logged in as <strong>{username}</strong></p>

      <div className="lobby-layout">
        <div className="panel">
          <h3>Rooms</h3>
          <div className="row">
            <input
              value={roomId}
              onChange={(e) => setRoomId(e.target.value)}
              placeholder="Room ID"
            />
            <button className="btn-primary" onClick={handleCreate}>
              Create
            </button>
          </div>

          <button className="btn-secondary" onClick={refreshRooms}>
            Refresh
          </button>

          <div className="room-list">
            {Object.keys(rooms).length === 0 && (
              <div className="muted">No rooms yet</div>
            )}
            {Object.entries(rooms).map(([id, info]) => (
              <div
                key={id}
                className="room-item"
                onClick={() => nav(`/rooms/${id}`)}
              >
                <div>
                  <strong>Room {id}</strong>
                </div>
                <div className="muted">
                  Host: {info.host} | Guest: {info.guest || "—"} | Status:{" "}
                  {info.status}
                </div>
                {info.guest ? null : (
                  <button
                    className="btn-small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleJoin(id);
                    }}
                  >
                    Join
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h3>Players</h3>
          <button className="btn-secondary" onClick={refreshUsers}>
            Refresh
          </button>
          <ul className="user-list">
            {users.map((u) => (
              <li key={u}>{u}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LobbyPage;
