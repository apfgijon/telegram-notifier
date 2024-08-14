import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import "@fontsource/open-sans/300.css"; // Light
import "@fontsource/open-sans/400.css"; // Regular
import "@fontsource/open-sans/600.css"; // Semi-bold
import "@fontsource/open-sans/700.css"; // Bold
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
