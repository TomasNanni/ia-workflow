import { useEffect, useState } from "react"
import { useParams } from "react-router"
import ChatInterface from "@/components/ChatInterface"
import PageHeader from "@/components/PageHeader"
import SchemaMap from "@/components/SchemaMap"

export default function ChatPage() {
  const { sessionId } = useParams()
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchSession() {
      try {
        setLoading(true)
        const token = localStorage.getItem("access_token")
        const response = await fetch(`http://localhost:8000/api/v1/sessions/${sessionId}`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        })
        if (response.ok) {
          const data = await response.json()
          setSession(data)
        } else {
          setError("No se pudo cargar la sesión")
        }
      } catch (err) {
        setError("Error de conexión")
        console.error("Failed to fetch session:", err)
      } finally {
        setLoading(false)
      }
    }

    if (sessionId) {
      fetchSession()
    }
  }, [sessionId])

  if (loading) {
    return (
      <div className="flex flex-col h-full items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (error || !session) {
    return (
      <div className="flex flex-col h-full items-center justify-center p-8 text-center">
        <h2 className="text-xl font-bold text-red-400 mb-2">Error</h2>
        <p className="text-muted-foreground">{error || "Sesión no encontrada"}</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader title={session.title || "Chat de Analítica"} />
      
      <div className="flex flex-1 overflow-hidden divide-x divide-border/40">
        {/* Chat Section */}
        <div className="flex-1 flex flex-col min-w-0">
          <ChatInterface 
            sessionId={sessionId} 
            initialMessages={session.messages || []} 
          />
        </div>
        
        {/* Schema Section - Hidden on small screens */}
        <div className="hidden lg:block w-80 xl:w-96 shrink-0 overflow-hidden">
          <SchemaMap />
        </div>
      </div>
    </div>
  )
}
