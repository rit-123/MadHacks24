import { useState, useEffect } from 'react'
import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider, Navigate } from 'react-router-dom'
import MainPage from './MainPage'
import LoginPage from './Login'
import RegisterPage from './RegisterPage'

const App = () => {
    const [username, setUsername] = useState(() => {
        try {
            return localStorage.getItem('username')
        } catch (error) {
            return null
        }
    })
    const [router, setRouter] = useState(null)

    useEffect(() => {
        const newRouter = createBrowserRouter(
            createRoutesFromElements(
                username ?
                    <>
                        <Route index element={<Navigate to="/listen" replace />} />
                        <Route path="/listen" element={<MainPage username={username} setUsername={setUsername} />} />
                        <Route path="/*" element={<MainPage username={username} setUsername={setUsername} />} />
                    </> :
                    <>
                        <Route index element={<LoginPage setUsername={setUsername} />} />
                        <Route path="/register" element={<RegisterPage setUsername={setUsername} />} />
                        <Route path="/*" element={<Navigate to="/" replace />} />
                    </>
            )
        )
        setRouter(newRouter)
    }, [username])

    if (!router) return null

    return <div id="helllooooo"><RouterProvider router={router} /></div>
}

export default App