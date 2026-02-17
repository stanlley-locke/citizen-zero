import { Shield, AlertTriangle, Check, XOctagon, Lock, Activity } from 'lucide-react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

const KPICard = ({ title, value, icon, color, subtext }) => (
    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm hover:border-[var(--color-ACCENT)] transition-colors group">
        <div className="flex justify-between items-start">
            <div>
                <p className="text-[var(--color-text-MUTED)] text-xs font-bold uppercase tracking-wider">{title}</p>
                <h3 className="text-3xl font-ocr mt-2 text-[var(--color-text-MAIN)] group-hover:text-[var(--color-ACCENT)] transition-colors">
                    {value}
                </h3>
            </div>
            <div className={`p-2 bg-[var(--color-bg-SURFACE)] rounded-full text-${color}-500 group-hover:bg-[var(--color-ACCENT)] group-hover:text-white transition-colors`}>
                {icon}
            </div>
        </div>
        {subtext && <p className="text-xs text-[var(--color-text-MUTED)] mt-4 font-mono">{subtext}</p>}
    </div>
);

export default function SecurityOverview() {
    const [stats, setStats] = useState(null);
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [analyticsRes, alertsRes] = await Promise.all([
                axios.get(ENDPOINTS.AUDIT.ANALYTICS),
                axios.get(ENDPOINTS.AUDIT.ALERTS)
            ]);
            setStats(analyticsRes.data.kpi);
            setAlerts(alertsRes.data || []);
        } catch (error) {
            console.error("Failed to fetch security data", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-8 text-[var(--color-text-MUTED)] font-mono animate-pulse">Scanning Security Matrix...</div>;

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Lock className="text-[var(--color-ACCENT)]" /> Security Command Center
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Real-time threat monitoring and system integrity status.</p>
                </div>
                <div className="flex gap-3">
                    <button onClick={fetchData} className="px-4 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)]">
                        Refresh Scope
                    </button>
                </div>
            </div>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <KPICard
                    title="Security Score"
                    value={`${stats?.security_score || 0}%`}
                    icon={<Shield size={20} />}
                    color="green"
                    subtext="Overall System Health"
                />
                <KPICard
                    title="Active Threats"
                    value={stats?.active_threats || 0}
                    icon={<AlertTriangle size={20} />}
                    color="red"
                    subtext="Critical incidents in last 24h"
                />
                <KPICard
                    title="Failed Logins"
                    value={stats?.failed_attempts || 0}
                    icon={<XOctagon size={20} />}
                    color="orange"
                    subtext="Authentication failures"
                />
                <KPICard
                    title="Total Events"
                    value={stats?.total_events || 0}
                    icon={<Activity size={20} />}
                    color="blue"
                    subtext="Logged activities today"
                />
            </div>

            {/* Recent Alerts Section */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-sm">
                <div className="p-4 border-b border-[var(--color-BORDER)] bg-[var(--color-bg-SURFACE)] flex justify-between items-center">
                    <h3 className="font-bold text-[var(--color-text-MAIN)] uppercase tracking-wider text-sm flex items-center gap-2">
                        <AlertTriangle size={16} className="text-red-500" /> Recent Security Alerts
                    </h3>
                    <span className="text-xs font-mono text-[var(--color-text-MUTED)]">{alerts.length} Detected</span>
                </div>
                <div className="divide-y divide-[var(--color-BORDER)]">
                    {alerts.length === 0 ? (
                        <div className="p-8 text-center text-[var(--color-text-MUTED)] text-sm">No active alerts. System secure.</div>
                    ) : (
                        alerts.map((alert, idx) => (
                            <div key={idx} className="p-4 flex items-start gap-4 hover:bg-[var(--color-bg-SURFACE)] transition-colors">
                                <div className={`p-2 rounded mt-1 ${alert.severity === 'CRITICAL' ? 'bg-red-100 text-red-700' : 'bg-orange-100 text-orange-700'}`}>
                                    <AlertTriangle size={16} />
                                </div>
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${alert.severity === 'CRITICAL' ? 'border-red-200 bg-red-50 text-red-700' : 'border-orange-200 bg-orange-50 text-orange-700'}`}>
                                            {alert.severity}
                                        </span>
                                        <span className="text-xs font-mono text-[var(--color-text-MUTED)]">
                                            {new Date(alert.timestamp).toLocaleString()}
                                        </span>
                                    </div>
                                    <p className="text-sm font-bold text-[var(--color-text-MAIN)]">{alert.action}</p>
                                    <p className="text-xs text-[var(--color-text-MUTED)] mt-1">{alert.details}</p>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
