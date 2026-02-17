import React, { useState } from 'react';
import Header from '../components/Header';
import {
    Building2,
    Users,
    Shield,
    LogOut,
    Plus,
    Save
} from 'lucide-react';

import Sidebar from '../components/Sidebar';

export default function OrgAdminDashboard() {
    const [activeSection, setActiveSection] = useState('users');
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    const menuItems = [
        {
            id: 'users',
            label: 'System Users',
            icon: Users,
            subItems: [
                { id: 'users-active', label: 'Active Users' },
                { id: 'users-roles', label: 'Roles & Permissions' }
            ]
        },
        {
            id: 'settings',
            label: 'Organization',
            icon: Building2,
            subItems: [
                { id: 'settings-profile', label: 'Profile' },
                { id: 'settings-locations', label: 'Locations' }
            ]
        },
        {
            id: 'policy',
            label: 'Security Policy',
            icon: Shield
        }
    ];

    const [orgName, setOrgName] = useState('Safaricom PLC');
    const [orgAddress, setOrgAddress] = useState('Safaricom House, Waiyaki Way, Nairobi');

    const logout = () => {
        localStorage.clear();
        window.location.href = 'http://localhost:3000/login';
    };

    return (
        <div className="min-h-screen bg-[var(--color-bg-MAIN)] flex">
            <Sidebar
                isOpen={isSidebarOpen}
                menuItems={menuItems}
                activePath={activeSection}
                onNavigate={setActiveSection}
                logout={logout}
            />

            <main className="flex-1 flex flex-col min-h-screen transition-all duration-300">
                <Header role="ORG_ADMIN" toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

                <div className="flex-1 p-12 max-w-5xl mx-auto w-full">
                    <header className="mb-12">
                        <h1 className="text-3xl font-bold text-[var(--color-text-MAIN)]">Organization Settings</h1>
                        <p className="text-[var(--color-text-MUTED)] mt-2">Manage access and profile for {orgName}</p>
                    </header>

                    {(activeSection === 'users' || activeSection === 'users-active') && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <div className="flex justify-between items-center">
                                <h2 className="text-xl font-bold text-[var(--color-text-MAIN)] flex items-center gap-2"><Users /> System Users</h2>
                                <button className="flex items-center gap-2 px-4 py-2 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] text-sm font-bold rounded hover:opacity-90">
                                    <Plus size={16} /> Add User
                                </button>
                            </div>

                            <div className="border border-[var(--color-BORDER)] rounded-lg overflow-hidden">
                                <table className="w-full text-sm text-left">
                                    <thead className="bg-[var(--color-bg-SURFACE)] font-bold text-[var(--color-text-MUTED)] uppercase text-xs">
                                        <tr>
                                            <th className="px-6 py-4">User</th>
                                            <th className="px-6 py-4">Role</th>
                                            <th className="px-6 py-4">Access Level</th>
                                            <th className="px-6 py-4">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-[var(--color-BORDER)]">
                                        <tr className="bg-[var(--color-bg-MAIN)]">
                                            <td className="px-6 py-4 font-bold">Admin User</td>
                                            <td className="px-6 py-4">ORG_ADMIN</td>
                                            <td className="px-6 py-4 text-xs font-mono">FULL_ACCESS</td>
                                            <td className="px-6 py-4 text-green-600 font-bold text-xs">ACTIVE</td>
                                        </tr>
                                        <tr className="bg-[var(--color-bg-MAIN)]">
                                            <td className="px-6 py-4 font-bold">John HR</td>
                                            <td className="px-6 py-4">HR_MANAGER</td>
                                            <td className="px-6 py-4 text-xs font-mono">READ_WRITE_HR</td>
                                            <td className="px-6 py-4 text-green-600 font-bold text-xs">ACTIVE</td>
                                        </tr>
                                        <tr className="bg-[var(--color-bg-MAIN)]">
                                            <td className="px-6 py-4 font-bold">Gate Guard 1</td>
                                            <td className="px-6 py-4">VERIFIER</td>
                                            <td className="px-6 py-4 text-xs font-mono">READ_ONLY_VERIFY</td>
                                            <td className="px-6 py-4 text-green-600 font-bold text-xs">ACTIVE</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}

                    {(activeSection === 'settings' || activeSection === 'settings-profile') && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <h2 className="text-xl font-bold text-[var(--color-text-MAIN)] flex items-center gap-2"><Building2 /> Company Profile</h2>

                            <div className="grid grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-xs font-bold uppercase text-[var(--color-text-MUTED)] mb-1">Company Name</label>
                                    <input
                                        type="text"
                                        value={orgName}
                                        onChange={(e) => setOrgName(e.target.value)}
                                        className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-[var(--color-text-MAIN)] font-bold focus:outline-none focus:border-[var(--color-ACCENT)] transition-colors"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold uppercase text-[var(--color-text-MUTED)] mb-1">Registration #</label>
                                    <input type="text" value="CPR/2023/99001" disabled className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-[var(--color-text-MUTED)] font-mono opacity-50" />
                                </div>
                                <div className="col-span-2">
                                    <label className="block text-xs font-bold uppercase text-[var(--color-text-MUTED)] mb-1">Address</label>
                                    <input
                                        type="text"
                                        value={orgAddress}
                                        onChange={(e) => setOrgAddress(e.target.value)}
                                        className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-[var(--color-text-MAIN)] focus:outline-none focus:border-[var(--color-ACCENT)] transition-colors"
                                    />
                                </div>
                            </div>

                            <button className="flex items-center gap-2 px-6 py-3 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] font-bold rounded hover:opacity-90">
                                <Save size={18} /> Save Changes
                            </button>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
