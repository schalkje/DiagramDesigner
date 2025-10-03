/**
 * Form for creating/editing Superdomains
 */
import React, { useState, useEffect } from "react";
import { useRepositoryStore } from "../../store";
import type { Superdomain } from "../../types/api";

interface SuperdomainFormProps {
  superdomain?: Superdomain; // If provided, edit mode
  onSuccess?: (superdomain: Superdomain) => void;
  onCancel?: () => void;
}

export const SuperdomainForm: React.FC<SuperdomainFormProps> = ({
  superdomain,
  onSuccess,
  onCancel,
}) => {
  const [name, setName] = useState(superdomain?.name || "");
  const [description, setDescription] = useState(superdomain?.description || "");
  const { createSuperdomain, updateSuperdomain, isLoading, error } = useRepositoryStore();

  useEffect(() => {
    if (superdomain) {
      setName(superdomain.name);
      setDescription(superdomain.description || "");
    }
  }, [superdomain]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (superdomain) {
        // Edit mode
        await updateSuperdomain(superdomain.id, name, description);
        onSuccess?.(superdomain);
      } else {
        // Create mode
        const created = await createSuperdomain({ name, description });
        onSuccess?.(created);
        setName("");
        setDescription("");
      }
    } catch (err) {
      // Error handled by store
    }
  };

  return (
    <form className="superdomain-form" onSubmit={handleSubmit}>
      <h3>{superdomain ? "Edit Superdomain" : "Create Superdomain"}</h3>

      <div className="form-group">
        <label htmlFor="name">Name *</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Business, Technical"
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
          {isLoading ? "Saving..." : superdomain ? "Update" : "Create"}
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
