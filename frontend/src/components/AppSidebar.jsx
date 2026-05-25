import { useEffect, useState } from "react"
import { NavLink, useNavigate } from "react-router"
import { format } from "date-fns"
import { es } from "date-fns/locale"
import { Plus, MessageSquare, LogOut, User } from "lucide-react"
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
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export function AppSidebar() {
  const [sessions, setSessions] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchSessions() {
      try {
        const response = await fetch("http://localhost:8000/api/v1/sessions")
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

  const handleNewChat = () => {
    navigate("/")
  }

  return (
    <Sidebar variant="floating" collapsible="icon" className="border-r border-border/50">
      <SidebarHeader className="p-4">
        <Button 
          onClick={handleNewChat}
          className="w-full justify-start gap-2 bg-primary hover:bg-primary/90 text-primary-foreground emerald-glow transition-all"
        >
          <Plus className="h-4 w-4" />
          <span className="group-data-[collapsible=icon]:hidden">Nuevo Chat</span>
        </Button>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-muted-foreground/50 px-4 mb-2">Conversaciones Recientes</SidebarGroupLabel>
          <SidebarMenu className="px-2">
            {sessions.map((session) => (
              <SidebarMenuItem key={session.id}>
                <SidebarMenuButton asChild tooltip={session.title}>
                  <NavLink
                    to={`/chat/${session.id}`}
                    className={({ isActive }) =>
                      cn(
                        "flex flex-col items-start gap-0.5 py-3 h-auto transition-colors rounded-md px-3",
                        isActive 
                          ? "bg-primary/10 text-primary border border-primary/20" 
                          : "hover:bg-muted/50 text-foreground/70 hover:text-foreground"
                      )
                    }
                  >
                    <div className="flex items-center gap-2 w-full">
                      <MessageSquare className={cn("h-4 w-4 shrink-0", "text-primary/70")} />
                      <span className="truncate font-medium">{session.title || "Sesión sin título"}</span>
                    </div>
                    <span className="text-[10px] text-muted-foreground/60 ml-6 group-data-[collapsible=icon]:hidden">
                      {format(new Date(session.created_at), "d 'de' MMMM", { locale: es })}
                    </span>
                  </NavLink>
                </SidebarMenuButton>
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
