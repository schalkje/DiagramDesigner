/**
 * Diagram API service
 */
import { apiClient } from "./api-client";
import type {
  Diagram,
  DiagramCreate,
  DiagramUpdate,
  DiagramObject,
  DiagramObjectCreate,
  DiagramObjectUpdate,
  PaginationParams,
  DeleteResponse,
} from "../types/api";

export class DiagramAPI {
  /**
   * List all diagrams with pagination
   */
  static async list(params?: PaginationParams): Promise<Diagram[]> {
    const response = await apiClient.get<Diagram[]>("/diagrams", { params });
    return response.data;
  }

  /**
   * Get diagram by ID with full details (includes objects and relationships)
   */
  static async get(id: number): Promise<Diagram> {
    const response = await apiClient.get<Diagram>(`/diagrams/${id}`);
    return response.data;
  }

  /**
   * Create new diagram
   */
  static async create(data: DiagramCreate): Promise<Diagram> {
    const response = await apiClient.post<Diagram>("/diagrams", data);
    return response.data;
  }

  /**
   * Update diagram metadata
   */
  static async update(id: number, data: DiagramUpdate): Promise<Diagram> {
    const response = await apiClient.put<Diagram>(`/diagrams/${id}`, data);
    return response.data;
  }

  /**
   * Delete diagram
   */
  static async delete(id: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(`/diagrams/${id}`);
    return response.data;
  }

  // Diagram Objects

  /**
   * Add object to diagram (Entity, Domain, or Superdomain)
   */
  static async addObject(diagramId: number, data: DiagramObjectCreate): Promise<DiagramObject> {
    const response = await apiClient.post<DiagramObject>(`/diagrams/${diagramId}/objects`, data);
    return response.data;
  }

  /**
   * Update diagram object position or visual style
   */
  static async updateObject(
    diagramId: number,
    objectId: number,
    data: DiagramObjectUpdate
  ): Promise<DiagramObject> {
    const response = await apiClient.put<DiagramObject>(
      `/diagrams/${diagramId}/objects/${objectId}`,
      data
    );
    return response.data;
  }

  /**
   * Remove object from diagram (doesn't delete from repository)
   */
  static async removeObject(diagramId: number, objectId: number): Promise<DeleteResponse> {
    const response = await apiClient.delete<DeleteResponse>(
      `/diagrams/${diagramId}/objects/${objectId}`
    );
    return response.data;
  }
}
