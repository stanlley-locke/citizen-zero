import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Save, Plus } from 'lucide-react';
import ENDPOINTS from '../../services/apiConfig';

export default function NewEnrollment() {
    const navigate = useNavigate();
    const [submitting, setSubmitting] = useState(false);

    // Initial State matching Citizen Model
    const [formData, setFormData] = useState({
        national_id: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: 'M',
        place_of_birth: '',
        county_of_birth: '047 - Nairobi', // Default
        phone_number: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            await axios.post(ENDPOINTS.CITIZENS.CREATE, formData);
            // Redirect to list on success
            navigate('/citizens');
        } catch (error) {
            console.error("Enrollment failed:", error);
            alert("Failed to enroll citizen. Check console for details.");
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-[var(--color-BORDER)] pb-6">
                <div className="flex items-center gap-4">
                    <button onClick={() => navigate('/citizens')} className="p-2 hover:bg-[var(--color-bg-SURFACE)] rounded-full transition-colors text-[var(--color-text-MUTED)]">
                        <ArrowLeft size={20} />
                    </button>
                    <div>
                        <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight">New Enrollment</h2>
                        <p className="text-[var(--color-text-MUTED)] text-sm">Register a new citizen into the National Registry (IPRS).</p>
                    </div>
                </div>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-8 shadow-sm space-y-8">

                {/* Section 1: Identity */}
                <div>
                    <h3 className="text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-widest mb-4 border-l-2 border-[var(--color-ACCENT)] pl-3">
                        Personal Identity
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">National ID Number</label>
                            <input
                                required
                                name="national_id"
                                value={formData.national_id}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none font-mono"
                                placeholder="e.g. 12345678"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">Gender</label>
                            <select
                                name="gender"
                                value={formData.gender}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                            >
                                <option value="M">Male</option>
                                <option value="F">Female</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">First Name</label>
                            <input
                                required
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">Last Name</label>
                            <input
                                required
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                            />
                        </div>
                    </div>
                </div>

                {/* Section 2: Birth Details */}
                <div>
                    <h3 className="text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-widest mb-4 border-l-2 border-[var(--color-ACCENT)] pl-3">
                        Birth Details
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">Date of Birth</label>
                            <input
                                required
                                type="date"
                                name="date_of_birth"
                                value={formData.date_of_birth}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">Place of Birth (Hospital/Town)</label>
                            <input
                                required
                                name="place_of_birth"
                                value={formData.place_of_birth}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                            />
                        </div>
                        <div className="space-y-2 md:col-span-2">
                            <label className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase">County of Birth</label>
                            <select
                                name="county_of_birth"
                                value={formData.county_of_birth}
                                onChange={handleChange}
                                className="w-full p-3 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-[var(--color-text-MAIN)] focus:border-[var(--color-ACCENT)] outline-none"
                            >
                                <option value="047 - Nairobi">047 - Nairobi</option>
                                <option value="001 - Mombasa">001 - Mombasa</option>
                                <option value="042 - Kisumu">042 - Kisumu</option>
                                <option value="032 - Nakuru">032 - Nakuru</option>
                                {/* Add more as needed */}
                            </select>
                        </div>
                    </div>
                </div>

                {/* Actions */}
                <div className="flex justify-end pt-6 border-t border-[var(--color-BORDER)]">
                    <button
                        type="submit"
                        disabled={submitting}
                        className="px-8 py-3 bg-[var(--color-ACCENT)] text-white hover:opacity-90 font-bold uppercase tracking-widest shadow-lg flex items-center gap-2 disabled:opacity-50"
                    >
                        {submitting ? 'Saving...' : <><Save size={18} /> Register Citizen</>}
                    </button>
                </div>
            </form>
        </div>
    );
}
