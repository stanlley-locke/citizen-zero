import { Database, HardDrive, RefreshCw, CheckCircle, XCircle } from 'lucide-react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

export default function DatabaseStatus() {
    const [dbs, setDbs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStatus();
    }, []);

    const fetchStatus = async () => {
        setLoading(true);
        try {
            const res = await axios.get(ENDPOINTS.MONITOR.STATS);
            const nodes = res.data.nodes || [];

            // Map service nodes to their databases
            const mapped = nodes.map(node => ({
                id: node.id,
                service: node.service || 'Unknown Service',
                // Assuming naming convention or single DB per service for MVP
                dbName: `${(node.service || 'unknown').replace('-service', '')}_db`,
                status: node.db_status === 'connected' ? 'active' : 'error',
                latency: node.latency || '0ms',
                lastBackup: '1 hr ago' // Mocked for MVP
            }));

            setDbs(mapped);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Database className="text-[var(--color-ACCENT)]" /> Database Health
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">PostgreSQL cluster status and connectivity metrics.</p>
                </div>
                <button onClick={fetchStatus} className="px-4 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)]">
                    Refresh Stats
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {dbs.map((db, idx) => (
                    <div key={idx} className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm hover:border-[var(--color-ACCENT)] transition-all group">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 bg-[var(--color-bg-SURFACE)] rounded-full text-[var(--color-text-MUTED)] group-hover:text-[var(--color-ACCENT)] transition-colors">
                                <Database size={24} />
                            </div>
                            <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${db.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                }`}>
                                {db.status === 'active' ? 'Operational' : 'Connection Error'}
                            </span>
                        </div>

                        <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] font-mono">{db.dbName}</h3>
                        <p className="text-xs text-[var(--color-text-MUTED)] mb-4">Bound to: {db.service}</p>

                        <div className="space-y-2 border-t border-[var(--color-BORDER)] pt-4 text-xs">
                            <div className="flex justify-between">
                                <span className="text-[var(--color-text-MUTED)]">Latency</span>
                                <span className="font-mono text-[var(--color-text-MAIN)]">{db.latency}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-[var(--color-text-MUTED)]">Last Backup</span>
                                <span className="font-mono text-[var(--color-text-MAIN)]">{db.lastBackup}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-[var(--color-text-MUTED)]">Driver</span>
                                <span className="font-mono text-[var(--color-text-MAIN)]">psycopg2</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
