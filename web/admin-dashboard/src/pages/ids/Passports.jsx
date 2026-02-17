import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Book, Eye, Download, Printer } from 'lucide-react';
import ENDPOINTS from '../../services/apiConfig';
import DocumentPreview from '../../components/documents/DocumentPreview';

function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);
    useEffect(() => {
        const handler = setTimeout(() => { setDebouncedValue(value); }, delay);
        return () => { clearTimeout(handler); };
    }, [value, delay]);
    return debouncedValue;
}

export default function Passports() {
    const [citizens, setCitizens] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);

    // Preview State
    const [previewUrl, setPreviewUrl] = useState(null);
    const [selectedCitizen, setSelectedCitizen] = useState(null);

    const debouncedSearch = useDebounce(search, 500);

    // Fetch Citizens (Ideally would filter by those eligible/applied)
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const params = { page, search: debouncedSearch };
                const res = await axios.get(ENDPOINTS.CITIZENS.LIST, { params });

                if (res.data.results) {
                    setCitizens(res.data.results);
                } else if (Array.isArray(res.data)) {
                    setCitizens(res.data);
                }
            } catch (err) {
                console.error("Failed to fetch citizens", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [page, debouncedSearch]);

    const handlePreview = async (citizen) => {
        const url = `http://localhost:8001/api/v1/documents/preview/?type=passport&citizen_id=${citizen.national_id}`;
        setPreviewUrl(url);
        setSelectedCitizen(citizen);
    };

    const handleDownload = (citizen) => {
        const url = `http://localhost:8001/api/v1/documents/download/?type=passport&citizen_id=${citizen.national_id}`;
        window.open(url, '_blank');
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 min-h-screen pb-10">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Book className="text-[var(--color-ACCENT)]" /> Electronic Passports
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">International travel document issuance.</p>
                </div>
            </div>

            {/* Controls */}
            <div className="flex gap-4 items-center bg-[var(--color-bg-MAIN)] p-4 border border-[var(--color-BORDER)] shadow-sm">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-MUTED)]" size={16} />
                    <input
                        type="text"
                        placeholder="Search Citizen..."
                        className="w-full pl-10 pr-4 py-2 bg-[var(--color-bg-SURFACE)] border border-[var(--color-BORDER)] rounded text-sm focus:outline-none focus:border-[var(--color-ACCENT)] text-[var(--color-text-MAIN)] transition-all"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
            </div>

            {/* Table */}
            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-sm overflow-hidden min-h-[400px]">
                <table className="w-full text-left text-sm">
                    <thead className="bg-[var(--color-bg-SURFACE)] border-b border-[var(--color-BORDER)]">
                        <tr>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Citizen</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Passport No</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Type</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--color-BORDER)]">
                        {loading ? (
                            <tr><td colSpan="4" className="px-6 py-12 text-center text-[var(--color-text-MUTED)] animate-pulse">Loading Identity Data...</td></tr>
                        ) : citizens.length === 0 ? (
                            <tr><td colSpan="4" className="px-6 py-12 text-center text-[var(--color-text-MUTED)]">No citizens found.</td></tr>
                        ) : (
                            citizens.map(c => (
                                <tr key={c.national_id} className="hover:bg-[var(--color-bg-SURFACE)] transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="font-bold text-[var(--color-text-MAIN)]">{c.first_name} {c.last_name}</div>
                                        <div className="text-xs text-[var(--color-text-MUTED)]">{c.date_of_birth}</div>
                                    </td>
                                    <td className="px-6 py-4 font-mono text-[var(--color-text-MAIN)]">
                                        {/* Mock Passport Logic based on ID */}
                                        P{c.national_id.substring(0, 7)}
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="px-2 py-1 bg-blue-500/10 text-blue-500 text-[10px] font-bold uppercase rounded border border-blue-500/20">Ordinary</span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <div className="flex justify-end gap-2">
                                            <button
                                                onClick={() => handlePreview(c)}
                                                className="px-3 py-1 border border-[var(--color-BORDER)] hover:border-[var(--color-ACCENT)] hover:text-[var(--color-ACCENT)] text-[var(--color-text-MUTED)] text-xs font-bold uppercase flex items-center gap-1 transition-colors"
                                            >
                                                <Eye size={14} /> Preview
                                            </button>
                                            <button
                                                onClick={() => handleDownload(c)}
                                                className="px-3 py-1 bg-[var(--color-ACCENT)] text-white hover:opacity-90 text-xs font-bold uppercase flex items-center gap-1 transition-colors shadow-sm"
                                            >
                                                <Printer size={14} /> Print
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Document Preview Modal */}
            {previewUrl && (
                <DocumentPreview
                    title={`Passport: ${selectedCitizen?.national_id}`}
                    pdfUrl={previewUrl}
                    onClose={() => setPreviewUrl(null)}
                    onDownload={() => handleDownload(selectedCitizen)}
                />
            )}
        </div>
    );
}
