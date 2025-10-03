# Feature Specification: Dual Repository Architecture (Object Repository & Diagram Repository)

**Feature Branch**: `001-repo`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "there should be an object repository for all the data objects (superdomain, domain, entity, attribute) and their relations and a diagram repo that uses the objects to create different views from different perspectives"

## User Scenarios & Testing

### Primary User Story
As a data architect, I need a centralized object repository that stores all my data model objects (superdomains, domains, entities, attributes) and their relationships separately from how they're visualized, so that I can create multiple diagram views showing different perspectives of the same underlying data model without duplicating or fragmenting the model definition.

### Acceptance Scenarios
1. **Given** I create a new entity "Customer" with attributes in the object repository, **When** I create two different diagrams, **Then** both diagrams can reference and display the same "Customer" entity without duplication
2. **Given** an entity "Customer" exists in the object repository and appears in three different diagrams, **When** I update the "Customer" entity's attributes in the repository, **Then** all three diagrams automatically reflect the updated definition
3. **Given** entities "Customer" and "Order" with a relationship in the object repository, **When** I create a new diagram view, **Then** I can choose to include both entities and their relationship in this view
4. **Given** a diagram displaying entities from the object repository, **When** I change the visual position of an entity on the diagram, **Then** the object repository data remains unchanged and other diagrams are unaffected
5. **Given** multiple diagrams showing overlapping subsets of entities, **When** I delete an entity from the object repository, **Then** a warning is shown what the impact will be of the deletion (list of diagrams), the user can choose to remove from the diagrams or mark as invalid.
6. **Given** a diagram view, **When** I create a new entity directly from the diagram, **Then** the entity is stored in the object repository and becomes available for use in other diagrams
7. **Given** the object repository contains 100 entities, **When** I create a new diagram, **Then** I can selectively include only the 10 entities relevant to my current perspective

### Edge Cases
- What happens when a relationship exists between two entities, but only one entity is included in a diagram view? Hide relationship
- Can a diagram reference objects from multiple object repositories, or is there one repository per project? There is just one repo per project
- What happens when deleting a diagram that contains the only visual representation of certain relationships? The relationship keeps existing in the repo; when deleting an enity that has relationships, the relationships should be deleted too (inform the user and ask for confirmation)
- How does the system handle concurrent modifications to the same entity in the repository from different diagrams? Display a message when trying to overwrite a concurrent modification; inform the user and give him actions to resolve
- Can relationships exist in the object repository without being displayed in any diagram? Yes

## Requirements

### Functional Requirements

#### Object Repository Requirements
- **FR-001**: System MUST provide a centralized object repository storing all superdomains, domains, entities, and attributes
- **FR-002**: Object repository MUST store the canonical definition of each data object (names, properties, metadata)
- **FR-003**: Object repository MUST store all relationships between entities with their cardinality configurations
- **FR-004**: Object repository MUST enforce referential integrity for the object hierarchy (attributes belong to entities, entities belong to domains, etc.)
- **FR-005**: Object repository MUST support versioning/history of object changes?
- **FR-006**: Object repository MUST allow queries to retrieve objects by type, by name, by relationship, by domain, by superdomain, by attribute
- **FR-007**: System MUST ensure that modifying an object in the repository updates all references across all diagrams
- **FR-008**: Object repository MUST support validation rules - unique names within scope, required fields, naming conventions
- **FR-009**: Object repository MUST persist all objects and relationships across application sessions
- **FR-010**: System MUST provide interface for managing objects - CRUD operations, bulk operations

#### Diagram Repository Requirements
- **FR-011**: System MUST provide a diagram repository that stores multiple diagram views
- **FR-012**: Each diagram MUST reference objects from the object repository without duplicating the object definitions
- **FR-013**: Diagram repository MUST store visual layout information for each diagram (entity positions, visual styling, zoom level)
- **FR-014**: Diagram repository MUST store which objects from the object repository are included in each diagram view
- **FR-015**: Diagram repository MUST store which relationships to display in each diagram view
- **FR-016**: Diagrams MUST support partial views showing only a subset of entities and their relationships
- **FR-017**: System MUST allow creating multiple diagrams that reference overlapping sets of objects
- **FR-018**: Diagram repository MUST persist all diagram configurations across sessions
- **FR-019**: Each diagram MUST have metadata like name, description (markdown format), purpose (markdown format), created date, author, last updated date, tags
- **FR-020**: System MUST support unlimited diagrams per project (expectations are max order 200)

#### Object-Diagram Synchronization Requirements
- **FR-021**: Changes to object definitions in the repository MUST automatically propagate to all diagrams displaying those objects
- **FR-022**: Visual changes in a diagram (position, styling) MUST NOT affect the object repository or other diagrams
- **FR-023**: Creating a new object from within a diagram MUST add it to the object repository
- **FR-024**: Deleting an object from the repository MUST Remove from all diagrams or Mark as deleted but preserve in diagrams, depending on the user choice.
- **FR-025**: System MUST support deleting objects from a diagram view without deleting from repository (if it's the last occurance in a diagram of this object ask if object needs to be deleted)
- **FR-026**: System MUST handle default position, user placement

#### Multi-Perspective View Requirements
- **FR-027**: Users MUST be able to create diagrams showing domain-specific perspectives (e.g., "Payments Domain", "Finance Domain")
- **FR-028**: Users MUST be able to create diagrams showing cross domain perspectives (e.g., "Investment management View", "Customer Journey")
- **FR-029**: Users MUST be able to filter which entities and relationships appear in each diagram based on Domain, tags, custom filters
- **FR-030**: System MUST support Saved filters or views that can be reused
- **FR-031**: Each diagram MUST independently control which relationships are visible, even if both connected entities are present; in edit mode it should be clear there are invisible connections

#### Data Integrity Requirements
- **FR-032**: System MUST prevent orphaned references (diagrams referencing non-existent objects)
- **FR-033**: System MUST maintain referential integrity when objects are renamed in the repository
- **FR-034**: System MUST provide validation that ensures diagrams remain consistent with repository state
- **FR-035**: System MUST support recovery mechanisms if repository becomes corrupted

#### Repository Management Requirements
- **FR-036**: System MUST provide UI for browsing the object repository - tree view, list, search
- **FR-037**: System MUST provide UI for browsing available diagrams - list, thumbnails, recent
- **FR-038**: Users MUST be able to see which diagrams reference a specific object
- **FR-039**: System MUST support Export/import of both object repository and diagrams repository
- **FR-040**: System MUST support Repository-level operations like merge, split, refactor

### Key Entities

#### Repository Layer
- **Object Repository**: Centralized storage for all data model objects; maintains canonical definitions, relationships, and referential integrity; provides query interface for retrieval
- **Data Object**: Base representation for superdomains, domains, entities, and attributes; stored once in repository; referenced by multiple diagrams
- **Relationship**: Connection between two entities stored in the repository; includes cardinality and constraint information; independent of visual representation
- **Repository Metadata**: Information about the repository itself including versioning, validation rules, and integrity constraints

#### Diagram Layer
- **Diagram Repository**: Collection of diagram views; stores visual configurations and object selections for each diagram
- **Diagram View**: A specific perspective on the data model; references a subset of objects from the object repository; stores layout and styling information
- **Visual Layout**: Positioning and styling information for objects within a specific diagram; includes coordinates, zoom, visual theme
- **Object Reference**: Link from a diagram to an object in the object repository; enables single-source-of-truth while supporting multiple views
- **Perspective Filter**: Criteria defining which objects and relationships are included in a diagram view; enables domain-specific, layer-specific, or custom views

## Requirements

### Functional Requirements
[See sections above - 40 functional requirements organized by category]

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
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
- Key ambiguities: deletion cascade behavior, versioning/history, query capabilities, validation rules, repository API design, diagram metadata, filter criteria, default placement behavior, repository browsing UI, export/import capabilities, repository operations, corruption recovery, orphan handling
- **Critical architectural decision**: This feature establishes the foundational separation of concerns between data model (object repository) and visualization (diagram repository) - all other features depend on this architecture
