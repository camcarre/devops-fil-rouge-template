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
