import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import MainPage from './MainPage'
import LoginPage from './Login'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
        <LoginPage></LoginPage>
    </>
  )
}

export default App
