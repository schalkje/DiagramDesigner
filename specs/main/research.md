# Research & Technical Decisions

**Feature**: DiagramDesigner Application
**Date**: 2025-10-03
**Status**: Complete

## Overview
This document captures technical research and architectural decisions for the DiagramDesigner application - a three-tier web application for creating and managing data model diagrams with support for local development and Azure cloud deployment.

## Technology Stack Decisions

### Primary Keys: Integer vs UUID

**Decision**: Use auto-incrementing integers for primary keys instead of UUIDs

**Rationale**:
- **Simplicity**: Integers are human-readable for debugging and support (e.g., "Entity #42" vs "a7b3c4d5-...")
- **Performance**: At target scale (2000 entities, 100K attributes), integer indexes are more efficient
  - 4 bytes (INT) vs 16 bytes (UUID) = 75% storage savings per key
  - Better index locality reduces B-tree fragmentation
  - Faster joins due to smaller key size
- **Single database instance**: Application uses one PostgreSQL/Azure SQL instance, no distributed writes requiring UUID collision prevention
- **No client-side generation needed**: Backend generates IDs, no optimistic UI updates requiring pre-generated IDs
- **Security not critical**: API uses authentication; predictable IDs acceptable for internal diagram tool (not public-facing SaaS)
- **Developer experience**: Stack traces, logs, and SQL queries more readable with small integers

**Alternatives Considered**:
- **UUIDs (UUIDv4 random)**:
  - Pros: Distributed-system friendly, non-enumerable, client-side generation
  - Cons: 4x storage overhead, random index fragmentation, poor human readability
  - Decision: Overkill for 20-user local/cloud application

- **UUIDs (UUIDv7 time-ordered)**:
  - Pros: Time-sortable, better index locality than UUIDv4
  - Cons: Still 16 bytes, adds complexity, solves problems we don't have
  - Decision: Not needed for current scale

- **Hybrid (UUID external, INT internal)**:
  - Pros: Best of both worlds (secure external IDs + fast internal joins)
  - Cons: Significant added complexity, two ID columns everywhere
  - Decision: Too complex for current needs

**Implementation Details**:
- **User, Superdomain, Domain, Entity, Diagram, Relationship, DiagramObject, DiagramRelationship**: INTEGER (auto-increment)
- **Attribute**: BIGINT (auto-increment) - supports 100,000+ attributes requirement
- **Database**: PostgreSQL SERIAL/BIGSERIAL (local), Azure SQL IDENTITY (production)
- **API**: All endpoints use integer IDs in paths and request/response bodies

**Trade-offs Accepted**:
- **No distributed writes**: If we later add multi-region writes or offline sync, would need UUID migration
- **ID enumeration**: Users can guess entity IDs (e.g., `/entities/1`, `/entities/2`), acceptable for authenticated internal tool
- **Sequential ordering**: IDs reveal creation order, acceptable for this use case

**Future Consideration**: If application evolves to require distributed ID generation (e.g., offline-first PWA, multi-region), can migrate to UUIDs via:
1. Add UUID column to all tables
2. Generate UUIDs for existing rows
3. Update foreign keys to reference UUIDs
4. Update API to use UUIDs
5. Drop integer columns

For current requirements (local development → Azure single-region deployment, 20 users), integers are the pragmatic choice.

### Frontend Framework: React with TypeScript

**Decision**: Use React 18+ with TypeScript 5.x for the frontend

**Rationale**:
- **React**: Mature ecosystem with excellent canvas/SVG rendering libraries (React-Konva, React-Flow, Fabric.js)
- **TypeScript**: Type safety crucial for complex data model operations and API contracts
- **Performance**: Virtual DOM and hooks enable efficient re-rendering for interactive canvas
- **Component architecture**: Aligns with constitutional requirement for modular design
- **Azure integration**: Azure Static Web Apps has first-class React support

**Alternatives Considered**:
- **Vue.js**: Simpler learning curve but smaller ecosystem for canvas libraries
- **Angular**: More opinionated framework, heavier bundle size, overkill for this use case
- **Svelte**: Excellent performance but smaller community and fewer canvas libraries

**Libraries & Tools**:
- **React-Flow** or **React-Konva**: For canvas-based diagram rendering with built-in zoom/pan
- **Zustand** or **React Context**: Lightweight state management for diagram state
- **Axios**: HTTP client for backend API communication
- **Vite**: Fast build tool with HMR for development
- **Vitest**: Testing framework compatible with Vite

### Backend Framework: Flask with Python

**Decision**: Use Flask 3.x with Python 3.12+ for the backend API

**Rationale**:
- **Simplicity**: Flask is lightweight and doesn't impose unnecessary complexity
- **Flexibility**: Can structure as needed for repository pattern and service layer
- **ORM Integration**: Excellent SQLAlchemy support for complex data models
- **Azure Support**: Runs well on Azure Container Apps and App Service
- **Testing**: pytest ecosystem is mature and comprehensive
- **Python 3.12**: Latest stable version with performance improvements and type hints

**Alternatives Considered**:
- **FastAPI**: Modern and fast, but async overhead unnecessary for this workload
- **Django**: Too opinionated and heavy, includes features (admin, forms) we don't need
- **.NET Core**: Excellent Azure integration but adds language fragmentation (C# vs TypeScript)
- **Node.js/Express**: Would unify frontend/backend language but Python ORM ecosystem is superior

**Libraries & Tools**:
- **Flask-CORS**: Handle cross-origin requests from frontend
- **Flask-RESTful**: REST API helpers and request parsing
- **SQLAlchemy 2.x**: Modern ORM with type hints and async support
- **Alembic**: Database migration management
- **Pydantic**: Request/response validation and OpenAPI schema generation
- **pytest + pytest-cov**: Testing and coverage

### Database: PostgreSQL (Local) / Azure SQL (Production)

**Decision**: PostgreSQL 15+ for local development, Azure SQL Database for production

**Rationale**:
- **PostgreSQL Local**:
  - Free and open-source for local development
  - Rich feature set (JSONB, CTEs, window functions)
  - Excellent SQLAlchemy support
  - Docker image readily available
  - ACID compliant for data integrity

- **Azure SQL Production**:
  - Managed service with automatic backups
  - Built-in monitoring and performance insights
  - Familiar SQL Server syntax
  - Elastic pools for cost optimization
  - High availability and disaster recovery built-in

**Portability Strategy**:
- Use SQLAlchemy ORM to abstract database-specific syntax
- Write migrations compatible with both PostgreSQL and SQL Server
- Use standard SQL features where possible
- Test migrations on both databases

**Alternatives Considered**:
- **SQLite**: Too limited for production scale (100k attributes)
- **Azure Cosmos DB**: Overkill for relational data model, more expensive
- **MySQL/MariaDB**: Less feature-rich than PostgreSQL for complex queries
- **PostgreSQL on Azure**: Considered but Azure SQL offers better monitoring integration

### State Management: Zustand

**Decision**: Use Zustand for frontend state management

**Rationale**:
- **Simplicity**: Minimal boilerplate compared to Redux
- **Performance**: Small bundle size (~1KB), fast re-renders
- **TypeScript**: Excellent type inference out of the box
- **Devtools**: Browser extension for debugging
- **No Context**: Avoids React Context performance pitfalls for frequent updates

**Alternatives Considered**:
- **React Context**: Built-in but re-render issues with large diagram state
- **Redux Toolkit**: Powerful but adds complexity and boilerplate
- **Jotai/Recoil**: Atomic approach may overcomplicate for this use case

### Canvas Rendering: React-Flow

**Decision**: Use React-Flow for diagram canvas implementation

**Rationale**:
- **Built for diagrams**: Specifically designed for node-edge diagrams
- **Performance**: Handles 1000+ elements efficiently
- **Features**: Built-in zoom, pan, drag-drop, minimap, controls
- **Customization**: Full control over node and edge rendering
- **TypeScript**: First-class TypeScript support
- **Hooks API**: Integrates naturally with React patterns

**Alternatives Considered**:
- **React-Konva**: More general canvas library, requires building diagram features from scratch
- **D3.js**: Powerful but imperative API conflicts with React's declarative model
- **Fabric.js**: Canvas manipulation library, not optimized for node-edge diagrams
- **Custom Canvas**: Would require significant effort to match React-Flow's features

## Architecture Patterns

### Repository Pattern

**Decision**: Implement repository pattern for data access layer

**Rationale**:
- **Separation of Concerns**: Isolates data access logic from business logic
- **Testability**: Easy to mock repositories for service layer tests
- **Consistency**: Single place to enforce query patterns and data access rules
- **Flexibility**: Can swap database implementations without changing service layer

**Implementation**:
```
backend/src/repositories/
├── base_repository.py        # Abstract base with common CRUD
├── entity_repository.py      # Entity-specific queries
├── diagram_repository.py     # Diagram-specific queries
└── relationship_repository.py
```

### Service Layer Pattern

**Decision**: Implement service layer for business logic

**Rationale**:
- **Business Logic**: Centralized location for validation, authorization, and workflow
- **Transaction Management**: Services manage transaction boundaries
- **API Independence**: Services can be used by API, CLI, or tests
- **Single Responsibility**: API layer handles HTTP, service layer handles domain logic

**Implementation**:
```
backend/src/services/
├── entity_service.py         # Entity CRUD + validation
├── diagram_service.py        # Diagram operations + sync logic
└── relationship_service.py   # Relationship management
```

### API-First Design with OpenAPI

**Decision**: Define API contracts first using OpenAPI 3.0 specification

**Rationale**:
- **Contract-Driven**: Frontend and backend teams can work in parallel
- **Documentation**: Auto-generated API docs with Swagger UI
- **Validation**: Request/response validation from schema
- **Testing**: Contract tests ensure API matches specification
- **Code Generation**: Can generate TypeScript types from OpenAPI schema

**Tools**:
- **Pydantic**: Generate OpenAPI schema from Python models
- **Swagger UI**: Interactive API documentation
- **openapi-typescript**: Generate TypeScript types from OpenAPI

## Local Development Setup

### Docker Compose Strategy

**Decision**: Use Docker Compose for local development environment

**Rationale**:
- **Consistency**: Same environment across all developers
- **Simplicity**: Single `docker-compose up` starts all services
- **Isolation**: Database runs in container, no local install needed
- **Hot Reload**: Volume mounts enable live code updates

**Services**:
```yaml
services:
  db:
    image: postgres:15
    ports: ["5432:5432"]

  backend:
    build: ./backend
    ports: ["5000:5000"]
    volumes: ["./backend:/app"]
    depends_on: [db]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    volumes: ["./frontend:/app"]
```

**Alternatives Considered**:
- **Local installs**: More fragile, version conflicts, onboarding friction
- **Full Kubernetes**: Overkill for local development
- **Manual startup**: Error-prone, inconsistent

## Azure Deployment Architecture

### Infrastructure-as-Code: Azure Bicep

**Decision**: Use Azure Bicep for infrastructure provisioning

**Rationale**:
- **Azure Native**: First-class support, better than ARM templates
- **Readability**: More concise than JSON ARM templates
- **Type Safety**: Validation at authoring time
- **Modularity**: Can compose reusable modules
- **Azure Integration**: Direct integration with Azure Portal and CLI

**Alternatives Considered**:
- **Terraform**: Multi-cloud but adds complexity for Azure-only deployment
- **ARM Templates**: More verbose and harder to maintain
- **Manual Portal**: Not reproducible, no version control

### Deployment Strategy

**Decision**: Azure Container Apps for backend, Azure Static Web Apps for frontend

**Rationale**:
- **Container Apps**:
  - Serverless containers with auto-scaling
  - Lower cost than App Service for variable load
  - Built-in Dapr integration for future features
  - Easy CI/CD with GitHub Actions

- **Static Web Apps**:
  - Optimized for React single-page apps
  - Global CDN distribution
  - Free SSL certificates
  - GitHub integration for preview deployments

**Alternatives Considered**:
- **App Service for both**: Simpler but less cost-effective for static content
- **Azure Functions**: Better for APIs but Container Apps preferred for Flask
- **AKS**: Overkill for initial deployment, consider for future scale

## Testing Strategy

### Test Pyramid Approach

**Decision**: Implement comprehensive testing at unit, integration, contract, and E2E levels

**Rationale**:
- **TDD Compliance**: Constitutional requirement for tests-first development
- **Confidence**: Multiple test levels catch different bug types
- **Speed**: Most tests are fast unit tests, fewer slow E2E tests
- **Documentation**: Tests serve as executable specifications

**Test Levels**:

1. **Unit Tests** (Vitest + pytest)
   - Frontend: Component logic, hooks, utilities
   - Backend: Services, repositories, models
   - Fast execution (<1s for all unit tests)
   - Mock external dependencies

2. **Contract Tests** (pytest)
   - Verify API matches OpenAPI specification
   - Request/response schema validation
   - Run against test database
   - Generated from OpenAPI contracts

3. **Integration Tests** (pytest)
   - Backend: Service + repository + database
   - Test transaction boundaries
   - Use test database with cleanup

4. **E2E Tests** (Playwright)
   - Critical user workflows
   - Full stack with real backend
   - Run in CI before deployment
   - Fewer tests (5-10 key scenarios)

### TDD Workflow

**Process**:
1. Write failing contract test from OpenAPI spec
2. Write failing integration test for service
3. Write failing unit tests for implementation
4. Implement minimum code to pass tests
5. Refactor with tests as safety net
6. Write E2E test for complete workflow

## Performance Considerations

### Canvas Rendering Optimization

**Strategies**:
- **Virtualization**: Render only visible nodes in viewport
- **Memoization**: React.memo for node/edge components to prevent unnecessary re-renders
- **Web Workers**: Offload layout calculations to worker threads
- **RequestAnimationFrame**: Batch canvas updates for smooth 60fps
- **Canvas vs SVG**: Use Canvas for >500 elements, SVG for better quality at lower counts

### API Performance

**Strategies**:
- **Pagination**: Limit result sets to 100 items per page
- **Selective Loading**: Load diagram metadata first, full data on demand
- **Caching**: Cache frequently accessed entities in backend memory
- **Database Indexes**: Index on commonly queried fields (domain_id, entity_id, diagram_id)
- **N+1 Prevention**: Use SQLAlchemy eager loading for relationships

### Database Performance

**Strategies**:
- **Indexes**: Primary keys, foreign keys, frequently filtered columns
- **Query Optimization**: Use EXPLAIN to analyze slow queries
- **Connection Pooling**: Reuse database connections
- **Read Replicas**: Consider for future read-heavy workloads (Azure SQL feature)

## Security Considerations

### Authentication & Authorization

**Decision**: Start with simple JWT authentication, migrate to Azure AD B2C for production

**Rationale**:
- **Phase 1**: Simple JWT allows rapid development and testing
- **Phase 2**: Azure AD B2C provides enterprise-grade auth for production
- **Flexibility**: Backend designed to support multiple auth providers

**Implementation**:
- **JWT for Local**: Short-lived tokens, HTTP-only cookies
- **Azure AD B2C**: OAuth 2.0 / OpenID Connect for production
- **Role-Based Access**: User owns diagrams, can share read/write access

### Data Security

**Strategies**:
- **Input Validation**: Pydantic schemas validate all API inputs
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **XSS Prevention**: React escapes rendered content by default
- **CORS**: Restrict origins to known frontend domains
- **HTTPS Only**: Enforce TLS in production
- **Secrets Management**: Azure Key Vault for connection strings and keys

## Migration & Deployment Strategy

### Database Migrations

**Tool**: Alembic for schema migrations

**Process**:
1. Developer creates migration script locally
2. Migration tested on local PostgreSQL
3. Migration tested on Azure SQL staging environment
4. Migration runs automatically during deployment
5. Rollback scripts available for failures

**Best Practices**:
- **Backward Compatible**: Old code works with new schema during deployment
- **Small Changes**: One logical change per migration
- **Reversible**: Down migrations for rollback
- **Idempotent**: Can run multiple times safely

### CI/CD Pipeline

**Tool**: GitHub Actions

**Workflow**:
1. **On Push**:
   - Run linting (ESLint, Ruff)
   - Run unit tests (Vitest, pytest)
   - Run contract tests

2. **On PR**:
   - All above +
   - Run integration tests
   - Build frontend and backend
   - Deploy to staging environment
   - Run E2E tests against staging

3. **On Merge to Main**:
   - Deploy to production
   - Run smoke tests
   - Notify team

### Deployment Process

1. Build Docker images for backend
2. Push images to Azure Container Registry
3. Deploy infrastructure with Bicep (if changed)
4. Deploy backend to Container Apps with new image
5. Run database migrations
6. Deploy frontend to Static Web Apps
7. Run post-deployment smoke tests
8. Monitor for errors

## Open Questions & Future Research

### Future Considerations

1. **Real-time Collaboration**:
   - WebSockets for live multi-user editing
   - Operational Transform or CRDT for conflict resolution
   - Consider Azure SignalR Service

2. **Offline Support**:
   - IndexedDB for local diagram storage
   - Service Workers for offline-first PWA
   - Sync strategy when connection restored

3. **Export Formats**:
   - SVG export (react-flow supports)
   - PNG export (canvas to image)
   - PDF generation (consider puppeteer or similar)

4. **AI Features**:
   - Auto-layout suggestions using graph algorithms
   - Entity relationship suggestions based on names
   - Consider Azure OpenAI integration

5. **Scalability Enhancements**:
   - Redis caching layer
   - Read replicas for database
   - CDN for static assets

## Summary

All technical decisions support the constitutional principles:
- **User-Centric**: React + React-Flow provide excellent UX for diagram editing
- **Visual Clarity**: Canvas rendering with 60fps performance
- **Modular**: Clear separation between frontend, backend, repositories, services
- **TDD**: Multiple test levels with contracts-first approach
- **Performance**: Optimizations for 1000+ elements and <100ms feedback

Tech stack is proven, well-supported, and aligns with Azure deployment requirements. All NEEDS CLARIFICATION items from Technical Context have been resolved.
