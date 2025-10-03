/**
 * Attribute and Relationship API services
 */
import { apiClient } from "./api-client";
import type {
  Attribute,
  AttributeCreate,
  AttributeUpdate,
  AttributeListResponse,
  Relationship,
  RelationshipCreate,
  PaginationParams,
  DeleteResponse,
} from "../types/api";

// Attribute API

export class AttributeAPI {
  /**
   * List attributes with optional entity filter
   */
  static async list(entityId?: number, params?: PaginationParams): Promise<AttributeListResponse> {
    const response = await apiClient.get<AttributeListResponse>("/attributes", {
      params: { entity_id: entityId, ...params },
    });
    return response.data;
  }

  /**
   * Get attribute by ID
   */
  static async get(id: number): Promise<Attribute> {
    const response = await apiClient.get<Attribute>(`/attributes/${id}`);
    return response.data;
  }

  /**
   * Create new attribute
   */
  static async create(data: AttributeCreate): Promise<Attribute> {
    const response = await apiClient.post<Attribute>("/attributes", data);
    return response.data;
  }

  /**
   * Update attribute
   */
  static async update(id: number, data: AttributeUpdate): Promise<Attribute> {
    const response = await apiClient.put<Attribute>(`/attributes/${id}`, data);
    return response.data;
  }

  /**
   * Delete attribute
   */
  static async delete(id: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/attributes/${id}`);
    return response.data;
  }
}

// Relationship API

export class RelationshipAPI {
  /**
   * List relationships with optional entity filter
   */
  static async list(entityId?: number): Promise<Relationship[]> {
    const response = await apiClient.get<Relationship[]>("/relationships", {
      params: { entity_id: entityId },
    });
    return response.data;
  }

  /**
   * Get relationship by ID
   */
  static async get(id: number): Promise<Relationship> {
    const response = await apiClient.get<Relationship>(`/relationships/${id}`);
    return response.data;
  }

  /**
   * Create new relationship between entities
   */
  static async create(data: RelationshipCreate): Promise<Relationship> {
    const response = await apiClient.post<Relationship>("/relationships", data);
    return response.data;
  }

  /**
   * Delete relationship
   */
  static async delete(id: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/relationships/${id}`);
    return response.data;
  }
}
