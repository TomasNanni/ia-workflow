import { BrowserRouter, Routes, Route, useParams } from "react-router"
import RootLayout from "@/layouts/RootLayout"
import Home from "@/pages/Home"
import About from "@/pages/About"
import NotFound from "@/pages/NotFound"
import Dashboard from "@/pages/dashboard/Dashboard"
import DashboardHome from "@/pages/dashboard/DashboardHome"
import Settings from "@/pages/dashboard/Settings"

const ChatPagePlaceholder = () => {
  const { sessionId } = useParams()
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4 text-emerald-500">Chat Session: {sessionId}</h1>
      <p className="text-zinc-400">This is a placeholder for the chat interface (STORY-004).</p>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<RootLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="chat/:sessionId" element={<ChatPagePlaceholder />} />
          <Route path="about" element={<About />} />
          <Route path="dashboard" element={<Dashboard />}>
            <Route index element={<DashboardHome />} />
            <Route path="settings" element={<Settings />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
