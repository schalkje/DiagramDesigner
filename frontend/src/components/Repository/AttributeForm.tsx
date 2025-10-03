/**
 * Form for creating/editing Attributes
 */
import React, { useState, useEffect } from "react";
import { useRepositoryStore } from "../../store";
import type { Attribute } from "../../types/api";

interface AttributeFormProps {
  attribute?: Attribute; // If provided, edit mode
  entityId?: number; // For create mode
  onSuccess?: (attribute: Attribute) => void;
  onCancel?: () => void;
}

const DATA_TYPES = [
  "String",
  "Integer",
  "Float",
  "Boolean",
  "Date",
  "DateTime",
  "UUID",
  "JSON",
  "Text",
  "Decimal",
];

export const AttributeForm: React.FC<AttributeFormProps> = ({
  attribute,
  entityId,
  onSuccess,
  onCancel,
}) => {
  const [name, setName] = useState(attribute?.name || "");
  const [dataType, setDataType] = useState(attribute?.data_type || "String");
  const [isNullable, setIsNullable] = useState(attribute?.is_nullable ?? true);
  const [isPrimaryKey, setIsPrimaryKey] = useState(attribute?.is_primary_key ?? false);
  const [defaultValue, setDefaultValue] = useState(attribute?.default_value || "");
  const [constraintsJson, setConstraintsJson] = useState(
    attribute?.constraints ? JSON.stringify(attribute.constraints, null, 2) : ""
  );

  const { createAttribute, updateAttribute, isLoading, error } = useRepositoryStore();

  useEffect(() => {
    if (attribute) {
      setName(attribute.name);
      setDataType(attribute.data_type);
      setIsNullable(attribute.is_nullable);
      setIsPrimaryKey(attribute.is_primary_key);
      setDefaultValue(attribute.default_value || "");
      setConstraintsJson(
        attribute.constraints ? JSON.stringify(attribute.constraints, null, 2) : ""
      );
    }
  }, [attribute]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!entityId && !attribute) {
      alert("Entity ID is required");
      return;
    }

    // Parse constraints JSON
    let constraints: Record<string, any> | undefined;
    if (constraintsJson.trim()) {
      try {
        constraints = JSON.parse(constraintsJson);
      } catch (err) {
        alert("Invalid JSON in constraints field");
        return;
      }
    }

    try {
      if (attribute) {
        // Edit mode
        await updateAttribute(attribute.id, {
          name,
          data_type: dataType,
          is_nullable: isNullable,
          is_primary_key: isPrimaryKey,
          default_value: defaultValue || undefined,
          constraints,
        });
        onSuccess?.(attribute);
      } else {
        // Create mode
        const created = await createAttribute({
          entity_id: entityId!,
          name,
          data_type: dataType,
          is_nullable: isNullable,
          is_primary_key: isPrimaryKey,
          default_value: defaultValue || undefined,
          constraints,
        });
        onSuccess?.(created);
        // Reset form
        setName("");
        setDataType("String");
        setIsNullable(true);
        setIsPrimaryKey(false);
        setDefaultValue("");
        setConstraintsJson("");
      }
    } catch (err) {
      // Error handled by store
    }
  };

  return (
    <form className="attribute-form" onSubmit={handleSubmit}>
      <h3>{attribute ? "Edit Attribute" : "Create Attribute"}</h3>

      <div className="form-group">
        <label htmlFor="name">Name *</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., email, created_at"
          required
          maxLength={100}
          disabled={isLoading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="dataType">Data Type *</label>
        <select
          id="dataType"
          value={dataType}
          onChange={(e) => setDataType(e.target.value)}
          required
          disabled={isLoading}
        >
          {DATA_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group-row">
        <div className="form-group-checkbox">
          <label>
            <input
              type="checkbox"
              checked={isNullable}
              onChange={(e) => setIsNullable(e.target.checked)}
              disabled={isLoading}
            />
            Nullable
          </label>
        </div>

        <div className="form-group-checkbox">
          <label>
            <input
              type="checkbox"
              checked={isPrimaryKey}
              onChange={(e) => setIsPrimaryKey(e.target.checked)}
              disabled={isLoading}
            />
            Primary Key
          </label>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="defaultValue">Default Value</label>
        <input
          id="defaultValue"
          type="text"
          value={defaultValue}
          onChange={(e) => setDefaultValue(e.target.value)}
          placeholder="e.g., NULL, NOW(), 0"
          disabled={isLoading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="constraints">Constraints (JSON)</label>
        <textarea
          id="constraints"
          value={constraintsJson}
          onChange={(e) => setConstraintsJson(e.target.value)}
          placeholder='e.g., {"min": 0, "max": 100}'
          rows={3}
          disabled={isLoading}
          className="code-input"
        />
        <small className="form-hint">Optional: JSON object with validation rules</small>
      </div>

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}

      <div className="form-actions">
        <button type="submit" className="btn-primary" disabled={isLoading}>
          {isLoading ? "Saving..." : attribute ? "Update" : "Create"}
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
