import { Search, Bell, HelpCircle, ChevronRight, Home, ChevronDown, User, LogOut, Settings } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../../context/AuthContext.jsx';

export default function Header() {
    const location = useLocation();
    const navigate = useNavigate();
    const { logout, user } = useAuth();
    const pathSegments = location.pathname.split('/').filter(Boolean);
    const [isProfileOpen, setIsProfileOpen] = useState(false);

    return (
        <header className="h-16 bg-[var(--color-bg-MAIN)] border-b border-[var(--color-BORDER)] sticky top-0 z-40 px-8 flex items-center justify-between shadow-sm transition-colors duration-300">
            {/* Left: Breadcrumbs */}
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-[var(--color-text-MUTED)]">
                <Home size={14} className="mb-0.5" />
                <ChevronRight size={12} />
                <span className={pathSegments.length === 0 ? 'text-[var(--color-text-MAIN)]' : ''}>Dashboard</span>
                {pathSegments.map((segment, index) => (
                    <div key={segment} className="flex items-center gap-2">
                        <ChevronRight size={12} />
                        <span className={index === pathSegments.length - 1 ? 'text-[var(--color-text-MAIN)]' : ''}>
                            {segment.replace('-', ' ')}
                        </span>
                    </div>
                ))}
            </div>

            {/* Right: Global Search & Actions */}
            <div className="flex items-center gap-6">
                {/* Search Bar */}
                <div className="relative group hidden md:block">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-MUTED)] group-focus-within:text-[var(--color-text-MAIN)] transition-colors" size={16} />
                    <input
                        type="text"
                        placeholder="Search Citizen ID or Record..."
                        className="pl-10 pr-4 py-2 w-64 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded-lg text-sm text-[var(--color-text-MAIN)] placeholder:text-[var(--color-text-MUTED)] focus:outline-none focus:ring-1 focus:ring-[var(--color-ACCENT)] focus:border-[var(--color-ACCENT)] transition-all font-medium"
                    />

                </div>

                {/* Divider */}
                <div className="h-6 w-px bg-[var(--color-BORDER)] hidden md:block"></div>

                {/* Icons */}
                <div className="flex items-center gap-4">
                    <button className="relative p-2 hover:bg-[var(--color-bg-SURFACE)] rounded-full transition-colors text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)]">
                        <Bell size={20} />
                        <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border border-[var(--color-bg-MAIN)]"></span>
                    </button>

                    {/* User Profile Dropdown */}
                    <div className="relative">
                        <button
                            onClick={() => setIsProfileOpen(!isProfileOpen)}
                            className="flex items-center gap-2 p-1.5 hover:bg-[var(--color-bg-SURFACE)] rounded-lg transition-colors border border-transparent hover:border-[var(--color-BORDER)]"
                        >
                            <div className="w-8 h-8 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] flex items-center justify-center font-ocr text-xs rounded-md">
                                SA
                            </div>
                            <ChevronDown size={14} className="text-[var(--color-text-MUTED)]" />
                        </button>

                        {/* Dropdown Menu */}
                        {isProfileOpen && (
                            <>
                                <div className="fixed inset-0 z-40" onClick={() => setIsProfileOpen(false)}></div>
                                <div className="absolute right-0 top-full mt-2 w-56 bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-xl rounded-lg z-50 py-1 animate-in fade-in slide-in-from-top-2 duration-200">
                                    <div className="px-4 py-3 border-b border-[var(--color-BORDER)]">
                                        <p className="text-sm font-bold text-[var(--color-text-MAIN)] uppercase">{user?.username || 'Super Admin'}</p>
                                        <p className="text-xs text-[var(--color-text-MUTED)] font-ocr">{user?.email || 'admin@citizen-zero.gov.ke'}</p>
                                    </div>
                                    <div className="py-1">
                                        <button className="w-full text-left px-4 py-2 text-sm text-[var(--color-text-MUTED)] hover:bg-[var(--color-bg-SURFACE)] hover:text-[var(--color-text-MAIN)] flex items-center gap-2">
                                            <User size={16} /> Profile
                                        </button>
                                        <button
                                            onClick={() => { setIsProfileOpen(false); window.location.href = '/settings/general'; }}
                                            className="w-full text-left px-4 py-2 text-sm text-[var(--color-text-MUTED)] hover:bg-[var(--color-bg-SURFACE)] hover:text-[var(--color-text-MAIN)] flex items-center gap-2"
                                        >
                                            <Settings size={16} /> Preference
                                        </button>
                                    </div>
                                    <div className="py-1 border-t border-[var(--color-BORDER)]">
                                        <button
                                            onClick={() => {
                                                setIsProfileOpen(false);
                                                logout();
                                            }}
                                            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2 font-medium"
                                        >
                                            <LogOut size={16} /> Sign Out
                                        </button>
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </header>
    );
}
