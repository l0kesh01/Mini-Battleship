import React from "react";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const TopBar = () => {
  const { username } = useAuth();
  const nav = useNavigate();

  return (
    <header className="topbar">
      <div className="topbar-title" onClick={() => nav("/lobby")}>
        Battleship
      </div>
      <div className="topbar-right">
        {username ? <span className="topbar-user">⚓ {username}</span> : null}
      </div>
    </header>
  );
};

export default TopBar;
