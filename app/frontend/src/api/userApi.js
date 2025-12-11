import { endpoints, postJson, getJson } from "./client";

export function registerUser(username) {
  return postJson(endpoints.user.register, { username });
}

export function loginUser(username) {
  return postJson(endpoints.user.login, { username });
}

export function getUsers() {
  return getJson(endpoints.user.users);
}
