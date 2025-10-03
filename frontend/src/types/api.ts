/**
 * TypeScript types generated from backend API schemas
 * Matches Pydantic schemas and OpenAPI specification
 */

// Enums

export enum AuthProvider {
  LOCAL = "LOCAL",
  AZURE_AD = "AZURE_AD",
}

export enum Cardinality {
  ZERO_ONE = "ZERO_ONE", // 0..1
  ONE = "ONE", // 1..1
  ZERO_MANY = "ZERO_MANY", // 0..N
  ONE_MANY = "ONE_MANY", // 1..N
}

export enum ObjectType {
  SUPERDOMAIN = "SUPERDOMAIN",
  DOMAIN = "DOMAIN",
  ENTITY = "ENTITY",
}

// Base Types

export interface Timestamps {
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
}

// User & Authentication Types

export interface User extends Timestamps {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  auth_provider: AuthProvider;
  is_active: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface RegisterResponse {
  token: string;
  user: User;
}

// Object Repository Types

export interface Superdomain extends Timestamps {
  id: number;
  name: string;
  description?: string;
}

export interface SuperdomainCreate {
  name: string;
  description?: string;
}

export interface SuperdomainUpdate {
  name?: string;
  description?: string;
}

export interface SuperdomainListResponse {
  superdomains: Superdomain[];
  total: number;
}

export interface Domain extends Timestamps {
  id: number;
  superdomain_id: number;
  name: string;
  description?: string;
}

export interface DomainCreate {
  superdomain_id: number;
  name: string;
  description?: string;
}

export interface DomainUpdate {
  name?: string;
  description?: string;
}

export interface DomainListResponse {
  domains: Domain[];
  total: number;
}

export interface Entity extends Timestamps {
  id: number;
  domain_id: number;
  name: string;
  description?: string;
}

export interface EntityCreate {
  domain_id: number;
  name: string;
  description?: string;
}

export interface EntityUpdate {
  name?: string;
  description?: string;
}

export interface EntityListResponse {
  entities: Entity[];
  total: number;
}

export interface Attribute extends Timestamps {
  id: number;
  entity_id: number;
  name: string;
  data_type: string; // String, Integer, Float, Boolean, Date, DateTime, UUID, JSON
  is_nullable: boolean;
  is_primary_key: boolean;
  default_value?: string;
  constraints?: Record<string, any>; // JSONB constraints
}

export interface AttributeCreate {
  entity_id: number;
  name: string;
  data_type: string;
  is_nullable?: boolean;
  is_primary_key?: boolean;
  default_value?: string;
  constraints?: Record<string, any>;
}

export interface AttributeUpdate {
  name?: string;
  data_type?: string;
  is_nullable?: boolean;
  is_primary_key?: boolean;
  default_value?: string;
  constraints?: Record<string, any>;
}

export interface AttributeListResponse {
  attributes: Attribute[];
  total: number;
}

// Relationship Types

export interface Relationship extends Timestamps {
  id: number;
  source_entity_id: number;
  target_entity_id: number;
  source_role: string;
  target_role: string;
  source_cardinality: Cardinality;
  target_cardinality: Cardinality;
  description?: string;
}

export interface RelationshipCreate {
  source_entity_id: number;
  target_entity_id: number;
  source_role: string;
  target_role: string;
  source_cardinality: Cardinality;
  target_cardinality: Cardinality;
  description?: string;
}

// Diagram Repository Types

export interface Diagram extends Timestamps {
  id: number;
  user_id: number;
  name: string;
  description?: string;
  tags?: string[];
  canvas_settings?: Record<string, any>; // JSONB canvas settings (zoom, pan, grid, etc.)
}

export interface DiagramCreate {
  name: string;
  description?: string;
  tags?: string[];
  canvas_settings?: Record<string, any>;
}

export interface DiagramUpdate {
  name?: string;
  description?: string;
  tags?: string[];
  canvas_settings?: Record<string, any>;
}

export interface DiagramObject extends Timestamps {
  id: number;
  diagram_id: number;
  object_type: ObjectType;
  object_id: number; // References ID in object repository
  position_x: number;
  position_y: number;
  visual_style?: Record<string, any>; // JSONB visual overrides
}

export interface DiagramObjectCreate {
  object_type: ObjectType;
  object_id: number;
  position_x: number;
  position_y: number;
  visual_style?: Record<string, any>;
}

export interface DiagramObjectUpdate {
  position_x?: number;
  position_y?: number;
  visual_style?: Record<string, any>;
}

export interface DiagramRelationship extends Timestamps {
  id: number;
  diagram_id: number;
  relationship_id: number;
  is_visible: boolean;
  path_points?: Record<string, any>; // JSONB routing points
  visual_style?: Record<string, any>; // JSONB visual overrides
}

// API Response Types

export interface ApiError {
  error: string;
  message: string;
}

export interface PaginationParams {
  skip?: number;
  limit?: number;
}

export interface DeleteResponse {
  message: string;
  impact?: {
    affected_domains?: string[];
    affected_entities?: string[];
    cascade: boolean;
  };
}
