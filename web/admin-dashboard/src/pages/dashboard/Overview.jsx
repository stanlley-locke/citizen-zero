import { Users, FileCheck, AlertTriangle, Activity, ArrowUpRight, Shield, RefreshCw, AlertOctagon } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#000000', '#333333', '#666666', '#999999']; // Monochrome Palette

export default function Overview() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [kpi, setKpi] = useState({
        total_citizens: 0,
        ids_issued: 0,
        pending_reviews: 0
    });
    const [trends, setTrends] = useState([]);
    const [demographics, setDemographics] = useState([]);
    const [systemHealth, setSystemHealth] = useState({
        status: 'Unknown',
        uptime: 0,
        services_online: 0,
        total_services: 0
    });
    const [logs, setLogs] = useState([]);
    const [activeAlerts, setActiveAlerts] = useState([]);
    const [lastUpdated, setLastUpdated] = useState(new Date());

    const fetchData = async () => {
        setLoading(true);
        console.log("Dashboard: Fetching data...");
        try {
            // 1. Fetch KPI & Trends from ID Service
            console.log("Dashboard: Requesting ID Analytics from", ENDPOINTS.ID.ANALYTICS);
            const idRes = await axios.get(ENDPOINTS.ID.ANALYTICS);
            console.log("Dashboard: ID Analytics Response:", idRes.data);

            if (idRes.data.kpi) {
                setKpi(idRes.data.kpi);
            }
            if (idRes.data.trends) {
                // Transform for Recharts
                const formattedTrends = idRes.data.trends.months.map((month, i) => ({
                    name: month,
                    registrations: idRes.data.trends.registrations[i]
                }));
                setTrends(formattedTrends);
            }
            if (idRes.data.demographics) {
                const formattedDemo = idRes.data.demographics.labels.map((label, i) => ({
                    name: label,
                    value: idRes.data.demographics.sizes[i]
                }));
                setDemographics(formattedDemo);
            }

            // 2. Fetch System Health
            console.log("Dashboard: Requesting Monitor Stats from", ENDPOINTS.MONITOR.STATS);
            const monitorRes = await axios.get(ENDPOINTS.MONITOR.STATS);
            console.log("Dashboard: Monitor Stats Response:", monitorRes.data);

            if (monitorRes.data.summary) {
                setSystemHealth({
                    status: monitorRes.data.summary.healthy_percentage > 90 ? 'Secure' : 'Degraded',
                    uptime: monitorRes.data.updated_at,
                    services_online: monitorRes.data.summary.online,
                    total_services: monitorRes.data.summary.total
                });
            }

            // 3. Fetch Alerts
            try {
                console.log("Dashboard: Requesting Alerts from", ENDPOINTS.AUDIT.ALERTS);
                const alertsRes = await axios.get(ENDPOINTS.AUDIT.ALERTS);
                console.log("Dashboard: Alerts Response:", alertsRes.data);
                if (Array.isArray(alertsRes.data)) {
                    setActiveAlerts(alertsRes.data);
                }
            } catch (err) {
                console.warn("Dashboard: Alerts fetch failed (likely empty or 404):", err.message);
                setActiveAlerts([]);
            }

            // 4. Fetch Recent Logs
            console.log("Dashboard: Requesting Audit Logs from", ENDPOINTS.AUDIT.LIST);
            const auditRes = await axios.get(ENDPOINTS.AUDIT.LIST);
            console.log("Dashboard: Audit Logs Response:", auditRes.data);

            if (auditRes.data.results) {
                setLogs(auditRes.data.results.slice(0, 5));
            } else if (Array.isArray(auditRes.data)) {
                setLogs(auditRes.data.slice(0, 5));
            }

            setLastUpdated(new Date());

        } catch (error) {
            console.error("Dashboard Data Fetch Error:", error);
            if (error.response) {
                console.error("Error Response Data:", error.response.data);
                console.error("Error Status:", error.response.status);
            } else if (error.request) {
                console.error("Error Request (No Response):", error.request);
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 30000); // 30s auto-refresh
        return () => clearInterval(interval);
    }, []);

    const stats = [
        { label: 'Total Citizens', value: kpi.total_citizens.toLocaleString(), trend: '+12.5%', icon: Users },
        { label: 'IDs Issued', value: kpi.ids_issued.toLocaleString(), trend: '+4.2%', icon: FileCheck },
        { label: 'Pending Reviews', value: kpi.pending_reviews.toLocaleString(), trend: kpi.pending_reviews > 10 ? 'High' : 'Low', icon: AlertTriangle },
        { label: 'System Health', value: `${((systemHealth.services_online / (systemHealth.total_services || 1)) * 100).toFixed(1)}%`, trend: systemHealth.status, icon: Activity },
    ];

    if (loading && !kpi.total_citizens) {
        return (
            <div className="flex h-96 items-center justify-center">
                <div className="flex flex-col items-center gap-4 text-[var(--color-text-MUTED)]">
                    <RefreshCw className="animate-spin" size={32} />
                    <p className="font-ocr text-xs uppercase tracking-widest">Initializing Secure Stream...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-ACCENT)] pb-6">
                <div>
                    <h2 className="text-3xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tighter">Executive Dashboard</h2>
                    <p className="text-[var(--color-text-MUTED)] mt-2 text-sm font-medium tracking-wide">National Registry System • Republic of Kenya</p>
                </div>
                <div className="flex gap-4 items-center">
                    <p className="text-[10px] text-[var(--color-text-MUTED)] uppercase font-ocr hidden md:block">
                        Updated: {lastUpdated.toLocaleTimeString()}
                    </p>
                    <button onClick={fetchData} className="px-4 py-2 border border-[var(--color-BORDER)] hover:border-[var(--color-ACCENT)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)] flex items-center gap-2">
                        <RefreshCw size={12} /> Refresh
                    </button>
                    <button onClick={() => navigate('/security/audit')} className="px-6 py-2 bg-[var(--color-ACCENT)] text-[var(--color-ACCENT-text)] hover:opacity-90 text-xs font-bold uppercase tracking-widest shadow-lg transition-transform hover:scale-105">
                        System Logs
                    </button>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, i) => (
                    <div key={i} className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-8 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
                        <span className="absolute -bottom-4 -right-4 text-9xl font-ocr text-[var(--color-text-MUTED)] opacity-10 group-hover:scale-110 transition-transform select-none">
                            {i + 1}
                        </span>
                        <div className="relative z-10">
                            <div className="flex justify-between items-start mb-4">
                                <p className="text-[var(--color-text-MUTED)] text-[10px] font-bold uppercase tracking-[0.2em]">{stat.label}</p>
                                <div className={`h-2 w-2 rounded-full ${stat.label === 'System Health' && systemHealth.status !== 'Secure' ? 'bg-red-500' : 'bg-[var(--color-ACCENT)]'}`} />
                            </div>
                            <h3 className="text-4xl font-ocr text-[var(--color-text-MAIN)] tracking-widest mb-3">
                                {stat.value}
                            </h3>
                            <div className="flex items-center gap-2 border-t border-[var(--color-BORDER)] pt-3 mt-2">
                                <span className={`text-xs font-bold text-[var(--color-text-MAIN)] px-2 py-0.5 rounded ${stat.label === 'Pending Reviews' && kpi.pending_reviews > 0 ? 'bg-yellow-100 text-yellow-800' : 'bg-[var(--color-bg-SURFACE)]'}`}>
                                    {stat.trend}
                                </span>
                                <span className="text-[10px] text-[var(--color-text-MUTED)] uppercase">Current Status</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Left Column: Charts */}
                <div className="col-span-2 space-y-8">

                    {/* Registration Trend Chart */}
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-8 shadow-sm">
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-widest flex items-center gap-2">
                                <Activity size={16} />
                                Enrollment Trends
                            </h3>
                        </div>
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={trends}>
                                    <defs>
                                        <linearGradient id="colorReg" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#000000" stopOpacity={0.1} />
                                            <stop offset="95%" stopColor="#000000" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#6B7280' }} />
                                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#6B7280' }} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#fff', borderColor: '#E5E7EB', fontSize: '12px' }}
                                        itemStyle={{ color: '#000' }}
                                    />
                                    <Area type="monotone" dataKey="registrations" stroke="#000000" fillOpacity={1} fill="url(#colorReg)" strokeWidth={2} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Demographics Area */}
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-8 shadow-sm">
                        <h3 className="text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-widest mb-6">Demographic Distribution</h3>
                        <div className="h-[250px] w-full flex items-center justify-center">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={demographics}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {demographics.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="flex justify-center gap-6 mt-4">
                            {demographics.map((entry, index) => (
                                <div key={index} className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }} />
                                    <span className="text-xs text-[var(--color-text-MUTED)] uppercase">{entry.name}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Panel: Alerts & Logs */}
                <div className="col-span-1 space-y-8">

                    {/* Security Status Card */}
                    <div className={`text-white p-6 shadow-xl relative overflow-hidden transition-colors duration-500 ${systemHealth.status === 'Secure' ? 'bg-[var(--color-ACCENT)]' : 'bg-red-600'}`}>
                        <div className="relative z-10">
                            <div className="flex items-center gap-3 mb-4">
                                <Shield className="text-white" size={20} />
                                <h3 className="text-sm font-bold uppercase tracking-widest">Security Status</h3>
                            </div>
                            <p className="font-ocr text-2xl tracking-widest mb-1">{systemHealth.status.toUpperCase()}</p>
                            <p className="text-xs text-white opacity-70 uppercase tracking-wide">
                                Services Online: {systemHealth.services_online}/{systemHealth.total_services}
                            </p>
                        </div>
                        <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -mr-16 -mt-16 blur-2xl"></div>
                    </div>

                    {/* Active Alerts List */}
                    {activeAlerts.length > 0 && (
                        <div className="bg-red-50 border border-red-200 p-6 shadow-sm animate-in slide-in-from-right duration-500">
                            <h3 className="text-xs font-bold text-red-900 uppercase tracking-widest mb-4 flex items-center gap-2">
                                <AlertOctagon size={14} /> Active Security Alerts
                            </h3>
                            <div className="space-y-3">
                                {activeAlerts.map((alert, idx) => (
                                    <div key={idx} className="bg-white p-3 border border-red-100 rounded shadow-sm">
                                        <p className="text-xs font-bold text-red-800">{alert.message || alert.details}</p>
                                        <p className="text-[10px] text-red-600 mt-1 uppercase">{alert.service || 'System'} • {new Date(alert.timestamp).toLocaleTimeString()}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Pending Actions / Recent Logs */}
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm">
                        <h3 className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase tracking-widest mb-6 border-b border-[var(--color-BORDER)] pb-2">Recent Activity</h3>
                        <div className="space-y-4">
                            {logs.length === 0 ? (
                                <p className="text-xs text-[var(--color-text-MUTED)]">No recent logs found.</p>
                            ) : (
                                logs.map((log, index) => (
                                    <div key={log.id || index} className="flex gap-4 items-start group cursor-pointer border-b border-[var(--color-bg-SURFACE)] pb-2 last:border-0 hover:bg-[var(--color-bg-SURFACE)] p-2 -mx-2 rounded transition-colors">
                                        <div className="font-ocr text-[10px] text-[var(--color-text-MUTED)] group-hover:text-[var(--color-text-MAIN)] transition-colors whitespace-nowrap pt-0.5">
                                            {new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-xs font-bold text-[var(--color-text-MAIN)] truncate">{log.action}</p>
                                            <p className="text-[10px] text-[var(--color-text-MUTED)] uppercase truncate">
                                                {log.actor_type}: {log.actor_id}
                                            </p>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
