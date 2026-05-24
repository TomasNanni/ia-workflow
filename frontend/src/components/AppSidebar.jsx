import { useEffect, useState } from "react"
import { NavLink, useNavigate } from "react-router"
import { format } from "date-fns"
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
    <Sidebar variant="floating" collapsible="icon">
      <SidebarHeader className="p-4">
        <Button 
          onClick={handleNewChat}
          className="w-full justify-start gap-2 bg-emerald-600 hover:bg-emerald-700 text-white"
        >
          <Plus className="h-4 w-4" />
          <span>New Chat</span>
        </Button>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Recent Conversations</SidebarGroupLabel>
          <SidebarMenu>
            {sessions.map((session) => (
              <SidebarMenuItem key={session.id}>
                <SidebarMenuButton asChild>
                  <NavLink
                    to={`/chat/${session.id}`}
                    className={({ isActive }) =>
                      cn(
                        "flex flex-col items-start gap-1 py-3 h-auto",
                        isActive && "bg-sidebar-accent text-sidebar-accent-foreground"
                      )
                    }
                  >
                    <div className="flex items-center gap-2 w-full">
                      <MessageSquare className="h-4 w-4 shrink-0" />
                      <span className="truncate font-medium">{session.title || "Untitled Session"}</span>
                    </div>
                    <span className="text-[10px] text-muted-foreground ml-6">
                      {format(new Date(session.created_at), "MMM d, yyyy")}
                    </span>
                  </NavLink>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="p-4 border-t border-sidebar-border">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton className="gap-2">
              <User className="h-4 w-4" />
              <span>Profile</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton className="gap-2 text-red-500 hover:text-red-600 hover:bg-red-50/10">
              <LogOut className="h-4 w-4" />
              <span>Logout</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
