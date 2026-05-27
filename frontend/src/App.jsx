import { BrowserRouter, Routes, Route } from "react-router"
import RootLayout from "@/layouts/RootLayout"
import Home from "@/pages/Home"
import About from "@/pages/About"
import NotFound from "@/pages/NotFound"
import Dashboard from "@/pages/dashboard/Dashboard"
import DashboardHome from "@/pages/dashboard/DashboardHome"
import Settings from "@/pages/dashboard/Settings"
import ChatPage from "@/pages/dashboard/ChatPage"
import Login from "@/pages/auth/Login"
import Register from "@/pages/auth/Register"
import RequireAuth from "@/components/auth/RequireAuth"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />

        <Route element={<RequireAuth />}>
          <Route element={<RootLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="chat/:sessionId" element={<ChatPage />} />
            <Route path="about" element={<About />} />
            <Route path="dashboard" element={<Dashboard />}>
              <Route index element={<DashboardHome />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Route>
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
