import { Server, Database, Cloud, Wifi, ArrowRight, Globe, Shield, Activity, X, Search, Terminal } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

// --- Visual Components ---

const Node = ({ label, icon: Icon, status, x, y, onMouseDown, onClick, selected }) => (
    <div
        onMouseDown={onMouseDown}
        onClick={(e) => { e.stopPropagation(); onClick(); }}
        className={`absolute flex flex-col items-center justify-center w-32 h-32 border-2 rounded-xl backdrop-blur-sm cursor-grab active:cursor-grabbing transition-shadow duration-300 z-10 group select-none ${selected ? 'scale-110 shadow-[0_0_30px_rgba(var(--color-accent-rgb),0.5)] border-[var(--color-ACCENT)] bg-[var(--color-bg-MAIN)]' :
            status === 'active' ? 'border-green-500/50 bg-[var(--color-bg-MAIN)]/80 hover:border-green-400 hover:shadow-[0_0_20px_rgba(0,255,0,0.2)]' :
                status === 'degraded' ? 'border-orange-500/50 bg-[var(--color-bg-MAIN)]/80' :
                    'border-red-500/50 bg-[var(--color-bg-MAIN)]/80'
            }`}
        style={{ left: x, top: y, transition: 'transform 0.1s' }} // Remove left/top transition for smooth dragging
    >
        {/* Connection Points */}
        <div className="absolute top-1/2 -left-1 w-2 h-2 bg-[var(--color-BORDER)] rounded-full"></div>
        <div className="absolute top-1/2 -right-1 w-2 h-2 bg-[var(--color-BORDER)] rounded-full"></div>

        <div className={`p-3 rounded-full mb-3 transition-colors ${selected ? 'bg-[var(--color-ACCENT)] text-white' :
            status === 'active' ? 'bg-green-500/10 text-green-500 group-hover:bg-green-500/20' :
                'bg-red-500/10 text-red-500'
            }`}>
            <Icon size={28} strokeWidth={1.5} />
        </div>
        <span className="font-bold text-[10px] uppercase tracking-widest text-center text-[var(--color-text-MAIN)] pointer-events-none">{label}</span>

        {/* Status indicator pulse */}
        <span className={`absolute -top-1 -right-1 flex h-3 w-3`}>
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${status === 'active' ? 'bg-green-400' : 'bg-red-400'
                }`}></span>
            <span className={`relative inline-flex rounded-full h-3 w-3 ${status === 'active' ? 'bg-green-500' : 'bg-red-500'
                }`}></span>
        </span>
    </div>
);

const Connection = ({ startX, startY, endX, endY, active }) => {
    const length = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2));
    const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;

    return (
        <div
            className="absolute h-[2px] z-0 origin-left overflow-hidden pointer-events-none"
            style={{
                left: startX + 64,
                top: startY + 64,
                width: length,
                transform: `rotate(${angle}deg)`,
                background: 'var(--color-BORDER)' // Base line
            }}
        >
            {/* Moving Packet Animation */}
            {active && (
                <div className="w-12 h-full bg-gradient-to-r from-transparent via-[var(--color-ACCENT)] to-transparent animate-packet-flow absolute top-0 left-0" />
            )}
        </div>
    );
};

// --- Initial Layout ---
const initialLayout = {
    'gateway': { x: 350, y: 300, label: "API Gateway", icon: Globe, service: 'gateway' },
    'auth-service': { x: 350, y: 80, label: "Auth Service", icon: Shield, service: 'auth-service' },
    'id-service': { x: 80, y: 300, label: "ID Service", icon: Database, service: 'id-service' },
    'verify-service': { x: 620, y: 300, label: "Verify Service", icon: Server, service: 'verify-service' },
    'audit-service': { x: 350, y: 520, label: "Audit Service", icon: Activity, service: 'audit-service' },
    'iprs-mock': { x: 80, y: 80, label: "IPRS Mock", icon: Cloud, service: 'iprs-mock' },
    'monitor-service': { x: 620, y: 80, label: "Monitor", icon: Terminal, service: 'monitor-service' }
};

export default function NetworkTopology() {
    const [nodes, setNodes] = useState([]);
    const [layout, setLayout] = useState(initialLayout);
    const [selectedNodeKey, setSelectedNodeKey] = useState(null);
    const [draggingNode, setDraggingNode] = useState(null);
    const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const res = await axios.get(ENDPOINTS.MONITOR.STATS);
                setNodes(res.data.nodes || []);
            } catch (e) {
                console.error("Topology Sync Failed", e);
            }
        };
        fetchStatus();
        const interval = setInterval(fetchStatus, 2000); // Polling every 2s for smoother log updates
        return () => clearInterval(interval);
    }, []);

    // --- Drag and Drop Handlers ---
    const handleMouseDown = (e, key) => {
        const node = layout[key];
        const rect = e.currentTarget.getBoundingClientRect();
        // Calculate offset from top-left of node
        const offsetX = e.clientX - rect.left;
        const offsetY = e.clientY - rect.top;

        setDraggingNode(key);
        setDragOffset({ x: offsetX, y: offsetY });
    };

    const handleMouseMove = (e) => {
        if (!draggingNode) return;

        const parentRect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - parentRect.left - dragOffset.x;
        const y = e.clientY - parentRect.top - dragOffset.y;

        setLayout(prev => ({
            ...prev,
            [draggingNode]: { ...prev[draggingNode], x, y }
        }));
    };

    const handleMouseUp = () => {
        setDraggingNode(null);
    };

    const getNodeStatus = (serviceName) => {
        const node = nodes.find(n => n.service === serviceName);
        return node ? (node.status === 'online' ? 'active' : 'offline') : 'active';
    };

    const getSelectedNodeData = () => {
        if (!selectedNodeKey) return null;
        // Merge static layout info with dynamic metrics
        const staticInfo = layout[selectedNodeKey];
        const dynamicInfo = nodes.find(n => n.service === staticInfo.service) || {};

        // Remove 'label' from dynamicInfo
        const { label, ...safeDynamic } = dynamicInfo;

        return { ...staticInfo, ...safeDynamic };
    };

    const selectedNodeData = getSelectedNodeData();

    return (
        <div className="flex h-[calc(100vh-140px)] animate-in fade-in duration-500 overflow-hidden border border-[var(--color-BORDER)] rounded bg-[var(--color-bg-SURFACE)] relative">

            {/* Left: Canvas */}
            <div
                className="flex-1 relative overflow-hidden bg-[url('/grid-pattern.svg')] bg-[length:40px_40px]"
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
            >
                <div className="absolute inset-0 opacity-20 pointer-events-none"
                    style={{ backgroundImage: 'radial-gradient(circle, var(--color-ACCENT) 1px, transparent 1px)', backgroundSize: '30px 30px' }}>
                </div>

                {/* Connections (Dynamic based on layout) */}
                {[
                    ['gateway', 'auth-service'],
                    ['gateway', 'id-service'],
                    ['gateway', 'verify-service'],
                    ['gateway', 'audit-service'],
                    ['auth-service', 'audit-service'],
                    ['id-service', 'iprs-mock'] // IPRS Lookup flow
                ].map(([start, end], idx) => (
                    <Connection
                        key={idx}
                        startX={layout[start].x}
                        startY={layout[start].y}
                        endX={layout[end].x}
                        endY={layout[end].y}
                        active={true}
                    />
                ))}

                {/* Nodes */}
                {Object.entries(layout).map(([key, data]) => (
                    <Node
                        key={key}
                        label={data.label}
                        icon={data.icon}
                        status={getNodeStatus(data.service)}
                        x={data.x}
                        y={data.y}
                        selected={selectedNodeKey === key}
                        onMouseDown={(e) => handleMouseDown(e, key)}
                        onClick={() => setSelectedNodeKey(key)}
                    />
                ))}

                {/* Instructions Overlay */}
                {!selectedNodeKey && (
                    <div className="absolute bottom-8 left-8 p-4 bg-[var(--color-bg-MAIN)]/90 border border-[var(--color-BORDER)] rounded max-w-xs backdrop-blur shadow-lg pointer-events-none">
                        <h4 className="font-bold text-[var(--color-text-MAIN)] flex items-center gap-2 mb-2">
                            <Activity size={16} className="text-[var(--color-ACCENT)]" /> Command Center
                        </h4>
                        <p className="text-xs text-[var(--color-text-MUTED)]">Drag nodes to reorganize. Select any node to view real-time log streams.</p>
                    </div>
                )}
            </div>

            {/* Right: Detail Drawer */}
            <div className={`w-96 bg-[var(--color-bg-MAIN)] border-l border-[var(--color-BORDER)] transform transition-transform duration-300 absolute right-0 top-0 bottom-0 shadow-2xl z-20 overflow-y-auto ${selectedNodeKey ? 'translate-x-0' : 'translate-x-full'
                }`}>
                {selectedNodeData && (
                    <div className="p-0 h-full flex flex-col">
                        {/* Drawer Header */}
                        <div className="p-6 border-b border-[var(--color-BORDER)] bg-[var(--color-bg-SURFACE)] sticky top-0 z-10">
                            <div className="flex justify-between items-start mb-4">
                                <h2 className="text-xl font-bold font-ocr text-[var(--color-text-MAIN)]">{selectedNodeData.label}</h2>
                                <button onClick={() => setSelectedNodeKey(null)} className="text-[var(--color-text-MUTED)] hover:text-red-500">
                                    <X size={20} />
                                </button>
                            </div>
                            <div className="flex gap-2 text-xs">
                                <span className={`px-2 py-1 rounded font-bold uppercase ${getNodeStatus(selectedNodeData.service) === 'active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                    }`}>
                                    {getNodeStatus(selectedNodeData.service) === 'active' ? 'OPERATIONAL' : 'OFFLINE'}
                                </span>
                                <span className="px-2 py-1 rounded bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] text-[var(--color-text-MUTED)] font-mono">
                                    Port: {selectedNodeData.metrics?.port || (selectedNodeData.service === 'gateway' ? '8000' : 'UNK')}
                                </span>
                            </div>
                        </div>

                        {/* Metrics */}
                        <div className="p-6 space-y-6 border-b border-[var(--color-BORDER)]">
                            <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--color-text-MUTED)] mb-4">Resource Usage</h3>

                            {/* CPU */}
                            <div>
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="text-[var(--color-text-MAIN)] font-mono">CPU Load</span>
                                    <span className="text-[var(--color-text-MAIN)] font-bold">{selectedNodeData.cpu_percent || 0}%</span>
                                </div>
                                <div className="h-2 bg-[var(--color-bg-SURFACE)] rounded-full overflow-hidden">
                                    <div className="h-full bg-[var(--color-ACCENT)] transition-all duration-500" style={{ width: `${selectedNodeData.cpu_percent || 0}%` }}></div>
                                </div>
                            </div>

                            {/* Memory */}
                            <div>
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="text-[var(--color-text-MAIN)] font-mono">Memory</span>
                                    <span className="text-[var(--color-text-MAIN)] font-bold">{selectedNodeData.memory_percent || 0}%</span>
                                </div>
                                <div className="h-2 bg-[var(--color-bg-SURFACE)] rounded-full overflow-hidden">
                                    <div className="h-full bg-blue-500 transition-all duration-500" style={{ width: `${selectedNodeData.memory_percent || 0}%` }}></div>
                                </div>
                            </div>
                        </div>

                        {/* Live Logs */}
                        <div className="flex-1 flex flex-col bg-[var(--color-bg-MAIN)] min-h-0">
                            <div className="p-4 bg-[var(--color-bg-SURFACE)] border-b border-[var(--color-BORDER)] flex justify-between items-center">
                                <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--color-text-MUTED)] flex items-center gap-2">
                                    <Terminal size={14} /> Live Traffic
                                </h3>
                                <span className="text-[10px] bg-[var(--color-ACCENT)] text-white px-2 py-0.5 rounded-full animate-pulse">STREAMING</span>
                            </div>

                            <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-[10px] bg-black text-green-500/80">
                                {(!selectedNodeData.metrics?.recent_traffic || selectedNodeData.metrics.recent_traffic.length === 0) ? (
                                    <div className="text-center py-4 text-[var(--color-text-MUTED)] opacity-50">
                                        No recent traffic logs captured.
                                    </div>
                                ) : (
                                    [...selectedNodeData.metrics.recent_traffic].reverse().map((log, i) => (
                                        <div key={i} className="break-all border-b border-white/5 pb-1 mb-1 last:border-0 hover:bg-white/5 transition-colors">
                                            <span className="text-[var(--color-text-MUTED)]">[{new Date(log.timestamp * 1000).toLocaleTimeString()}]</span>
                                            <span className="text-white font-bold mx-1">"{log.method} {log.path} HTTP/1.1"</span>
                                            <span className={log.status >= 400 ? 'text-red-500' : 'text-green-400'}>{log.status}</span>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
