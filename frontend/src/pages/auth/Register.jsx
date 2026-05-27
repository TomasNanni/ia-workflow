import { useState } from "react"
import { useNavigate, Link } from "react-router"
import { UserPlus, Mail, Lock, CheckCircle2, AlertCircle, Loader2, ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function Register() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setSuccess("")

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden")
      return
    }

    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || "Error al registrarse")
      }

      setSuccess("¡Cuenta creada con éxito! Redirigiendo...")
      setTimeout(() => {
        navigate("/login")
      }, 2000)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#020817] p-4 relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-500/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[120px]" />
      </div>

      <Card className="w-full max-w-md border-zinc-800 bg-zinc-950/50 backdrop-blur-xl shadow-2xl relative z-10">
        <CardHeader className="space-y-1 text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 emerald-glow-subtle">
              <UserPlus className="h-8 w-8 text-emerald-500" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold tracking-tight text-white">Crear Cuenta</CardTitle>
          <CardDescription className="text-zinc-400">
            Únete para empezar a analizar tus datos con IA
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4 pt-4">
            {error && (
              <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center gap-2 text-red-400 text-sm animate-in fade-in zoom-in duration-200">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <p>{error}</p>
              </div>
            )}
            {success && (
              <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center gap-2 text-emerald-400 text-sm animate-in fade-in zoom-in duration-200">
                <CheckCircle2 className="h-4 w-4 shrink-0" />
                <p>{success}</p>
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="email" className="text-zinc-300 ml-1">Correo electrónico</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
                <Input
                  id="email"
                  type="email"
                  placeholder="nombre@ejemplo.com"
                  className="pl-10 bg-zinc-900/50 border-zinc-800 focus:border-emerald-500/50 focus:ring-emerald-500/20 transition-all text-zinc-200"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password" className="text-zinc-300 ml-1">Contraseña</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  className="pl-10 bg-zinc-900/50 border-zinc-800 focus:border-emerald-500/50 focus:ring-emerald-500/20 transition-all text-zinc-200"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="text-zinc-300 ml-1">Confirmar Contraseña</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-500" />
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  className="pl-10 bg-zinc-900/50 border-zinc-800 focus:border-emerald-500/50 focus:ring-emerald-500/20 transition-all text-zinc-200"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4 pb-8">
            <Button 
              type="submit" 
              className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-6 rounded-xl transition-all emerald-glow group" 
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <div className="flex items-center justify-center gap-2">
                  <span>Registrarse</span>
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </div>
              )}
            </Button>
            <p className="text-sm text-zinc-500 text-center">
              ¿Ya tienes una cuenta?{" "}
              <Link to="/login" className="text-emerald-500 hover:text-emerald-400 font-medium transition-colors">
                Inicia sesión
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
