import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext.jsx';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Login from './pages/auth/Login';
import Layout from './components/layout/Layout';
import Overview from './pages/dashboard/Overview';
import CollectorDashboard from './pages/dashboard/CollectorDashboard';
import InvestigatorDashboard from './pages/dashboard/InvestigatorDashboard';
import GeneralSettings from './pages/settings/GeneralSettings';

import SecurityOverview from './pages/security/SecurityOverview';
import SystemLogs from './pages/security/SystemLogs';
import VerificationLogs from './pages/security/VerificationLogs';
import AccessControl from './pages/security/AccessControl';

import CitizenList from './pages/citizens/CitizenList';
import NewEnrollment from './pages/citizens/NewEnrollment';
import CitizenDetails from './pages/citizens/CitizenDetails';

import NationalIDs from './pages/ids/NationalIDs';
import Passports from './pages/ids/Passports';
import BirthCertificates from './pages/ids/BirthCertificates';

import SystemHealth from './pages/infrastructure/SystemHealth';
import NetworkTopology from './pages/infrastructure/NetworkTopology';
import DatabaseStatus from './pages/infrastructure/DatabaseStatus';

import SystemSettings from './pages/settings/SystemSettings';
import APIConfiguration from './pages/settings/APIConfiguration';

// Placeholder Component for New Pages
const PlaceholderPage = ({ title }) => (
    <div className="h-96 flex flex-col items-center justify-center border-2 border-dashed border-[var(--color-BORDER)] rounded-lg bg-[var(--color-bg-SURFACE)] animate-in fade-in">
        <h2 className="text-xl font-bold text-[var(--color-text-MAIN)] font-ocr">{title}</h2>
        <p className="text-[var(--color-text-MUTED)] mt-2">Under Construction</p>
    </div>
);

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    {/* Public Routes */}
                    <Route path="/login" element={<Login />} />

                    {/* Protected Routes */}
                    {/* Protected Routes with Role Checks */}
                    <Route element={<ProtectedRoute />}>
                        <Route path="/" element={<Layout />}>
                            {/* Role-Specific Dashboards */}
                            <Route index element={<Overview />} /> {/* Will redirect in component if needed or show restricted view */}
                            <Route path="collector" element={<CollectorDashboard />} />
                            <Route path="investigation" element={<InvestigatorDashboard />} />

                            {/* Full Access Routes (Guarded) */}
                            {/* In a real app, wrap these in <RoleGuard allowed={['ADMIN']} /> */}
                            {/* For now, Sidebar hiding provides UI security, but we should add logical checks if time permits */}
                            {/* Basic Route Structure */}
                            <Route index element={<Overview />} />
                            <Route path="collector" element={<CollectorDashboard />} />
                            <Route path="investigation" element={<InvestigatorDashboard />} />

                            {/* Citizen Registry */}
                            <Route path="citizens" element={<CitizenList />} />
                            <Route path="citizens/new" element={<NewEnrollment />} />
                            <Route path="citizens/:id" element={<CitizenDetails />} />
                            <Route path="citizens/biometrics" element={<PlaceholderPage title="Biometrics" />} />
                            <Route path="citizens/families" element={<PlaceholderPage title="Family Units" />} />

                            {/* Identity Management */}
                            <Route path="ids/national" element={<NationalIDs />} />
                            <Route path="ids/passports" element={<Passports />} />
                            <Route path="ids/birth-certs" element={<BirthCertificates />} />

                            {/* Security Suite */}
                            <Route path="security/overview" element={<SecurityOverview />} />
                            <Route path="security/verifications" element={<VerificationLogs />} />
                            <Route path="security/audit" element={<SystemLogs />} />
                            <Route path="security/access" element={<AccessControl />} />

                            {/* Infrastructure */}
                            <Route path="infrastructure/topology" element={<NetworkTopology />} />
                            <Route path="infrastructure/nodes" element={<SystemHealth />} />
                            <Route path="infrastructure/databases" element={<DatabaseStatus />} />

                            {/* System Routes */}
                            <Route path="settings/general" element={<SystemSettings />} />
                            <Route path="settings/api" element={<APIConfiguration />} />

                            {/* 404 */}
                            <Route path="*" element={<PlaceholderPage title="404 - Not Found" />} />
                        </Route>
                    </Route>
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;
