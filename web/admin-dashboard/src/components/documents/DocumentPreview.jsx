import { X, Download, Printer, Maximize2 } from 'lucide-react';

export default function DocumentPreview({ title, pdfUrl, onClose, onDownload }) {
    if (!pdfUrl) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-[var(--color-bg-MAIN)] w-full max-w-4xl h-[90vh] flex flex-col rounded-lg shadow-2xl border border-[var(--color-BORDER)]">
                {/* Header */}
                <div className="flex justify-between items-center p-4 border-b border-[var(--color-BORDER)]">
                    <h3 className="text-lg font-bold text-[var(--color-text-MAIN)] flex items-center gap-2">
                        <Maximize2 size={18} className="text-[var(--color-ACCENT)]" /> {title}
                    </h3>
                    <div className="flex gap-2">
                        <button
                            onClick={onDownload}
                            className="px-4 py-2 bg-[var(--color-ACCENT)] text-white text-xs font-bold uppercase tracking-widest hover:opacity-90 flex items-center gap-2 rounded"
                        >
                            <Download size={16} /> Download
                        </button>
                        <button
                            onClick={onClose}
                            className="p-2 text-[var(--color-text-MUTED)] hover:text-[var(--color-text-MAIN)] transition-colors"
                        >
                            <X size={20} />
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="flex-1 bg-gray-100 p-4 flex justify-center items-center overflow-auto">
                    <iframe
                        src={pdfUrl}
                        className="w-full h-full shadow-lg"
                        title="Document Preview"
                    />
                </div>
            </div>
        </div>
    );
}
