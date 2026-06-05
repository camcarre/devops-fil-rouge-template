import { useEffect, useState } from "react"
import { getCategories, getTopics, currentUserId, type Category, type Topic } from "@/lib/api"
import { useAuth } from "@/lib/auth"
import { UserAvatar } from "@/components/UserAvatar"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

export function Sidebar({ onSelectTopic }: { onSelectTopic: (t: Topic) => void }) {
  const { logout } = useAuth()
  const me = currentUserId()
  const [cats, setCats] = useState<Category[]>([])
  const [topics, setTopics] = useState<Record<number, Topic[]>>({})
  const [open, setOpen] = useState<Record<number, boolean>>({})
  const [selected, setSelected] = useState<number | null>(null)

  useEffect(() => { getCategories().then(setCats).catch(() => setCats([])) }, [])

  async function toggle(cat: Category) {
    setOpen((p) => ({ ...p, [cat.id]: !p[cat.id] }))
    if (!topics[cat.id]) {
      const t = await getTopics(cat.id).catch(() => [])
      setTopics((prev) => ({ ...prev, [cat.id]: t }))
    }
  }

  function pick(t: Topic) {
    setSelected(t.id)
    onSelectTopic(t)
  }

  return (
    <aside className="flex h-screen w-[272px] flex-col border-r border-line bg-cloud">
      {/* En-tête */}
      <div className="flex items-center gap-2.5 px-4 py-4">
        <div className="grid h-8 w-8 place-items-center rounded-[9px] bg-ink-black text-[14px] font-semibold text-snow">
          F
        </div>
        <span className="text-subheading font-semibold text-ink-black">Forum</span>
      </div>

      {/* Catégories & sujets */}
      <ScrollArea className="flex-1 px-2">
        {cats.map((c) => (
          <div key={c.id} className="mb-0.5">
            <button
              onClick={() => toggle(c)}
              className="flex w-full items-center gap-2 rounded-[10px] px-2.5 py-2 text-left text-caption font-medium text-ink-black transition-colors hover:bg-fog"
            >
              <span className={cn("text-[11px] text-ash transition-transform duration-150", open[c.id] && "rotate-90")}>
                ▶
              </span>
              <span className="truncate">{c.name}</span>
            </button>

            {open[c.id] &&
              (topics[c.id] || []).map((t) => (
                <button
                  key={t.id}
                  onClick={() => pick(t)}
                  className={cn(
                    "ml-3.5 block w-full truncate rounded-[8px] px-2.5 py-1.5 text-left text-caption transition-colors",
                    selected === t.id
                      ? "bg-snow font-medium text-ink-black shadow-[0_1px_2px_rgba(0,0,0,0.06)]"
                      : "text-smoke hover:bg-fog",
                  )}
                >
                  {t.title}
                </button>
              ))}

            {open[c.id] && topics[c.id]?.length === 0 && (
              <div className="ml-3.5 px-2.5 py-1.5 text-[13px] text-ash">Aucun sujet pour l'instant</div>
            )}
          </div>
        ))}
      </ScrollArea>

      {/* Bouton nouveau sujet */}
      <div className="px-3 pb-2 pt-1.5">
        <Button className="w-full rounded-[10px] bg-ink-black text-snow hover:bg-[#262626]">+ Nouveau sujet</Button>
      </div>

      {/* Profil utilisateur */}
      <div className="flex items-center gap-2.5 border-t border-line px-3 py-3">
        {me != null && <UserAvatar userId={me} className="h-9 w-9" />}
        <div className="min-w-0 flex-1">
          <div className="truncate text-caption font-medium text-ink-black">Mon compte</div>
          <div className="truncate text-[12px] text-ash">Connecté</div>
        </div>
        <button
          onClick={logout}
          title="Se déconnecter"
          className="rounded-[8px] px-2.5 py-1.5 text-[13px] font-medium text-smoke transition-colors hover:bg-fog hover:text-ink-black"
        >
          Quitter
        </button>
      </div>
    </aside>
  )
}
