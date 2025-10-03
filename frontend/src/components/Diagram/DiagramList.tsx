/**
 * Diagram list component with search/filter by tags
 */
import React, { useEffect, useState } from "react";
import { useDiagramStore } from "../../store";
import type { Diagram } from "../../types/api";

interface DiagramListProps {
  onDiagramSelect?: (diagram: Diagram) => void;
  onDiagramCreate?: () => void;
}

export const DiagramList: React.FC<DiagramListProps> = ({ onDiagramSelect, onDiagramCreate }) => {
  const { diagrams, loadDiagrams, deleteDiagram, isLoading, error } = useDiagramStore();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  useEffect(() => {
    loadDiagrams();
  }, [loadDiagrams]);

  // Extract all unique tags from diagrams
  const allTags = Array.from(
    new Set(diagrams.flatMap((d) => d.tags || []))
  ).sort();

  // Filter diagrams by search term and selected tag
  const filteredDiagrams = diagrams.filter((diagram) => {
    const matchesSearch =
      !searchTerm ||
      diagram.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      diagram.description?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesTag = !selectedTag || diagram.tags?.includes(selectedTag);

    return matchesSearch && matchesTag;
  });

  const handleDelete = async (diagramId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    if (window.confirm("Are you sure you want to delete this diagram?")) {
      try {
        await deleteDiagram(diagramId);
      } catch (err) {
        // Error handled by store
      }
    }
  };

  return (
    <div className="diagram-list">
      <div className="diagram-list-header">
        <h2>Diagrams</h2>
        {onDiagramCreate && (
          <button className="btn-primary" onClick={onDiagramCreate}>
            + New Diagram
          </button>
        )}
      </div>

      <div className="diagram-list-filters">
        <input
          type="search"
          placeholder="Search diagrams..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />

        {allTags.length > 0 && (
          <div className="tag-filter">
            <button
              className={`tag-btn ${!selectedTag ? "active" : ""}`}
              onClick={() => setSelectedTag(null)}
            >
              All
            </button>
            {allTags.map((tag) => (
              <button
                key={tag}
                className={`tag-btn ${selectedTag === tag ? "active" : ""}`}
                onClick={() => setSelectedTag(tag)}
              >
                {tag}
              </button>
            ))}
          </div>
        )}
      </div>

      {isLoading && diagrams.length === 0 ? (
        <div className="loading">Loading diagrams...</div>
      ) : error ? (
        <div className="error">Error: {error}</div>
      ) : filteredDiagrams.length === 0 ? (
        <div className="empty-state">
          {searchTerm || selectedTag
            ? "No diagrams match your filters"
            : "No diagrams yet. Create one to get started!"}
        </div>
      ) : (
        <div className="diagram-grid">
          {filteredDiagrams.map((diagram) => (
            <div
              key={diagram.id}
              className="diagram-card"
              onClick={() => onDiagramSelect?.(diagram)}
              role="button"
              tabIndex={0}
              onKeyPress={(e) => {
                if (e.key === "Enter") onDiagramSelect?.(diagram);
              }}
            >
              <div className="diagram-card-header">
                <h3>{diagram.name}</h3>
                <button
                  className="btn-icon-small"
                  onClick={(e) => handleDelete(diagram.id, e)}
                  title="Delete"
                >
                  🗑️
                </button>
              </div>

              {diagram.description && (
                <p className="diagram-description">{diagram.description}</p>
              )}

              {diagram.tags && diagram.tags.length > 0 && (
                <div className="diagram-tags">
                  {diagram.tags.map((tag) => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              <div className="diagram-card-footer">
                <span className="diagram-date">
                  Updated: {new Date(diagram.updated_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
