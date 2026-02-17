import { Search, Network, FileWarning, Eye } from 'lucide-react';

export default function InvestigatorDashboard() {
    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight text-red-500">
                        Investigation Unit
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">
                        Forensic Data Analysis & Audit
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-xs font-bold px-2 py-1 bg-red-500/10 text-red-500 border border-red-500/20">CONFIDENTIAL</span>
                </div>
            </div>

            {/* Tools */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-red-500 transition-all cursor-pointer group">
                    <Search className="mb-2 text-[var(--color-text-MUTED)] group-hover:text-red-500" />
                    <h3 className="font-bold text-sm uppercase">Deep Search</h3>
                </div>
                <div className="p-4 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-red-500 transition-all cursor-pointer group">
                    <Network className="mb-2 text-[var(--color-text-MUTED)] group-hover:text-red-500" />
                    <h3 className="font-bold text-sm uppercase">Family Tree</h3>
                </div>
                <div className="p-4 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-red-500 transition-all cursor-pointer group">
                    <FileWarning className="mb-2 text-[var(--color-text-MUTED)] group-hover:text-red-500" />
                    <h3 className="font-bold text-sm uppercase">Flagged Profiles</h3>
                </div>
                <div className="p-4 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-red-500 transition-all cursor-pointer group">
                    <Eye className="mb-2 text-[var(--color-text-MUTED)] group-hover:text-red-500" />
                    <h3 className="font-bold text-sm uppercase">Surveillance Logs</h3>
                </div>
            </div>

            {/* Case Files Placeholder */}
            <div className="mt-8">
                <div className="bg-black/20 border border-red-500/20 p-4 rounded min-h-[300px] flex items-center justify-center">
                    <span className="font-mono text-red-500/50 text-xs">AUTHORIZED PERSONNEL ONLY // AUDIT TRAIL ACTIVE</span>
                </div>
            </div>
        </div>
    );
}
