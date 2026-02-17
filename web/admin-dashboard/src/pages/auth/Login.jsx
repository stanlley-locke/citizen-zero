import { useState } from 'react';
import { useAuth } from '../../context/AuthContext.jsx';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, AlertCircle, Loader2, QrCode } from 'lucide-react';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login, loading, error } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const role = await login(username, password);

        if (role) {
            if (role) {
                // Unifed Login Redirect Logic
                const adminDashRoles = ['SYSTEM_ADMIN', 'DATA_COLLECTOR', 'INVESTIGATOR', 'ADMIN'];
                const employerPortalRoles = ['DATA_CONTROLLER', 'DPO', 'ORG_ADMIN', 'HR_MANAGER', 'INT_AUDITOR', 'VERIFIER'];

                if (adminDashRoles.includes(role)) {
                    if (role === 'DATA_COLLECTOR') navigate('/collector');
                    else if (role === 'INVESTIGATOR') navigate('/investigation');
                    else navigate('/');
                } else if (employerPortalRoles.includes(role)) {
                    // Redirect to Employer Portal (Port 3001) with Token Hand-off
                    const token = localStorage.getItem('accessToken');
                    window.location.href = `http://localhost:3001?token=${token}&role=${role}`;
                } else if (role === 'CITIZEN') {
                    // Redirect to Worker Portal (Port 3002)
                    const token = localStorage.getItem('accessToken');
                    window.location.href = `http://localhost:3002?token=${token}`;
                } else {
                    navigate('/'); // Default
                }
            }
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[var(--color-bg-MAIN)] text-[var(--color-text-MAIN)] font-sans relative overflow-hidden transition-colors duration-500">
            {/* Background Decorations - Very Subtle */}
            <div className="absolute top-0 left-0 w-full h-full opacity-5 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[var(--color-ACCENT)] rounded-full blur-[200px] opacity-10"></div>
            </div>

            {/* Login Card */}
            <div className="w-full max-w-[360px] p-8 relative z-10 animate-in fade-in zoom-in-95 duration-700 flex flex-col items-center">

                {/* Logo Section */}
                <div className="mb-8 flex flex-col items-center text-center">
                    <div className="w-16 h-16 bg-[var(--color-text-MAIN)] text-[var(--color-bg-MAIN)] rounded flex items-center justify-center mb-6 shadow-xl shadow-[var(--color-ACCENT)]/10">
                        <QrCode size={40} strokeWidth={1.5} />
                    </div>

                    <h1 className="text-3xl font-bold tracking-[0.2em] uppercase leading-none mb-2">CITIZEN ZERO</h1>
                    <p className="text-[var(--color-text-MUTED)] text-[10px] tracking-[0.3em] uppercase opacity-70 mb-12">
                        Beyond Physical Identity
                    </p>

                    <h2 className="text-sm font-bold uppercase tracking-widest border-b border-[var(--color-ACCENT)] pb-1 text-[var(--color-ACCENT)]">
                        Access Portal
                    </h2>
                </div>

                <form onSubmit={handleSubmit} className="w-full space-y-10">
                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-500/10 border-l-2 border-red-500 text-red-500 px-4 py-2 text-xs flex items-center gap-2 animate-in fade-in">
                            <AlertCircle size={14} />
                            {error}
                        </div>
                    )}

                    <div className="space-y-6">
                        <div className="group relative">
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="peer w-full bg-transparent border-b border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] py-2 focus:border-[var(--color-ACCENT)] outline-none transition-colors font-ocr text-sm placeholder-transparent"
                                placeholder="Admin ID"
                                required
                            />
                            <label className="absolute left-0 -top-3.5 text-[10px] font-bold uppercase tracking-widest text-[var(--color-text-MUTED)] transition-all peer-placeholder-shown:text-xs peer-placeholder-shown:top-2 peer-placeholder-shown:text-[var(--color-text-MUTED)] peer-focus:-top-3.5 peer-focus:text-[10px] peer-focus:text-[var(--color-ACCENT)]">
                                Admin ID / Username
                            </label>
                        </div>

                        <div className="group relative">
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="peer w-full bg-transparent border-b border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] py-2 focus:border-[var(--color-ACCENT)] outline-none transition-colors font-ocr text-sm placeholder-transparent"
                                placeholder="PIN"
                                required
                            />
                            <label className="absolute left-0 -top-3.5 text-[10px] font-bold uppercase tracking-widest text-[var(--color-text-MUTED)] transition-all peer-placeholder-shown:text-xs peer-placeholder-shown:top-2 peer-placeholder-shown:text-[var(--color-text-MUTED)] peer-focus:-top-3.5 peer-focus:text-[10px] peer-focus:text-[var(--color-ACCENT)]">
                                PIN
                            </label>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-[var(--color-text-MAIN)] text-[var(--color-bg-MAIN)] py-4 font-bold uppercase tracking-[0.2em] text-xs hover:bg-[var(--color-ACCENT)] hover:text-white transition-all duration-300 flex items-center justify-center gap-3 shadow-lg hover:shadow-[var(--color-ACCENT)]/30 group"
                    >
                        {loading ? <Loader2 className="animate-spin" size={16} /> : (
                            <>
                                Authenticate <ChevronRight size={14} className="group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>
                </form>

                <div className="mt-16 text-center opacity-30">
                    <p className="font-ocr text-[8px] tracking-widest">SECURE CONNECTION V2.0</p>
                </div>
            </div>
        </div>
    );
}
