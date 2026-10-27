const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

// FastAPI sends {detail: "text"} for our own errors,
// and {detail: [{loc, msg}, ...]} when request validation fails.
function errorMessage(data, fallback) {
  if (typeof data?.detail === "string") return data.detail;
  if (Array.isArray(data?.detail)) {
    return data.detail.map((e) => `${e.loc.at(-1)}: ${e.msg}`).join(", ");
  }
  return fallback;
}

/**
 * Calls the SplitKaro API.
 *   api("/groups", { token })                                  -> GET
 *   api("/groups", { method: "POST", body: { name }, token })  -> JSON body
 *   api("/auth/login", { method: "POST", form: { ... } })      -> form body (OAuth2 login)
 */
export async function api(path, { method = "GET", body, form, token } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;

  let payload;
  if (form) {
    payload = new URLSearchParams(form);
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  let res;
  try {
    res = await fetch(`${API_URL}${path}`, { method, headers, body: payload });
  } catch {
    throw new ApiError(0, "Can't reach the server. Is the backend running?");
  }

  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new ApiError(res.status, errorMessage(data, `Request failed (${res.status})`));
  return data;
}
