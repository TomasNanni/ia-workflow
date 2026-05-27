import { cn } from "@/lib/utils"

export default function PageHeader({ title, description, className, children, actions }) {
  return (
    <div className={cn(
      "flex items-center justify-between px-6 py-4 border-b border-border/40 bg-zinc-950/30 backdrop-blur-sm sticky top-0 z-10",
      className
    )}>
      <div className="space-y-0.5">
        {title && (
          <h1 className="text-lg font-bold tracking-tight text-white/90">
            {title}
          </h1>
        )}
        {description && (
          <p className="text-xs text-muted-foreground/80 font-medium">
            {description}
          </p>
        )}
      </div>
      
      <div className="flex items-center gap-3">
        {actions}
        {children}
      </div>
    </div>
  )
}
