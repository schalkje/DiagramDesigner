
# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
DiagramDesigner is a three-tier web application for creating and managing data model diagrams with entity-relationship visualization. The application features a frontend for interactive diagram editing, a backend API for business logic and data management, and a database for persistent storage. It supports local development environments and deployment to Azure cloud infrastructure, enabling both individual use and collaborative scenarios.

## Technical Context
**Language/Version**: TypeScript 5.x (frontend), Python 3.12+ (backend)
**Primary Dependencies**: React 18+ (frontend), Flask 3.x (backend), SQLAlchemy 2.x (ORM), Alembic (migrations)
**Storage**: PostgreSQL (local dev), Azure SQL Database (production)
**Testing**: Vitest/Jest (frontend unit), pytest (backend unit), Playwright (E2E integration)
**Target Platform**: Local Windows 11 (dev), Linux containers on Azure Container Apps (production)
**Project Type**: web (frontend + backend architecture)
**Performance Goals**: 60fps canvas rendering, <200ms API response, interactive feel without delays
**Constraints**: <100ms user action feedback, 10+ concurrent users
**Scale/Scope**: 5 superdomains, 50 domains, 2000 entities, 100,000 attributes, 20 concurrent users, 200 diagrams

**User-Provided Context**: The application has a front-end, a backend and a database that runs locally and can later be deployed to azure

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. User-Centric Design
- [x] Feature validated against real user workflows - Addresses data architects' needs for diagram creation with local dev and cloud deployment
- [x] No complexity without clear user value - Three-tier architecture provides separation of concerns, scalability, and deployment flexibility
- [x] User experience prioritized in design decisions - Frontend focuses on interactive canvas, backend handles complexity

### II. Visual Clarity
- [x] Rendering quality maintained across all export formats - 60fps canvas rendering requirement ensures smooth visual experience
- [x] Pixel-perfect accuracy ensured - Canvas-based rendering with React provides precise control
- [x] Consistent styling verified - Component-based architecture ensures consistent UI patterns

### III. Modular Architecture
- [x] Feature implemented as independent module - Frontend, backend, and database are separate layers with clear boundaries
- [x] Clear interfaces defined - REST API contracts define frontend-backend communication
- [x] Components reusable across diagram types - Repository pattern separates data model from visualization

### IV. Test-Driven Development
- [x] TDD approach planned (tests before implementation) - Phase 1 generates contract tests before implementation
- [x] Red-Green-Refactor cycle documented - Contract tests will fail initially, implementation makes them pass
- [x] Test approval process defined - Tests at unit (Vitest/pytest), integration (Playwright), and contract levels

### V. Performance & Responsiveness
- [x] 60fps interaction maintained - Explicitly required in performance goals for canvas rendering
- [x] Handles 1000+ elements without degradation - Designed to support 2000 entities and 100,000 attributes
- [x] User actions provide <100ms feedback - Specified in constraints section

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
backend/
├── src/
│   ├── models/           # SQLAlchemy models (Superdomain, Domain, Entity, Attribute, Diagram, etc.)
│   ├── services/         # Business logic layer
│   ├── api/              # Flask API routes and controllers
│   ├── repositories/     # Data access layer
│   └── utils/            # Helper functions and utilities
├── tests/
│   ├── contract/         # API contract tests (generated from OpenAPI)
│   ├── integration/      # Integration tests
│   └── unit/             # Unit tests for services and models
├── migrations/           # Alembic database migrations
└── requirements.txt      # Python dependencies

frontend/
├── src/
│   ├── components/       # React components (Canvas, EntityCard, RelationshipLine, etc.)
│   ├── pages/            # Page-level components (DiagramEditor, RepositoryBrowser, etc.)
│   ├── services/         # API client services
│   ├── hooks/            # Custom React hooks
│   ├── store/            # State management (React Context or Zustand)
│   └── types/            # TypeScript type definitions
├── tests/
│   ├── unit/             # Component unit tests
│   └── e2e/              # Playwright end-to-end tests
└── package.json          # Node.js dependencies

infrastructure/
├── local/                # Docker Compose for local development
│   └── docker-compose.yml
└── azure/                # Azure deployment configuration
    ├── bicep/            # Infrastructure-as-code templates
    └── pipelines/        # CI/CD pipeline definitions
```

**Structure Decision**: Web application structure with separate frontend and backend directories. This aligns with the three-tier architecture requirement and supports independent development, testing, and deployment of each layer. The infrastructure directory contains environment-specific configurations for both local development (Docker Compose) and Azure deployment (Bicep templates).

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
The /tasks command will generate tasks from Phase 1 artifacts in this order:

1. **Infrastructure & Setup Tasks**:
   - Create Docker Compose configuration for local environment
   - Create database schema migration scripts
   - Set up backend Flask project structure
   - Set up frontend React project structure
   - Configure CI/CD pipeline templates

2. **Contract Test Generation** (from openapi.yaml):
   - For each endpoint group (Superdomains, Domains, Entities, Attributes, Relationships, Diagrams)
   - Generate contract test file [P] - can run in parallel
   - Tests must fail initially (no implementation yet)

3. **Data Model Implementation** (from data-model.md):
   - Create SQLAlchemy models for each entity [P]:
     - User model
     - Superdomain model
     - Domain model
     - Entity model
     - Attribute model
     - Relationship model
     - Diagram model
     - DiagramObject model
     - DiagramRelationship model
   - Create Alembic migration for initial schema
   - Create repository classes for each model [P]

4. **Service Layer Implementation** (from data-model.md + openapi.yaml):
   - Create service classes with business logic:
     - SuperdomainService (validation, cascade delete logic)
     - DomainService
     - EntityService
     - AttributeService
     - RelationshipService
     - DiagramService
   - Write integration tests for each service

5. **API Layer Implementation** (from openapi.yaml):
   - Create Flask routes for each endpoint group [P]:
     - Auth routes (login, register)
     - Superdomain routes
     - Domain routes
     - Entity routes
     - Attribute routes
     - Relationship routes
     - Diagram routes
   - Wire up routes to services
   - Implement request validation with Pydantic
   - Implement JWT authentication middleware

6. **Frontend State & Types** (from openapi.yaml + data-model.md):
   - Generate TypeScript types from OpenAPI schema
   - Create API client service with typed methods
   - Set up Zustand store structure
   - Create custom hooks for data fetching

7. **Frontend Components** (from quickstart.md + spec.md):
   - Create authentication components (Login, Register)
   - Create repository browser components (Tree view, Entity cards)
   - Create diagram canvas components (Canvas, EntityNode, RelationshipEdge)
   - Create forms (Entity form, Relationship form, Diagram settings)
   - Write component unit tests

8. **Integration Tests** (from quickstart.md scenarios):
   - Test: Create superdomain → domain → entity → attributes workflow
   - Test: Create relationship between entities
   - Test: Create diagram and add objects
   - Test: Update entity and verify diagram sync
   - Test: Delete with cascade and impact analysis

9. **E2E Tests** (from quickstart.md sections):
   - E2E: Complete user registration and login flow
   - E2E: Create complete data model (Section 3 of quickstart)
   - E2E: Create and edit diagram (Section 4 of quickstart)
   - E2E: Verify persistence and sync (Section 5 of quickstart)
   - E2E: Test delete operations (Section 6 of quickstart)

10. **Documentation & Deployment**:
    - Create README with setup instructions
    - Create API documentation (Swagger UI setup)
    - Create Azure Bicep templates for infrastructure
    - Create deployment scripts for Azure
    - Update CLAUDE.md with final implementation notes

**Ordering Strategy**:
- **TDD Order**: All contract and test tasks before corresponding implementation tasks
- **Dependency Order**:
  - Infrastructure → Models → Repositories → Services → API → Frontend
  - Backend can proceed in parallel with frontend after contracts are defined
- **Parallel Execution**: Mark tasks with [P] when they operate on independent files/modules
- **Constitutional Compliance**: Tests written and approved before implementation code

**Estimated Output**: 80-100 numbered tasks organized into the above phases

**Task Template Format**:
```
## Task N: [Short description]
**Type**: [Setup|Test|Implementation|Documentation]
**Phase**: [Infrastructure|Backend|Frontend|Integration|E2E]
**Parallel**: [Yes|No]
**Depends On**: [Task numbers or "None"]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Files to Create/Modify
- `path/to/file.py`

### Test Validation
- Run: `pytest tests/path/test_file.py` → MUST PASS
```

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - research.md created
- [x] Phase 1: Design complete (/plan command) - data-model.md, contracts/openapi.yaml, quickstart.md, CLAUDE.md created
- [x] Phase 2: Task planning complete (/plan command - describe approach only) - Strategy documented above
- [ ] Phase 3: Tasks generated (/tasks command) - NOT EXECUTED (awaiting /tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS - All 5 principles validated
- [x] Post-Design Constitution Check: PASS - Design aligns with constitutional requirements
- [x] All NEEDS CLARIFICATION resolved - All technical unknowns researched and decided
- [x] Complexity deviations documented - No violations requiring justification (Complexity Tracking section empty)

**Artifacts Generated**:
- [x] specs/main/spec.md - Feature specification with 56 functional requirements
- [x] specs/main/research.md - Technical decisions and architecture patterns
- [x] specs/main/data-model.md - 9 entities with complete schemas and relationships
- [x] specs/main/contracts/openapi.yaml - REST API contract with 30+ endpoints
- [x] specs/main/quickstart.md - End-to-end validation guide with 8 sections
- [x] CLAUDE.md - Agent context file with project overview and key information

**Ready for Next Command**: `/tasks` to generate tasks.md from design artifacts

---
*Based on Constitution v1.1.0 - See `.specify/memory/constitution.md`*
