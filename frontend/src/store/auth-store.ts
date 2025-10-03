/**
 * Authentication store with Zustand
 */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AuthAPI } from "../services/auth-api";
import { getToken, removeToken } from "../services/api-client";
import type { User, ApiError } from "../types/api";

interface AuthState {
  // State
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
  initializeAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Login action
      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await AuthAPI.login(email, password);
          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (err) {
          const apiError = err as ApiError;
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: apiError.message || "Login failed",
          });
          throw err;
        }
      },

      // Register action
      register: async (email: string, username: string, password: string, fullName?: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await AuthAPI.register(email, username, password, fullName);
          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (err) {
          const apiError = err as ApiError;
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: apiError.message || "Registration failed",
          });
          throw err;
        }
      },

      // Logout action
      logout: () => {
        AuthAPI.logout();
        set({
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      // Clear error
      clearError: () => {
        set({ error: null });
      },

      // Initialize auth from stored token
      initializeAuth: () => {
        const token = getToken();
        if (!token) {
          set({ isAuthenticated: false, user: null });
          return;
        }

        // Token exists - user is considered authenticated
        // User data is restored from persisted state
        // If token is invalid, API will return 401 and middleware will remove it
        set({ isAuthenticated: true });
      },
    }),
    {
      name: "diagramdesigner-auth", // localStorage key
      partialize: (state) => ({
        // Only persist user data, not loading/error states
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
