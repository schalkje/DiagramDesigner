# Feature Specification: Canvas with Entity Relationships and Crow's Foot Notation

**Feature Branch**: `003-add-a-canvas`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "add a canvas then entities can be connected and drawn; using configurable cardinality, that is displayed using crow notation"

## User Scenarios & Testing

### Primary User Story
As a data modeler, I need a visual canvas where I can draw entities, connect them with relationship lines, and configure cardinality constraints displayed using crow's foot notation, so that I can create professional entity-relationship diagrams (ERDs) that communicate database design clearly.

### Acceptance Scenarios
1. **Given** an empty canvas, **When** I drag an entity "Customer" onto the canvas, **Then** the entity appears at the dropped position and can be moved freely
2. **Given** two entities "Customer" and "Order" on the canvas, **When** I create a relationship between them, **Then** a connecting line appears between the two entities
3. **Given** a relationship between "Customer" and "Order", **When** I configure it as one-to-many (1:N), **Then** the line displays crow's foot notation showing one crow's foot on the "many" side
4. **Given** a relationship line on the canvas, **When** I change the cardinality from one-to-many to many-to-many, **Then** the crow's foot notation updates to show crow's feet on both ends
5. **Given** entities connected by a relationship, **When** I move one entity, **Then** the relationship line automatically adjusts to maintain the connection
6. **Given** multiple entities on the canvas, **When** I zoom in or out, **Then** all entities and relationship lines scale proportionally while maintaining visual clarity
7. **Given** a relationship line, **When** I delete it, **Then** the connection is removed but both entities remain on the canvas

### Edge Cases
- What happens when entities overlap on the canvas? Z-order behavior, order can be changed by the user; parent child behavior automatically determines z-order
- How does the system handle relationship lines when entities are very close together or far apart? The user determines the layour manually, but the system guides the user when placing objects to snap at nice positions
- What happens when a user tries to create a self-referencing relationship (entity to itself)? This can be perfectly fine
- Can multiple relationships exist between the same two entities? Yes, the relations should have a role so they can be differentiated between
- What are the bounds of the canvas? infinite canvas
- How does the system handle very long entity names that might affect layout? give the possibility to abreviate (...) user can override; mouse over should show the full name

## Requirements

### Functional Requirements

#### Canvas Requirements
- **FR-001**: System MUST provide a canvas workspace where entities can be placed and moved
- **FR-002**: System MUST support drag-and-drop placement of entities onto the canvas
- **FR-003**: System MUST allow users to freely reposition entities by dragging them
- **FR-004**: System MUST support zoom levels and pan navigation
- **FR-005**: System MUST support infinite canvas
- **FR-006**: System MUST support free positioning with a push towards grid snap
- **FR-007**: System MUST support selection model - single select, multi-select and marquee selection

#### Relationship Connection Requirements
- **FR-008**: System MUST allow users to create relationship lines connecting two entities
- **FR-009**: System MUST support creating relations by drag from entity to entity
- **FR-010**: Relationship lines MUST automatically update when connected entities are moved
- **FR-011**: Relationship lines MUST remain visually connected to entities at all times
- **FR-012**: System MUST support visual logical connection of the relationship endpoints using anchor points, the user chooses link to object or link to one of the connection points, each object has 8 by default (corners and centers) user can add more
- **FR-013**: System MUST allow users to delete relationships without deleting connected entities
- **FR-014**: System MUST support self-referencing relationships they should be displayed as a line goin out of the object and back again in a circle
- **FR-015**: System MUST handle multiple relationships between same entities

#### Cardinality Configuration Requirements
- **FR-016**: System MUST allow users to configure cardinality for each relationship
- **FR-017**: System MUST support the following cardinality types: one-to-one (1:1), one-to-many (1:N), many-to-one (N:1), and many-to-many (N:N)
- **FR-018**: System MUST support Optional vs. mandatory participation (0 or 1 minimum)? E.g., 0..1, 1..1, 0..N, 1..N, 1..N?, 0..N?
- **FR-019**: System MUST provide cardinality is configured using a Dialog, properties panel or  right-click menu
- **FR-020**: Cardinality changes MUST update the visual notation immediately

#### Crow's Foot Notation Requirements
- **FR-021**: System MUST display relationships using standard crow's foot notation
- **FR-022**: System MUST display the "crow's foot" symbol (⊢<) on the "many" side of relationships
- **FR-023**: System MUST display a single line (|) or dash (|) on the "one" side of relationships
- **FR-024**: System MUST distinguish between mandatory and optional participation using circle vs. bar notation conventions (in the cardinality selection, show the visualisation and the explanation, to make it easy for the user)
- **FR-025**: Crow's foot notation MUST remain legible at different zoom levels, until zoom out makes this detail too messy
- **FR-026**: System MUST render notation symbols with size constraints relative to visual line thickness

#### Visual Quality Requirements
- **FR-027**: System MUST maintain 60fps rendering during entity dragging and panning
- **FR-028**: System MUST render relationship lines with anti-aliasing for smooth appearance
- **FR-029**: System MUST support styling options for lines - color, thickness, dashed vs solid
- **FR-030**: System MUST ensure visual clarity when multiple relationship lines connect the same entities

#### Persistence Requirements
- **FR-031**: System MUST persist entity positions on the canvas across sessions
- **FR-032**: System MUST persist all relationship connections and cardinality configurations
- **FR-033**: System MUST support undo/redo for canvas operations - move, connect, delete

### Key Entities
- **Canvas**: The visual workspace where entities are placed and relationships are drawn; supports pan, zoom, and layout operations
- **Entity (visual)**: A visual representation of a data entity on the canvas; has position (x, y coordinates), dimensions, and references the underlying data entity
- **Relationship Line**: A visual connector between two entities; has a source entity, target entity, cardinality configuration, and visual path
- **Cardinality**: Configuration for a relationship defining the numerical constraints on each side; includes minimum and maximum values for each end (e.g., 1:1, 1:N, N:N)
- **Crow's Foot Symbol**: Visual notation element rendered at relationship endpoints; varies based on cardinality (single line, crow's foot, circle for optional)

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [X] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [x] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed

---

**WARNINGS**:
- Key ambiguities: canvas navigation (zoom/pan), canvas bounds, interaction model (how to create relationships), positioning (grid snap, anchor points), cardinality details (optional/mandatory notation), selection model, styling options, undo/redo support, multiple relationships handling, self-referencing relationships, endpoint positioning
