import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { cn } from "@/lib/utils"

// Palette déterministe par user_id (style iMessage : pastilles colorées).
const COLORS = [
  "bg-[#FF9500]", "bg-[#34C759]", "bg-[#00C7BE]", "bg-[#30B0C7]",
  "bg-[#5856D6]", "bg-[#AF52DE]", "bg-[#FF2D55]", "bg-[#A2845E]",
]

// L'API ne renvoie pas de nom : on dérive une lettre A–Z de l'id.
function initial(userId: number): string {
  return String.fromCharCode(65 + ((userId - 1) % 26))
}

export function UserAvatar({ userId, className }: { userId: number; className?: string }) {
  const color = COLORS[((userId - 1) % COLORS.length + COLORS.length) % COLORS.length]
  return (
    <Avatar className={cn("h-7 w-7 shrink-0", className)}>
      <AvatarFallback className={cn("text-[12px] font-medium text-white", color)}>
        {initial(userId)}
      </AvatarFallback>
    </Avatar>
  )
}
