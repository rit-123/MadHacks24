import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import MainPage from './MainPage'
import LoginPage from './Login'
import RegisterPage from './RegisterPage'

import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from 'react-router-dom'

username = localStorage.getItem('username')
const router = createBrowserRouter(
    createRoutesFromElements(
        username ?
            <>
                <Route index element={<MainPage />} />
            </> :
            <>
                <Route index element={<LoginPage />} />
                <Route path="/about" element={<RegisterPage />} />
            </>
    )
);

const App = () => {
    return <RouterProvider router={router} />
}

export default App
