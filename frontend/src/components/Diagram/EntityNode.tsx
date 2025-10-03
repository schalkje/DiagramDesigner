/**
 * Custom React-Flow node for displaying Entity with attributes
 */
import React, { useEffect, useState } from "react";
import { Handle, Position, NodeProps } from "reactflow";
import { useRepositoryStore } from "../../store";
import type { Entity, Attribute } from "../../types/api";

export const EntityNode: React.FC<NodeProps> = ({ data }) => {
  const { entities, attributes, loadAttributes } = useRepositoryStore();
  const [entity, setEntity] = useState<Entity | null>(null);
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Find entity from all domains
  useEffect(() => {
    const allEntities = Object.values(entities).flat();
    const found = allEntities.find((e) => e.id === data.objectId);
    if (found) {
      setEntity(found);
      loadAttributes(found.id);
    }
  }, [data.objectId, entities, loadAttributes]);

  const entityAttributes = entity ? attributes[entity.id] || [] : [];

  if (!entity) {
    return (
      <div className="entity-node loading">
        <Handle type="target" position={Position.Top} />
        <div className="entity-node-header">Loading...</div>
        <Handle type="source" position={Position.Bottom} />
      </div>
    );
  }

  return (
    <div className="entity-node" style={data.style}>
      <Handle type="target" position={Position.Top} />

      <div className="entity-node-header" onClick={() => setIsCollapsed(!isCollapsed)}>
        <span className="entity-icon">📄</span>
        <span className="entity-name">{entity.name}</span>
        <button className="collapse-btn" type="button">
          {isCollapsed ? "▼" : "▲"}
        </button>
      </div>

      {!isCollapsed && (
        <div className="entity-node-body">
          {entityAttributes.length === 0 ? (
            <div className="no-attributes">No attributes</div>
          ) : (
            <ul className="attributes-list">
              {entityAttributes.map((attr) => (
                <li key={attr.id} className={attr.is_primary_key ? "primary-key" : ""}>
                  <span className="attr-icon">{attr.is_primary_key ? "🔑" : "•"}</span>
                  <span className="attr-name">{attr.name}</span>
                  <span className="attr-type">{attr.data_type}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};
