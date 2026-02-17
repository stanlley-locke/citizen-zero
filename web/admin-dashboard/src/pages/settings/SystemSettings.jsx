import { Settings, Save, Server, Globe, ToggleLeft, ToggleRight, Shield, Monitor, Moon, Sun, CircuitBoard } from 'lucide-react';
import { useState } from 'react';
import { useTheme } from '../../context/ThemeContext.jsx';

const Toggle = ({ label, description, enabled, onToggle }) => (
    <div className="flex items-center justify-between p-4 border border-[var(--color-BORDER)] bg-[var(--color-bg-MAIN)] hover:border-[var(--color-ACCENT)] transition-all group">
        <div>
            <h4 className="font-bold text-[var(--color-text-MAIN)] text-sm uppercase tracking-wide">{label}</h4>
            <p className="text-xs text-[var(--color-text-MUTED)] mt-1">{description}</p>
        </div>
        <button onClick={onToggle} className={`transition-colors ${enabled ? 'text-[var(--color-ACCENT)]' : 'text-[var(--color-text-MUTED)]'}`}>
            {enabled ? <ToggleRight size={28} /> : <ToggleLeft size={28} />}
        </button>
    </div>
);

export default function SystemSettings() {
    const { theme, setTheme } = useTheme();

    // Theme Options
    const themes = [
        { id: 'light', label: 'Visa White', icon: Sun, desc: 'High contrast light mode (Default)' },
        { id: 'dark', label: 'Command Dark', icon: Moon, desc: 'Professional dark interface' },
        { id: 'kenya', label: 'Kenya Official', icon: CircuitBoard, desc: 'Government standard (Red/Green)' },
    ];

    const [settings, setSettings] = useState({
        maintenanceMode: false,
        strictAuditLogging: true,
        autoBackup: true,
        debugMode: false,
        allowExternalAccess: false
    });

    const [loading, setLoading] = useState(false);

    const toggle = (key) => {
        setSettings(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleSave = async () => {
        setLoading(true);
        // Simulate API Call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setLoading(false);
        alert("System configuration updated successfully.");
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Settings className="text-[var(--color-ACCENT)]" /> System Configuration
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Global variables and feature flags.</p>
                </div>
                <button
                    onClick={handleSave}
                    disabled={loading}
                    className="px-6 py-2 bg-[var(--color-ACCENT)] text-white hover:opacity-90 text-xs font-bold uppercase tracking-widest shadow-sm flex items-center gap-2 disabled:opacity-50"
                >
                    <Save size={14} /> {loading ? 'Saving...' : 'Save Changes'}
                </button>
            </div>

            {/* Theme Section */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm mb-6">
                <div className="flex items-center gap-2 mb-4">
                    <Monitor className="text-[var(--color-text-MAIN)]" size={16} />
                    <h3 className="text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-wide">Interface Theme</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {themes.map((t) => (
                        <button
                            key={t.id}
                            onClick={() => setTheme(t.id)}
                            className={`flex flex-col items-center p-4 border rounded transition-all duration-200 ${theme === t.id
                                ? 'border-[var(--color-ACCENT)] bg-[var(--color-bg-SURFACE)]'
                                : 'border-[var(--color-BORDER)] hover:border-[var(--color-text-MUTED)]'
                                }`}
                        >
                            <t.icon size={24} className={`mb-2 ${theme === t.id ? 'text-[var(--color-ACCENT)]' : 'text-[var(--color-text-MUTED)]'}`} />
                            <span className={`font-bold uppercase text-xs ${theme === t.id ? 'text-[var(--color-text-MAIN)]' : 'text-[var(--color-text-MUTED)]'}`}>
                                {t.label}
                            </span>
                            {theme === t.id && (
                                <span className="mt-2 w-1.5 h-1.5 rounded-full bg-[var(--color-ACCENT)]" />
                            )}
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* General Section */}
                <div className="space-y-4">
                    <h3 className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase tracking-widest border-b border-[var(--color-BORDER)] pb-2 mb-4">
                        <Globe size={14} className="inline mr-2" /> General
                    </h3>
                    <Toggle
                        label="Maintenance Mode"
                        description="Suspend all user-facing services and show maintenance page."
                        enabled={settings.maintenanceMode}
                        onToggle={() => toggle('maintenanceMode')}
                    />
                    <Toggle
                        label="Debug Mode"
                        description="Enable verbose logging and frontend debug overlays."
                        enabled={settings.debugMode}
                        onToggle={() => toggle('debugMode')}
                    />
                </div>

                {/* Security Section */}
                <div className="space-y-4">
                    <h3 className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase tracking-widest border-b border-[var(--color-BORDER)] pb-2 mb-4">
                        <Shield size={14} className="inline mr-2" /> Security & Infrastructure
                    </h3>
                    <Toggle
                        label="Strict Audit Logging"
                        description="Log every read access to citizen records (High Storage Usage)."
                        enabled={settings.strictAuditLogging}
                        onToggle={() => toggle('strictAuditLogging')}
                    />
                    <Toggle
                        label="Auto-Backup"
                        description="Perform hourly incremental backups of all databases."
                        enabled={settings.autoBackup}
                        onToggle={() => toggle('autoBackup')}
                    />
                    <Toggle
                        label="External Gateway Access"
                        description="Allow API access from non-whitelisted IPs."
                        enabled={settings.allowExternalAccess}
                        onToggle={() => toggle('allowExternalAccess')}
                    />
                </div>
            </div>
        </div>
    );
}
