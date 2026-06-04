const BASE = "/api"

function authHeader(): Record<string, string> {
  const t = localStorage.getItem("token")
  return t ? { Authorization: `Bearer ${t}` } : {}
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { ...(init?.headers || {}), ...authHeader() },
  })
  if (!res.ok) throw new Error(`API ${res.status}`)
  return res.status === 204 ? (undefined as T) : res.json()
}

// Quirk : /auth/login attend l'EMAIL dans le champ 'username', en form-urlencoded.
export async function login(email: string, password: string): Promise<void> {
  const body = new URLSearchParams({ username: email, password }).toString()
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  })
  if (!res.ok) throw new Error("Identifiants invalides")
  const data = await res.json()
  localStorage.setItem("token", data.access_token)
}

export async function register(username: string, email: string, password: string) {
  return req("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  })
}

export function logout() { localStorage.removeItem("token") }
export function isLoggedIn() { return !!localStorage.getItem("token") }

export type Category = { id: number; name: string; description: string }
export type Topic = { id: number; title: string; category_id: number; user_id: number }
export type Post = { id: number; content: string; topic_id: number; user_id: number; created_at: string }

export const getCategories = () => req<Category[]>("/categories/")
export const getTopics = (catId: number) => req<Topic[]>(`/categories/${catId}/topics`)
export const getPosts = (topicId: number) => req<Post[]>(`/topics/${topicId}/posts`)
export const createTopic = (catId: number, title: string, content: string) =>
  req<Topic>(`/categories/${catId}/topics`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  })
export const createPost = (topicId: number, content: string) =>
  req<Post>(`/topics/${topicId}/posts`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  })
