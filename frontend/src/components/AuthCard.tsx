import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { login, register } from "@/lib/api"
import { useAuth } from "@/lib/auth"

export function AuthCard() {
  const { setAuthed } = useAuth()
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  async function doLogin() {
    try { await login(email, password); setAuthed(true) }
    catch { setError("Identifiants invalides") }
  }
  async function doRegister() {
    try { await register(username, email, password); await login(email, password); setAuthed(true) }
    catch { setError("Inscription impossible") }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-snow">
      <Card className="w-[360px] rounded-[10px] border-fog p-6">
        <Tabs defaultValue="login">
          <TabsList className="mb-4 w-full">
            <TabsTrigger value="login" className="flex-1">Connexion</TabsTrigger>
            <TabsTrigger value="register" className="flex-1">Inscription</TabsTrigger>
          </TabsList>
          <TabsContent value="login" className="flex flex-col gap-3">
            <Label>Email</Label>
            <Input value={email} onChange={(e) => setEmail(e.target.value)} />
            <Label>Mot de passe</Label>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <Button className="mt-2 rounded-[10px] bg-ink-black text-snow" onClick={doLogin}>Se connecter</Button>
          </TabsContent>
          <TabsContent value="register" className="flex flex-col gap-3">
            <Label>Nom d'utilisateur</Label>
            <Input value={username} onChange={(e) => setUsername(e.target.value)} />
            <Label>Email</Label>
            <Input value={email} onChange={(e) => setEmail(e.target.value)} />
            <Label>Mot de passe</Label>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <Button className="mt-2 rounded-[10px] bg-ink-black text-snow" onClick={doRegister}>S'inscrire</Button>
          </TabsContent>
        </Tabs>
        {error && <p className="mt-3 text-caption text-smoke">{error}</p>}
      </Card>
    </div>
  )
}
