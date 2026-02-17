import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header.jsx'; // Explicit extension

export default function Layout() {
    const [isCollapsed, setIsCollapsed] = useState(false);

    return (
        <div className="min-h-screen bg-[var(--color-bg-MAIN)] font-sans text-[var(--color-text-MAIN)] selection:bg-[var(--color-ACCENT)] selection:text-[var(--color-ACCENT-text)] flex transition-colors duration-300">
            {/* Sidebar with controlled state */}
            <Sidebar
                isCollapsed={isCollapsed}
                toggleCollapse={() => setIsCollapsed(!isCollapsed)}
            />

            {/* Main Content Wrapper */}
            <main
                className={`flex-1 min-h-screen bg-[var(--color-bg-SURFACE)] transition-all duration-300 ease-in-out flex flex-col ${isCollapsed ? 'ml-20' : 'ml-72'
                    }`}
            >
                {/* Top Navigation Header */}
                <Header />

                {/* Page Content */}
                <div className="p-8 max-w-[1800px] w-full mx-auto animate-in fade-in duration-300">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
