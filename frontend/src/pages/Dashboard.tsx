/**
 * Dashboard landing page
 */
import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../store";

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="page dashboard">
      <header className="dashboard-header">
        <h1>DiagramDesigner</h1>
        <div className="user-menu">
          <span className="user-name">{user?.full_name || user?.username || user?.email}</span>
          <button className="btn-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="dashboard-content">
        <div className="welcome-section">
          <h2>Welcome back!</h2>
          <p>Create and manage data model diagrams with entity-relationship visualization.</p>
        </div>

        <div className="quick-actions">
          <div className="action-card" onClick={() => navigate("/repository")}>
            <div className="action-icon">📚</div>
            <h3>Object Repository</h3>
            <p>Manage your data model: Superdomains, Domains, Entities, and Attributes</p>
            <button className="btn-primary">Browse Repository</button>
          </div>

          <div className="action-card" onClick={() => navigate("/diagrams")}>
            <div className="action-icon">📊</div>
            <h3>Diagrams</h3>
            <p>Create and edit visual diagrams with entity relationships</p>
            <button className="btn-primary">View Diagrams</button>
          </div>
        </div>

        <div className="features-section">
          <h3>Features</h3>
          <ul className="features-list">
            <li>✓ Hierarchical data model organization (Superdomain → Domain → Entity → Attribute)</li>
            <li>✓ Interactive diagram canvas with drag & drop</li>
            <li>✓ Entity-Relationship diagrams with crow's foot notation</li>
            <li>✓ Reusable entities across multiple diagrams</li>
            <li>✓ Search and filter diagrams by tags</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
