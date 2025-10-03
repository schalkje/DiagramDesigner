/**
 * Entity detail card showing attributes
 */
import React, { useEffect, useState } from "react";
import { useRepositoryStore } from "../../store";
import type { Entity, Attribute } from "../../types/api";

interface EntityCardProps {
  entity: Entity;
  onClose?: () => void;
  onEdit?: (entity: Entity) => void;
}

export const EntityCard: React.FC<EntityCardProps> = ({ entity, onClose, onEdit }) => {
  const { attributes, loadAttributes, deleteAttribute, isLoading } = useRepositoryStore();
  const [editingAttributeId, setEditingAttributeId] = useState<number | null>(null);

  useEffect(() => {
    loadAttributes(entity.id);
  }, [entity.id, loadAttributes]);

  const handleDeleteAttribute = async (attributeId: number) => {
    if (window.confirm("Are you sure you want to delete this attribute?")) {
      try {
        await deleteAttribute(attributeId);
      } catch (err) {
        // Error handled by store
      }
    }
  };

  const entityAttributes = attributes[entity.id] || [];

  return (
    <div className="entity-card">
      <div className="entity-card-header">
        <div>
          <h3>{entity.name}</h3>
          {entity.description && <p className="entity-description">{entity.description}</p>}
        </div>
        <div className="entity-card-actions">
          {onEdit && (
            <button className="btn-icon" onClick={() => onEdit(entity)} title="Edit entity">
              ✏️
            </button>
          )}
          {onClose && (
            <button className="btn-icon" onClick={onClose} title="Close">
              ✕
            </button>
          )}
        </div>
      </div>

      <div className="entity-card-body">
        <div className="attributes-section">
          <div className="section-header">
            <h4>Attributes ({entityAttributes.length})</h4>
          </div>

          {isLoading && entityAttributes.length === 0 ? (
            <div className="loading">Loading attributes...</div>
          ) : entityAttributes.length === 0 ? (
            <div className="empty-state">No attributes yet. Add one to define this entity.</div>
          ) : (
            <table className="attributes-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Nullable</th>
                  <th>PK</th>
                  <th>Default</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {entityAttributes.map((attr) => (
                  <tr key={attr.id} className={attr.is_primary_key ? "primary-key" : ""}>
                    <td className="attr-name">{attr.name}</td>
                    <td className="attr-type">{attr.data_type}</td>
                    <td className="attr-nullable">{attr.is_nullable ? "✓" : ""}</td>
                    <td className="attr-pk">{attr.is_primary_key ? "🔑" : ""}</td>
                    <td className="attr-default">
                      {attr.default_value ? (
                        <code>{attr.default_value}</code>
                      ) : (
                        <span className="text-muted">-</span>
                      )}
                    </td>
                    <td className="attr-actions">
                      <button
                        className="btn-icon-small"
                        onClick={() => setEditingAttributeId(attr.id)}
                        title="Edit"
                      >
                        ✏️
                      </button>
                      <button
                        className="btn-icon-small"
                        onClick={() => handleDeleteAttribute(attr.id)}
                        title="Delete"
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <div className="entity-card-footer">
        <button className="btn-secondary">Add Attribute</button>
        <button className="btn-secondary">Add Relationship</button>
      </div>
    </div>
  );
};
