import { Outlet } from "react-router"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"

export default function RootLayout() {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-zinc-950 text-zinc-50">
        <AppSidebar />
        <main className="flex-1 flex flex-col">
          <header className="h-16 flex items-center px-4 border-b border-zinc-800">
            <SidebarTrigger />
            <div className="ml-4 font-semibold text-emerald-500">
              DB Analytics AI
            </div>
          </header>
          <div className="flex-1 overflow-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </SidebarProvider>
  )
}
