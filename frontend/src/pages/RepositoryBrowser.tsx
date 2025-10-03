/**
 * Repository Browser page
 * Layout with RepositoryTree, EntityCard, and forms
 */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { RepositoryTree } from "../components/Repository/RepositoryTree";
import { EntityCard } from "../components/Repository/EntityCard";
import { SuperdomainForm } from "../components/Repository/SuperdomainForm";
import { DomainForm } from "../components/Repository/DomainForm";
import { EntityForm } from "../components/Repository/EntityForm";
import { AttributeForm } from "../components/Repository/AttributeForm";
import type { Entity } from "../types/api";

type ActiveForm = "superdomain" | "domain" | "entity" | "attribute" | null;

export const RepositoryBrowser: React.FC = () => {
  const navigate = useNavigate();
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);
  const [activeForm, setActiveForm] = useState<ActiveForm>(null);

  const handleFormSuccess = () => {
    setActiveForm(null);
  };

  return (
    <div className="page repository-browser">
      <header className="page-header">
        <h1>Object Repository</h1>
        <div className="header-actions">
          <button className="btn-secondary" onClick={() => navigate("/")}>
            ← Dashboard
          </button>
          <button className="btn-secondary" onClick={() => navigate("/diagrams")}>
            Diagrams
          </button>
        </div>
      </header>

      <div className="repository-layout">
        {/* Left panel: Tree + Create buttons */}
        <aside className="repository-sidebar">
          <div className="sidebar-actions">
            <button className="btn-primary btn-block" onClick={() => setActiveForm("superdomain")}>
              + Superdomain
            </button>
            <button className="btn-secondary btn-block" onClick={() => setActiveForm("domain")}>
              + Domain
            </button>
            <button className="btn-secondary btn-block" onClick={() => setActiveForm("entity")}>
              + Entity
            </button>
            <button className="btn-secondary btn-block" onClick={() => setActiveForm("attribute")}>
              + Attribute
            </button>
          </div>

          <RepositoryTree onEntitySelect={setSelectedEntity} />
        </aside>

        {/* Main panel: Forms or EntityCard */}
        <main className="repository-main">
          {activeForm === "superdomain" && (
            <SuperdomainForm onSuccess={handleFormSuccess} onCancel={() => setActiveForm(null)} />
          )}

          {activeForm === "domain" && (
            <DomainForm onSuccess={handleFormSuccess} onCancel={() => setActiveForm(null)} />
          )}

          {activeForm === "entity" && (
            <EntityForm onSuccess={handleFormSuccess} onCancel={() => setActiveForm(null)} />
          )}

          {activeForm === "attribute" && selectedEntity && (
            <AttributeForm
              entityId={selectedEntity.id}
              onSuccess={handleFormSuccess}
              onCancel={() => setActiveForm(null)}
            />
          )}

          {!activeForm && selectedEntity && (
            <EntityCard
              entity={selectedEntity}
              onClose={() => setSelectedEntity(null)}
              onEdit={(entity) => {
                setSelectedEntity(entity);
                setActiveForm("entity");
              }}
            />
          )}

          {!activeForm && !selectedEntity && (
            <div className="empty-state-main">
              <h2>Welcome to the Object Repository</h2>
              <p>Select an entity from the tree or create new objects using the buttons on the left.</p>
              <div className="help-text">
                <h3>Getting Started:</h3>
                <ol>
                  <li>Create a <strong>Superdomain</strong> (e.g., "Business", "Technical")</li>
                  <li>Add <strong>Domains</strong> within your superdomain (e.g., "Sales", "Marketing")</li>
                  <li>Create <strong>Entities</strong> within domains (e.g., "Customer", "Order")</li>
                  <li>Define <strong>Attributes</strong> for each entity (e.g., "email: String", "created_at: DateTime")</li>
                </ol>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
