import React, { useState } from 'react';
import Header from '../components/Header';
import {
    Users,
    ShieldCheck,
    FileText,
    UserPlus,
    Search,
    AlertTriangle,
    CheckCircle,
    MoreVertical,
    LogOut
} from 'lucide-react';

import Sidebar from '../components/Sidebar';

export default function HRDashboard() {
    const [activeTab, setActiveTab] = useState('overview');
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const role = 'HR_MANAGER'; // Or fetch from context

    // Menu Structure
    const menuItems = [
        {
            id: 'staff',
            label: 'Staff Registry',
            icon: Users,
            subItems: [
                { id: 'overview', label: 'All Staff' },
                { id: 'onboarding', label: 'Onboarding' },
                { id: 'terminated', label: 'Terminated' }
            ]
        },
        {
            id: 'verify',
            label: 'Verification',
            icon: ShieldCheck,
            subItems: [
                { id: 'verify-pending', label: 'Pending Reviews' },
                { id: 'verify-history', label: 'History' }
            ]
        },
        {
            id: 'audit',
            label: 'Payroll Audit',
            icon: FileText
        }
    ];

    // Mock Data
    const stats = [
        { label: 'Total Staff', value: '1,248', icon: Users, color: 'text-blue-600', bg: 'bg-blue-100/50' },
        { label: 'Verified IDs', value: '1,242', icon: ShieldCheck, color: 'text-green-600', bg: 'bg-green-100/50' },
        { label: 'Pending Verification', value: '6', icon: AlertTriangle, color: 'text-amber-600', bg: 'bg-amber-100/50' },
        { label: 'Audit Flags', value: '0', icon: FileText, color: 'text-red-600', bg: 'bg-red-100/50' },
    ];

    const staffList = [
        { name: 'John Kamau', id: '22345678', role: 'Senior Analyst', status: 'VERIFIED', date: '2023-01-15' },
        { name: 'Sarah Ochieng', id: '29876543', role: 'Product Manager', status: 'VERIFIED', date: '2023-03-10' },
        { name: 'David Koech', id: '33445566', role: 'Intern', status: 'PENDING', date: '2024-02-01' },
    ];

    const logout = () => {
        localStorage.clear();
        window.location.href = 'http://localhost:3000/login'; // Back to main login
    };

    return (
        <div className="min-h-screen bg-[var(--color-bg-SURFACE)] flex">
            <Sidebar
                isOpen={isSidebarOpen}
                menuItems={menuItems}
                activePath={activeTab}
                onNavigate={setActiveTab}
                logout={logout}
            />

            {/* Main Content */}
            <main className="flex-1 min-h-screen flex flex-col transition-all duration-300">
                {/* Global Header */}
                <Header role={role} toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

                <div className="p-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500 w-full">

                    {/* Stats Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        {stats.map((stat) => (
                            <div key={stat.label} className="bg-[var(--color-bg-MAIN)] p-6 rounded-lg border border-[var(--color-BORDER)] shadow-sm">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <p className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase tracking-wide">{stat.label}</p>
                                        <h3 className="text-2xl font-bold text-[var(--color-text-MAIN)] mt-2">{stat.value}</h3>
                                    </div>
                                    <div className={`p-2 rounded-md ${stat.bg} ${stat.color}`}>
                                        <stat.icon size={20} />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Quick Actions */}
                    <div className="flex gap-4">
                        <button className="flex items-center gap-2 px-6 py-3 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] font-bold rounded-md hover:opacity-90 shadow-sm">
                            <UserPlus size={18} /> New Hire Onboarding
                        </button>
                        <button className="flex items-center gap-2 px-6 py-3 bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] font-bold rounded-md hover:bg-[var(--color-bg-SURFACE)] shadow-sm">
                            <FileText size={18} /> Generate Compliance Report
                        </button>
                    </div>

                    {/* Staff Table */}
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] rounded-lg shadow-sm">
                        <div className="p-6 border-b border-[var(--color-BORDER)] flex justify-between items-center">
                            <h3 className="font-bold text-[var(--color-text-MAIN)]">Staff Directory</h3>
                            <div className="relative">
                                <Search className="absolute left-3 top-2.5 text-gray-400" size={16} />
                                <input
                                    type="text"
                                    placeholder="Search by ID or Name..."
                                    className="pl-9 pr-4 py-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded-md text-sm outline-none focus:border-[var(--color-ACCENT)] w-64"
                                />
                            </div>
                        </div>
                        <table className="w-full text-sm text-left">
                            <thead className="bg-[var(--color-bg-SURFACE)] text-[var(--color-text-MUTED)] font-bold uppercase text-xs">
                                <tr>
                                    <th className="px-6 py-4">Employee</th>
                                    <th className="px-6 py-4">National ID</th>
                                    <th className="px-6 py-4">Role</th>
                                    <th className="px-6 py-4">Verification Status</th>
                                    <th className="px-6 py-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[var(--color-BORDER)]">
                                {staffList.map((staff) => (
                                    <tr key={staff.id} className="hover:bg-[var(--color-bg-SURFACE)] transition-colors">
                                        <td className="px-6 py-4 font-bold text-[var(--color-text-MAIN)]">{staff.name}</td>
                                        <td className="px-6 py-4 font-mono text-[var(--color-text-MUTED)]">{staff.id}</td>
                                        <td className="px-6 py-4 text-[var(--color-text-MAIN)]">{staff.role}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase flex items-center gap-1 w-fit ${staff.status === 'VERIFIED' ? 'bg-green-100/50 text-green-600' : 'bg-amber-100/50 text-amber-600'
                                                }`}>
                                                {staff.status === 'VERIFIED' ? <CheckCircle size={10} /> : <AlertTriangle size={10} />}
                                                {staff.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button className="p-1 hover:bg-gray-100 rounded text-gray-400 hover:text-gray-600">
                                                <MoreVertical size={16} />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
        </div>
    );
}
