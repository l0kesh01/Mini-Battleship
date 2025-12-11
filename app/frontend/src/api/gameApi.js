import { endpoints } from "./client";

export function openGameSocket(roomId, player) {
  const url = endpoints.game.wsUrl(roomId, player);
  return new WebSocket(url);
}
