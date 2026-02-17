/**
 * Centralized API Configuration
 * Manages all backend service endpoints and base URLs.
 */

// Base URLs for different services 
// We use relative paths for Auth to leverage the Vite Proxy (fixes CORS)
const SERVICES = {
    AUTH: '', // Relative path, proxied to port 8000
    ID: 'http://localhost:8001',
    VERIFY: 'http://localhost:8002',
    AUDIT: 'http://localhost:8003',
    IPRS: 'http://localhost:8005',
    MONITOR: 'http://localhost:8006',
};

export const ENDPOINTS = {
    // Authentication Service
    AUTH: {
        // Corrected: Admin Dashboard uses the Admin Login endpoint
        LOGIN: `${SERVICES.AUTH}/api/v1/auth/admin/login/`,      // POST: username, password
        CITIZEN_LOGIN: `${SERVICES.AUTH}/api/v1/auth/login/`,   // POST: national_id (for Citizen App)
        REFRESH: `${SERVICES.AUTH}/api/v1/auth/token/refresh/`, // POST: refresh
        ME: `${SERVICES.AUTH}/api/v1/auth/users/me/`,           // GET: User Profile
        ADMINS: `${SERVICES.AUTH}/api/v1/auth/admin/users/`,    // GET: List Admin Users
    },

    // Citizen Registry (IPRS Source of Truth)
    CITIZENS: {
        LIST: `${SERVICES.IPRS}/api/v1/citizens/`,           // GET: List all
        DETAIL: (id) => `${SERVICES.IPRS}/api/v1/citizens/${id}/`, // GET: Single
        CREATE: `${SERVICES.IPRS}/api/v1/citizens/`,         // POST: New Citizen
        SEARCH: `${SERVICES.IPRS}/api/v1/citizens/search/`,  // GET: ?q=query
    },

    // Biometrics (ID Service)
    BIOMETRICS: {
        ENROLL: `${SERVICES.ID}/api/biometrics/enroll/`, // POST: Biometric data
    },

    // ID Service Analytics
    ID: {
        ANALYTICS: `${SERVICES.ID}/api/v1/digital_ids/analytics/`, // GET: Dashboard KPI
    },

    // System Monitoring
    MONITOR: {
        STATS: `${SERVICES.MONITOR}/api/v1/monitor/stats/`, // GET: System Stats
        LOGS: `${SERVICES.MONITOR}/api/v1/monitor/logs/`,       // GET: Recent Logs
    },

    // Audit Logs
    AUDIT: {
        LIST: `${SERVICES.AUDIT}/api/v1/audit/logs/`,       // GET: All logs      
        ALERTS: `${SERVICES.AUDIT}/api/v1/audit/logs/alerts/`, // GET: Warnings/Critical
        ANALYTICS: `${SERVICES.AUDIT}/api/v1/audit/logs/analytics/`, // GET: Security KPI
        VERIFICATIONS: `${SERVICES.AUDIT}/api/v1/audit/logs/?action=VERIFY_ID` // GET: Filtered Logs
    }
};

export default ENDPOINTS;
