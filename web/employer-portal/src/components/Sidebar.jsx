import React, { useState } from 'react';
import { ChevronDown, ChevronRight, LogOut } from 'lucide-react';

export default function Sidebar({ isOpen, menuItems, activePath, onNavigate, logout }) {
    const [expandedMenus, setExpandedMenus] = useState({});

    const toggleSubMenu = (label) => {
        setExpandedMenus(prev => ({
            ...prev,
            [label]: !prev[label]
        }));
    };

    return (
        <aside className={`${isOpen ? 'w-64' : 'w-20'} bg-[var(--color-bg-MAIN)] border-r border-[var(--color-BORDER)] flex flex-col fixed h-full z-20 transition-all duration-300 md:relative`}>
            {/* Brand / Logo Area */}
            <div className={`h-16 flex items-center ${isOpen ? 'justify-start px-6' : 'justify-center'} border-b border-[var(--color-BORDER)] whitespace-nowrap overflow-hidden`}>
                <div className="w-8 h-8 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] rounded flex items-center justify-center font-bold shrink-0">
                    CZ
                </div>
                {isOpen && (
                    <div className="ml-3">
                        <h1 className="font-bold text-lg tracking-tight text-[var(--color-text-MAIN)]">EMPLOYER</h1>
                        <p className="text-[10px] text-[var(--color-text-MUTED)] uppercase tracking-wider">Portal</p>
                    </div>
                )}
            </div>

            {/* Navigation Items */}
            <nav className="flex-1 overflow-y-auto py-4 space-y-1 custom-scrollbar">
                {menuItems.map((item) => (
                    <div key={item.label}>
                        <button
                            onClick={() => {
                                if (item.subItems) {
                                    toggleSubMenu(item.label);
                                    if (!isOpen && item.subItems) {
                                        // If collapsed and clicked, maybe expand sidebar? Or just show popover (complex). 
                                        // For now, let's assume clicking expands if it has children, or user must expand sidebar first.
                                        // Design choice: Clicking a parent with children while collapsed usually does nothing or expands sidebar.
                                    }
                                } else {
                                    onNavigate(item.id);
                                }
                            }}
                            className={`w-full flex items-center ${isOpen ? 'justify-between px-6' : 'justify-center px-2'} py-3 text-sm font-bold transition-colors
                                ${activePath === item.id || (item.subItems && item.subItems.some(sub => sub.id === activePath))
                                    ? 'text-[var(--color-text-MAIN)] bg-[var(--color-bg-SURFACE)] border-r-4 border-[var(--color-ACCENT)]'
                                    : 'text-[var(--color-text-MUTED)] hover:bg-[var(--color-bg-SURFACE)] hover:text-[var(--color-text-MAIN)]'}
                            `}
                            title={!isOpen ? item.label : ''}
                        >
                            <div className="flex items-center gap-3">
                                <item.icon size={20} />
                                {isOpen && <span>{item.label}</span>}
                            </div>
                            {isOpen && item.subItems && (
                                <div className="text-[var(--color-text-MUTED)]">
                                    {expandedMenus[item.label] ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                                </div>
                            )}
                        </button>

                        {/* Submenu */}
                        {isOpen && item.subItems && expandedMenus[item.label] && (
                            <div className="bg-[var(--color-bg-SURFACE)] py-1 space-y-1">
                                {item.subItems.map((sub) => (
                                    <button
                                        key={sub.id}
                                        onClick={() => onNavigate(sub.id)}
                                        className={`w-full flex items-center pl-14 pr-6 py-2 text-xs font-medium transition-colors
                                            ${activePath === sub.id
                                                ? 'text-[var(--color-ACCENT)]'
                                                : 'text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)]'}
                                        `}
                                    >
                                        {sub.label}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </nav>

            {/* Footer / Logout */}
            <div className="p-4 border-t border-[var(--color-BORDER)]">
                <button
                    onClick={logout}
                    className={`flex items-center ${isOpen ? 'justify-start px-2' : 'justify-center'} gap-2 text-sm font-bold text-red-600 hover:text-red-700 w-full py-2 hover:bg-red-50/10 rounded-md transition-colors`}
                    title="Sign Out"
                >
                    <LogOut size={20} />
                    {isOpen && <span>Sign Out</span>}
                </button>
                {isOpen && <p className="text-[10px] text-[var(--color-text-MUTED)] mt-4 text-center">v2.4.0 • Authorized</p>}
            </div>
        </aside>
    );
}
