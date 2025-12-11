const USER_BASE = "http://127.0.0.1:8001";
const ROOM_BASE = "http://127.0.0.1:8003";
const GAME_BASE = "http://127.0.0.1:8002";

export const endpoints = {
  user: {
    base: USER_BASE,
    register: `${USER_BASE}/register`,
    login: `${USER_BASE}/login`,
    users: `${USER_BASE}/users`
  },
  room: {
    base: ROOM_BASE,
    create: `${ROOM_BASE}/create_room`,
    join: `${ROOM_BASE}/join_room`,
    list: `${ROOM_BASE}/list_rooms`,
    start: (roomId, username) =>
      `${ROOM_BASE}/start_game/${roomId}?username=${encodeURIComponent(
        username
      )}`
  },
  game: {
    base: GAME_BASE,
    list: `${GAME_BASE}/list_games`,
    wsUrl: (roomId, player) =>
      `ws://127.0.0.1:8002/ws/${roomId}?player=${encodeURIComponent(player)}`
  }
};

export async function getJson(url) {
  const res = await fetch(url);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

export async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body ?? {})
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}
