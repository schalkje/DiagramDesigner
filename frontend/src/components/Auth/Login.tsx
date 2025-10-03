/**
 * Login component
 */
import React, { useState } from "react";
import { useAuthStore } from "../../store";

interface LoginProps {
  onSuccess?: () => void;
  onRegisterClick?: () => void;
}

export const Login: React.FC<LoginProps> = ({ onSuccess, onRegisterClick }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, isLoading, error, clearError } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    try {
      await login(email, password);
      onSuccess?.();
    } catch (err) {
      // Error is handled by store
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>DiagramDesigner</h1>
        <h2>Login</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@example.com"
              required
              autoComplete="email"
              disabled={isLoading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
              autoComplete="current-password"
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account?{" "}
            <button
              type="button"
              className="btn-link"
              onClick={onRegisterClick}
              disabled={isLoading}
            >
              Register
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};
