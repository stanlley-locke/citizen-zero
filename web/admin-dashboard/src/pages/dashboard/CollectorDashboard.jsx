import { FileText, Plus, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function CollectorDashboard() {
    const navigate = useNavigate();

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight">
                        Field Data Collection
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">
                        National Registration Bureau / Civil Registration
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-[var(--color-ACCENT)]">SESSION: ACTIVE</span>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <button
                    onClick={() => navigate('/citizens/new')}
                    className="p-6 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-[var(--color-ACCENT)] transition-all group text-left"
                >
                    <div className="w-12 h-12 bg-[var(--color-bg-MAIN)] rounded-full flex items-center justify-center text-[var(--color-text-MAIN)] mb-4 group-hover:bg-[var(--color-ACCENT)] group-hover:text-white transition-colors">
                        <Plus size={24} />
                    </div>
                    <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] uppercase">New Registration</h3>
                    <p className="text-xs text-[var(--color-text-MUTED)] mt-2">Enroll a new citizen (Birth/ID)</p>
                </button>

                <button
                    onClick={() => navigate('/citizens')}
                    className="p-6 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-[var(--color-ACCENT)] transition-all group text-left"
                >
                    <div className="w-12 h-12 bg-[var(--color-bg-MAIN)] rounded-full flex items-center justify-center text-[var(--color-text-MAIN)] mb-4 group-hover:bg-[var(--color-ACCENT)] group-hover:text-white transition-colors">
                        <FileText size={24} />
                    </div>
                    <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] uppercase">Manage Records</h3>
                    <p className="text-xs text-[var(--color-text-MUTED)] mt-2">View and update existing drafts</p>
                </button>

                <button
                    className="p-6 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] hover:border-[var(--color-ACCENT)] transition-all group text-left opacity-50 cursor-not-allowed"
                >
                    <div className="w-12 h-12 bg-[var(--color-bg-MAIN)] rounded-full flex items-center justify-center text-[var(--color-text-MAIN)] mb-4">
                        <Search size={24} />
                    </div>
                    <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] uppercase">Search Registry</h3>
                    <p className="text-xs text-[var(--color-text-MUTED)] mt-2">Offline sync not available</p>
                </button>
            </div>

            {/* Recent Activity Placeholder */}
            <div className="mt-8">
                <h3 className="text-sm font-bold text-[var(--color-text-MUTED)] uppercase mb-4">Recent Enrolments</h3>
                <div className="h-48 border border-[var(--color-BORDER)] rounded bg-[var(--color-bg-SURFACE)] flex items-center justify-center text-[var(--color-text-MUTED)] text-xs font-mono">
                    NO RECENT ACTIVITY
                </div>
            </div>
        </div>
    );
}
