# Feature Specification: Data Model Management Screens

**Feature Branch**: `002-add-screens`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "Add screens to create, edit, delete objects: superdomain, domain, entity and attribute"

## User Scenarios & Testing

### Primary User Story
As a data modeler, I need dedicated screens to manage my diagram's data model hierarchy (superdomains, domains, entities, and attributes) so that I can create, modify, and organize data structures efficiently without manually drawing or editing diagram elements.

### Acceptance Scenarios
1. **Given** an empty diagram workspace, **When** I create a new superdomain named "Business", **Then** the superdomain appears in the diagram and is available in the data model tree
2. **Given** an existing superdomain "Business", **When** I create a domain named "Sales" within it, **Then** the domain is nested under the superdomain in both the diagram and model hierarchy
3. **Given** an existing domain "Sales", **When** I create an entity named "Customer" with attributes "ID", "Name", "Email", **Then** the entity appears with all three attributes visible
4. **Given** an existing entity "Customer", **When** I edit it to add a new attribute "Phone", **Then** the attribute is added to the entity and visible in the diagram
5. **Given** an entity "Customer" with dependencies, **When** I attempt to delete it, **Then** The system should inform the user of the impact and only when confirmed to a cascade delete
6. **Given** multiple entities exist, **When** I delete an attribute from "Customer", **Then** the attribute is removed and if there are relationships to this attribute inform the user of the impact and only delete after confirmation

### Edge Cases
- What happens when a user tries to create a superdomain with a duplicate name? Prevent
- How does the system handle empty names or names with special characters? Empty names are illegal, avoid special characters that can cause problems with queries or readability
- What happens when editing an object that another user is also editing? it is a collaborative tool
- What are the character limits for names and descriptions? Names should be consize (max 100), descriptions can be long markdown
- Can entities exist without a parent domain, or domains without a superdomain? No, there is a strict hierarchy: superdomain, domain, entity, attribute; there is a default super domain: other and a default domain: other

## Requirements

### Functional Requirements
- **FR-001**: System MUST provide a screen to create new superdomains with a name and optional description
- **FR-002**: System MUST provide a screen to create new domains within a selected superdomain
- **FR-003**: System MUST provide a screen to create new entities within a selected domain
- **FR-004**: System MUST provide a screen to create new attributes within a selected entity
- **FR-005**: System MUST allow users to edit the name and properties of existing superdomains
- **FR-006**: System MUST allow users to edit the name and properties of existing domains
- **FR-007**: System MUST allow users to edit the name and properties of existing entities
- **FR-008**: System MUST allow users to edit attributes (name, data type, constraints)
- **FR-009**: System MUST allow users to delete superdomains with confirmation dialog that informs of the impact and after confirmation cascade delete
- **FR-010**: System MUST allow users to delete with confirmation dialog that informs of the impact and after confirmation cascade delete
- **FR-011**: System MUST allow users to delete entities with confirmation dialog that informs of the impact and after confirmation cascade delete, including relations
- **FR-012**: System MUST allow users to delete attributes with confirmation dialog that informs of the impact and after confirmation cascade delete, including relations
- **FR-013**: System MUST validate that names are not empty before saving
- **FR-014**: System MUST persist all changes so they survive application restart
- **FR-015**: System MUST reflect all create/edit/delete operations immediately in the diagram visualization, support differen screens, different users collaborative; show when someone is editing something to others
- **FR-016**: System MUST support undo/redo for all operations
- **FR-017**: Attribute creation MUST allow specifying What properties? Data type, nullability, default value, constraints, dataquality
- **FR-018**: System MUST support a clean ui, with Menu, toolbar, context menu, sidebar panel
- **FR-019**: System MUST enforce domains always have a super domain (default: other), enities always have a domain  (default: other) attributes always have a parent entity
- **FR-020**: System MUST handle expected scale is 5 superdomains, 50 domain, 2000 entities, 100000 attributes

### Key Entities
- **Superdomain**: Top-level container in the data model hierarchy; contains multiple domains; has a name and optional description
- **Domain**: Mid-level grouping within a superdomain; contains multiple entities; represents a logical business area or subject domain
- **Entity**: Represents a business object or concept; contains multiple attributes; belongs to a domain; equivalent to a table in database modeling
- **Attribute**: Property or field of an entity; has a name and data type; belongs to an entity; equivalent to a column in database modeling

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
- Key ambiguities: deletion behavior, cascade rules, UI access patterns, attribute properties, collaboration model, naming constraints, hierarchy rules, scale expectations
