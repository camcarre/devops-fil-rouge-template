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
