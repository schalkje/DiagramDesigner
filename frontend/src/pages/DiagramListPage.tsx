/**
 * Diagram List page
 */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { DiagramList } from "../components/Diagram/DiagramList";
import { useDiagramStore } from "../store";
import type { Diagram } from "../types/api";

export const DiagramListPage: React.FC = () => {
  const navigate = useNavigate();
  const { createDiagram } = useDiagramStore();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newDiagramName, setNewDiagramName] = useState("");
  const [newDiagramDescription, setNewDiagramDescription] = useState("");
  const [newDiagramTags, setNewDiagramTags] = useState("");

  const handleDiagramSelect = (diagram: Diagram) => {
    navigate(`/diagrams/${diagram.id}`);
  };

  const handleCreateDiagram = async (e: React.FormEvent) => {
    e.preventDefault();

    const tags = newDiagramTags
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    try {
      const diagram = await createDiagram({
        name: newDiagramName,
        description: newDiagramDescription || undefined,
        tags: tags.length > 0 ? tags : undefined,
      });

      // Reset form
      setNewDiagramName("");
      setNewDiagramDescription("");
      setNewDiagramTags("");
      setShowCreateForm(false);

      // Navigate to new diagram
      navigate(`/diagrams/${diagram.id}`);
    } catch (err) {
      // Error handled by store
    }
  };

  return (
    <div className="page diagram-list-page">
      <header className="page-header">
        <h1>Diagrams</h1>
        <div className="header-actions">
          <button className="btn-secondary" onClick={() => navigate("/")}>
            ← Dashboard
          </button>
          <button className="btn-secondary" onClick={() => navigate("/repository")}>
            Repository
          </button>
        </div>
      </header>

      <div className="page-content">
        {showCreateForm ? (
          <div className="create-diagram-form-container">
            <form className="create-diagram-form" onSubmit={handleCreateDiagram}>
              <h2>Create New Diagram</h2>

              <div className="form-group">
                <label htmlFor="name">Diagram Name *</label>
                <input
                  id="name"
                  type="text"
                  value={newDiagramName}
                  onChange={(e) => setNewDiagramName(e.target.value)}
                  placeholder="e.g., Sales Domain Overview"
                  required
                  maxLength={200}
                />
              </div>

              <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea
                  id="description"
                  value={newDiagramDescription}
                  onChange={(e) => setNewDiagramDescription(e.target.value)}
                  placeholder="Optional description"
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label htmlFor="tags">Tags (comma-separated)</label>
                <input
                  id="tags"
                  type="text"
                  value={newDiagramTags}
                  onChange={(e) => setNewDiagramTags(e.target.value)}
                  placeholder="e.g., sales, customer, v1"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  Create Diagram
                </button>
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowCreateForm(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        ) : (
          <DiagramList
            onDiagramSelect={handleDiagramSelect}
            onDiagramCreate={() => setShowCreateForm(true)}
          />
        )}
      </div>
    </div>
  );
};
