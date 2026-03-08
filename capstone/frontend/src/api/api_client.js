import axios from "axios";

// Standardizing API client for the application
const apiClient = axios.create({
  // Use environment variable for base URL, fallback to localhost for development
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Response interceptor for centralized error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || "An unexpected error occurred.";
    console.error("API Error:", message);
    return Promise.reject(error);
  }
);

export default apiClient;
