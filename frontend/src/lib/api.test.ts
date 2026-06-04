import { describe, it, expect, vi, beforeEach } from "vitest"
import { login } from "./api"

describe("login", () => {
  beforeEach(() => { localStorage.clear(); vi.restoreAllMocks() })

  it("envoie email dans 'username' en form-urlencoded et stocke le token", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ access_token: "jwt123", token_type: "bearer" }),
    })
    vi.stubGlobal("fetch", fetchMock)

    await login("a@b.fr", "pw")

    const [url, opts] = fetchMock.mock.calls[0]
    expect(url).toBe("/api/auth/login")
    expect(opts.headers["Content-Type"]).toBe("application/x-www-form-urlencoded")
    expect(opts.body).toBe("username=a%40b.fr&password=pw")
    expect(localStorage.getItem("token")).toBe("jwt123")
  })
})
