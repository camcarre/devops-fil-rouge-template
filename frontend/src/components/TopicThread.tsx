import { useEffect, useRef, useState } from "react"
import { ArrowUp } from "lucide-react"
import { getPosts, createPost, currentUserId, type Post, type Topic } from "@/lib/api"
import { Textarea } from "@/components/ui/textarea"
import { UserAvatar } from "@/components/UserAvatar"

function time(iso: string): string {
  const d = new Date(iso)
  return isNaN(d.getTime()) ? "" : d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

export function TopicThread({ topic }: { topic: Topic }) {
  const [posts, setPosts] = useState<Post[]>([])
  const [draft, setDraft] = useState("")
  const me = currentUserId()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => { getPosts(topic.id).then(setPosts).catch(() => setPosts([])) }, [topic.id])
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }) }, [posts])

  async function send() {
    if (!draft.trim()) return
    const p = await createPost(topic.id, draft)
    setPosts((prev) => [...prev, p]); setDraft("")
  }

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send() }
  }

  return (
    <div className="mx-auto flex h-screen max-w-2xl flex-col px-6 py-6">
      <h1 className="mb-4 border-b border-fog pb-3 text-center text-subheading text-ink-black">{topic.title}</h1>

      <div className="flex-1 space-y-1 overflow-y-auto px-1">
        {posts.map((p) => {
          const own = me != null && p.user_id === me
          return (
            <div key={p.id} className={own ? "flex flex-col items-end" : "flex flex-col items-start"}>
              <div className={own ? "flex flex-row-reverse items-end gap-2" : "flex flex-row items-end gap-2"}>
                <UserAvatar userId={p.user_id} />
                <div
                  className={
                    "max-w-[78%] whitespace-pre-wrap break-words px-3.5 py-2 text-body " +
                    (own
                      ? "rounded-[18px] rounded-br-[5px] bg-[#007AFF] text-white"
                      : "rounded-[18px] rounded-bl-[5px] bg-[#e9e9eb] text-ink-black")
                  }
                >
                  {p.content}
                </div>
              </div>
              <span className={"mt-0.5 px-9 text-[11px] text-ash " + (own ? "text-right" : "text-left")}>
                {time(p.created_at)}
              </span>
            </div>
          )
        })}
        <div ref={bottomRef} />
      </div>

      <div className="mt-3 flex items-end gap-2 rounded-[20px] border border-fog bg-snow py-1.5 pl-4 pr-1.5">
        <Textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Message"
          rows={1}
          className="max-h-32 min-h-[28px] flex-1 resize-none border-0 bg-transparent p-0 text-body shadow-none focus-visible:ring-0"
        />
        <button
          onClick={send}
          disabled={!draft.trim()}
          aria-label="Envoyer"
          className="mb-0.5 flex h-7 w-7 items-center justify-center rounded-full bg-[#007AFF] text-white transition-opacity disabled:opacity-30"
        >
          <ArrowUp className="h-4 w-4" strokeWidth={2.5} />
        </button>
      </div>
    </div>
  )
}
