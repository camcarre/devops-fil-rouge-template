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
