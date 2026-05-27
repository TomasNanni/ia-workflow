import { useEffect, useState } from "react"
import { Database, Table, Loader2, AlertCircle } from "lucide-react"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { cn } from "@/lib/utils"

export default function SchemaMap({ className }) {
  const [schema, setSchema] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchSchema() {
      try {
        setLoading(true)
        const token = localStorage.getItem("access_token")
        const response = await fetch("http://localhost:8000/api/v1/analytics/schema", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        })
        if (response.ok) {
          const data = await response.json()
          setSchema(data)
        } else {
          setError("No se pudo cargar el esquema")
        }
      } catch (err) {
        setError("Error de conexión")
        console.error("Failed to fetch schema:", err)
      } finally {
        setLoading(false)
      }
    }

    fetchSchema()
  }, [])

  if (loading) {
    return (
      <div className={cn("flex flex-col items-center justify-center h-full p-8 space-y-4", className)}>
        <Loader2 className="h-8 w-8 text-primary animate-spin" />
        <p className="text-sm text-muted-foreground">Cargando esquema...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className={cn("flex flex-col items-center justify-center h-full p-8 text-center space-y-4", className)}>
        <AlertCircle className="h-8 w-8 text-red-500/50" />
        <p className="text-sm text-muted-foreground">{error}</p>
      </div>
    )
  }

  return (
    <div className={cn("flex flex-col h-full bg-zinc-950/30", className)}>
      <div className="p-4 border-b border-border/40 flex items-center gap-2 bg-zinc-900/20">
        <Database className="h-4 w-4 text-emerald-500" />
        <h2 className="text-sm font-semibold tracking-tight uppercase text-zinc-400">Mapa del Esquema</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent">
        {schema.length === 0 ? (
          <p className="text-xs text-center text-muted-foreground p-8">No se encontraron tablas.</p>
        ) : (
          <Accordion type="multiple" className="space-y-1">
            {schema.map((table) => (
              <AccordionItem 
                key={table.name} 
                value={table.name}
                className="border border-emerald-500/5 bg-zinc-900/40 rounded-lg overflow-hidden px-0"
              >
                <AccordionTrigger className="hover:no-underline hover:bg-emerald-500/5 px-4 py-3 transition-colors">
                  <div className="flex items-center gap-2">
                    <Table className="h-3.5 w-3.5 text-emerald-500/70" />
                    <span className="text-xs font-medium text-zinc-300">{table.name}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-3 pt-1">
                  <div className="space-y-1.5 pl-5 border-l border-emerald-500/10 ml-1.5">
                    {table.columns.map((col) => (
                      <div key={col.name} className="flex items-center justify-between group">
                        <span className="text-[11px] text-zinc-400 font-mono">{col.name}</span>
                        <span className="text-[9px] text-zinc-600 font-mono uppercase bg-zinc-950 px-1.5 py-0.5 rounded border border-zinc-800 group-hover:border-zinc-700 transition-colors">
                          {col.type.split("(")[0]}
                        </span>
                      </div>
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        )}
      </div>
    </div>
  )
}
