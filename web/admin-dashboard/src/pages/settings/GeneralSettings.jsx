import { useTheme } from '../../context/ThemeContext.jsx';
import { Monitor, Moon, Sun, CircuitBoard } from 'lucide-react';

export default function GeneralSettings() {
    const { theme, setTheme } = useTheme();

    const themes = [
        { id: 'light', label: 'Visa White', icon: Sun, desc: 'High contrast light mode (Default)' },
        { id: 'dark', label: 'Command Dark', icon: Moon, desc: 'Professional dark interface' },
        { id: 'kenya', label: 'Kenya Official', icon: CircuitBoard, desc: 'Government standard (Red/Green)' },
    ];

    return (
        <div className="space-y-8 max-w-4xl animate-in fade-in duration-500">
            <div>
                <h2 className="text-3xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight">Preferences</h2>
                <p className="text-[var(--color-text-MUTED)] mt-2">Customize your admin experience.</p>
            </div>

            {/* Theme Section */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-8 rounded shadow-sm">
                <div className="flex items-center gap-3 mb-6">
                    <Monitor className="text-[var(--color-text-MAIN)]" />
                    <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] uppercase">Interface Theme</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {themes.map((t) => (
                        <button
                            key={t.id}
                            onClick={() => setTheme(t.id)}
                            className={`flex flex-col items-center p-6 border-2 rounded-lg transition-all duration-200 ${theme === t.id
                                ? 'border-[var(--color-ACCENT)] bg-[var(--color-bg-SURFACE)]'
                                : 'border-[var(--color-BORDER)] hover:border-[var(--color-text-MUTED)]'
                                }`}
                        >
                            <t.icon size={32} className={`mb-4 ${theme === t.id ? 'text-[var(--color-ACCENT)]' : 'text-[var(--color-text-MUTED)]'}`} />
                            <span className={`font-bold uppercase text-sm ${theme === t.id ? 'text-[var(--color-text-MAIN)]' : 'text-[var(--color-text-MUTED)]'}`}>
                                {t.label}
                            </span>
                            <span className="text-[10px] text-[var(--color-text-MUTED)] mt-2 text-center">
                                {t.desc}
                            </span>
                            {theme === t.id && (
                                <span className="mt-4 px-3 py-1 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] text-[10px] font-bold uppercase rounded-full">
                                    Active
                                </span>
                            )}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex justify-end">
                <button className="bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] px-6 py-2 rounded font-bold uppercase text-sm tracking-widest hover:opacity-90 transition-opacity">
                    Save Preferences
                </button>
            </div>
        </div>
    );
}
