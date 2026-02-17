import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, User, Calendar, MapPin, Phone, Shield, FileText, Activity } from 'lucide-react';
import ENDPOINTS from '../../services/apiConfig';

export default function CitizenDetails() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [citizen, setCitizen] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCitizen = async () => {
            try {
                // Assuming the endpoint is /api/v1/citizens/:id/
                // We construct it manually since apiConfig might just have the list endpoint
                // Ideally apiConfig should have a details builder or we append to list
                // Based on previous checks, CITIZENS.LIST is .../api/v1/citizens/
                const url = `${ENDPOINTS.CITIZENS.LIST}${id}/`;
                const res = await axios.get(url);
                setCitizen(res.data);
            } catch (err) {
                console.error("Failed to fetch citizen details", err);
                setError("Citizen not found or access denied.");
            } finally {
                setLoading(false);
            }
        };

        if (id) fetchCitizen();
    }, [id]);

    if (loading) {
        return (
            <div className="h-96 flex flex-col items-center justify-center animate-pulse">
                <div className="w-12 h-12 border-4 border-[var(--color-ACCENT)] border-t-transparent rounded-full animate-spin mb-4"></div>
                <p className="text-[var(--color-text-MUTED)] font-ocr uppercase tracking-widest text-xs">Retrieving digital identity...</p>
            </div>
        );
    }

    if (error || !citizen) {
        return (
            <div className="h-96 flex flex-col items-center justify-center text-center">
                <Shield size={48} className="text-red-500 mb-4" />
                <h2 className="text-xl font-bold text-[var(--color-text-MAIN)] mb-2">Identity Not Found</h2>
                <p className="text-[var(--color-text-MUTED)] mb-6">{error || "The requested national ID does not exist in the registry."}</p>
                <button
                    onClick={() => navigate('/citizens')}
                    className="px-6 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)] flex items-center gap-2"
                >
                    <ArrowLeft size={16} /> Return to Registry
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-500 pb-10">
            {/* Header */}
            <div>
                <button
                    onClick={() => navigate('/citizens')}
                    className="mb-4 text-[var(--color-text-MUTED)] hover:text-[var(--color-ACCENT)] text-xs font-bold uppercase tracking-widest flex items-center gap-2 transition-colors"
                >
                    <ArrowLeft size={14} /> Back to Registry
                </button>
                <div className="flex justify-between items-start">
                    <div>
                        <h1 className="text-3xl font-bold text-[var(--color-text-MAIN)] font-mono tracking-tight">{citizen.first_name} {citizen.last_name}</h1>
                        <p className="text-[var(--color-text-MUTED)] mt-1 font-ocr text-sm uppercase tracking-wider">
                            National ID: <span className="text-[var(--color-ACCENT)]">{citizen.national_id}</span>
                        </p>
                    </div>
                    <div className="px-3 py-1 bg-green-500/10 border border-green-500/20 text-green-500 text-[10px] font-bold uppercase tracking-widest rounded">
                        Active Citizen
                    </div>
                </div>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Left Column: Profile Card */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm flex flex-col items-center text-center">
                        <div className="w-32 h-32 bg-[var(--color-bg-SURFACE)] rounded-full mb-4 flex items-center justify-center border-2 border-[var(--color-BORDER)]">
                            <User size={48} className="text-[var(--color-text-MUTED)]" />
                        </div>
                        <h3 className="text-lg font-bold text-[var(--color-text-MAIN)]">{citizen.first_name} {citizen.last_name}</h3>
                        <p className="text-[var(--color-text-MUTED)] text-xs uppercase tracking-widest mt-1">{citizen.county_of_birth} | {citizen.gender === 'M' ? 'Male' : 'Female'}</p>
                    </div>

                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm space-y-4">
                        <h4 className="text-xs font-bold text-[var(--color-text-MUTED)] uppercase tracking-widest border-b border-[var(--color-BORDER)] pb-2 mb-4">
                            Biometric Status
                        </h4>
                        <div className="flex justify-between items-center text-sm">
                            <span className="text-[var(--color-text-MAIN)]">Fingerprints</span>
                            <span className="text-green-500 text-xs font-bold uppercase">Captured</span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                            <span className="text-[var(--color-text-MAIN)]">Iris Scan</span>
                            <span className="text-yellow-500 text-xs font-bold uppercase">Pending</span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                            <span className="text-[var(--color-text-MAIN)]">Face Photo</span>
                            <span className="text-green-500 text-xs font-bold uppercase">Captured</span>
                        </div>
                    </div>
                </div>

                {/* Right Column: Detailed Info */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Identity Details */}
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm">
                        <h4 className="flex items-center gap-2 text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-widest mb-6">
                            <FileText size={16} className="text-[var(--color-ACCENT)]" /> Personal Information
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-y-6 gap-x-12">
                            <div>
                                <label className="block text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Date of Birth</label>
                                <div className="text-sm text-[var(--color-text-MAIN)] font-mono flex items-center gap-2">
                                    <Calendar size={14} /> {citizen.date_of_birth}
                                </div>
                            </div>
                            <div>
                                <label className="block text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Place of Birth</label>
                                <div className="text-sm text-[var(--color-text-MAIN)] flex items-center gap-2">
                                    <MapPin size={14} /> {citizen.place_of_birth}
                                </div>
                            </div>
                            <div>
                                <label className="block text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Gender</label>
                                <div className="text-sm text-[var(--color-text-MAIN)]">
                                    {citizen.gender === 'M' ? 'Male' : 'Female'}
                                </div>
                            </div>
                            <div>
                                <label className="block text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase mb-1">Phone Number</label>
                                <div className="text-sm text-[var(--color-text-MAIN)] flex items-center gap-2">
                                    <Phone size={14} /> {citizen.phone_number || 'N/A'}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Timeline / Activity Placeholder */}
                    <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] p-6 shadow-sm">
                        <h4 className="flex items-center gap-2 text-sm font-bold text-[var(--color-text-MAIN)] uppercase tracking-widest mb-6">
                            <Activity size={16} className="text-[var(--color-ACCENT)]" /> Recent Activity
                        </h4>
                        <div className="border-l-2 border-[var(--color-BORDER)] pl-4 space-y-6 ml-2">
                            <div className="relative">
                                <div className="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-green-500"></div>
                                <p className="text-xs font-bold text-[var(--color-text-MAIN)]">Identity Verified</p>
                                <p className="text-[10px] text-[var(--color-text-MUTED)]">System - {new Date(citizen.updated_at).toLocaleString()}</p>
                            </div>
                            <div className="relative">
                                <div className="absolute -left-[21px] top-1 w-3 h-3 rounded-full bg-[var(--color-BORDER)]"></div>
                                <p className="text-xs font-bold text-[var(--color-text-MAIN)]">Record Created</p>
                                <p className="text-[10px] text-[var(--color-text-MUTED)]">Registration Officer - {new Date(citizen.created_at).toLocaleString()}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
