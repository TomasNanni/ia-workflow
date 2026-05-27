import { useEffect, useState } from "react"
import { NavLink, useNavigate, useParams } from "react-router"
import { format } from "date-fns"
import { es } from "date-fns/locale"
import { Plus, MessageSquare, LogOut, User, Trash2 } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export function AppSidebar() {
  const [sessions, setSessions] = useState([])
  const navigate = useNavigate()
  const { sessionId: activeSessionId } = useParams()

  useEffect(() => {
    async function fetchSessions() {
      try {
        const token = localStorage.getItem("access_token")
        const response = await fetch("http://localhost:8000/api/v1/sessions", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        })
        if (response.ok) {
          const data = await response.json()
          // Sort by created_at descending (newest first)
          const sortedData = data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          setSessions(sortedData)
        }
      } catch (error) {
        console.error("Failed to fetch sessions:", error)
      }
    }

    fetchSessions()
  }, [])

  const handleNewChat = async () => {
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
        setSessions(prev => [newSession, ...prev])
        navigate(`/chat/${newSession.id}`)
      }
    } catch (error) {
      console.error("Failed to create new session:", error)
    }
  }

  const handleDeleteSession = async (sessionId) => {
    try {
      const token = localStorage.getItem("access_token")
      const response = await fetch(`http://localhost:8000/api/v1/sessions/${sessionId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
      })

      if (response.ok) {
        setSessions((prev) => prev.filter((s) => s.id !== sessionId))
        if (activeSessionId === String(sessionId)) {
          navigate("/")
        }
      } else {
        console.error("Failed to delete session")
      }
    } catch (error) {
      console.error("Error deleting session:", error)
    }
  }

  return (
    <Sidebar variant="floating" collapsible="icon" className="border-r border-border/50">
      <SidebarHeader className="p-4">
        <Button 
          onClick={handleNewChat}
          className="w-full justify-start gap-2 bg-primary hover:bg-primary/90 text-primary-foreground font-bold tracking-tight emerald-glow transition-all rounded-xl py-6"
        >
          <Plus className="h-5 w-5" />
          <span className="group-data-[collapsible=icon]:hidden text-base">Nueva Sesión</span>
        </Button>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-muted-foreground/50 px-4 mb-2">Conversaciones Recientes</SidebarGroupLabel>
          <SidebarMenu className="px-2">
            {sessions.map((session) => (
              <SidebarMenuItem key={session.id} className="group/item relative">
                <SidebarMenuButton asChild tooltip={session.title}>
                  <NavLink
                    to={`/chat/${session.id}`}
                    className={({ isActive }) =>
                      cn(
                        "flex flex-col items-start gap-0.5 py-3 h-auto transition-colors rounded-md px-3 pr-10",
                        isActive 
                          ? "bg-primary/10 text-primary border border-primary/20" 
                          : "hover:bg-muted/50 text-foreground/70 hover:text-foreground"
                      )
                    }
                  >
                    {({ isActive }) => (
                      <>
                        <div className="flex items-center gap-2 w-full">
                          <MessageSquare className={cn("h-4 w-4 shrink-0", isActive ? "text-primary" : "text-primary/70")} />
                          <span className={cn(
                            "truncate", 
                            session.title === "Nueva Sesión" ? "font-bold text-foreground/90" : "font-medium"
                          )}>
                            {session.title || "Sesión sin título"}
                          </span>
                        </div>
                        <span className="text-[10px] text-muted-foreground/60 ml-6 group-data-[collapsible=icon]:hidden">
                          {format(new Date(session.created_at), "d 'de' MMMM", { locale: es })}
                        </span>
                      </>
                    )}
                  </NavLink>
                </SidebarMenuButton>
                
                <div className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover/item:opacity-100 transition-opacity group-data-[collapsible=icon]:hidden">
                  <AlertDialog>
                    <AlertDialogTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-7 w-7 text-muted-foreground hover:text-red-400 hover:bg-red-500/10"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>¿Estás seguro?</AlertDialogTitle>
                        <AlertDialogDescription>
                          Esta acción no se puede deshacer. Se eliminará permanentemente la sesión de chat y todo su historial.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancelar</AlertDialogCancel>
                        <AlertDialogAction
                          onClick={() => handleDeleteSession(session.id)}
                          className="bg-red-600 hover:bg-red-700 text-white"
                        >
                          Eliminar
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="p-4 border-t border-border/50">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton className="gap-2 hover:bg-muted/50 transition-colors">
              <User className="h-4 w-4" />
              <span>Perfil</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton className="gap-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-colors">
              <LogOut className="h-4 w-4" />
              <span>Cerrar Sesión</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
