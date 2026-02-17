import { Server, Play, CheckCircle, XCircle, Terminal } from 'lucide-react';
import { useState } from 'react';
import ENDPOINTS from '../../services/apiConfig';
// Flatten the endpoints object for easier display
const flattenEndpoints = (obj, prefix = '') => {
    return Object.keys(obj).reduce((acc, k) => {
        const pre = prefix.length ? prefix + '.' : '';
        if (typeof obj[k] === 'object' && obj[k] !== null && !Array.isArray(obj[k]))
            Object.assign(acc, flattenEndpoints(obj[k], pre + k));
        else
            acc[pre + k] = obj[k];
        return acc;
    }, {});
};

export default function APIConfiguration() {
    const flatEndpoints = flattenEndpoints(ENDPOINTS);
    const [results, setResults] = useState({});
    const [testing, setTesting] = useState({});

    const testEndpoint = async (key, url) => {
        setTesting(prev => ({ ...prev, [key]: true }));
        try {
            // NOTE: Many endpoints need Auth/POST. We just check if server responds (even 401/405/404 is response).
            // A fetch failure (Network Error) is what we want to detect.
            const res = await fetch(url, { method: 'HEAD' }).catch(() => null)
                || await fetch(url).catch(e => ({ error: true }));

            if (res.error) throw new Error("Network Error");

            setResults(prev => ({ ...prev, [key]: 'ONLINE' }));
        } catch (error) {
            setResults(prev => ({ ...prev, [key]: 'UNREACHABLE' }));
        } finally {
            setTesting(prev => ({ ...prev, [key]: false }));
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex justify-between items-end border-b border-[var(--color-BORDER)] pb-6">
                <div>
                    <h2 className="text-2xl font-bold text-[var(--color-text-MAIN)] uppercase tracking-tight flex items-center gap-3">
                        <Terminal className="text-[var(--color-ACCENT)]" /> API Configuration
                    </h2>
                    <p className="text-[var(--color-text-MUTED)] mt-1 text-sm">Endpoint inspection and connectivity verification.</p>
                </div>
            </div>

            <div className="bg-[var(--color-bg-MAIN)] border border-[var(--color-BORDER)] shadow-sm overflow-hidden rounded">
                <table className="w-full text-left text-sm">
                    <thead className="bg-[var(--color-bg-SURFACE)] border-b border-[var(--color-BORDER)]">
                        <tr>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Key</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Endpoint URL</th>
                            <th className="px-6 py-3 font-ocr text-xs text-[var(--color-text-MUTED)] uppercase tracking-wider">Test</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--color-BORDER)]">
                        {Object.entries(flatEndpoints).map(([key, url]) => (
                            <tr key={key} className="hover:bg-[var(--color-bg-SURFACE)] transition-colors">
                                <td className="px-6 py-4 font-bold font-mono text-xs text-[var(--color-text-MAIN)]">
                                    {key}
                                </td>
                                <td className="px-6 py-4 font-mono text-xs text-[var(--color-text-MUTED)] break-all max-w-md">
                                    {url}
                                </td>
                                <td className="px-6 py-4">
                                    {results[key] ? (
                                        <div className={`flex items-center gap-2 font-bold text-xs ${results[key] === 'ONLINE' ? 'text-green-600' : 'text-red-600'}`}>
                                            {results[key] === 'ONLINE' ? <CheckCircle size={14} /> : <XCircle size={14} />}
                                            {results[key]}
                                        </div>
                                    ) : (
                                        <button
                                            onClick={() => testEndpoint(key, url)}
                                            disabled={testing[key]}
                                            className="flex items-center gap-2 px-3 py-1 border border-[var(--color-BORDER)] hover:bg-[var(--color-bg-SURFACE)] text-[var(--color-text-MAIN)] text-[10px] font-bold uppercase transition-colors"
                                        >
                                            {testing[key] ? 'Pinging...' : <><Play size={10} /> Check</>}
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
