/**
 * Diagram Editor page
 * Layout with DiagramCanvas and object repository panel
 */
import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { DiagramCanvas } from "../components/Diagram/DiagramCanvas";
import { RepositoryTree } from "../components/Repository/RepositoryTree";
import { useDiagramStore } from "../store";
import type { Entity } from "../types/api";

export const DiagramEditor: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const diagramId = parseInt(id || "0");

  const { activeDiagram, canvasSettings, setGridEnabled, setSnapToGrid } = useDiagramStore();
  const [isPanelOpen, setIsPanelOpen] = useState(true);

  const handleEntityDragStart = (entity: Entity) => {
    // Entity drag is handled by RepositoryTree and DiagramCanvas
    console.log("Dragging entity:", entity.name);
  };

  if (!diagramId || isNaN(diagramId)) {
    return (
      <div className="page diagram-editor error">
        <p>Invalid diagram ID</p>
        <button className="btn-primary" onClick={() => navigate("/diagrams")}>
          Back to Diagrams
        </button>
      </div>
    );
  }

  return (
    <div className="page diagram-editor">
      <header className="diagram-editor-header">
        <div className="header-left">
          <button className="btn-icon" onClick={() => navigate("/diagrams")} title="Back to diagrams">
            ←
          </button>
          <h1>{activeDiagram?.name || "Loading..."}</h1>
        </div>

        <div className="header-center">
          <div className="toolbar">
            <label className="toolbar-item">
              <input
                type="checkbox"
                checked={canvasSettings.gridEnabled}
                onChange={(e) => setGridEnabled(e.target.checked)}
              />
              Grid
            </label>
            <label className="toolbar-item">
              <input
                type="checkbox"
                checked={canvasSettings.snapToGrid}
                onChange={(e) => setSnapToGrid(e.target.checked)}
              />
              Snap to Grid
            </label>
          </div>
        </div>

        <div className="header-right">
          <button
            className="btn-secondary"
            onClick={() => setIsPanelOpen(!isPanelOpen)}
            title={isPanelOpen ? "Hide panel" : "Show panel"}
          >
            {isPanelOpen ? "Hide Objects" : "Show Objects"}
          </button>
          <button className="btn-secondary" onClick={() => navigate("/")}>
            Dashboard
          </button>
        </div>
      </header>

      <div className="diagram-editor-layout">
        {/* Object repository panel */}
        {isPanelOpen && (
          <aside className="diagram-sidebar">
            <div className="sidebar-header">
              <h3>Object Repository</h3>
              <p className="help-text">Drag entities onto the canvas</p>
            </div>
            <RepositoryTree onEntityDragStart={handleEntityDragStart} />
          </aside>
        )}

        {/* Canvas */}
        <main className="diagram-canvas-container">
          <DiagramCanvas diagramId={diagramId} />
        </main>
      </div>
    </div>
  );
};
