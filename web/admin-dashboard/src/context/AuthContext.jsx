import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios'; // Direct axios for initial login
import ENDPOINTS from '../services/apiConfig';
// We don't use apiClient for login to avoid circular dep or interceptor issues on 401 login failures

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('accessToken'));
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('accessToken'));
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Initial Load: Check if token exists
    useEffect(() => {
        if (token) {
            setIsAuthenticated(true);
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                try {
                    setUser(JSON.parse(storedUser));
                } catch (e) {
                    console.error("Failed to parse user data", e);
                }
            }
        }
    }, [token]);

    const login = async (username, password) => {
        setLoading(true);
        setError(null);
        try {
            // Determine Login Type
            const isNationalId = /^\d+$/.test(username);

            let response;
            let role = 'CITIZEN'; // Default for citizen login
            let access, refresh, userData;

            if (isNationalId) {
                // Citizen Login (No password usually, using LoginSerializer which expects national_id only? 
                // Wait, LoginSerializer in backend expects national_id. Front end sends username/password? 
                // The citizen login usually doesn't have a password in this MVP or uses one?
                // Looking at LoginSerializer: it just takes national_id. 
                // We'll treat the "password" field as national_id if using the unified form, 
                // or assume the form input 'username' IS the national_id.

                // ADJUSTMENT: The current backend LoginView POSTs { "national_id": "..." }
                response = await axios.post(ENDPOINTS.AUTH.CITIZEN_LOGIN, {
                    national_id: username
                });

                // Response: { status, tokens, citizen, role } (I added role to tokenizer but maybe not top level response for Citizen? I should check views.py again. 
                // I added 'role' to token claims. I did NOT add 'role' to LoginView response top level in the REPLACE call for LoginSerializer??
                // I added `attrs['role']` to validated_data, but the View returns: ` 'citizen': serializer.validated_data['citizen_data']`.
                // It does NOT explicitly return `role` at top level in LoginView.
                // However, I added `token['role']`
                const data = response.data;
                access = data.tokens.access;
                refresh = data.tokens.refresh;
                userData = data.citizen;
                role = 'CITIZEN';

            } else {
                // Admin/Staff Login
                response = await axios.post(ENDPOINTS.AUTH.LOGIN, {
                    username,
                    password
                });

                const data = response.data;
                access = data.tokens.access;
                refresh = data.tokens.refresh;
                userData = data.user;
                role = data.role || 'ADMIN'; // Default fallback
            }

            // Store Tokens & User & Role
            localStorage.setItem('accessToken', access);
            localStorage.setItem('refreshToken', refresh);
            localStorage.setItem('user', JSON.stringify(userData));
            localStorage.setItem('role', role); // Persist Role for Sidebar Logic

            setToken(access);
            setUser(userData);
            setIsAuthenticated(true);

            // Allow caller to handle redirect
            return role; // RETURN ROLE
        } catch (err) {
            console.error("Login failed", err);
            setError(err.response?.data?.detail || err.response?.data?.error || 'Authentication failed. Please check credentials.');
            setIsAuthenticated(false);
            return false;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
        window.location.href = '/login';
    };

    return (
        <AuthContext.Provider value={{
            user,
            token,
            isAuthenticated,
            loading,
            error,
            login,
            logout
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
