# DiagramDesigner - Docker Quickstart (1 Command!)

## Prerequisites

- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)

That's it! No Python, Node, or PostgreSQL needed.

## Run the Application (1 Command)

```bash
cd infrastructure/local
docker-compose up
```

Wait 1-2 minutes for containers to build and start.

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Database**: localhost:5432

## Test It's Working

1. Open http://localhost:3000
2. Click "Register" and create an account
3. Start building your data model!

## Stop the Application

```bash
# Press Ctrl+C in the terminal, then:
docker-compose down
```

## Common Commands

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Reset database (deletes all data!)
docker-compose down -v
docker-compose up
```

## Troubleshooting

### Ports Already in Use
If ports 3000, 5000, or 5432 are in use:

Edit `docker-compose.yml` and change the **first** port number:
```yaml
ports:
  - "3001:3000"  # Frontend now on 3001
```

### Container Build Fails
```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Database Connection Error
The backend waits for PostgreSQL to be healthy. If it fails:
```bash
# Check database logs
docker-compose logs db

# Restart
docker-compose restart backend
```

---

**That's it!** Way easier than manual setup. 🐳
