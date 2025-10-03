# DiagramDesigner - Local Testing Quickstart

Get the application running locally in 5 minutes!

## Prerequisites

- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)

## Quick Setup (3 Steps)

### Step 1: Database Setup (2 minutes)

```bash
# Create PostgreSQL user and database
psql -U postgres
```

```sql
CREATE USER diagramdesigner WITH PASSWORD 'diagramdesigner';
CREATE DATABASE diagramdesigner OWNER diagramdesigner;
\q
```

### Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start backend server
python app.py
```

Backend should now be running on **http://localhost:5000**

### Step 3: Frontend Setup (1 minute)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start frontend dev server
npm run dev
```

Frontend should now be running on **http://localhost:3000**

## Testing the Application

1. **Open browser**: http://localhost:3000
2. **Register** a new account
3. **Create** your first Superdomain → Domain → Entity
4. **Create** a diagram and drag entities onto the canvas

## API Health Check

Test backend is running:
```bash
curl http://localhost:5000/health
# Should return: {"status":"healthy"}
```

## Troubleshooting

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify credentials in `backend/.env`
- Ensure database exists: `psql -U postgres -l | grep diagramdesigner`

### Port Already in Use
- **Backend (5000)**: Change port in `backend/app.py`
- **Frontend (3000)**: Change port in `frontend/vite.config.ts`

### Module Not Found (Python)
- Ensure virtual environment is activated
- Re-run: `pip install -r requirements.txt`

### Module Not Found (Node)
- Delete `node_modules` and `package-lock.json`
- Re-run: `npm install`

## Using Docker (Alternative)

```bash
cd infrastructure/local
docker-compose up -d
```

All services will start automatically:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- PostgreSQL: localhost:5432

## Next Steps

- **API Documentation**: Open http://localhost:5000/docs (if Swagger is configured)
- **Run Tests**:
  - Backend: `cd backend && pytest`
  - Frontend: `cd frontend && npm test`
- **View Logs**: Check terminal output for both backend and frontend

## Sample Data

Create test data manually or run:
```bash
cd backend
python scripts/seed_data.py  # (if available)
```

---

**Need Help?** Check the [full documentation](./README.md) or [open an issue](https://github.com/your-org/diagramdesigner/issues).
