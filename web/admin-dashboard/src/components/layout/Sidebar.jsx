import { useState, useEffect } from 'react';
import {
    LayoutDashboard, Users, CreditCard, ShieldCheck, Activity, Settings,
    Server, ChevronRight, ChevronDown, UserPlus, Fingerprint, FileText,
    Globe, Database, Lock, Menu, X, Zap
} from 'lucide-react';
import { NavLink, useLocation } from 'react-router-dom';

const getNavStructure = (role) => {
    // 1. DATA COLLECTOR
    if (role === 'DATA_COLLECTOR') {
        return [
            {
                label: 'Dashboard',
                path: '/collector',
                icon: LayoutDashboard,
                primary: true
            },
            {
                label: 'Citizen Registry',
                icon: Users,
                children: [
                    { label: 'All Citizens', path: '/citizens', icon: Users },
                    { label: 'New Enrollment', path: '/citizens/new', icon: UserPlus },
                    { label: 'Biometrics', path: '/citizens/biometrics', icon: Fingerprint },
                    { label: 'Family Units', path: '/citizens/families', icon: Users }
                ]
            }
        ];
    }

    // 2. INVESTIGATOR
    if (role === 'INVESTIGATOR') {
        return [
            {
                label: 'Dashboard',
                path: '/investigation',
                icon: LayoutDashboard,
                primary: true
            },
            {
                label: 'Investigation',
                icon: ShieldCheck,
                children: [
                    { label: 'Verification Logs', path: '/security/verifications', icon: ShieldCheck },
                    { label: 'Audit Trail', path: '/security/audit', icon: Activity },
                    { label: 'Access Control', path: '/security/access', icon: Lock } // Maybe read-only?
                ]
            },
            {
                label: 'Identity Records',
                icon: CreditCard,
                children: [
                    { label: 'National ID Cards', path: '/ids/national', icon: CreditCard },
                    { label: 'Passports', path: '/ids/passports', icon: Globe },
                ]
            }
        ];
    }

    // 3. SYSTEM ADMIN / ROOT (Full Access)
    return [
        {
            label: 'Dashboard',
            path: '/',
            icon: LayoutDashboard,
            primary: true
        },
        {
            label: 'Citizen Registry',
            icon: Users,
            children: [
                { label: 'All Citizens', path: '/citizens', icon: Users },
                { label: 'New Enrollment', path: '/citizens/new', icon: UserPlus },
                { label: 'Biometrics', path: '/citizens/biometrics', icon: Fingerprint },
                { label: 'Family Units', path: '/citizens/families', icon: Users }
            ]
        },
        {
            label: 'Identity Management',
            icon: CreditCard,
            children: [
                { label: 'National ID Cards', path: '/ids/national', icon: CreditCard },
                { label: 'Passports', path: '/ids/passports', icon: Globe },
                { label: 'Birth Certificates', path: '/ids/birth-certs', icon: FileText }
            ]
        },
        {
            label: 'Security Suite',
            icon: ShieldCheck,
            children: [
                { label: 'Overview', path: '/security/overview', icon: LayoutDashboard },
                { label: 'Verification Logs', path: '/security/verifications', icon: ShieldCheck },
                { label: 'Audit Trail', path: '/security/audit', icon: Activity },
                { label: 'Access Control', path: '/security/access', icon: Lock }
            ]
        },
        {
            label: 'Infrastructure',
            icon: Server,
            children: [
                { label: 'Network Topology', path: '/infrastructure/topology', icon: Globe },
                { label: 'Nodes & Resources', path: '/infrastructure/nodes', icon: Server },
                { label: 'Databases', path: '/infrastructure/databases', icon: Database }
            ]
        },
        {
            label: 'System',
            icon: Settings,
            children: [
                { label: 'General Settings', path: '/settings/general', icon: Settings },
                { label: 'API Configuration', path: '/settings/api', icon: Server }
            ]
        }
    ];
};

export default function Sidebar({ isCollapsed, toggleCollapse }) {
    const location = useLocation();
    const role = localStorage.getItem('role') || 'SYSTEM_ADMIN'; // Fallback
    const navStructure = getNavStructure(role);

    // State to track expanded menus.
    const [expanded, setExpanded] = useState({});

    // Effect: Auto-collapse submenus when sidebar minimizes
    useEffect(() => {
        if (isCollapsed) {
            setExpanded({}); // Close all
        }
    }, [isCollapsed]);

    // Effect: Auto-expand parent menu if active on load or navigation, ONLY if sidebar is open
    useEffect(() => {
        if (!isCollapsed) {
            const activeParent = navStructure.find(item =>
                item.children?.some(child => location.pathname === child.path)
            );
            if (activeParent) {
                setExpanded(prev => ({ ...prev, [activeParent.label]: true }));
            }
        }
    }, [location.pathname, isCollapsed]);

    const toggleMenu = (label) => {
        if (isCollapsed) {
            toggleCollapse(); // Expand sidebar if clicking a menu header while collapsed
            setTimeout(() => {
                setExpanded(prev => ({ ...prev, [label]: true }));
            }, 50); // Small delay to allow expansion transition
        } else {
            setExpanded(prev => ({ ...prev, [label]: !prev[label] }));
        }
    };

    return (
        <aside
            className={`bg-[var(--color-bg-MAIN)] border-r border-[var(--color-BORDER)] flex flex-col h-screen fixed left-0 top-0 z-50 shadow-[4px_0_24px_rgba(0,0,0,0.02)] transition-all duration-300 ease-in-out ${isCollapsed ? 'w-20' : 'w-72'
                }`}
        >
            {/* Header */}
            <div className={`h-20 flex items-center border-b border-[var(--color-BORDER)] bg-[var(--color-bg-MAIN)] z-10 transition-all duration-300 ${isCollapsed ? 'justify-center px-0' : 'justify-between px-8'
                }`}>
                {!isCollapsed && (
                    <div className="flex flex-col overflow-hidden">
                        <h1 className="text-xl font-ocr tracking-widest text-[var(--color-text-MAIN)] uppercase whitespace-nowrap">
                            CITIZEN ZERO
                        </h1>
                        <p className="text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase tracking-[0.2em] mt-1 pl-0.5 whitespace-nowrap">
                            Republic of Kenya
                        </p>
                    </div>
                )}

                <button
                    onClick={toggleCollapse}
                    className="p-2 hover:bg-[var(--color-bg-SURFACE)] rounded-md text-[var(--color-text-MAIN)] transition-colors shrink-0"
                >
                    {isCollapsed ? <Menu size={20} /> : <X size={20} className="text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)]" />}
                </button>
            </div>

            {/* Navigation */}
            <nav className={`flex-1 py-6 space-y-2 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-200 overflow-x-hidden ${isCollapsed ? 'px-2' : 'px-4'
                }`}>
                {navStructure.map((item) => {
                    const isChildActive = item.children?.some(child => location.pathname === child.path);
                    const isItemActive = location.pathname === item.path;
                    const isActive = isChildActive || isItemActive;

                    if (item.children) {
                        return (
                            <div key={item.label} className="mb-2 relative group">
                                <button
                                    onClick={() => toggleMenu(item.label)}
                                    className={`w-full flex items-center transition-all duration-200 group relative z-10 ${isCollapsed
                                        ? 'justify-center py-3 rounded-lg hover:bg-[var(--color-ACCENT)] hover:text-[var(--color-ACCENT-text)]'
                                        : `justify-between px-4 py-3 rounded-md ${isActive ? 'bg-[var(--color-bg-SURFACE)]' : 'hover:bg-[var(--color-bg-SURFACE)]'}`
                                        } ${isActive && isCollapsed ? 'bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)]' : ''}`}
                                >
                                    <div className="flex items-center gap-3">
                                        <item.icon size={20} className={
                                            isCollapsed
                                                ? (isActive ? 'text-[var(--color-ACCENT-text)]' : 'text-[var(--color-text-MUTED)] group-hover:text-[var(--color-ACCENT-text)]')
                                                : (isActive ? 'text-[var(--color-text-MAIN)]' : 'text-[var(--color-text-MUTED)] group-hover:text-[var(--color-text-MAIN)]')
                                        } />

                                        {!isCollapsed && (
                                            <span className={`text-xs font-bold uppercase tracking-wide whitespace-nowrap ${isActive ? 'text-[var(--color-text-MAIN)]' : 'text-[var(--color-text-MUTED)] group-hover:text-[var(--color-text-MAIN)]'}`}>
                                                {item.label}
                                            </span>
                                        )}
                                    </div>

                                    {!isCollapsed && (
                                        <ChevronDown
                                            size={14}
                                            className={`text-[var(--color-text-MUTED)] transition-transform duration-300 ${expanded[item.label] ? 'rotate-180' : ''}`}
                                        />
                                    )}
                                </button>

                                {/* Collapsed Hover Tooltip */}
                                {isCollapsed && (
                                    <div className="absolute left-14 top-0 hidden group-hover:flex flex-col bg-[var(--color-text-MAIN)] text-[var(--color-bg-MAIN)] p-3 rounded-md shadow-xl z-[60] w-56 ml-4 animate-in fade-in slide-in-from-left-2 duration-200">
                                        <p className="text-xs font-bold uppercase tracking-widest mb-2 border-b border-[var(--color-BORDER)] pb-2 opacity-70">{item.label}</p>
                                        <div className="space-y-1">
                                            {item.children.map(child => (
                                                <NavLink
                                                    key={child.path}
                                                    to={child.path}
                                                    end={true}
                                                    className={({ isActive }) =>
                                                        `flex items-center gap-2 p-2 rounded text-[11px] transition-colors ${isActive ? 'bg-[var(--color-bg-MAIN)] text-[var(--color-text-MAIN)] font-bold' : 'opacity-70 hover:opacity-100 hover:bg-[var(--color-bg-MAIN)]/10'
                                                        }`
                                                    }
                                                >
                                                    <child.icon size={12} />
                                                    {child.label}
                                                </NavLink>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Submenu (Expanded State only) */}
                                {!isCollapsed && (
                                    <div className={`overflow-hidden transition-all duration-300 ease-in-out ${expanded[item.label] ? 'max-h-96 opacity-100 mt-1' : 'max-h-0 opacity-0'}`}>
                                        <div className="pl-4 space-y-1 relative">
                                            <div className="absolute left-6 top-0 bottom-2 w-px bg-[var(--color-BORDER)]"></div>
                                            {item.children.map(child => (
                                                <NavLink
                                                    key={child.label}
                                                    to={child.path}
                                                    end={true}
                                                    className={({ isActive }) =>
                                                        `flex items-center gap-3 px-4 py-2.5 ml-3 rounded-md transition-all duration-200 relative z-10 ${isActive
                                                            ? 'bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] shadow-md transform translate-x-1'
                                                            : 'text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)]'
                                                        }`
                                                    }
                                                >
                                                    {({ isActive }) => (
                                                        <>
                                                            <child.icon size={14} className={isActive ? 'text-[var(--color-ACCENT-text)]' : 'text-[var(--color-text-MUTED)]'} />
                                                            <span className="text-[11px] font-bold uppercase tracking-wider whitespace-nowrap">{child.label}</span>
                                                        </>
                                                    )}
                                                </NavLink>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        );
                    }

                    // Single Item
                    return (
                        <NavLink
                            key={item.label}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center transition-all duration-200 mb-2 group relative z-10 ${isCollapsed
                                    ? 'justify-center py-3 rounded-lg hover:bg-[var(--color-ACCENT)] hover:text-[var(--color-ACCENT-text)]'
                                    : `gap-3 px-4 py-3 rounded-md ${isActive ? 'bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] shadow-lg' : 'text-[var(--color-text-MUTED)] hover:bg-[var(--color-bg-SURFACE)] hover:text-[var(--color-text-MAIN)]'}`
                                } ${isActive && isCollapsed ? 'bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)]' : ''}`
                            }
                        >
                            <item.icon size={20} className={
                                isCollapsed
                                    ? (isActive ? 'text-[var(--color-ACCENT-text)]' : 'text-[var(--color-text-MUTED)] group-hover:text-[var(--color-ACCENT-text)]')
                                    : (isActive ? 'text-[var(--color-ACCENT-text)]' : '')
                            } />

                            {!isCollapsed && (
                                <span className="text-xs font-bold uppercase tracking-wide whitespace-nowrap">{item.label}</span>
                            )}

                            {/* Collapsed Tooltip for Single Items */}
                            {isCollapsed && (
                                <div className="absolute left-14 top-2 hidden group-hover:flex items-center bg-[var(--color-text-MAIN)] text-[var(--color-bg-MAIN)] px-4 py-2 rounded-md shadow-xl z-[60] ml-4 animate-in fade-in slide-in-from-left-2 duration-200 whitespace-nowrap">
                                    <p className="text-[10px] font-bold uppercase tracking-widest">{item.label}</p>
                                </div>
                            )}
                        </NavLink>
                    );
                })}


            </nav>

            {/* User Footer */}
            <div className={`border-t border-[var(--color-BORDER)] bg-[var(--color-bg-MAIN)] transition-all duration-300 ${isCollapsed ? 'p-4' : 'p-6'}`}>
                <div className={`flex items-center ${isCollapsed ? 'justify-center' : 'gap-3'}`}>
                    <div className="w-8 h-8 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] flex items-center justify-center font-ocr text-sm rounded-sm shrink-0">
                        {isCollapsed ? 'A' : 'AD'}
                    </div>
                    {!isCollapsed && (
                        <div className="overflow-hidden">
                            <p className="text-xs font-bold text-[var(--color-text-MAIN)] uppercase tracking-wide truncate">{role.replace(/_/g, ' ')}</p>
                            <p className="text-[10px] text-[var(--color-text-MUTED)] truncate">SECURE SESSION</p>
                        </div>
                    )}
                </div>
            </div>
        </aside>
    );
}
