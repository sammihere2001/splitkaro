import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api } from "./api.js";

const TOKEN_KEY = "splitkaro_token";
const AuthContext = createContext(null);

/** Keeps the login token and current user, and shares them with every page. */
export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState(null);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  }, []);

  // Whenever we have a token, load who it belongs to. A bad or expired token logs us out.
  useEffect(() => {
    if (!token) return;
    api("/auth/me", { token }).then(setUser).catch(logout);
  }, [token, logout]);

  async function login(email, password) {
    const { access_token } = await api("/auth/login", {
      method: "POST",
      form: { username: email, password },
    });
    localStorage.setItem(TOKEN_KEY, access_token);
    setToken(access_token);
  }

  async function register(name, email, password) {
    await api("/auth/register", { method: "POST", body: { name, email, password } });
    await login(email, password);
  }

  // Like api(), but sends the token and logs out if the server says it is no longer valid.
  const request = useCallback(
    async (path, options = {}) => {
      try {
        return await api(path, { ...options, token });
      } catch (err) {
        if (err.status === 401) logout();
        throw err;
      }
    },
    [token, logout],
  );

  const value = { token, user, loading: Boolean(token) && !user, login, register, logout, request };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
