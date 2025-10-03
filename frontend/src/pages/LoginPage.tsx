/**
 * Login page
 */
import React from "react";
import { useNavigate } from "react-router-dom";
import { Login } from "../components/Auth/Login";

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSuccess = () => {
    navigate("/");
  };

  const handleRegisterClick = () => {
    navigate("/register");
  };

  return (
    <div className="page login-page">
      <Login onSuccess={handleSuccess} onRegisterClick={handleRegisterClick} />
    </div>
  );
};
