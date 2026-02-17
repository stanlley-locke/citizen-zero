import { Server, Database, Activity, HardDrive, Cpu, Clock, RefreshCw } from 'lucide-react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

const ServiceCard = ({ node }) => {
    const isOnline = node.status === 'online';

    return (
        <div className={`border ${isOnline ? 'border-[var(--color-BORDER)]' : 'border-red-200'} bg-[var(--color-bg-MAIN)] p-5 shadow-sm hover:shadow-md transition-all group animate-in fade-in duration-500`}>
            <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${isOnline ? 'bg-blue-50 text-blue-600' : 'bg-red-50 text-red-600'}`}>
                        <Server size={20} />
                    </div>
                    <div>
                        <h3 className="font-bold text-[var(--color-text-MAIN)] uppercase tracking-wide text-sm">{node.label}</h3>
                        <div className="flex items-center gap-2 mt-0.5">
                            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                            <span className="text-xs font-mono text-[var(--color-text-MUTED)] uppercase">{node.status}</span>
                        </div>
                    </div>
                </div>
                <div className="text-right">
                    <p className="text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase tracking-wider">LATENCY</p>
                    <p className={`text-sm font-mono ${node.latency > 500 ? 'text-orange-500' : 'text-[var(--color-ACCENT)]'}`}>
                        {node.latency}ms
                    </p>
                </div>
            </div>

            {/* Resources Grid */}
            <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-[var(--color-bg-SURFACE)] p-2 rounded border border-[var(--color-BORDER)]">
                    <div className="flex items-center gap-2 mb-1">
                        <Cpu size={12} className="text-[var(--color-text-MUTED)]" />
                        <span className="text-[10px] uppercase font-bold text-[var(--color-text-MUTED)]">CPU</span>
                    </div>
                    <div className="h-1.5 w-full bg-gray-200 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-[var(--color-ACCENT)]"
                            style={{ width: `${node.resources?.cpu || 0}%` }}
                        />
                    </div>
                    <p className="text-right text-[10px] font-mono mt-1">{node.resources?.cpu?.toFixed(1) || 0}%</p>
                </div>
                <div className="bg-[var(--color-bg-SURFACE)] p-2 rounded border border-[var(--color-BORDER)]">
                    <div className="flex items-center gap-2 mb-1">
                        <HardDrive size={12} className="text-[var(--color-text-MUTED)]" />
                        <span className="text-[10px] uppercase font-bold text-[var(--color-text-MUTED)]">RAM</span>
                    </div>
                    <div className="h-1.5 w-full bg-gray-200 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-purple-500"
                            style={{ width: `${node.resources?.memory || 0}%` }}
                        />
                    </div>
                    <p className="text-right text-[10px] font-mono mt-1">{node.resources?.memory?.toFixed(1) || 0}%</p>
                </div>
            </div>

            {/* Database Status */}
            {node.database && (
                <div className="flex items-center justify-between pt-3 border-t border-[var(--color-BORDER)]">
                    <div className="flex items-center gap-2">
                        <Database size={14} className="text-[var(--color-text-MUTED)]" />
                        <span className="text-xs text-[var(--color-text-MAIN)] font-mono">DB Connection</span>
                    </div>
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${node.database.status === 'connected' || node.database.connected ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                        {node.database.status || (node.database.connected ? 'OK' : 'ERR')}
                    </span>
                </div>
            )}
        </div>
    );
};

export default function SystemHealth() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        setLoading(true);
        try {
            const res = await axios.get(ENDPOINTS.MONITOR.STATS);
            setData(res.data);
        } catch (error) {
            console.error("Failed to monitor infrastructure:", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-8 text-[var(--color-text-MUTED)] font-mono animate-pulse">Establishing Uplink to Monitor Service...</div>;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Activity className="text-[var(--color-ACCENT)]" /> Infrastructure Health
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Real-time status of backend microservices and resources.</p>
                </div>
                <button onClick={fetchStats} className="px-4 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors flex items-center gap-2 text-[var(--color-text-MAIN)]">
                    <RefreshCw size={14} /> Refresh
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data?.nodes?.map((node) => (
                    <ServiceCard key={node.id} node={node} />
                ))}
            </div>
        </div>
    );
}
