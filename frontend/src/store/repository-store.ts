/**
 * Repository store for Object Repository (Superdomain → Domain → Entity → Attribute)
 */
import { create } from "zustand";
import {
  SuperdomainAPI,
  DomainAPI,
  EntityAPI,
} from "../services/object-repository-api";
import { AttributeAPI, RelationshipAPI } from "../services/relationship-api";
import type {
  Superdomain,
  Domain,
  Entity,
  Attribute,
  Relationship,
  SuperdomainCreate,
  DomainCreate,
  EntityCreate,
  AttributeCreate,
  RelationshipCreate,
  ApiError,
} from "../types/api";

interface RepositoryState {
  // State - Hierarchical tree structure
  superdomains: Superdomain[];
  domains: Record<number, Domain[]>; // keyed by superdomain_id
  entities: Record<number, Entity[]>; // keyed by domain_id
  attributes: Record<number, Attribute[]>; // keyed by entity_id
  relationships: Relationship[];

  // UI State
  isLoading: boolean;
  error: string | null;

  // Actions - Superdomains
  loadSuperdomains: () => Promise<void>;
  createSuperdomain: (data: SuperdomainCreate) => Promise<Superdomain>;
  updateSuperdomain: (id: number, name?: string, description?: string) => Promise<void>;
  deleteSuperdomain: (id: number, confirm?: boolean) => Promise<void>;

  // Actions - Domains
  loadDomains: (superdomainId: number) => Promise<void>;
  createDomain: (data: DomainCreate) => Promise<Domain>;
  updateDomain: (id: number, name?: string, description?: string) => Promise<void>;
  deleteDomain: (id: number, confirm?: boolean) => Promise<void>;

  // Actions - Entities
  loadEntities: (domainId: number) => Promise<void>;
  createEntity: (data: EntityCreate) => Promise<Entity>;
  updateEntity: (id: number, name?: string, description?: string) => Promise<void>;
  deleteEntity: (id: number, confirm?: boolean) => Promise<void>;

  // Actions - Attributes
  loadAttributes: (entityId: number) => Promise<void>;
  createAttribute: (data: AttributeCreate) => Promise<Attribute>;
  updateAttribute: (id: number, data: Partial<AttributeCreate>) => Promise<void>;
  deleteAttribute: (id: number) => Promise<void>;

  // Actions - Relationships
  loadRelationships: () => Promise<void>;
  createRelationship: (data: RelationshipCreate) => Promise<Relationship>;
  deleteRelationship: (id: number) => Promise<void>;

  // Utility
  clearError: () => void;
}

export const useRepositoryStore = create<RepositoryState>((set, get) => ({
  // Initial state
  superdomains: [],
  domains: {},
  entities: {},
  attributes: {},
  relationships: [],
  isLoading: false,
  error: null,

  // Superdomains
  loadSuperdomains: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await SuperdomainAPI.list();
      set({ superdomains: response.superdomains, isLoading: false });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
    }
  },

  createSuperdomain: async (data: SuperdomainCreate) => {
    set({ isLoading: true, error: null });
    try {
      const superdomain = await SuperdomainAPI.create(data);
      set((state) => ({
        superdomains: [...state.superdomains, superdomain],
        isLoading: false,
      }));
      return superdomain;
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateSuperdomain: async (id: number, name?: string, description?: string) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await SuperdomainAPI.update(id, { name, description });
      set((state) => ({
        superdomains: state.superdomains.map((s) => (s.id === id ? updated : s)),
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  deleteSuperdomain: async (id: number, confirm = false) => {
    set({ isLoading: true, error: null });
    try {
      await SuperdomainAPI.delete(id, confirm);
      set((state) => ({
        superdomains: state.superdomains.filter((s) => s.id !== id),
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  // Domains
  loadDomains: async (superdomainId: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await DomainAPI.list(superdomainId);
      set((state) => ({
        domains: { ...state.domains, [superdomainId]: response.domains },
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
    }
  },

  createDomain: async (data: DomainCreate) => {
    set({ isLoading: true, error: null });
    try {
      const domain = await DomainAPI.create(data);
      set((state) => ({
        domains: {
          ...state.domains,
          [data.superdomain_id]: [...(state.domains[data.superdomain_id] || []), domain],
        },
        isLoading: false,
      }));
      return domain;
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateDomain: async (id: number, name?: string, description?: string) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await DomainAPI.update(id, { name, description });
      set((state) => {
        const newDomains = { ...state.domains };
        Object.keys(newDomains).forEach((key) => {
          newDomains[Number(key)] = newDomains[Number(key)].map((d) =>
            d.id === id ? updated : d
          );
        });
        return { domains: newDomains, isLoading: false };
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  deleteDomain: async (id: number, confirm = false) => {
    set({ isLoading: true, error: null });
    try {
      await DomainAPI.delete(id, confirm);
      set((state) => {
        const newDomains = { ...state.domains };
        Object.keys(newDomains).forEach((key) => {
          newDomains[Number(key)] = newDomains[Number(key)].filter((d) => d.id !== id);
        });
        return { domains: newDomains, isLoading: false };
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  // Entities
  loadEntities: async (domainId: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await EntityAPI.list(domainId);
      set((state) => ({
        entities: { ...state.entities, [domainId]: response.entities },
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
    }
  },

  createEntity: async (data: EntityCreate) => {
    set({ isLoading: true, error: null });
    try {
      const entity = await EntityAPI.create(data);
      set((state) => ({
        entities: {
          ...state.entities,
          [data.domain_id]: [...(state.entities[data.domain_id] || []), entity],
        },
        isLoading: false,
      }));
      return entity;
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateEntity: async (id: number, name?: string, description?: string) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await EntityAPI.update(id, { name, description });
      set((state) => {
        const newEntities = { ...state.entities };
        Object.keys(newEntities).forEach((key) => {
          newEntities[Number(key)] = newEntities[Number(key)].map((e) =>
            e.id === id ? updated : e
          );
        });
        return { entities: newEntities, isLoading: false };
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  deleteEntity: async (id: number, confirm = false) => {
    set({ isLoading: true, error: null });
    try {
      await EntityAPI.delete(id, confirm);
      set((state) => {
        const newEntities = { ...state.entities };
        Object.keys(newEntities).forEach((key) => {
          newEntities[Number(key)] = newEntities[Number(key)].filter((e) => e.id !== id);
        });
        return { entities: newEntities, isLoading: false };
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  // Attributes
  loadAttributes: async (entityId: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await AttributeAPI.list(entityId);
      set((state) => ({
        attributes: { ...state.attributes, [entityId]: response.attributes },
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
    }
  },

  createAttribute: async (data: AttributeCreate) => {
    set({ isLoading: true, error: null });
    try {
      const attribute = await AttributeAPI.create(data);
      set((state) => ({
        attributes: {
          ...state.attributes,
          [data.entity_id]: [...(state.attributes[data.entity_id] || []), attribute],
        },
        isLoading: false,
      }));
      return attribute;
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateAttribute: async (id: number, data: Partial<AttributeCreate>) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await AttributeAPI.update(id, data);
      set((state) => {
        const newAttributes = { ...state.attributes };
        Object.keys(newAttributes).forEach((key) => {
          newAttributes[Number(key)] = newAttributes[Number(key)].map((a) =>
            a.id === id ? updated : a
          );
        });
        return { attributes: newAttributes, isLoading: false };
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  deleteAttribute: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      await AttributeAPI.delete(id);
      set((state) => {
        const newAttributes = { ...state.attributes };
        Object.keys(newAttributes).forEach((key) => {
          newAttributes[Number(key)] = newAttributes[Number(key)].filter((a) => a.id !== id);
        });
        return { attributes: newAttributes, isLoading: false };
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  // Relationships
  loadRelationships: async () => {
    set({ isLoading: true, error: null });
    try {
      const relationships = await RelationshipAPI.list();
      set({ relationships, isLoading: false });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
    }
  },

  createRelationship: async (data: RelationshipCreate) => {
    set({ isLoading: true, error: null });
    try {
      const relationship = await RelationshipAPI.create(data);
      set((state) => ({
        relationships: [...state.relationships, relationship],
        isLoading: false,
      }));
      return relationship;
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  deleteRelationship: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      await RelationshipAPI.delete(id);
      set((state) => ({
        relationships: state.relationships.filter((r) => r.id !== id),
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  // Utility
  clearError: () => set({ error: null }),
}));
