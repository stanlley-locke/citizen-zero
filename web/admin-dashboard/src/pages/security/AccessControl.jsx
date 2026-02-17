import { Lock, UserCog, Shield, Plus, MoreVertical } from 'lucide-react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ENDPOINTS from '../../services/apiConfig';

export default function AccessControl() {
    const [admins, setAdmins] = useState([]);
    const [loading, setLoading] = useState(true);

    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        role: 'SYSTEM_ADMIN',
        organization: ''
    });
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        fetchAdmins();
    }, []);

    const fetchAdmins = async () => {
        setLoading(true);
        try {
            const res = await axios.get(ENDPOINTS.AUTH.ADMINS);
            setAdmins(res.data);
        } catch (error) {
            console.error("Failed to fetch admin users:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            await axios.post(ENDPOINTS.AUTH.ADMINS, formData);
            setShowModal(false);
            setFormData({ username: '', email: '', password: '', role: 'SYSTEM_ADMIN', organization: '' });
            fetchAdmins(); // Refresh list
            alert("User created successfully.");
        } catch (error) {
            console.error("Failed to create user:", error);
            const errorMsg = error.response?.data ? JSON.stringify(error.response.data) : error.message;
            alert(`Failed to create user: ${errorMsg}`);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 relative">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Lock className="text-[var(--color-ACCENT)]" /> Access Control
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Manage users, roles, and access permissions.</p>
                </div>
                <button onClick={() => setShowModal(true)} className="px-4 py-2 bg-[var(--color-ACCENT)] text-white hover:opacity-90 text-xs font-bold uppercase tracking-widest shadow-sm flex items-center gap-2">
                    <Plus size={14} /> Add User
                </button>
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] w-full max-w-md p-6 shadow-2xl animate-in zoom-in-95 duration-200">
                        <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] uppercase mb-4">New User</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-xs font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Username</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] p-2 text-sm text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                                    value={formData.username}
                                    onChange={e => setFormData({ ...formData, username: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Email</label>
                                <input
                                    type="email"
                                    required
                                    className="w-full bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] p-2 text-sm text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                                    value={formData.email}
                                    onChange={e => setFormData({ ...formData, email: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Password</label>
                                <input
                                    type="password"
                                    required
                                    className="w-full bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] p-2 text-sm text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                                    value={formData.password}
                                    onChange={e => setFormData({ ...formData, password: e.target.value })}
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-xs font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Role</label>
                                    <select
                                        className="w-full bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] p-2 text-sm text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                                        value={formData.role}
                                        onChange={e => setFormData({ ...formData, role: e.target.value })}
                                    >
                                        <optgroup label="System">
                                            <option value="SYSTEM_ADMIN">System Admin (Platform)</option>
                                        </optgroup>
                                        <optgroup label="Registry / Investigation (Admin Dash)">
                                            <option value="DATA_COLLECTOR">Field Data Collector (NRB)</option>
                                            <option value="INVESTIGATOR">Investigation Officer (DCI)</option>
                                        </optgroup>
                                        <optgroup label="Employer / Org (Employer Portal)">
                                            <option value="DATA_CONTROLLER">Data Controller (CEO)</option>
                                            <option value="DPO">Data Protection Officer</option>
                                            <option value="ORG_ADMIN">System Administrator (Org)</option>
                                            <option value="HR_MANAGER">HR Manager</option>
                                            <option value="INT_AUDITOR">Internal Auditor</option>
                                            <option value="VERIFIER">Verifier (Frontline)</option>
                                        </optgroup>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Organization</label>
                                    <input
                                        type="text"
                                        className="w-full bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] p-2 text-sm text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                                        placeholder="Optional"
                                        value={formData.organization}
                                        onChange={e => setFormData({ ...formData, organization: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div className="flex gap-3 pt-4">
                                <button type="button" onClick={() => setShowModal(false)} className="flex-1 py-2 border border-[var(--color-BORDER)] text-[var(--color-text-MUTED)] uppercase text-xs font-bold hover:bg-[var(--color-bg-SURFACE)]">Cancel</button>
                                <button type="submit" disabled={submitting} className="flex-1 py-2 bg-[var(--color-ACCENT)] text-white uppercase text-xs font-bold hover:opacity-90 disabled:opacity-50">
                                    {submitting ? 'Creating...' : 'Create User'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* User List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {loading ? (
                    <div className="col-span-full py-12 text-center text-[var(--color-text-MUTED)] animate-pulse font-mono">
                        Loading ecosystem users...
                    </div>
                ) : (
                    admins.map((user) => (
                        <div key={user.id} className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm hover:border-[var(--color-ACCENT)] transition-all group relative">
                            <button className="absolute top-4 right-4 text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)]">
                                <MoreVertical size={16} />
                            </button>

                            <div className="flex items-center gap-4 mb-4">
                                <div className="w-12 h-12 bg-[var(--color-bg-SURFACE)] rounded-full flex items-center justify-center text-[var(--color-text-MUTED)] group-hover:bg-[var(--color-ACCENT)] group-hover:text-white transition-colors">
                                    <UserCog size={24} />
                                </div>
                                <div>
                                    <h3 className="font-bold text-[var(--color-text-MAIN)]">{user.username}</h3>
                                    <p className="text-xs text-[var(--color-text-MUTED)]">{user.email}</p>
                                    {user.organization && <p className="text-[10px] text-[var(--color-ACCENT)] mt-1 font-bold uppercase">{user.organization}</p>}
                                </div>
                            </div>

                            <div className="space-y-2 border-t border-[var(--color-BORDER)] pt-4">
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-[var(--color-text-MUTED)] uppercase font-bold">Role</span>
                                    <span className="flex items-center gap-1 font-bold text-[var(--color-text-MAIN)]">
                                        <Shield size={12} className="text-[var(--color-ACCENT)]" />
                                        {user.role || (user.is_superuser ? 'ADMIN' : 'STAFF')}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-[var(--color-text-MUTED)] uppercase font-bold">Status</span>
                                    <span className={`px-2 py-0.5 rounded ${user.is_active ? 'bg-green-100/10 text-green-500' : 'bg-red-100/10 text-red-500'} font-bold`}>
                                        {user.is_active ? 'ACTIVE' : 'SUSPENDED'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
