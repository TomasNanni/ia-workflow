import { useState, useRef, useEffect } from "react"
import { Send, User, Bot, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

export default function ChatInterface({ sessionId, initialMessages = [] }) {
  const [messages, setMessages] = useState(initialMessages)
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const scrollRef = useRef(null)

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = { role: "user", content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await fetch(`http://localhost:8000/api/v1/sessions/${sessionId}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      })

      if (response.ok) {
        const data = await response.json()
        setMessages((prev) => [...prev, { role: "assistant", content: data.response }])
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "Lo siento, hubo un error al procesar tu solicitud." },
        ])
      }
    } catch (error) {
      console.error("Chat error:", error)
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error de conexión con el servidor." },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const renderMessageContent = (content) => {
    // Simple parser for SQL blocks
    const parts = content.split(/(```sql[\s\S]*?```)/g)
    return parts.map((part, index) => {
      if (part.startsWith("```sql")) {
        const sql = part.replace(/```sql\n?|```/g, "").trim()
        return (
          <div key={index} className="relative group my-3">
            <div className="absolute -top-3 left-4 px-2 py-0.5 bg-zinc-800 text-[10px] text-zinc-400 rounded border border-emerald-500/20 font-mono">
              SQL
            </div>
            <pre className="bg-zinc-950 p-4 pt-6 rounded-lg overflow-x-auto font-mono text-xs border border-emerald-500/10 emerald-glow-subtle">
              <code className="text-emerald-400/90 leading-relaxed">{sql}</code>
            </pre>
          </div>
        )
      }
      return <span key={index} className="whitespace-pre-wrap">{part}</span>
    })
  }

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto border-x border-border/40 bg-zinc-950/50 backdrop-blur-sm">
      {/* Messages Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent"
      >
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-50">
            <Bot className="h-12 w-12 text-primary/50" />
            <div>
              <p className="text-lg font-medium">¿En qué puedo ayudarte hoy?</p>
              <p className="text-sm">Pregunta sobre ventas, clientes o productos.</p>
            </div>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div 
            key={idx} 
            className={cn(
              "flex w-full gap-3 animate-in fade-in slide-in-from-bottom-2 duration-300",
              msg.role === "user" ? "flex-row-reverse" : "flex-row"
            )}
          >
            <div className={cn(
              "h-8 w-8 rounded-full flex items-center justify-center shrink-0 border",
              msg.role === "user" 
                ? "bg-zinc-800 border-zinc-700 text-zinc-400" 
                : "bg-emerald-500/10 border-emerald-500/20 text-emerald-500"
            )}>
              {msg.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>
            
            <div className={cn(
              "max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm",
              msg.role === "user" 
                ? "bg-zinc-900 text-zinc-100 rounded-tr-none border border-zinc-800" 
                : "bg-zinc-900/40 text-zinc-300 rounded-tl-none border border-zinc-800/50"
            )}>
              {renderMessageContent(msg.content)}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex w-full gap-3 animate-pulse">
            <div className="h-8 w-8 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0">
              <Loader2 className="h-4 w-4 text-emerald-500 animate-spin" />
            </div>
            <div className="bg-zinc-900/40 border border-zinc-800/50 rounded-2xl rounded-tl-none px-4 py-3">
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-emerald-500/40 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                <span className="w-1.5 h-1.5 bg-emerald-500/40 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                <span className="w-1.5 h-1.5 bg-emerald-500/40 rounded-full animate-bounce"></span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-border/40 bg-zinc-950/80 backdrop-blur-md">
        <form 
          onSubmit={handleSend}
          className="relative flex items-center max-w-3xl mx-auto"
        >
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu consulta analítica..."
            className="pr-12 py-6 bg-zinc-900/50 border-zinc-800 focus:border-primary/50 focus:ring-primary/20 transition-all rounded-xl"
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            size="icon" 
            disabled={!input.trim() || isLoading}
            className="absolute right-2 h-9 w-9 bg-primary hover:bg-primary/90 text-primary-foreground emerald-glow transition-all rounded-lg"
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
        <p className="text-[10px] text-center mt-3 text-muted-foreground/40">
          El agente puede cometer errores. Verifica las consultas SQL generadas.
        </p>
      </div>
    </div>
  )
}
