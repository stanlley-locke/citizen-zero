import { Shield, Search, Filter, Download, Activity, Clock, Server } from 'lucide-react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

export default function SystemLogs() {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetchLogs();
    }, []);

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const res = await axios.get(ENDPOINTS.AUDIT.LIST);
            if (res.data.results) {
                setLogs(res.data.results);
            } else if (Array.isArray(res.data)) {
                setLogs(res.data);
            }
        } catch (error) {
            console.error("Failed to fetch logs:", error);
        } finally {
            setLoading(false);
        }
    };

    const filteredLogs = logs.filter(log =>
        log.action?.toLowerCase().includes(filter.toLowerCase()) ||
        log.actor_id?.toLowerCase().includes(filter.toLowerCase()) ||
        log.details?.toLowerCase().includes(filter.toLowerCase())
    );

    const downloadCSV = () => {
        if (filteredLogs.length === 0) return;

        const headers = ['Timestamp', 'Actor ID', 'Actor Type', 'Action', 'Service', 'Status', 'Details'];
        const rows = filteredLogs.map(log => [
            new Date(log.timestamp).toLocaleString(),
            log.actor_id,
            log.actor_type,
            log.action,
            log.service,
            log.status,
            `"${(log.details || '').replace(/"/g, '""')}"` // Escape quotes
        ]);

        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `system_logs_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Shield className="text-[var(--color-ACCENT)]" /> System Audit Trail
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Secure record of all system activities and security events.</p>
                </div>
                <div className="flex gap-3">
                    <button onClick={fetchLogs} className="px-4 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)]">
                        Refresh
                    </button>
                    <button onClick={downloadCSV} className="px-4 py-2 bg-[var(--color-ACCENT)] text-white hover:opacity-90 text-xs font-bold uppercase tracking-widest shadow-sm flex items-center gap-2">
                        <Download size={14} /> Export CSV
                    </button>
                </div>
            </div>

            {/* Controls */}
            <div className="flex gap-4 items-center bg-[var(--color-bg-MAIN)] p-4 border border-[var(--color-BORDER)] shadow-sm">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-MUTED)]" size={16} />
                    <input
                        type="text"
                        placeholder="Search logs by action, actor, or details..."
                        className="w-full pl-10 pr-4 py-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-sm focus:outline-none focus:border-[var(--color-ACCENT)] text-[var(--color-text-MAIN)]"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    />
                </div>
                <button className="px-4 py-2 border border-[var(--color-BORDER)] bg-[var(--color-bg-SURFACE)] text-[var(--color-text-MUTED)] text-xs font-bold uppercase tracking-widest flex items-center gap-2">
                    <Filter size={14} /> Filter
                </button>
            </div>

            {/* Logs Table */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-sm overflow-hidden">
                <table className="w-full text-left text-sm">
                    <thead className="bg-[var(--color-bg-SURFACE)] border-b border-[var(--color-BORDER)]">
                        <tr>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Timestamp</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Actor</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Action</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Service</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Details</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--color-BORDER)]">
                        {loading ? (
                            <tr>
                                <td colSpan="6" className="px-6 py-12 text-center text-[var(--color-text-MUTED)] animate-pulse">
                                    Loading secure audit logs...
                                </td>
                            </tr>
                        ) : filteredLogs.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="px-6 py-12 text-center text-[var(--color-text-MUTED)]">
                                    No logs found matching your criteria.
                                </td>
                            </tr>
                        ) : (
                            filteredLogs.map((log, idx) => (
                                <tr key={log.id || idx} className="hover:bg-[var(--color-bg-SURFACE)] transition-colors group">
                                    <td className="px-6 py-4 whitespace-nowrap font-mono text-xs text-[var(--color-text-MUTED)]">
                                        {new Date(log.timestamp).toLocaleString()}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex items-center gap-2">
                                            <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-600">
                                                {log.actor_type?.[0] || '?'}
                                            </div>
                                            <span className="font-bold text-[var(--color-text-MAIN)]">{log.actor_id}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className="px-2 py-1 rounded-full text-[10px] uppercase font-bold bg-blue-50 text-blue-700 border border-blue-100">
                                            {log.action}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-xs text-[var(--color-text-MUTED)] uppercase">
                                        {log.service || 'System'}
                                    </td>
                                    <td className="px-6 py-4 text-[var(--color-text-MAIN)] max-w-xs truncate" title={log.details}>
                                        {log.details || '-'}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`flex items-center gap-1.5 text-xs font-bold ${log.status === 'ERROR' || log.status === 'FAILURE' ? 'text-red-600' : 'text-green-600'}`}>
                                            <div className={`w-1.5 h-1.5 rounded-full ${log.status === 'ERROR' || log.status === 'FAILURE' ? 'bg-red-500' : 'bg-green-500'}`} />
                                            {log.status || 'SUCCESS'}
                                        </span>
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
