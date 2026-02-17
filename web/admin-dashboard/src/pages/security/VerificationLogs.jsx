import { ShieldCheck, Search, Filter, CheckCircle, XCircle } from 'lucide-react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

export default function VerificationLogs() {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetchLogs();
    }, []);

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const res = await axios.get(ENDPOINTS.AUDIT.VERIFICATIONS);
            if (res.data.results) {
                setLogs(res.data.results);
            } else if (Array.isArray(res.data)) {
                setLogs(res.data);
            }
        } catch (error) {
            console.error("Failed to fetch verification logs:", error);
        } finally {
            setLoading(false);
        }
    };

    const filteredLogs = logs.filter(log =>
        log.user_id?.toLowerCase().includes(filter.toLowerCase()) ||
        log.details?.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <ShieldCheck className="text-[var(--color-ACCENT)]" /> Verification History
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Log of all identity verification attempts and their outcomes.</p>
                </div>
                <button onClick={fetchLogs} className="px-4 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)]">
                    Refresh
                </button>
            </div>

            {/* Controls */}
            <div className="flex gap-4 items-center bg-[var(--color-bg-MAIN)] p-4 border border-[var(--color-BORDER)] shadow-sm">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-MUTED)]" size={16} />
                    <input
                        type="text"
                        placeholder="Search by User ID or Verifier..."
                        className="w-full pl-10 pr-4 py-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-sm focus:outline-none focus:border-[var(--color-ACCENT)] text-[var(--color-text-MAIN)]"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    />
                </div>
            </div>

            {/* Logs Table */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-sm overflow-hidden">
                <table className="w-full text-left text-sm">
                    <thead className="bg-[var(--color-bg-SURFACE)] border-b border-[var(--color-BORDER)]">
                        <tr>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Timestamp</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Subject ID</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Verifier</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Result</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Details</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--color-BORDER)]">
                        {loading ? (
                            <tr>
                                <td colSpan="5" className="px-6 py-12 text-center text-[var(--color-text-MUTED)] animate-pulse">
                                    Retrieving verification records...
                                </td>
                            </tr>
                        ) : filteredLogs.length === 0 ? (
                            <tr>
                                <td colSpan="5" className="px-6 py-12 text-center text-[var(--color-text-MUTED)]">
                                    No verification records found.
                                </td>
                            </tr>
                        ) : (
                            filteredLogs.map((log, idx) => (
                                <tr key={log.id || idx} className="hover:bg-[var(--color-bg-SURFACE)] transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap font-mono text-xs text-[var(--color-text-MUTED)]">
                                        {new Date(log.timestamp).toLocaleString()}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap font-bold text-[var(--color-text-MAIN)]">
                                        {log.user_id}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-[var(--color-text-MAIN)]">
                                        {log.username}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {log.status === 'SUCCESS' ? (
                                            <span className="flex items-center gap-1.5 text-xs font-bold text-green-600">
                                                <CheckCircle size={14} /> VERIFIED
                                            </span>
                                        ) : (
                                            <span className="flex items-center gap-1.5 text-xs font-bold text-red-600">
                                                <XCircle size={14} /> FAILED
                                            </span>
                                        )}
                                    </td>
                                    <td className="px-6 py-4 text-[var(--color-text-MUTED)] text-xs">
                                        {log.details}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
