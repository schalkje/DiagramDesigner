/**
 * Form for creating/editing Entities
 */
import React, { useState, useEffect } from "react";
import { useRepositoryStore } from "../../store";
import type { Entity, Domain } from "../../types/api";

interface EntityFormProps {
  entity?: Entity; // If provided, edit mode
  domainId?: number; // For create mode - pre-select domain
  onSuccess?: (entity: Entity) => void;
  onCancel?: () => void;
}

export const EntityForm: React.FC<EntityFormProps> = ({ entity, domainId, onSuccess, onCancel }) => {
  const [name, setName] = useState(entity?.name || "");
  const [description, setDescription] = useState(entity?.description || "");
  const [selectedDomainId, setSelectedDomainId] = useState(entity?.domain_id || domainId || 0);

  const { domains, createEntity, updateEntity, isLoading, error } = useRepositoryStore();

  useEffect(() => {
    if (entity) {
      setName(entity.name);
      setDescription(entity.description || "");
      setSelectedDomainId(entity.domain_id);
    }
  }, [entity]);

  // Flatten domains from all superdomains
  const allDomains: Domain[] = Object.values(domains).flat();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedDomainId === 0) {
      alert("Please select a domain");
      return;
    }

    try {
      if (entity) {
        // Edit mode
        await updateEntity(entity.id, name, description);
        onSuccess?.(entity);
      } else {
        // Create mode
        const created = await createEntity({
          domain_id: selectedDomainId,
          name,
          description,
        });
        onSuccess?.(created);
        setName("");
        setDescription("");
      }
    } catch (err) {
      // Error handled by store
    }
  };

  return (
    <form className="entity-form" onSubmit={handleSubmit}>
      <h3>{entity ? "Edit Entity" : "Create Entity"}</h3>

      <div className="form-group">
        <label htmlFor="domain">Domain *</label>
        <select
          id="domain"
          value={selectedDomainId}
          onChange={(e) => setSelectedDomainId(Number(e.target.value))}
          required
          disabled={isLoading || !!entity} // Can't change parent in edit mode
        >
          <option value={0}>-- Select Domain --</option>
          {allDomains.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="name">Name *</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Customer, Order"
          required
          maxLength={100}
          disabled={isLoading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Optional description"
          rows={3}
          disabled={isLoading}
        />
      </div>

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}

      <div className="form-actions">
        <button type="submit" className="btn-primary" disabled={isLoading}>
          {isLoading ? "Saving..." : entity ? "Update" : "Create"}
        </button>
        {onCancel && (
          <button type="button" className="btn-secondary" onClick={onCancel} disabled={isLoading}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};
