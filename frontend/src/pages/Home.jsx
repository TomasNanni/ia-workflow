import { useNavigate } from "react-router"
import { Database, Plus, MessageSquare, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function Home() {
  const navigate = useNavigate()

  const handleStartChat = async () => {
    try {
      const token = localStorage.getItem("access_token")
      const response = await fetch("http://localhost:8000/api/v1/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title: "Nueva Sesión" })
      })
      if (response.ok) {
        const newSession = await response.json()
        navigate(`/chat/${newSession.id}`)
      }
    } catch (error) {
      console.error("Failed to create new session:", error)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center h-full p-8 text-center space-y-8 animate-in fade-in duration-700">
      <div className="relative">
        <div className="absolute inset-0 bg-primary/20 blur-3xl rounded-full" />
        <div className="relative p-6 rounded-3xl bg-zinc-900 border border-primary/20 shadow-2xl">
          <Database className="h-16 w-16 text-primary" />
        </div>
        <Sparkles className="absolute -top-2 -right-2 h-8 w-8 text-primary animate-pulse" />
      </div>

      <div className="max-w-md space-y-3">
        <h1 className="text-4xl font-bold tracking-tight text-white">Analítica Inteligente</h1>
        <p className="text-zinc-400 text-lg">
          Conversa con tus datos. Realiza consultas complejas en lenguaje natural y obtén resultados instantáneos.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-lg">
        <Button 
          onClick={handleStartChat}
          className="h-auto py-6 px-8 flex flex-col items-center gap-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-2xl transition-all emerald-glow group"
        >
          <Plus className="h-6 w-6 group-hover:rotate-90 transition-transform duration-300" />
          <div className="text-left">
            <div className="font-extrabold text-lg tracking-tight">Nueva Sesión</div>
            <div className="text-xs font-medium opacity-70">Comienza un nuevo análisis</div>
          </div>
        </Button>

        <Button 
          variant="outline"
          className="h-auto py-6 px-8 flex flex-col items-center gap-3 border-zinc-800 bg-zinc-900/50 hover:bg-zinc-800 text-zinc-300 rounded-2xl transition-all"
          onClick={() => {
            const sidebarBtn = document.querySelector('[data-sidebar="menu-button"]')
            if (sidebarBtn) sidebarBtn.click()
          }}
        >
          <MessageSquare className="h-6 w-6" />
          <div className="text-left">
            <div className="font-bold">Historial</div>
            <div className="text-xs opacity-80">Explora chats anteriores</div>
          </div>
        </Button>
      </div>

      <div className="pt-8 grid grid-cols-3 gap-8 opacity-40 grayscale hover:grayscale-0 transition-all duration-500">
        <div className="flex flex-col items-center gap-2">
          <div className="h-1 w-8 bg-primary rounded-full" />
          <span className="text-[10px] font-mono uppercase tracking-widest">SQL Auto</span>
        </div>
        <div className="flex flex-col items-center gap-2">
          <div className="h-1 w-8 bg-primary rounded-full" />
          <span className="text-[10px] font-mono uppercase tracking-widest">Seguro</span>
        </div>
        <div className="flex flex-col items-center gap-2">
          <div className="h-1 w-8 bg-primary rounded-full" />
          <span className="text-[10px] font-mono uppercase tracking-widest">Rápido</span>
        </div>
      </div>
    </div>
  )
}
