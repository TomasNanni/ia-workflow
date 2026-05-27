import { Outlet } from "react-router"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { TooltipProvider } from "@/components/ui/tooltip"
import { AppSidebar } from "@/components/AppSidebar"

export default function RootLayout() {
  return (
    <TooltipProvider>
      <SidebarProvider>
        <div className="min-h-screen flex w-full bg-obsidian-gradient text-foreground font-sans selection:bg-primary/30 selection:text-primary">
          <AppSidebar />
          <main className="flex-1 flex flex-col relative">
            {/* Subtle background glow effect */}
            <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-primary/5 blur-[120px] rounded-full pointer-events-none" />
            
            <header className="h-16 flex items-center px-4 border-b border-border/50 backdrop-blur-md sticky top-0 z-10">
              <SidebarTrigger className="hover:text-primary transition-colors" />
              <div className="ml-4 font-semibold text-primary tracking-tight">
                Analítica IA de BD
              </div>
            </header>
            <div className="flex-1 overflow-auto relative">
              <Outlet />
            </div>
          </main>
        </div>
      </SidebarProvider>
    </TooltipProvider>
  )
}
