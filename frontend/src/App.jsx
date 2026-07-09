import { useState } from 'react'
import AuthScreen from './components/AuthScreen'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  const [userRole, setUserRole] = useState(null)

  return userRole ? (
    <Dashboard role={userRole} onLogout={() => setUserRole(null)} />
  ) : (
    <AuthScreen onLogin={setUserRole} />
  )
}

export default App
