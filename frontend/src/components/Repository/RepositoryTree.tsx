/**
 * Hierarchical tree view for Object Repository
 * Displays Superdomain → Domain → Entity structure
 */
import React, { useEffect, useState } from "react";
import { useRepositoryStore } from "../../store";
import type { Superdomain, Domain, Entity } from "../../types/api";

interface RepositoryTreeProps {
  onEntitySelect?: (entity: Entity) => void;
  onEntityDragStart?: (entity: Entity) => void;
}

export const RepositoryTree: React.FC<RepositoryTreeProps> = ({
  onEntitySelect,
  onEntityDragStart,
}) => {
  const {
    superdomains,
    domains,
    entities,
    loadSuperdomains,
    loadDomains,
    loadEntities,
    isLoading,
    error,
  } = useRepositoryStore();

  const [expandedSuperdomains, setExpandedSuperdomains] = useState<Set<number>>(new Set());
  const [expandedDomains, setExpandedDomains] = useState<Set<number>>(new Set());

  useEffect(() => {
    loadSuperdomains();
  }, [loadSuperdomains]);

  const toggleSuperdomain = async (superdomainId: number) => {
    const newExpanded = new Set(expandedSuperdomains);

    if (newExpanded.has(superdomainId)) {
      newExpanded.delete(superdomainId);
    } else {
      newExpanded.add(superdomainId);
      // Load domains for this superdomain if not already loaded
      if (!domains[superdomainId]) {
        await loadDomains(superdomainId);
      }
    }

    setExpandedSuperdomains(newExpanded);
  };

  const toggleDomain = async (domainId: number) => {
    const newExpanded = new Set(expandedDomains);

    if (newExpanded.has(domainId)) {
      newExpanded.delete(domainId);
    } else {
      newExpanded.add(domainId);
      // Load entities for this domain if not already loaded
      if (!entities[domainId]) {
        await loadEntities(domainId);
      }
    }

    setExpandedDomains(newExpanded);
  };

  const handleEntityDragStart = (e: React.DragEvent, entity: Entity) => {
    e.dataTransfer.effectAllowed = "copy";
    e.dataTransfer.setData("application/json", JSON.stringify(entity));
    e.dataTransfer.setData("entity-id", entity.id.toString());
    onEntityDragStart?.(entity);
  };

  if (isLoading && superdomains.length === 0) {
    return <div className="repository-tree loading">Loading repository...</div>;
  }

  if (error) {
    return <div className="repository-tree error">Error: {error}</div>;
  }

  return (
    <div className="repository-tree">
      <div className="tree-header">
        <h3>Object Repository</h3>
      </div>

      <div className="tree-content">
        {superdomains.length === 0 ? (
          <div className="empty-state">No superdomains yet. Create one to get started.</div>
        ) : (
          <ul className="tree-level superdomain-level">
            {superdomains.map((superdomain) => (
              <li key={superdomain.id} className="tree-node superdomain-node">
                <div className="tree-node-header">
                  <button
                    className="tree-toggle"
                    onClick={() => toggleSuperdomain(superdomain.id)}
                    aria-label={
                      expandedSuperdomains.has(superdomain.id) ? "Collapse" : "Expand"
                    }
                  >
                    {expandedSuperdomains.has(superdomain.id) ? "▼" : "▶"}
                  </button>
                  <span className="tree-node-label" title={superdomain.description || undefined}>
                    {superdomain.name}
                  </span>
                </div>

                {expandedSuperdomains.has(superdomain.id) && (
                  <ul className="tree-level domain-level">
                    {domains[superdomain.id]?.map((domain) => (
                      <li key={domain.id} className="tree-node domain-node">
                        <div className="tree-node-header">
                          <button
                            className="tree-toggle"
                            onClick={() => toggleDomain(domain.id)}
                            aria-label={expandedDomains.has(domain.id) ? "Collapse" : "Expand"}
                          >
                            {expandedDomains.has(domain.id) ? "▼" : "▶"}
                          </button>
                          <span className="tree-node-label" title={domain.description || undefined}>
                            {domain.name}
                          </span>
                        </div>

                        {expandedDomains.has(domain.id) && (
                          <ul className="tree-level entity-level">
                            {entities[domain.id]?.map((entity) => (
                              <li
                                key={entity.id}
                                className="tree-node entity-node"
                                draggable
                                onDragStart={(e) => handleEntityDragStart(e, entity)}
                              >
                                <div
                                  className="tree-node-header"
                                  onClick={() => onEntitySelect?.(entity)}
                                  role="button"
                                  tabIndex={0}
                                  onKeyPress={(e) => {
                                    if (e.key === "Enter") onEntitySelect?.(entity);
                                  }}
                                >
                                  <span className="tree-node-icon">📄</span>
                                  <span
                                    className="tree-node-label"
                                    title={entity.description || undefined}
                                  >
                                    {entity.name}
                                  </span>
                                </div>
                              </li>
                            ))}
                            {(!entities[domain.id] || entities[domain.id].length === 0) && (
                              <li className="empty-state">No entities</li>
                            )}
                          </ul>
                        )}
                      </li>
                    ))}
                    {(!domains[superdomain.id] || domains[superdomain.id].length === 0) && (
                      <li className="empty-state">No domains</li>
                    )}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
