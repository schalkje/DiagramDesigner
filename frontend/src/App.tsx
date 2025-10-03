/**
 * Main App component with routing
 */
import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./store";

// Pages
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { Dashboard } from "./pages/Dashboard";
import { RepositoryBrowser } from "./pages/RepositoryBrowser";
import { DiagramListPage } from "./pages/DiagramListPage";
import { DiagramEditor } from "./pages/DiagramEditor";

// Protected Route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

function App() {
  const { initializeAuth } = useAuthStore();

  // Initialize auth on app mount
  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/repository"
          element={
            <ProtectedRoute>
              <RepositoryBrowser />
            </ProtectedRoute>
          }
        />
        <Route
          path="/diagrams"
          element={
            <ProtectedRoute>
              <DiagramListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/diagrams/:id"
          element={
            <ProtectedRoute>
              <DiagramEditor />
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
