/**
 * API Client base with Axios instance and JWT authentication
 */
import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from "axios";
import type { ApiError } from "../types/api";

// API base URL - can be overridden via environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api/v1";

// Local storage key for JWT token
const TOKEN_STORAGE_KEY = "diagramdesigner_token";

/**
 * Get JWT token from localStorage
 */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_STORAGE_KEY);
};

/**
 * Set JWT token in localStorage
 */
export const setToken = (token: string): void => {
  localStorage.setItem(TOKEN_STORAGE_KEY, token);
};

/**
 * Remove JWT token from localStorage
 */
export const removeToken = (): void => {
  localStorage.removeItem(TOKEN_STORAGE_KEY);
};

/**
 * Create Axios instance with base configuration
 */
const createApiClient = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000, // 10 second timeout
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Request interceptor - Add JWT token to Authorization header
  instance.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const token = getToken();
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor - Handle errors globally
  instance.interceptors.response.use(
    (response) => {
      return response;
    },
    (error: AxiosError<ApiError>) => {
      // Handle 401 Unauthorized - remove invalid token
      if (error.response?.status === 401) {
        removeToken();
        // Optionally redirect to login
        // window.location.href = '/login';
      }

      // Standardize error response
      const apiError: ApiError = {
        error: error.response?.data?.error || "Network Error",
        message: error.response?.data?.message || error.message || "An error occurred",
      };

      return Promise.reject(apiError);
    }
  );

  return instance;
};

/**
 * Global API client instance
 */
export const apiClient = createApiClient();

/**
 * Health check endpoint
 */
export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await axios.get(`${API_BASE_URL.replace("/api/v1", "")}/health`);
  return response.data;
};
