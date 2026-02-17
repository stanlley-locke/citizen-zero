import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { ThemeProvider } from './context/ThemeContext.jsx';
import './index.css';

console.log('Main.jsx: Mounting React App...');

try {
    ReactDOM.createRoot(document.getElementById('root')).render(
        <React.StrictMode>
            <ThemeProvider>
                <App />
            </ThemeProvider>
        </React.StrictMode>,
    );
    console.log('Main.jsx: App mounted successfully.');
} catch (error) {
    console.error('Main.jsx: Critical Error during mount:', error);
    document.getElementById('root').innerHTML = `<div style="color:red; padding: 20px;">CRITICAL ERROR: ${error.message}</div>`;
}
