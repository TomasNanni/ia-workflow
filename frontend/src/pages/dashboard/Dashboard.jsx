import { Outlet, NavLink } from "react-router"
import { cn } from "@/lib/utils"

export default function Dashboard() {
  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-foreground mb-2">Panel de Control</h1>
        <p className="text-muted-foreground">Gestiona tu configuración y revisa el estado de tus análisis.</p>
      </div>
      
      <nav className="flex gap-1 mb-8 bg-muted/30 p-1 rounded-lg w-fit border border-border/50">
        <NavLink 
          to="/dashboard" 
          end 
          className={({ isActive }) => cn(
            "px-4 py-2 rounded-md transition-all text-sm font-medium",
            isActive 
              ? "bg-primary text-primary-foreground shadow-sm" 
              : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
          )}
        >
          Resumen
        </NavLink>
        <NavLink 
          to="/dashboard/settings" 
          className={({ isActive }) => cn(
            "px-4 py-2 rounded-md transition-all text-sm font-medium",
            isActive 
              ? "bg-primary text-primary-foreground shadow-sm" 
              : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
          )}
        >
          Configuración
        </NavLink>
      </nav>
      
      <div className="bg-card/30 rounded-xl border border-border/50 p-6 backdrop-blur-sm relative overflow-hidden">
        {/* Decorative corner glow */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 blur-3xl pointer-events-none" />
        <Outlet />
      </div>
    </div>
  )
}
