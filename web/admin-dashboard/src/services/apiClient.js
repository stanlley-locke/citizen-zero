import axios from 'axios';
import ENDPOINTS from './apiConfig';

// Create Axios Instance
const apiClient = axios.create({
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor: Attach Token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401 (Unauthorized)
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If 401 and not already retrying
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Attempt Refresh
                const refreshToken = localStorage.getItem('refreshToken');
                if (!refreshToken) throw new Error('No refresh token');

                const response = await axios.post(ENDPOINTS.AUTH.REFRESH, {
                    refresh: refreshToken
                });

                const { access } = response.data;
                localStorage.setItem('accessToken', access);

                // Retry original request with new token
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return apiClient(originalRequest);

            } catch (refreshError) {
                // Refresh failed - Logout
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
