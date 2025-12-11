import { endpoints, postJson, getJson } from "./client";

export function createRoom(roomId, hostPlayer) {
  return postJson(endpoints.room.create, {
    room_id: roomId,
    host_player: hostPlayer
  });
}

export function joinRoom(roomId, guestPlayer) {
  return postJson(endpoints.room.join, {
    room_id: roomId,
    guest_player: guestPlayer
  });
}

export function listRooms() {
  return getJson(endpoints.room.list);
}

export async function startGame(roomId, username) {
  const url = endpoints.room.start(roomId, username);
  const res = await fetch(url, { method: "POST" });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}
