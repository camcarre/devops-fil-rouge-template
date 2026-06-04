import { createContext, useContext, useState, type ReactNode } from "react"
import { isLoggedIn, logout as apiLogout } from "./api"

type AuthCtx = { authed: boolean; setAuthed: (v: boolean) => void; logout: () => void }
const Ctx = createContext<AuthCtx | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authed, setAuthed] = useState(isLoggedIn())
  const logout = () => { apiLogout(); setAuthed(false) }
  return <Ctx.Provider value={{ authed, setAuthed, logout }}>{children}</Ctx.Provider>
}

export function useAuth() {
  const c = useContext(Ctx)
  if (!c) throw new Error("useAuth hors AuthProvider")
  return c
}
