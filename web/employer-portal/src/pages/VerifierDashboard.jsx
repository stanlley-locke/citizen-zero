import React, { useState } from 'react';
import Header from '../components/Header';
import {
    Scan,
    Search,
    CheckCircle,
    XCircle,
    Clock,
    LogOut
} from 'lucide-react';

export default function VerifierDashboard() {
    const [query, setQuery] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    // Mock History
    const history = [
        { id: '22345678', name: 'John Kamau', time: '10:42 AM', status: 'MATCH', location: 'Gate A' },
        { id: '99887766', name: 'Unknown User', time: '10:15 AM', status: 'NO_MATCH', location: 'Gate A' },
        { id: '11223344', name: 'Alice Wanjiku', time: '09:30 AM', status: 'MATCH', location: 'Gate B' },
    ];

    const handleVerify = (e) => {
        e.preventDefault();
        setLoading(true);
        // Mock API Call
        setTimeout(() => {
            setResult({
                status: 'VALID',
                name: 'JAMES MWANGI',
                id: query,
                dob: '1990-05-12',
                photo: null // Placeholder
            });
            setLoading(false);
        }, 1500);
    };

    const logout = () => {
        localStorage.clear();
        window.location.href = 'http://localhost:3000/login';
    };

    return (
        <div className="min-h-screen bg-[var(--color-bg-SURFACE)] flex flex-col">
            {/* Global Header */}
            <Header role="VERIFIER" />

            <main className="flex-1 max-w-lg w-full mx-auto p-6 space-y-8">

                {/* Main Action Card */}
                <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] rounded-xl shadow-lg p-8 text-center animate-in zoom-in-95 duration-300">
                    <h2 className="text-xl font-bold text-[var(--color-text-MAIN)] mb-6">Identity Check</h2>

                    <form onSubmit={handleVerify} className="space-y-4">
                        <div className="relative">
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="Enter National ID"
                                className="w-full text-center text-2xl font-mono p-4 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded-lg outline-none focus:border-[var(--color-ACCENT)] transition-colors placeholder:text-gray-300"
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading || !query}
                            className="w-full py-4 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] font-bold rounded-lg hover:opacity-90 disabled:opacity-50 transition-opacity flex items-center justify-center gap-2"
                        >
                            {loading ? 'Verifying...' : <><Search size={20} /> VERIFY IDENTITY</>}
                        </button>
                    </form>
                </div>

                {/* Result Display */}
                {result && (
                    <div className={`border-l-4 rounded-r-lg p-6 shadow-md animate-in slide-in-from-bottom-4 duration-300 ${result.status === 'VALID' ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`}>
                        <div className="flex items-center gap-4">
                            <div className={`p-3 rounded-full ${result.status === 'VALID' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                                {result.status === 'VALID' ? <CheckCircle size={32} /> : <XCircle size={32} />}
                            </div>
                            <div>
                                <h3 className={`text-lg font-bold ${result.status === 'VALID' ? 'text-green-800' : 'text-red-800'}`}>
                                    {result.status === 'VALID' ? 'IDENTITY CONFIRMED' : 'INVALID ID'}
                                </h3>
                                <p className="font-mono text-sm opacity-80">{result.id}</p>
                            </div>
                        </div>
                        {result.status === 'VALID' && (
                            <div className="mt-4 pt-4 border-t border-green-200">
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div>
                                        <p className="text-[10px] uppercase font-bold text-green-700 opacity-70">Full Name</p>
                                        <p className="font-bold text-green-900">{result.name}</p>
                                    </div>
                                    <div>
                                        <p className="text-[10px] uppercase font-bold text-green-700 opacity-70">DOB</p>
                                        <p className="font-bold text-green-900">{result.dob}</p>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* Simple History */}
                <div className="space-y-3">
                    <h3 className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase tracking-wider pl-2">Recent Scans</h3>
                    {history.map((item, i) => (
                        <div key={i} className="flex justify-between items-center p-4 bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] rounded-lg text-sm">
                            <div className="flex items-center gap-3">
                                <div className={`w-2 h-2 rounded-full ${item.status === 'MATCH' ? 'bg-green-500' : 'bg-red-500'}`} />
                                <span className="font-bold text-[var(--color-text-MAIN)]">{item.id}</span>
                            </div>
                            <span className="text-[var(--color-text-MUTED)] text-xs flex items-center gap-1">
                                <Clock size={12} /> {item.time}
                            </span>
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}
