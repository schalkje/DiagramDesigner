/**
 * Form for creating/editing Domains
 */
import React, { useState, useEffect } from "react";
import { useRepositoryStore } from "../../store";
import type { Domain, Superdomain } from "../../types/api";

interface DomainFormProps {
  domain?: Domain; // If provided, edit mode
  superdomainId?: number; // For create mode - pre-select superdomain
  onSuccess?: (domain: Domain) => void;
  onCancel?: () => void;
}

export const DomainForm: React.FC<DomainFormProps> = ({
  domain,
  superdomainId,
  onSuccess,
  onCancel,
}) => {
  const [name, setName] = useState(domain?.name || "");
  const [description, setDescription] = useState(domain?.description || "");
  const [selectedSuperdomainId, setSelectedSuperdomainId] = useState(
    domain?.superdomain_id || superdomainId || 0
  );

  const { superdomains, createDomain, updateDomain, loadSuperdomains, isLoading, error } =
    useRepositoryStore();

  useEffect(() => {
    if (superdomains.length === 0) {
      loadSuperdomains();
    }
  }, [superdomains.length, loadSuperdomains]);

  useEffect(() => {
    if (domain) {
      setName(domain.name);
      setDescription(domain.description || "");
      setSelectedSuperdomainId(domain.superdomain_id);
    }
  }, [domain]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedSuperdomainId === 0) {
      alert("Please select a superdomain");
      return;
    }

    try {
      if (domain) {
        // Edit mode
        await updateDomain(domain.id, name, description);
        onSuccess?.(domain);
      } else {
        // Create mode
        const created = await createDomain({
          superdomain_id: selectedSuperdomainId,
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
    <form className="domain-form" onSubmit={handleSubmit}>
      <h3>{domain ? "Edit Domain" : "Create Domain"}</h3>

      <div className="form-group">
        <label htmlFor="superdomain">Superdomain *</label>
        <select
          id="superdomain"
          value={selectedSuperdomainId}
          onChange={(e) => setSelectedSuperdomainId(Number(e.target.value))}
          required
          disabled={isLoading || !!domain} // Can't change parent in edit mode
        >
          <option value={0}>-- Select Superdomain --</option>
          {superdomains.map((sd) => (
            <option key={sd.id} value={sd.id}>
              {sd.name}
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
          placeholder="e.g., Sales, Marketing"
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
          {isLoading ? "Saving..." : domain ? "Update" : "Create"}
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
