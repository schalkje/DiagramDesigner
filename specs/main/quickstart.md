# Quickstart Guide

**Feature**: DiagramDesigner Application
**Date**: 2025-10-03
**Purpose**: Validate core user workflows end-to-end

## Overview
This quickstart guide provides step-by-step instructions to validate the DiagramDesigner application from initial setup through core workflows. Each section can be executed as an automated test scenario.

## Prerequisites
- Windows 11, macOS, or Linux
- Docker Desktop installed and running
- Git installed
- Node.js 18+ installed
- Python 3.12+ installed

## Section 1: Local Environment Setup

### 1.1 Clone and Initialize

```bash
# Clone repository
git clone <repository-url>
cd DiagramDesigner

# Verify structure
ls -la backend/ frontend/ infrastructure/
```

**Expected Result**: All three directories exist

### 1.2 Start Local Environment

```bash
# Start all services with Docker Compose
cd infrastructure/local
docker-compose up -d

# Verify services are running
docker-compose ps
```

**Expected Result**:
- PostgreSQL database on port 5432 (status: Up)
- Backend API on port 5000 (status: Up)
- Frontend dev server on port 3000 (status: Up)

### 1.3 Verify Database Initialization

```bash
# Check database schema
docker-compose exec db psql -U diagramdesigner -d diagramdesigner -c "\dt"
```

**Expected Result**: Tables exist for:
- user
- superdomain
- domain
- entity
- attribute
- relationship
- diagram
- diagram_object
- diagram_relationship

### 1.4 Access Frontend

```bash
# Open browser
open http://localhost:3000
```

**Expected Result**: Frontend loads with login page

---

## Section 2: User Authentication

### 2.1 Register New User

**UI Steps**:
1. Navigate to http://localhost:3000
2. Click "Register" button
3. Fill in form:
   - Email: test@example.com
   - Username: testuser
   - Password: Test123!
4. Click "Create Account"

**Expected Result**:
- User created successfully
- Redirected to dashboard

**API Test** (alternative):
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test123!"
  }'
```

**Expected Response**: HTTP 201 with user object and JWT token

### 2.2 Login

**UI Steps**:
1. Navigate to http://localhost:3000/login
2. Enter credentials:
   - Email: test@example.com
   - Password: Test123!
3. Click "Login"

**Expected Result**: Redirected to dashboard with user menu visible

---

## Section 3: Create Data Model (Object Repository)

### 3.1 Create Superdomain

**UI Steps**:
1. From dashboard, click "Object Repository" in sidebar
2. Click "New Superdomain" button
3. Fill in form:
   - Name: Business
   - Description: Business-related data models
4. Click "Create"

**Expected Result**:
- "Business" superdomain appears in repository tree
- Success notification displayed

**API Test** (alternative):
```bash
TOKEN="<jwt_token_from_login>"

curl -X POST http://localhost:5000/api/v1/superdomains \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Business",
    "description": "Business-related data models"
  }'
```

**Expected Response**: HTTP 201 with superdomain object containing ID

### 3.2 Create Domain

**UI Steps**:
1. In repository tree, right-click "Business" superdomain
2. Select "New Domain"
3. Fill in form:
   - Name: Sales
   - Description: Sales and customer management
4. Click "Create"

**Expected Result**:
- "Sales" domain appears nested under "Business" in tree
- Success notification displayed

**API Test** (alternative):
```bash
SUPERDOMAIN_ID="<id_from_previous_step>"

curl -X POST http://localhost:5000/api/v1/domains \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "superdomainId": "'$SUPERDOMAIN_ID'",
    "name": "Sales",
    "description": "Sales and customer management"
  }'
```

### 3.3 Create Entity with Attributes

**UI Steps**:
1. In repository tree, right-click "Sales" domain
2. Select "New Entity"
3. Fill in form:
   - Name: Customer
   - Description: Customer information
4. Click "Create"
5. In entity detail view, click "Add Attribute" (repeat for each):
   - Attribute 1:
     - Name: id
     - Data Type: UUID
     - Nullable: No
   - Attribute 2:
     - Name: name
     - Data Type: String
     - Nullable: No
   - Attribute 3:
     - Name: email
     - Data Type: String
     - Nullable: No
   - Attribute 4:
     - Name: createdAt
     - Data Type: DateTime
     - Nullable: No

**Expected Result**:
- "Customer" entity appears under "Sales" domain
- All 4 attributes visible in entity detail view
- Success notification for each attribute

**API Test** (alternative):
```bash
DOMAIN_ID="<id_from_previous_step>"

# Create entity
ENTITY_RESPONSE=$(curl -X POST http://localhost:5000/api/v1/entities \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domainId": "'$DOMAIN_ID'",
    "name": "Customer",
    "description": "Customer information"
  }')

ENTITY_ID=$(echo $ENTITY_RESPONSE | jq -r '.id')

# Create attributes
curl -X POST http://localhost:5000/api/v1/entities/$ENTITY_ID/attributes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "id",
    "dataType": "UUID",
    "isNullable": false
  }'

curl -X POST http://localhost:5000/api/v1/entities/$ENTITY_ID/attributes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "name",
    "dataType": "String",
    "isNullable": false
  }'

curl -X POST http://localhost:5000/api/v1/entities/$ENTITY_ID/attributes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "email",
    "dataType": "String",
    "isNullable": false
  }'

curl -X POST http://localhost:5000/api/v1/entities/$ENTITY_ID/attributes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "createdAt",
    "dataType": "DateTime",
    "isNullable": false
  }'
```

### 3.4 Create Second Entity

**UI Steps**:
1. Right-click "Sales" domain, select "New Entity"
2. Fill in:
   - Name: Order
   - Description: Customer orders
3. Add attributes:
   - id (UUID, not nullable)
   - customerId (UUID, not nullable)
   - orderDate (DateTime, not nullable)
   - totalAmount (Decimal, not nullable)

**Expected Result**: "Order" entity created with 4 attributes

### 3.5 Create Relationship

**UI Steps**:
1. In repository, select "Customer" entity
2. Click "Add Relationship" button
3. Fill in form:
   - Target Entity: Order
   - Source Role: customer
   - Target Role: orders
   - Source Cardinality: ONE (1..1)
   - Target Cardinality: ZERO_MANY (0..N)
4. Click "Create"

**Expected Result**:
- Relationship created between Customer and Order
- Relationship visible in both entities' relationship lists
- Cardinality shows "1:N" notation

**API Test** (alternative):
```bash
curl -X POST http://localhost:5000/api/v1/relationships \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceEntityId": "'$CUSTOMER_ENTITY_ID'",
    "targetEntityId": "'$ORDER_ENTITY_ID'",
    "sourceRole": "customer",
    "targetRole": "orders",
    "sourceCardinality": "ONE",
    "targetCardinality": "ZERO_MANY"
  }'
```

---

## Section 4: Create Diagram Visualization

### 4.1 Create New Diagram

**UI Steps**:
1. Click "Diagrams" in sidebar
2. Click "New Diagram" button
3. Fill in form:
   - Name: Sales Overview
   - Description: Overview of sales data model
   - Tags: sales, customer
4. Click "Create"

**Expected Result**:
- New blank canvas displayed
- Diagram name "Sales Overview" in header
- Object repository panel visible on left

**API Test** (alternative):
```bash
curl -X POST http://localhost:5000/api/v1/diagrams \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales Overview",
    "description": "Overview of sales data model",
    "tags": ["sales", "customer"]
  }'
```

### 4.2 Add Entities to Canvas

**UI Steps**:
1. From object repository panel, drag "Customer" entity onto canvas
2. Drop at position approximately (100, 100)
3. Drag "Order" entity onto canvas
4. Drop at position approximately (400, 100)

**Expected Result**:
- Both entities visible on canvas
- Customer entity shows all 4 attributes
- Order entity shows all 4 attributes
- Entities can be selected and moved

**API Test** (alternative):
```bash
DIAGRAM_ID="<id_from_previous_step>"

# Add Customer entity
curl -X POST http://localhost:5000/api/v1/diagrams/$DIAGRAM_ID/objects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "objectType": "ENTITY",
    "objectId": "'$CUSTOMER_ENTITY_ID'",
    "positionX": 100,
    "positionY": 100
  }'

# Add Order entity
curl -X POST http://localhost:5000/api/v1/diagrams/$DIAGRAM_ID/objects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "objectType": "ENTITY",
    "objectId": "'$ORDER_ENTITY_ID'",
    "positionX": 400,
    "positionY": 100
  }'
```

### 4.3 Display Relationship

**UI Steps**:
1. Relationship line automatically appears between Customer and Order
2. Verify crow's foot notation:
   - Single line on Customer side (1)
   - Crow's foot on Order side (N)
3. Hover over line to see relationship details (source role, target role)

**Expected Result**:
- Relationship line connects entities
- Crow's foot notation correct for 1:N
- Line updates when entities are moved

### 4.4 Customize Canvas

**UI Steps**:
1. Click Customer entity and drag to new position (150, 200)
2. Verify relationship line follows entity
3. Use mouse wheel to zoom in/out
4. Click and drag canvas background to pan
5. Click "Canvas Settings" button
6. Enable "Snap to Grid"
7. Move Customer entity again, verify it snaps to grid

**Expected Result**:
- Smooth 60fps rendering during drag operations
- Zoom works from 25% to 400%
- Pan works in all directions (infinite canvas)
- Grid snap works when enabled
- All changes persist automatically

---

## Section 5: Data Persistence & Sync

### 5.1 Verify Auto-Save

**UI Steps**:
1. Make changes to diagram (move entities)
2. Wait 2 seconds
3. Observe "Saved" indicator in top-right corner
4. Close browser tab
5. Reopen http://localhost:3000
6. Navigate to "Sales Overview" diagram

**Expected Result**:
- All changes persisted
- Diagram loads with entities in last saved positions
- No data loss

### 5.2 Update Entity in Repository

**UI Steps**:
1. Keep "Sales Overview" diagram open in one browser tab
2. Open new tab to http://localhost:3000/repository
3. Navigate to Customer entity
4. Add new attribute:
   - Name: phone
   - Data Type: String
   - Nullable: Yes
5. Save attribute
6. Switch back to diagram tab

**Expected Result**:
- Customer entity on canvas automatically shows new "phone" attribute
- No manual refresh required
- Change propagates in real-time

### 5.3 Test Concurrent Editing (optional, requires 2 browsers)

**UI Steps**:
1. Open diagram in Chrome browser
2. Open same diagram in Firefox browser (logged in as same user)
3. In Chrome: Move Customer entity to (200, 300)
4. In Firefox: Observe Customer entity position updates

**Expected Result**: Position changes visible in both browsers (eventual consistency within 2 seconds)

---

## Section 6: Delete Operations

### 6.1 Delete from Diagram (without deleting from repository)

**UI Steps**:
1. In diagram, right-click Order entity
2. Select "Remove from Diagram"
3. Confirm action

**Expected Result**:
- Order entity removed from canvas
- Relationship line also removed
- Order entity still exists in repository
- Order entity still visible in repository tree

### 6.2 Delete with Impact Analysis

**UI Steps**:
1. In repository, right-click Order entity
2. Select "Delete"
3. View impact analysis dialog:
   - "Order entity is used in X relationships"
   - "Order entity appears in X diagrams"
4. Cancel deletion

**Expected Result**:
- Impact dialog shows accurate counts
- Cancel button aborts deletion
- Order entity still exists

### 6.3 Cascade Delete

**UI Steps**:
1. Right-click "Sales" domain
2. Select "Delete"
3. View impact dialog:
   - "Will delete 2 entities (Customer, Order)"
   - "Will delete all attributes"
   - "Will delete relationships"
   - "Will remove from diagrams"
4. Check "Confirm cascade delete"
5. Click "Delete"

**Expected Result**:
- Sales domain deleted
- Customer and Order entities deleted
- All attributes deleted
- All relationships deleted
- Diagram canvas now empty (entities removed)

---

## Section 7: Export & Deployment Readiness

### 7.1 Export Diagram

**UI Steps**:
1. Create new simple diagram with 2 entities
2. Click "Export" button
3. Select "SVG" format
4. Click "Download"
5. Open SVG file

**Expected Result**:
- SVG file downloads
- SVG renders correctly in browser or image viewer
- All entities and relationships visible
- Quality matches canvas display

### 7.2 Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U diagramdesigner diagramdesigner > backup.sql

# Verify backup
ls -lh backup.sql
```

**Expected Result**: backup.sql file created with size >0

### 7.3 Shutdown Local Environment

```bash
# Stop services
docker-compose down

# Verify services stopped
docker-compose ps
```

**Expected Result**: All services stopped (status: Exit or not listed)

---

## Section 8: Azure Deployment (Production)

### 8.1 Deploy Infrastructure

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-diagramdesigner --location eastus

# Deploy infrastructure with Bicep
cd infrastructure/azure/bicep
az deployment group create \
  --resource-group rg-diagramdesigner \
  --template-file main.bicep \
  --parameters environmentName=prod

# Verify resources created
az resource list --resource-group rg-diagramdesigner --output table
```

**Expected Result**:
- Azure SQL Database created
- Container Apps environment created
- Backend container app created
- Static Web App created
- Key Vault created

### 8.2 Deploy Application

```bash
# Build and push backend image
cd backend
az acr build --registry <registry_name> --image diagramdesigner-backend:latest .

# Deploy backend
az containerapp update \
  --name ca-diagramdesigner-backend \
  --resource-group rg-diagramdesigner \
  --image <registry_name>.azurecr.io/diagramdesigner-backend:latest

# Deploy frontend
cd frontend
npm run build
az staticwebapp deploy \
  --name swa-diagramdesigner \
  --resource-group rg-diagramdesigner \
  --app-location ./dist
```

**Expected Result**:
- Backend deployed successfully
- Frontend deployed successfully
- Health check endpoints return 200 OK

### 8.3 Run Database Migrations

```bash
# Run migrations on Azure SQL
cd backend
export DATABASE_URL="<azure_sql_connection_string>"
alembic upgrade head
```

**Expected Result**: All migrations applied successfully

### 8.4 Verify Production Deployment

**UI Steps**:
1. Navigate to https://<your-static-web-app-url>
2. Register new user
3. Create superdomain, domain, entity
4. Create diagram
5. Verify all workflows work as in local environment

**Expected Result**: All functionality works in production environment

---

## Success Criteria

✅ All sections completed without errors
✅ Local environment starts in <2 minutes
✅ Frontend renders diagrams at 60fps
✅ API response times <200ms for simple queries
✅ Canvas handles 10+ entities smoothly
✅ Changes persist across browser restarts
✅ Cascade deletes work correctly with impact analysis
✅ Azure deployment succeeds
✅ Production environment handles test workflows

## Troubleshooting

### Issue: Docker services fail to start
**Solution**: Check Docker Desktop is running, ports 3000/5000/5432 are not in use

### Issue: Database migrations fail
**Solution**: Verify DATABASE_URL is correct, check database is accessible

### Issue: Frontend can't connect to backend
**Solution**: Check CORS configuration, verify API_BASE_URL in frontend .env

### Issue: Slow canvas rendering
**Solution**: Reduce number of entities, check browser dev tools for performance bottlenecks

### Issue: Azure deployment fails
**Solution**: Check Azure CLI authentication, verify subscription has quota for resources

---

## Cleanup

### Local Environment
```bash
docker-compose down -v  # Remove containers and volumes
```

### Azure Environment
```bash
az group delete --name rg-diagramdesigner --yes --no-wait
```

---

**Document Version**: 1.0
**Last Updated**: 2025-10-03
**Status**: Ready for Implementation
