import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Search, Filter, UserPlus, MoreHorizontal, Download, Users, ChevronLeft, ChevronRight, X, FileText, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ENDPOINTS from '../../services/apiConfig';

// Simple debounce hook
function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);
    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);
        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);
    return debouncedValue;
}

export default function CitizenList() {
    const navigate = useNavigate();
    const [citizens, setCitizens] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    // UI States
    const [showExportMenu, setShowExportMenu] = useState(false);
    const [showFilterMenu, setShowFilterMenu] = useState(false);

    // Filter States
    const [filterGender, setFilterGender] = useState('');
    const [filterCounty, setFilterCounty] = useState('');

    const exportMenuRef = useRef(null);
    const filterMenuRef = useRef(null);

    const debouncedSearch = useDebounce(search, 500);

    // Close menus when clicking outside
    useEffect(() => {
        function handleClickOutside(event) {
            if (exportMenuRef.current && !exportMenuRef.current.contains(event.target)) {
                setShowExportMenu(false);
            }
            if (filterMenuRef.current && !filterMenuRef.current.contains(event.target)) {
                setShowFilterMenu(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [exportMenuRef, filterMenuRef]);

    useEffect(() => {
        setPage(1);
    }, [debouncedSearch, filterGender, filterCounty]);

    useEffect(() => {
        fetchCitizens();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [page, debouncedSearch, filterGender, filterCounty]);

    const fetchCitizens = async () => {
        setLoading(true);
        try {
            const params = { page: page };
            if (debouncedSearch) params.search = debouncedSearch;
            if (filterGender) params.gender = filterGender;
            if (filterCounty) params.county = filterCounty;

            console.log("Fetching with params:", params);

            const res = await axios.get(ENDPOINTS.CITIZENS.LIST, { params });

            if (res.data.results) {
                setCitizens(res.data.results);
                if (res.data.count) {
                    setTotalPages(Math.ceil(res.data.count / 10));
                }
            } else if (Array.isArray(res.data)) {
                setCitizens(res.data);
                setTotalPages(1);
            }
        } catch (error) {
            console.error("Failed to fetch citizens:", error);
            setCitizens([]);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = async (type) => {
        setShowExportMenu(false);
        let dataToExport = [];

        // Build Params for Export
        const exportParams = { search: debouncedSearch };
        if (filterGender) exportParams.gender = filterGender;
        if (filterCounty) exportParams.county = filterCounty;
        if (type === 'all') exportParams.page_size = 1000;

        try {
            const res = await axios.get(ENDPOINTS.CITIZENS.LIST, { params: exportParams });
            if (res.data.results) {
                dataToExport = res.data.results;
            } else if (Array.isArray(res.data)) {
                dataToExport = res.data;
            }
        } catch (e) {
            console.error("Export all failed", e);
            alert("Failed to fetch records for export.");
            return;
        }

        if (dataToExport.length === 0) return;

        const headers = ['National ID', 'First Name', 'Last Name', 'Gender', 'DOB', 'County', 'Phone'];
        const csvContent = [
            headers.join(','),
            ...dataToExport.map(c => [
                c.national_id,
                c.first_name,
                c.last_name,
                c.gender,
                c.date_of_birth,
                c.county_of_birth,
                c.phone_number || ''
            ].join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `citizens_export_${type}_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const clearFilters = () => {
        setFilterGender('');
        setFilterCounty('');
        setSearch('');
        setShowFilterMenu(false);
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 min-h-screen pb-10">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Users className="text-[var(--color-ACCENT)]" /> Citizen Registry
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Master database of all registered nationals.</p>
                </div>
                <div className="flex gap-3 relative">
                    <button onClick={() => navigate('/citizens/new')} className="px-4 py-2 bg-[var(--color-ACCENT)] text-white hover:opacity-90 text-xs font-bold uppercase tracking-widest shadow-sm flex items-center gap-2">
                        <UserPlus size={14} /> New Enrollment
                    </button>

                    <div ref={exportMenuRef}>
                        <button
                            onClick={() => setShowExportMenu(!showExportMenu)}
                            className="px-4 py-2 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest transition-colors text-[var(--color-text-MAIN)] flex items-center gap-2"
                        >
                            <Download size={14} /> Export
                        </button>

                        {/* Export Menu Dropdown */}
                        {showExportMenu && (
                            <div className="absolute right-0 top-full mt-2 w-48 bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-xl z-50 animate-in fade-in zoom-in-95 duration-200">
                                <div className="p-2 border-b border-[var(--color-BORDER)] bg-[var(--color-bg-SURFACE)] text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase">
                                    Export Options
                                </div>
                                <button onClick={() => handleExport('current')} className="w-full text-left px-4 py-3 text-xs font-bold text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] flex items-center gap-2">
                                    <FileText size={14} /> Current View
                                </button>
                                <button onClick={() => handleExport('all')} className="w-full text-left px-4 py-3 text-xs font-bold text-[var(--color-text-MAIN)] hover:bg-[var(--color-bg-SURFACE)] flex items-center gap-2">
                                    <Download size={14} /> All Data (CSV)
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Controls */}
            <div className="relative z-20 flex gap-4 items-center bg-[var(--color-bg-MAIN)] p-4 border border-[var(--color-BORDER)] shadow-sm">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-MUTED)]" size={16} />
                    <input
                        type="text"
                        placeholder="Search by ID, First Name, or Last Name..."
                        className="w-full pl-10 pr-4 py-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-sm focus:outline-none focus:border-[var(--color-ACCENT)] text-[var(--color-text-MAIN)] transition-all"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                    {search && (
                        <button onClick={() => setSearch('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-text-MUTED)] hover:text-[var(--color-ACCENT)]">
                            <X size={14} />
                        </button>
                    )}
                </div>

                {loading && <span className="text-xs text-[var(--color-text-MUTED)] animate-pulse uppercase font-ocr">Syncing...</span>}

                <div className="relative" ref={filterMenuRef}>
                    <button
                        onClick={() => setShowFilterMenu(!showFilterMenu)}
                        className={`px-4 py-2 border ${filterGender || filterCounty ? 'border-[var(--color-ACCENT)] text-[var(--color-ACCENT)]' : 'border-[var(--color-BORDER)] text-[var(--color-text-MUTED)]'} bg-[var(--color-bg-SURFACE)] text-xs font-bold uppercase tracking-widest flex items-center gap-2 transition-colors`}
                    >
                        <Filter size={14} /> Filter {(filterGender || filterCounty) && '•'}
                    </button>

                    {showFilterMenu && (
                        <div className="absolute right-0 top-full mt-2 w-64 bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-xl z-50 animate-in fade-in zoom-in-95 duration-200 p-4 space-y-4">
                            <div className="flex justify-between items-center border-b border-[var(--color-BORDER)] pb-2">
                                <span className="text-[10px] font-bold text-[var(--color-text-MUTED)] uppercase">Filter Records</span>
                                {(filterGender || filterCounty) && (
                                    <button onClick={clearFilters} className="text-[10px] text-red-500 font-bold hover:underline">Clear All</button>
                                )}
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs font-bold text-[var(--color-text-MAIN)] uppercase">Gender</label>
                                <select
                                    value={filterGender}
                                    onChange={(e) => setFilterGender(e.target.value)}
                                    className="w-full p-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-xs text-[var(--color-text-MAIN)] outline-none focus:border-[var(--color-ACCENT)]"
                                >
                                    <option value="">All Genders</option>
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                </select>
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs font-bold text-[var(--color-text-MAIN)] uppercase">County</label>
                                <select
                                    value={filterCounty}
                                    onChange={(e) => setFilterCounty(e.target.value)}
                                    className="w-full p-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] text-xs text-[var(--color-text-MAIN)] outline-none focus:border-[var(--color-ACCENT)]"
                                >
                                    <option value="">All Counties</option>
                                    <option value="Nairobi">Nairobi</option>
                                    <option value="Mombasa">Mombasa</option>
                                    <option value="Kisumu">Kisumu</option>
                                    <option value="Nakuru">Nakuru</option>
                                    <option value="Kiambu">Kiambu</option>
                                    <option value="Machakos">Machakos</option>
                                </select>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Table */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-sm overflow-hidden min-h-[400px]">
                <table className="w-full text-left text-sm">
                    <thead className="bg-[var(--color-bg-SURFACE)] border-b border-[var(--color-BORDER)]">
                        <tr>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">National ID</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Full Name</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Gender</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Date of Birth</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">County</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--color-BORDER)]">
                        {loading && citizens.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="px-6 py-12 text-center text-[var(--color-text-MUTED)] animate-pulse">
                                    accessing secure registry...
                                </td>
                            </tr>
                        ) : citizens.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="px-6 py-12 text-center text-[var(--color-text-MUTED)]">
                                    No records found matching query.
                                </td>
                            </tr>
                        ) : (
                            citizens.map((citizen) => (
                                <tr
                                    key={citizen.national_id}
                                    className="hover:bg-[var(--color-bg-SURFACE)] transition-colors group cursor-pointer"
                                    onDoubleClick={() => navigate(`/citizens/${citizen.national_id}`)}
                                >
                                    <td className="px-6 py-4 whitespace-nowrap font-mono font-bold text-[var(--color-text-MAIN)]">
                                        {citizen.national_id}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-[var(--color-text-MAIN)]">
                                        {citizen.first_name} {citizen.last_name}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-[var(--color-text-MUTED)]">
                                        {citizen.gender === 'M' ? 'Male' : 'Female'}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-[var(--color-text-MUTED)] font-mono">
                                        {citizen.date_of_birth}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-[var(--color-text-MUTED)]">
                                        {citizen.county_of_birth}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex items-center gap-2">
                                            <button
                                                onClick={(e) => { e.stopPropagation(); navigate(`/citizens/${citizen.national_id}`); }}
                                                className="text-[var(--color-text-MUTED)] hover:text-[var(--color-ACCENT)] transition-colors"
                                                title="View Details"
                                            >
                                                <Eye size={16} />
                                            </button>
                                            <button className="text-[var(--color-text-MUTED)] hover:text-[var(--color-ACCENT)] transition-colors">
                                                <MoreHorizontal size={16} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
                <div className="flex justify-between items-center border-t border-[var(--color-BORDER)] pt-4">
                    <p className="text-xs text-[var(--color-text-MUTED)] uppercase">
                        Page <span className="text-[var(--color-text-MAIN)] font-bold">{page}</span> of {totalPages}
                    </p>
                    <div className="flex gap-2 text-xs font-bold uppercase">
                        <button
                            disabled={page === 1}
                            onClick={() => setPage(p => p - 1)}
                            className="px-3 py-1 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1 transition-colors text-[var(--color-text-MAIN)]"
                        >
                            <ChevronLeft size={14} /> Prev
                        </button>
                        <button
                            disabled={page === totalPages}
                            onClick={() => setPage(p => p + 1)}
                            className="px-3 py-1 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1 transition-colors text-[var(--color-text-MAIN)]"
                        >
                            Next <ChevronRight size={14} />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
