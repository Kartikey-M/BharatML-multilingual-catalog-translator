# 🚀 Multi-Lingual Catalog Translator - Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Current Status Verification
- [x] Real IndicTrans2 models working
- [x] Backend API running on port 8001
- [x] Frontend running on port 8501
- [x] Database properly initialized
- [x] Language mapping working correctly

### ✅ Required Files Check
- [x] Backend requirements.txt
- [x] Frontend requirements.txt
- [x] Environment configuration (.env)
- [x] IndicTrans2 models downloaded
- [x] Database schema ready

---

## 🎯 Deployment Options (Choose Your Level)

### 🟢 **Option 1: Quick Demo Deployment (5 minutes)**
*Perfect for interviews and quick demos*

### 🟡 **Option 2: Docker Deployment (15 minutes)**
*Professional containerized deployment*

### 🔴 **Option 3: Cloud Production Deployment (30+ minutes)**
*Full production-ready deployment*

---

## 🟢 **Option 1: Quick Demo Deployment**

### Step 1: Create Startup Scripts

**Windows (startup.bat):**
```batch
@echo off
echo Starting Multi-Lingual Catalog Translator...

echo Starting Backend...
start "Backend" cmd /k "cd backend && uvicorn main:app --host 0.0.0.0 --port 8001"

echo Waiting for backend to start...
timeout /t 5

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && streamlit run app.py --server.port 8501"

echo.
echo ✅ Deployment Complete!
echo.
echo 🔗 Frontend: http://localhost:8501
echo 🔗 Backend API: http://localhost:8001
echo 🔗 API Docs: http://localhost:8001/docs
echo.
echo Press any key to stop all services...
pause
taskkill /f /im python.exe
```

**Linux/Mac (startup.sh):**
```bash
#!/bin/bash
echo "Starting Multi-Lingual Catalog Translator..."

# Start backend in background
echo "Starting Backend..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting Frontend..."
cd ../frontend
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🔗 Frontend: http://localhost:8501"
echo "🔗 Backend API: http://localhost:8001"
echo "🔗 API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

### Step 2: Environment Setup
```bash
# Create production environment file
cp .env .env.production

# Update for production
echo "MODEL_TYPE=indictrans2" >> .env.production
echo "MODEL_PATH=models/indictrans2" >> .env.production
echo "DEVICE=cpu" >> .env.production
echo "DATABASE_PATH=data/translations.db" >> .env.production
```

### Step 3: Quick Start
```bash
# Make script executable (Linux/Mac)
chmod +x startup.sh
./startup.sh

# Or run directly (Windows)
startup.bat
```

---

## 🟡 **Option 2: Docker Deployment**

### Step 1: Create Dockerfiles

**Backend Dockerfile:**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD curl -f http://localhost:8001/ || exit 1

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Frontend Dockerfile:**
```dockerfile
# frontend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
      - ./.env:/app/.env
    environment:
      - MODEL_TYPE=indictrans2
      - MODEL_PATH=models/indictrans2
      - DEVICE=cpu
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    depends_on:
      backend:
        condition: service_healthy
    environment:
      - API_BASE_URL=http://backend:8001
    restart: unless-stopped

  # Optional: Add database service
  # postgres:
  #   image: postgres:15
  #   environment:
  #     POSTGRES_DB: translations
  #     POSTGRES_USER: translator
  #     POSTGRES_PASSWORD: secure_password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

volumes:
  postgres_data:

networks:
  default:
    name: translator_network
```

### Step 3: Build and Deploy
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🔴 **Option 3: Cloud Production Deployment**

### 🔵 **3A: AWS Deployment**

#### Prerequisites
```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure
```

#### ECS Deployment
```bash
# Create ECR repositories
aws ecr create-repository --repository-name translator-backend
aws ecr create-repository --repository-name translator-frontend

# Get login token
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

# Build and push images
docker build -t translator-backend ./backend
docker tag translator-backend:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/translator-backend:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/translator-backend:latest

docker build -t translator-frontend ./frontend
docker tag translator-frontend:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/translator-frontend:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/translator-frontend:latest
```

### 🔵 **3B: Google Cloud Platform Deployment**

#### Cloud Run Deployment
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy backend
gcloud run deploy translator-backend \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10

# Build and deploy frontend
gcloud run deploy translator-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 5
```

### 🔵 **3C: Heroku Deployment**

#### Backend Deployment
```bash
# Install Heroku CLI
# Create Procfile for backend
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# Create Heroku app
heroku create translator-backend-app

# Add Python buildpack
heroku buildpacks:set heroku/python -a translator-backend-app

# Set environment variables
heroku config:set MODEL_TYPE=indictrans2 -a translator-backend-app
heroku config:set MODEL_PATH=models/indictrans2 -a translator-backend-app

# Deploy
cd backend
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a translator-backend-app
git push heroku main
```

#### Frontend Deployment
```bash
# Create Procfile for frontend
echo "web: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0" > frontend/Procfile

# Create Heroku app
heroku create translator-frontend-app

# Deploy
cd frontend
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a translator-frontend-app
git push heroku main
```

---

## 🛠️ **Production Optimizations**

### 1. Environment Configuration
```bash
# .env.production
MODEL_TYPE=indictrans2
MODEL_PATH=/app/models/indictrans2
DEVICE=cpu
DATABASE_URL=postgresql://user:pass@localhost/translations
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
```

### 2. Nginx Configuration
```nginx
# nginx.conf
upstream backend {
    server backend:8001;
}

upstream frontend {
    server frontend:8501;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Database Migration
```python
# migrations/001_initial.py
def upgrade():
    """Create initial tables"""
    # Add database migration logic here
    pass

def downgrade():
    """Remove initial tables"""
    # Add rollback logic here
    pass
```

---

## 📊 **Monitoring & Maintenance**

### Health Checks
```bash
# Check backend health
curl http://localhost:8001/

# Check frontend health
curl http://localhost:8501/_stcore/health

# Check model loading
curl http://localhost:8001/supported-languages
```

### Log Management
```bash
# View Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Save logs to file
docker-compose logs > deployment.log
```

### Performance Monitoring
```python
# Add to backend/main.py
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

## 🎯 **Recommended Deployment Path**

### For Interview Demo:
1. **Start with Option 1** (Quick Demo) - Shows it works end-to-end
2. **Mention Option 2** (Docker) - Shows production awareness
3. **Discuss Option 3** (Cloud) - Shows scalability thinking

### For Production:
1. **Use Option 2** (Docker) for consistent environments
2. **Add monitoring and logging**
3. **Set up CI/CD pipeline**
4. **Implement proper security measures**

---

## 🚀 **Next Steps After Deployment**

1. **Performance Testing** - Load test the APIs
2. **Security Audit** - Check for vulnerabilities
3. **Backup Strategy** - Database and model backups
4. **Monitoring Setup** - Alerts and dashboards
5. **Documentation** - API docs and user guides

Would you like me to help you with any specific deployment option?
