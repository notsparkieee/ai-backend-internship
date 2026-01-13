# Docker Setup Guide

## Prerequisites Installation

### Step 1: Install Docker Desktop for Windows

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Run the installer: `Docker Desktop Installer.exe`

2. **Installation Options**
   - ✅ Enable WSL 2 (recommended)
   - ✅ Use WSL 2 instead of Hyper-V
   - Follow the installation wizard

3. **Post-Installation**
   - Restart your computer when prompted
   - Launch Docker Desktop from Start Menu
   - Wait for "Docker Desktop is running" notification (green whale icon in system tray)

4. **Verify Installation**
   ```powershell
   docker --version
   # Expected: Docker version 24.x.x or higher
   
   docker-compose --version
   # Expected: Docker Compose version v2.x.x or higher
   ```

### Step 2: Configure WSL 2 (if not automatically configured)

If Docker requires WSL 2 setup:

```powershell
# Run PowerShell as Administrator
wsl --install
wsl --set-default-version 2
```

Restart your computer after WSL installation.

---

## Running the Application

### Option 1: Quick Start (Recommended)

```powershell
# Navigate to project directory
cd C:\ai-backend-internship

# Build and start all services
docker-compose up --build
```

This will:
- Build the FastAPI application image
- Pull MySQL 8.0 image
- Create network and volumes
- Start both containers
- Initialize the database

### Option 2: Run in Background (Detached Mode)

```powershell
docker-compose up --build -d
```

View logs:
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f mysql
```

---

## Accessing the Application

Once containers are running:

- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000
- **MySQL**: localhost:3306
  - Username: `root`
  - Password: `gameswerelifedude`
  - Database: `ai_backend`

---

## Common Commands

### Container Management

```powershell
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v

# Restart services
docker-compose restart

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a
```

### Logs and Debugging

```powershell
# Follow logs in real-time
docker-compose logs -f

# Last 100 lines of logs
docker-compose logs --tail=100

# Execute commands inside container
docker exec -it ai-backend-app bash

# Connect to MySQL container
docker exec -it ai-backend-mysql mysql -u root -p
```

### Database Management

```powershell
# Create tables (run inside app container)
docker exec -it ai-backend-app python -m app.create_tables

# Check database connection
docker exec -it ai-backend-app python -m app.test_db
```

---

## Persistent Data

Data is stored in Docker volumes:

- `mysql_data`: MySQL database files
- `uploaded_documents`: User-uploaded files
- `vector_index.faiss`: FAISS vector index (bind mount)
- `chunk_metadata.pkl`: Chunk metadata (bind mount)

To backup FAISS index:
```powershell
# Files are in your project root
copy vector_index.faiss vector_index.backup.faiss
copy chunk_metadata.pkl chunk_metadata.backup.pkl
```

---

## Troubleshooting

### Port Already in Use

If port 3306 or 8000 is already in use:

```powershell
# Find process using port 3306
netstat -ano | findstr :3306

# Kill process (replace PID)
taskkill /PID <PID> /F
```

Or modify `docker-compose.yml` ports:
```yaml
ports:
  - "3307:3306"  # Use 3307 instead
```

### Container Fails to Start

```powershell
# View detailed error logs
docker-compose logs app

# Check container status
docker ps -a

# Rebuild without cache
docker-compose build --no-cache
docker-compose up
```

### Database Connection Errors

Wait for MySQL healthcheck to pass:
```powershell
docker-compose logs mysql | findstr "ready for connections"
```

If timeout issues, increase healthcheck retries in `docker-compose.yml`.

### Permission Issues with Volumes

If FAISS files can't be written:
```powershell
# Remove read-only attribute
attrib -r vector_index.faiss
attrib -r chunk_metadata.pkl
```

---

## Development Workflow

### Making Code Changes

1. **Stop containers**:
   ```powershell
   docker-compose down
   ```

2. **Edit code** in `app/` directory

3. **Rebuild and restart**:
   ```powershell
   docker-compose up --build
   ```

### Live Reload (Development)

Modify `docker-compose.yml` to add volume mount:
```yaml
services:
  app:
    volumes:
      - ./app:/app/app  # Mount source code
      - ./vector_index.faiss:/app/vector_index.faiss
      - ./chunk_metadata.pkl:/app/chunk_metadata.pkl
```

Change Dockerfile CMD:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## Production Deployment

### Environment Variables

Create `.env.prod` for production:
```env
DB_USER=admin
DB_PASSWORD=<strong-password>
DB_HOST=mysql
DB_PORT=3306
DB_NAME=ai_backend

AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_VERSION=<version>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
```

Use in docker-compose:
```yaml
services:
  app:
    env_file:
      - .env.prod
```

### Security Hardening

1. Change MySQL root password
2. Create non-root database user
3. Use secrets management (Docker secrets)
4. Enable HTTPS with reverse proxy (nginx)
5. Implement rate limiting

---

## Testing the Setup

### 1. Check Services Health

```powershell
# All containers running
docker ps

# MySQL is ready
docker exec ai-backend-mysql mysqladmin ping -h localhost

# App is responding
curl http://localhost:8000
```

### 2. Create a User

```powershell
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d "{\"name\":\"TestUser\",\"email\":\"test@example.com\"}"
```

### 3. Upload a Document

```powershell
curl -X POST "http://localhost:8000/documents/upload?owner_id=1" -F "file=@sample.pdf"
```

### 4. Query with RAG

```powershell
curl -X POST http://localhost:8000/ai/ask -H "Content-Type: application/json" -d "{\"question\":\"What is in my document?\",\"owner_id\":1}"
```

---

## Cleanup

### Remove All Docker Resources

```powershell
# Stop and remove containers, networks
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Remove Docker images
docker rmi ai-backend-internship-app
docker rmi mysql:8.0

# Prune unused resources
docker system prune -a
```

---

## Next Steps

1. ✅ Install Docker Desktop
2. ✅ Run `docker-compose up --build`
3. ✅ Access http://localhost:8000/docs
4. ✅ Test API endpoints
5. ✅ Upload documents and test RAG
6. Consider adding CI/CD pipeline for automated deployments

---

## Support

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **MySQL Docker**: https://hub.docker.com/_/mysql

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   FastAPI    │◄───┤    MySQL     │  │
│  │     App      │    │   Database   │  │
│  │  Port: 8000  │    │  Port: 3306  │  │
│  └──────────────┘    └──────────────┘  │
│         │                    │          │
│         │                    │          │
│  ┌──────▼─────┐      ┌──────▼──────┐  │
│  │   Volume   │      │   Volume    │  │
│  │  FAISS +   │      │ mysql_data  │  │
│  │   Docs     │      └─────────────┘  │
│  └────────────┘                        │
└─────────────────────────────────────────┘
            ▲
            │
    Exposed Ports
    (localhost:8000, :3306)
```
