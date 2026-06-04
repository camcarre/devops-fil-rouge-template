# Front-end Forum (style ChatGPT) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construire un front React (style ChatGPT) pour le forum, consommant l'API FastAPI, conteneurisé (nginx) et déployé sur Kubernetes.

**Architecture:** Monorepo — dossier `frontend/` (Vite+React+TS+Tailwind v4+shadcn) compilé en statique, servi par nginx qui fait aussi reverse-proxy `/api/*` → service `api` (donc pas de CORS). Mapping ChatGPT→forum : sidebar = catégories/sujets, centre = fil d'un sujet, champ de saisie = poster un message.

**Tech Stack:** Vite, React 18, TypeScript, Tailwind CSS v4, shadcn/ui, nginx:alpine, Docker, Kubernetes (minikube).

**Spec:** `docs/superpowers/specs/2026-06-04-frontend-forum-design.md`

---

## File Structure

| Fichier | Responsabilité |
|---------|----------------|
| `frontend/package.json`, `vite.config.ts`, `tsconfig*.json` | Scaffold + alias `@` + proxy dev |
| `frontend/src/index.css` | Import Tailwind + `@theme` avec les tokens du design |
| `frontend/components.json` | Config shadcn |
| `frontend/src/lib/utils.ts` | Helper `cn()` (shadcn) |
| `frontend/src/lib/api.ts` | Wrapper fetch typé vers `/api` (encapsule le quirk login + JWT) |
| `frontend/src/lib/auth.tsx` | Contexte d'authentification (token, login, logout) |
| `frontend/src/components/ui/*` | Composants shadcn générés |
| `frontend/src/components/Sidebar.tsx` | Liste catégories→sujets, bouton + Sujet |
| `frontend/src/components/TopicThread.tsx` | Messages d'un sujet + champ poster |
| `frontend/src/components/EmptyState.tsx` | « Where should I begin? » |
| `frontend/src/components/AuthCard.tsx` | Login / register |
| `frontend/src/App.tsx` | Shell 2 colonnes + routing d'état |
| `frontend/Dockerfile`, `frontend/nginx.conf`, `frontend/.dockerignore` | Conteneurisation |
| `docker-compose.yml` | + service `frontend` |
| `k8s/50-frontend-deployment.yaml`, `k8s/51-frontend-service.yaml`, `k8s/30-ingress.yaml` | Déploiement K8s |

---

## Task F1 : Scaffold Vite + React + Tailwind v4 + shadcn + tokens

**Files:**
- Create: `frontend/` (scaffold Vite), `frontend/src/index.css`, `frontend/components.json`, `frontend/src/lib/utils.ts`
- Modify: `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/tsconfig.app.json`

- [ ] **Step 1: Scaffolder le projet Vite**

Run (depuis la racine du repo) :
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend && npm install
```
Expected: dossier `frontend/` créé avec un projet React-TS qui build.

- [ ] **Step 2: Installer Tailwind v4 + dépendances shadcn**

Run (dans `frontend/`) :
```bash
npm install tailwindcss @tailwindcss/vite
npm install class-variance-authority clsx tailwind-merge lucide-react tailwindcss-animate
```

- [ ] **Step 3: Configurer Vite (plugin Tailwind + alias `@` + proxy dev)**

Remplacer `frontend/vite.config.ts` par :
```ts
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"
import path from "path"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
  server: {
    // En dev, proxy /api vers l'API FastAPI lancée localement (docker compose up api db)
    proxy: { "/api": { target: "http://localhost:8000", changeOrigin: true, rewrite: (p) => p.replace(/^\/api/, "") } },
  },
})
```

- [ ] **Step 4: Activer l'alias `@` dans TypeScript**

Dans `frontend/tsconfig.json`, ajouter dans `compilerOptions` :
```json
"baseUrl": ".",
"paths": { "@/*": ["./src/*"] }
```
Faire de même dans `frontend/tsconfig.app.json` (mêmes deux clés dans `compilerOptions`).

- [ ] **Step 5: Écrire `frontend/src/index.css` avec les tokens du design**

Remplacer le contenu par :
```css
@import "tailwindcss";

@theme {
  --color-ink-black: #0d0d0d;
  --color-paper: #f9f9f9;
  --color-snow: #ffffff;
  --color-smoke: #5d5d5d;
  --color-ash: #8f8f8f;
  --color-fog: #ececec;

  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;

  --radius-input: 10px;
  --radius-button: 10px;
  --radius-large: 28px;
}

:root {
  font-feature-settings: "liga" 0;
  color: var(--color-ink-black);
  background: var(--color-snow);
}

body { margin: 0; font-family: var(--font-sans); }
```

- [ ] **Step 6: Créer `frontend/src/lib/utils.ts` (helper shadcn)**

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

- [ ] **Step 7: Créer `frontend/components.json` (config shadcn)**

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": { "config": "", "css": "src/index.css", "baseColor": "neutral", "cssVariables": true },
  "aliases": { "components": "@/components", "utils": "@/lib/utils", "ui": "@/components/ui" }
}
```

- [ ] **Step 8: Ajouter les composants shadcn nécessaires**

Run (dans `frontend/`) :
```bash
npx shadcn@latest add button card input label textarea scroll-area separator avatar tabs
```
Expected: fichiers générés dans `frontend/src/components/ui/`.

- [ ] **Step 9: Vérifier que le build passe**

Run : `npm run build`
Expected: build réussi, dossier `frontend/dist/` créé.

- [ ] **Step 10: Commit**

```bash
cd /Users/cooker/Desktop/devops-fil-rouge-template
git add frontend/
git commit -m "feat(front): scaffold Vite+React+Tailwind v4+shadcn + tokens design (F1)"
```

---

## Task F2 : Wrapper API typé (avec le quirk login) + tests

**Files:**
- Create: `frontend/src/lib/api.ts`, `frontend/src/lib/api.test.ts`
- Modify: `frontend/package.json` (script test), install vitest

- [ ] **Step 1: Installer vitest**

Run (dans `frontend/`) : `npm install -D vitest`
Puis ajouter dans `frontend/package.json` → `"scripts"` : `"test": "vitest run"`.

- [ ] **Step 2: Écrire le test du wrapper (login en form-urlencoded avec email)**

Create `frontend/src/lib/api.test.ts` :
```ts
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
```

- [ ] **Step 3: Lancer le test et vérifier qu'il échoue**

Run : `npm test`
Expected: FAIL (`login` n'existe pas encore).

- [ ] **Step 4: Implémenter `frontend/src/lib/api.ts`**

```ts
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
```

- [ ] **Step 5: Lancer le test et vérifier qu'il passe**

Run : `npm test`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
cd /Users/cooker/Desktop/devops-fil-rouge-template
git add frontend/src/lib/api.ts frontend/src/lib/api.test.ts frontend/package.json frontend/package-lock.json
git commit -m "feat(front): wrapper API typé + quirk login + test vitest (F2)"
```

---

## Task F3 : Contexte d'auth + écran Login/Register

**Files:**
- Create: `frontend/src/lib/auth.tsx`, `frontend/src/components/AuthCard.tsx`

- [ ] **Step 1: Créer le contexte d'auth `frontend/src/lib/auth.tsx`**

```tsx
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
```

- [ ] **Step 2: Créer `frontend/src/components/AuthCard.tsx`**

```tsx
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
```

- [ ] **Step 3: Vérifier le build**

Run : `cd frontend && npm run build`
Expected: build OK.

- [ ] **Step 4: Commit**

```bash
cd /Users/cooker/Desktop/devops-fil-rouge-template
git add frontend/src/lib/auth.tsx frontend/src/components/AuthCard.tsx
git commit -m "feat(front): contexte auth + écran login/register (F3)"
```

---

## Task F4 : Shell (sidebar + fil de sujet + empty state)

**Files:**
- Create: `frontend/src/components/Sidebar.tsx`, `frontend/src/components/TopicThread.tsx`, `frontend/src/components/EmptyState.tsx`
- Modify: `frontend/src/App.tsx`, `frontend/src/main.tsx`

- [ ] **Step 1: Créer `frontend/src/components/EmptyState.tsx`**

```tsx
export function EmptyState() {
  return (
    <div className="flex h-full items-center justify-center">
      <p className="text-heading text-ink-black">Where should I begin?</p>
    </div>
  )
}
```

- [ ] **Step 2: Créer `frontend/src/components/Sidebar.tsx`**

```tsx
import { useEffect, useState } from "react"
import { getCategories, getTopics, type Category, type Topic } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"

export function Sidebar({ onSelectTopic }: { onSelectTopic: (t: Topic) => void }) {
  const [cats, setCats] = useState<Category[]>([])
  const [topics, setTopics] = useState<Record<number, Topic[]>>({})

  useEffect(() => { getCategories().then(setCats).catch(() => setCats([])) }, [])

  async function toggle(cat: Category) {
    if (topics[cat.id]) return
    const t = await getTopics(cat.id).catch(() => [])
    setTopics((prev) => ({ ...prev, [cat.id]: t }))
  }

  return (
    <aside className="flex h-screen w-[260px] flex-col bg-paper p-3">
      <div className="mb-4 px-2 text-body font-medium text-ink-black">Forum</div>
      <ScrollArea className="flex-1">
        {cats.map((c) => (
          <div key={c.id} className="mb-1">
            <button onClick={() => toggle(c)}
              className="w-full rounded-[10px] px-2 py-1.5 text-left text-caption text-ink-black hover:bg-fog">
              ▸ {c.name}
            </button>
            {(topics[c.id] || []).map((t) => (
              <button key={t.id} onClick={() => onSelectTopic(t)}
                className="ml-3 block w-full rounded-[10px] px-2 py-1 text-left text-caption text-smoke hover:bg-fog">
                {t.title}
              </button>
            ))}
          </div>
        ))}
      </ScrollArea>
      <Button className="mt-2 rounded-[10px] bg-ink-black text-snow">+ Sujet</Button>
    </aside>
  )
}
```

- [ ] **Step 3: Créer `frontend/src/components/TopicThread.tsx`**

```tsx
import { useEffect, useState } from "react"
import { getPosts, createPost, type Post, type Topic } from "@/lib/api"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"

export function TopicThread({ topic }: { topic: Topic }) {
  const [posts, setPosts] = useState<Post[]>([])
  const [draft, setDraft] = useState("")

  useEffect(() => { getPosts(topic.id).then(setPosts).catch(() => setPosts([])) }, [topic.id])

  async function send() {
    if (!draft.trim()) return
    const p = await createPost(topic.id, draft)
    setPosts((prev) => [...prev, p]); setDraft("")
  }

  return (
    <div className="mx-auto flex h-screen max-w-3xl flex-col px-16 py-8">
      <h1 className="mb-4 text-subheading text-ink-black">{topic.title}</h1>
      <div className="flex-1 overflow-y-auto">
        {posts.map((p) => (
          <div key={p.id} className="mb-3 rounded-[10px] border border-fog bg-snow p-3 text-body">{p.content}</div>
        ))}
      </div>
      <div className="mt-4 flex items-end gap-2 rounded-[10px] border border-fog bg-snow p-2">
        <Textarea value={draft} onChange={(e) => setDraft(e.target.value)}
          placeholder="Écrire un message…" className="min-h-[44px] flex-1 border-0 focus-visible:ring-0" />
        <Button className="rounded-[10px] bg-ink-black text-snow" onClick={send}>Envoyer</Button>
      </div>
    </div>
  )
}
```

- [ ] **Step 4: Câbler le shell dans `frontend/src/App.tsx`**

```tsx
import { useState } from "react"
import { AuthProvider, useAuth } from "@/lib/auth"
import { AuthCard } from "@/components/AuthCard"
import { Sidebar } from "@/components/Sidebar"
import { TopicThread } from "@/components/TopicThread"
import { EmptyState } from "@/components/EmptyState"
import type { Topic } from "@/lib/api"
import "./index.css"

function Shell() {
  const { authed } = useAuth()
  const [topic, setTopic] = useState<Topic | null>(null)
  if (!authed) return <AuthCard />
  return (
    <div className="flex">
      <Sidebar onSelectTopic={setTopic} />
      <main className="h-screen flex-1 bg-snow">
        {topic ? <TopicThread topic={topic} /> : <EmptyState />}
      </main>
    </div>
  )
}

export default function App() {
  return <AuthProvider><Shell /></AuthProvider>
}
```

- [ ] **Step 5: Nettoyer `frontend/src/main.tsx`**

S'assurer qu'il importe `./index.css` et rend `<App />` (supprimer le CSS/contenu par défaut de Vite, et le fichier `App.css` s'il existe).

- [ ] **Step 6: Vérifier le build**

Run : `cd frontend && npm run build`
Expected: build OK.

- [ ] **Step 7: Commit**

```bash
cd /Users/cooker/Desktop/devops-fil-rouge-template
git add frontend/src
git commit -m "feat(front): shell 2 colonnes — sidebar, fil de sujet, empty state (F4)"
```

---

## Task F5 : Conteneurisation (Dockerfile nginx + proxy + compose)

**Files:**
- Create: `frontend/Dockerfile`, `frontend/nginx.conf`, `frontend/.dockerignore`
- Modify: `docker-compose.yml`

- [ ] **Step 1: Créer `frontend/nginx.conf`**

```nginx
server {
  listen 8080;
  root /usr/share/nginx/html;
  index index.html;

  # SPA : toute route inconnue retombe sur index.html
  location / {
    try_files $uri $uri/ /index.html;
  }

  # Reverse-proxy vers l'API (strip /api/) → pas de CORS
  location /api/ {
    proxy_pass http://api:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}
```

- [ ] **Step 2: Créer `frontend/Dockerfile` (multi-stage)**

```dockerfile
# Étape build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Étape runtime : nginx léger servant le statique
FROM nginx:alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
```

- [ ] **Step 3: Créer `frontend/.dockerignore`**

```
node_modules
dist
.vite
*.log
```

- [ ] **Step 4: Ajouter le service `frontend` dans `docker-compose.yml`**

Insérer ce service sous `api:` (au même niveau d'indentation que `api` et `db`) :
```yaml
  frontend:
    build: ./frontend
    container_name: forum-frontend
    ports:
      - "8080:8080"
    depends_on:
      - api
    networks:
      - forum-network
```

- [ ] **Step 5: Vérifier la stack complète**

Run (racine du repo) :
```bash
docker compose up --build -d
sleep 8
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/          # attendu : 200 (front)
curl -s -w "\n%{http_code}\n" http://localhost:8080/api/health           # attendu : {"status":"ok"} 200 (proxy → api)
```
Expected: 200 pour le front, et `{"status":"ok"}` via `/api/health` (preuve que le proxy marche, sans CORS).

- [ ] **Step 6: Commit**

```bash
git add frontend/Dockerfile frontend/nginx.conf frontend/.dockerignore docker-compose.yml
git commit -m "feat(front): conteneurisation nginx + reverse-proxy /api + service compose (F5)"
```

---

## Task F6 : Déploiement Kubernetes (manifests + ingress)

**Files:**
- Create: `k8s/50-frontend-deployment.yaml`, `k8s/51-frontend-service.yaml`
- Modify: `k8s/30-ingress.yaml`

- [ ] **Step 1: Créer `k8s/50-frontend-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: forum
  labels:
    app: forum-frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: forum-frontend
  template:
    metadata:
      labels:
        app: forum-frontend
    spec:
      containers:
        - name: frontend
          image: devops-fil-rouge-template-frontend:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet: { path: /, port: 8080 }
            initialDelaySeconds: 3
            periodSeconds: 5
```

- [ ] **Step 2: Créer `k8s/51-frontend-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: forum
  labels:
    app: forum-frontend
spec:
  type: ClusterIP
  selector:
    app: forum-frontend
  ports:
    - port: 8080
      targetPort: 8080
      name: http
```

- [ ] **Step 3: Mettre à jour `k8s/30-ingress.yaml` pour router vers le front**

Remplacer le bloc `backend:` existant pour que `forum.local/` pointe sur le service `frontend` (le front proxy ensuite `/api` en interne vers `api`). Nouveau contenu :
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: forum-ingress
  namespace: forum
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: forum.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 8080
```

- [ ] **Step 4: Build + charger l'image dans minikube**

Run (racine du repo) :
```bash
docker build -t devops-fil-rouge-template-frontend:latest ./frontend
minikube image load devops-fil-rouge-template-frontend:latest --profile=forum
```

- [ ] **Step 5: Déployer et vérifier**

Run :
```bash
kubectl --context forum apply -f k8s/50-frontend-deployment.yaml -f k8s/51-frontend-service.yaml -f k8s/30-ingress.yaml
kubectl --context forum -n forum rollout status deployment/frontend --timeout=90s
# Test via le nœud (front + proxy api) :
minikube --profile=forum ssh -- "curl -s -o /dev/null -w '%{http_code}\n' -H 'Host: forum.local' http://127.0.0.1/"
minikube --profile=forum ssh -- "curl -s -H 'Host: forum.local' http://127.0.0.1/api/health"
```
Expected: `200` pour `/`, et `{"status":"ok"}` pour `/api/health`.

- [ ] **Step 6: Commit**

```bash
git add k8s/50-frontend-deployment.yaml k8s/51-frontend-service.yaml k8s/30-ingress.yaml
git commit -m "feat(front): déploiement K8s frontend + route ingress (F6)"
```

---

## Self-Review (effectuée)

- **Couverture spec :** architecture (proxy nginx, monorepo) → F5/F1 ; écrans (shell, auth, fil, empty) → F3/F4 ; tokens → F1 ; wrapper API + quirk login + JWT → F2 ; conteneurisation → F5 ; K8s → F6. Tous les éléments de la spec sont couverts.
- **Cohérence des types :** `Topic`, `Category`, `Post`, et les fonctions (`getCategories`, `getTopics`, `getPosts`, `createPost`, `login`, `register`) définies en F2 sont utilisées avec la même signature en F3/F4.
- **Pas de placeholder :** chaque étape contient le code/commande réel.

## Notes
- En dev, l'API doit tourner (`docker compose up api db`) pour que le proxy Vite `/api` réponde.
- Le `.gitignore` ignore déjà `node_modules` à la racine ? Sinon, ajouter `frontend/node_modules/` et `frontend/dist/` au `.gitignore`.
- La règle « aucun secret versionné » : le front ne contient aucun secret (le JWT est obtenu au runtime).
