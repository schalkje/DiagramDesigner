/**
 * Object Repository API services (Superdomain, Domain, Entity)
 */
import { apiClient } from "./api-client";
import type {
  Superdomain,
  SuperdomainCreate,
  SuperdomainUpdate,
  SuperdomainListResponse,
  Domain,
  DomainCreate,
  DomainUpdate,
  DomainListResponse,
  Entity,
  EntityCreate,
  EntityUpdate,
  EntityListResponse,
  PaginationParams,
  DeleteResponse,
} from "../types/api";

// Superdomain API

export class SuperdomainAPI {
  /**
   * List all superdomains with pagination
   */
  static async list(params?: PaginationParams): Promise<SuperdomainListResponse> {
    const response = await apiClient.get<SuperdomainListResponse>("/superdomains", { params });
    return response.data;
  }

  /**
   * Get superdomain by ID
   */
  static async get(id: number): Promise<Superdomain> {
    const response = await apiClient.get<Superdomain>(`/superdomains/${id}`);
    return response.data;
  }

  /**
   * Create new superdomain
   */
  static async create(data: SuperdomainCreate): Promise<Superdomain> {
    const response = await apiClient.post<Superdomain>("/superdomains", data);
    return response.data;
  }

  /**
   * Update superdomain
   */
  static async update(id: number, data: SuperdomainUpdate): Promise<Superdomain> {
    const response = await apiClient.put<Superdomain>(`/superdomains/${id}`, data);
    return response.data;
  }

  /**
   * Delete superdomain (with optional cascade confirmation)
   */
  static async delete(id: number, confirm: boolean = false): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/superdomains/${id}`, {
      params: { confirm },
    });
    return response.data;
  }
}

// Domain API

export class DomainAPI {
  /**
   * List domains with optional superdomain filter
   */
  static async list(
    superdomainId?: number,
    params?: PaginationParams
  ): Promise<DomainListResponse> {
    const response = await apiClient.get<DomainListResponse>("/domains", {
      params: { superdomain_id: superdomainId, ...params },
    });
    return response.data;
  }

  /**
   * Get domain by ID
   */
  static async get(id: number): Promise<Domain> {
    const response = await apiClient.get<Domain>(`/domains/${id}`);
    return response.data;
  }

  /**
   * Create new domain
   */
  static async create(data: DomainCreate): Promise<Domain> {
    const response = await apiClient.post<Domain>("/domains", data);
    return response.data;
  }

  /**
   * Update domain
   */
  static async update(id: number, data: DomainUpdate): Promise<Domain> {
    const response = await apiClient.put<Domain>(`/domains/${id}`, data);
    return response.data;
  }

  /**
   * Delete domain (with optional cascade confirmation)
   */
  static async delete(id: number, confirm: boolean = false): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/domains/${id}`, {
      params: { confirm },
    });
    return response.data;
  }
}

// Entity API

export class EntityAPI {
  /**
   * List entities with optional domain filter
   */
  static async list(domainId?: number, params?: PaginationParams): Promise<EntityListResponse> {
    const response = await apiClient.get<EntityListResponse>("/entities", {
      params: { domain_id: domainId, ...params },
    });
    return response.data;
  }

  /**
   * Get entity by ID
   */
  static async get(id: number): Promise<Entity> {
    const response = await apiClient.get<Entity>(`/entities/${id}`);
    return response.data;
  }

  /**
   * Create new entity
   */
  static async create(data: EntityCreate): Promise<Entity> {
    const response = await apiClient.post<Entity>("/entities", data);
    return response.data;
  }

  /**
   * Update entity
   */
  static async update(id: number, data: EntityUpdate): Promise<Entity> {
    const response = await apiClient.put<Entity>(`/entities/${id}`, data);
    return response.data;
  }

  /**
   * Delete entity (with optional cascade confirmation)
   */
  static async delete(id: number, confirm: boolean = false): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/entities/${id}`, {
      params: { confirm },
    });
    return response.data;
  }
}
