import React, { useState, useEffect } from 'react';
import {
    Bell,
    Search,
    Moon,
    Sun,
    Flag,
    ChevronDown,
    LogOut,
    Menu,
    User,
    Settings
} from 'lucide-react';

export default function Header({ role, toggleSidebar }) {
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
    const [showProfileMenu, setShowProfileMenu] = useState(false);

    // Apply Theme Effect
    useEffect(() => {
        const root = document.documentElement;

        // Reset
        root.classList.remove('dark', 'kenya');

        if (theme === 'dark') {
            root.classList.add('dark');
        } else if (theme === 'kenya') {
            root.classList.add('kenya'); // Ensure .kenya class exists in CSS
        }

        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        if (theme === 'light') setTheme('dark');
        else if (theme === 'dark') setTheme('kenya');
        else setTheme('light');
    };

    const logout = () => {
        localStorage.clear();
        window.location.href = 'http://localhost:3000/login';
    };

    const getThemeIcon = () => {
        if (theme === 'light') return <Sun size={18} />;
        if (theme === 'dark') return <Moon size={18} />;
        return <Flag size={18} />; // Kenya Theme
    };

    return (
        <header className="h-16 bg-[var(--color-bg-MAIN)] border-b border-[var(--color-BORDER)] flex items-center justify-between px-6 sticky top-0 z-30 transition-colors duration-300">
            {/* Left: Toggle & Search */}
            <div className="flex items-center gap-4">
                <button
                    onClick={toggleSidebar}
                    className="p-2 -ml-2 text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] rounded-md transition-colors"
                >
                    <Menu size={20} />
                </button>

                <div className="relative hidden md:block">
                    <Search className="absolute left-3 top-2.5 text-[var(--color-text-MUTED)]" size={16} />
                    <input
                        type="text"
                        placeholder="Search records..."
                        className="pl-10 pr-4 py-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] text-sm w-64 focus:outline-none focus:border-[var(--color-ACCENT)] transition-colors"
                    />
                </div>
            </div>

            {/* Right: Actions */}
            <div className="flex items-center gap-4">
                {/* Theme Toggle */}
                <button
                    onClick={toggleTheme}
                    className="p-2 text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] transition-colors"
                    title="Toggle Theme"
                >
                    {getThemeIcon()}
                </button>

                {/* Notifications */}
                <button className="p-2 text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] transition-colors relative">
                    <Bell size={18} />
                    <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>

                {/* Divider */}
                <div className="h-6 w-px bg-[var(--color-BORDER)]"></div>

                {/* Profile */}
                <div className="relative">
                    <button
                        onClick={() => setShowProfileMenu(!showProfileMenu)}
                        className="flex items-center gap-3 hover:bg-[var(--color-bg-SURFACE)] p-2 transition-colors ml-1"
                    >
                        <div className="text-right hidden md:block">
                            <p className="text-xs font-bold text-[var(--color-text-MAIN)] uppercase">{role?.replace(/_/g, ' ')}</p>
                            <p className="text-[10px] text-[var(--color-text-MUTED)]">Safaricom PLC</p>
                        </div>
                        <div className="w-8 h-8 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] flex items-center justify-center font-bold text-xs uppercase shadow-sm">
                            {role ? role[0] : 'U'}
                        </div>
                        <ChevronDown size={14} className="text-[var(--color-text-MUTED)]" />
                    </button>

                    {/* Dropdown */}
                    {showProfileMenu && (
                        <div className="absolute right-0 mt-2 w-48 bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-lg py-1 animate-in fade-in slide-in-from-top-2 duration-200 z-50">
                            <button className="w-full text-left px-4 py-2 text-sm text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] flex items-center gap-2">
                                <User size={16} /> Profile
                            </button>
                            <button className="w-full text-left px-4 py-2 text-sm text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] flex items-center gap-2">
                                <Settings size={16} /> Settings
                            </button>
                            <div className="border-t border-[var(--color-BORDER)] my-1"></div>
                            <button
                                onClick={logout}
                                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50/10 flex items-center gap-2"
                            >
                                <LogOut size={16} /> Sign Out
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}
