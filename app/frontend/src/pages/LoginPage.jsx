import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser, loginUser } from "../api/userApi";
import { useAuth } from "../hooks/useAuth";

const LoginPage = () => {
  const [name, setName] = useState("");
  const [mode, setMode] = useState("login"); // or "register"
  const [error, setError] = useState(null);
  const { setUsername } = useAuth();
  const nav = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    const trimmed = name.trim();
    if (!trimmed) {
      setError("Username is required");
      return;
    }

    const fn = mode === "register" ? registerUser : loginUser;
    const { ok, data } = await fn(trimmed);
    if (!ok) {
      setError(data?.detail || "Request failed");
      return;
    }
    setUsername(trimmed);
    nav("/lobby");
  }

  return (
    <div className="page-center">
      <div className="card">
        <h1>Battleship</h1>
        <p className="muted">Log in or register to play</p>

        <form onSubmit={handleSubmit} className="form-vertical">
          <label>
            Username
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. luke"
            />
          </label>

          {error && <div className="error">{error}</div>}

          <button type="submit" className="btn-primary">
            {mode === "register" ? "Register" : "Login"}
          </button>
        </form>

        <div className="toggle-mode">
          {mode === "login" ? (
            <button
              type="button"
              className="btn-link"
              onClick={() => setMode("register")}
            >
              Need an account? Register
            </button>
          ) : (
            <button
              type="button"
              className="btn-link"
              onClick={() => setMode("login")}
            >
              Already have an account? Login
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
