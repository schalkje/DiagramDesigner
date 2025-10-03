/**
 * Register page
 */
import React from "react";
import { useNavigate } from "react-router-dom";
import { Register } from "../components/Auth/Register";

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSuccess = () => {
    navigate("/");
  };

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <div className="page register-page">
      <Register onSuccess={handleSuccess} onLoginClick={handleLoginClick} />
    </div>
  );
};
