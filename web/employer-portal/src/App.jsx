import { BrowserRouter, Routes, Route, useNavigate, useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import HRDashboard from './pages/HRDashboard';
import VerifierDashboard from './pages/VerifierDashboard';
import OrgAdminDashboard from './pages/OrgAdminDashboard';

// Token Handoff Handler
function AuthHandler() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    useEffect(() => {
        const token = searchParams.get('token');
        const role = searchParams.get('role');

        if (token && role) {
            localStorage.setItem('accessToken', token);
            localStorage.setItem('role', role);
            // Clear params from URL
            navigate('/', { replace: true });
        } else {
            // Check if already logged in
            const storedToken = localStorage.getItem('accessToken');
            if (!storedToken) {
                window.location.href = 'http://localhost:3000/login'; // Back to centralized login
            }
        }
    }, [searchParams, navigate]);

    return null; // Invisible component
}

function DashboardRouter() {
    const role = localStorage.getItem('role') || 'Unknown';
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) return null;

    // Dashboards handle their own full-page layout
    if (role === 'HR_MANAGER') return <HRDashboard />;
    if (role === 'VERIFIER' || role === 'EMPLOYER_VERIFIER') return <VerifierDashboard />;
    if (['ORG_ADMIN', 'DATA_CONTROLLER', 'DPO', 'INT_AUDITOR'].includes(role)) return <OrgAdminDashboard />;

    // Default Fallback
    return (
        <div className="min-h-screen bg-[var(--color-bg-MAIN)] flex items-center justify-center p-4">
            <div className="text-center">
                <h2 className="text-xl font-bold text-[var(--color-text-MAIN)]">Access Denied Or Role Unknown</h2>
                <p className="text-[var(--color-text-MUTED)] mt-2">{role}</p>
                <button
                    onClick={() => { localStorage.clear(); window.location.href = 'http://localhost:3000/login'; }}
                    className="mt-4 px-4 py-2 border border-[var(--color-BORDER)] rounded hover:bg-[var(--color-bg-SURFACE)] text-[var(--color-text-MAIN)]"
                >
                    Return to Login
                </button>
            </div>
        </div>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AuthHandler />
            <Routes>
                <Route path="/" element={<DashboardRouter />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App;
