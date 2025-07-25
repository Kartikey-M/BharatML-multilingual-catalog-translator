# 🚀 Quick Deployment Guide

## 🎯 Choose Your Deployment Method

### 🟢 **Option 1: Quick Demo (Recommended for Interviews)**
Perfect for demonstrations and quick testing.

**Windows:**
```bash
# Double-click or run:
start_demo.bat
```

**Linux/Mac:**
```bash
./start_demo.sh
```

**What it does:**
- Starts backend on port 8001
- Starts frontend on port 8501
- Opens browser automatically
- Shows progress in separate windows

---

### 🟡 **Option 2: Docker Deployment (Recommended for Production)**
Professional containerized deployment.

**Prerequisites:**
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Windows:**
```bash
# Double-click or run:
deploy_docker.bat
```

**Linux/Mac:**
```bash
./deploy_docker.sh
```

**What it does:**
- Builds Docker containers
- Sets up networking
- Provides health checks
- Includes nginx reverse proxy (optional)

---

## 📊 **Check Deployment Status**

**Windows:**
```bash
check_status.bat
```

**Linux/Mac:**
```bash
curl http://localhost:8001/    # Backend health
curl http://localhost:8501/    # Frontend health
```

---

## 🔗 **Access Your Application**

Once deployed, access these URLs:

- **🎨 Frontend UI:** http://localhost:8501
- **⚡ Backend API:** http://localhost:8001  
- **📚 API Documentation:** http://localhost:8001/docs

---

## 🛑 **Stop Services**

**Quick Demo:**
- Windows: Run `stop_services.bat` or close command windows
- Linux/Mac: Press `Ctrl+C` in terminal

**Docker:**
```bash
docker-compose down
```

---

## 🆘 **Troubleshooting**

### Common Issues:

1. **Port already in use:**
   ```bash
   # Kill existing processes
   taskkill /f /im python.exe     # Windows
   pkill -f python                # Linux/Mac
   ```

2. **Models not loading:**
   - Check if `models/indictrans2/` directory exists
   - Ensure models were downloaded properly
   - Check backend logs for errors

3. **Frontend can't connect to backend:**
   - Verify backend is running on port 8001
   - Check `frontend/app.py` has correct API_BASE_URL

4. **Docker issues:**
   ```bash
   # Check Docker status
   docker ps
   docker-compose logs
   
   # Reset Docker
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

---

## 🔧 **Configuration**

### Environment Variables:
Create `.env` file in root directory:
```bash
MODEL_TYPE=indictrans2
MODEL_PATH=models/indictrans2
DEVICE=cpu
DATABASE_PATH=data/translations.db
```

### For Production:
- Copy `.env.production` to `.env`
- Update database settings
- Configure CORS origins
- Set up monitoring

---

## 📈 **Performance Tips**

1. **Use GPU if available:**
   ```bash
   DEVICE=cuda  # in .env file
   ```

2. **Increase memory for Docker:**
   - Docker Desktop → Settings → Resources → Memory: 8GB+

3. **Monitor resource usage:**
   ```bash
   docker stats           # Docker containers
   htop                   # System resources
   ```

---

## 🎉 **Success Indicators**

✅ **Deployment Successful When:**
- Backend responds at http://localhost:8001
- Frontend loads at http://localhost:8501  
- Can translate "Hello" to Hindi
- API docs accessible at http://localhost:8001/docs
- No error messages in logs

---

## 🆘 **Need Help?**

1. Check the logs:
   - Quick Demo: Look at command windows
   - Docker: `docker-compose logs -f`

2. Verify prerequisites:
   - Python 3.11+ installed
   - All dependencies in requirements.txt
   - Models downloaded in correct location

3. Test individual components:
   - Backend: `curl http://localhost:8001/`
   - Frontend: Open browser to http://localhost:8501

---

**🎯 For Interview Demos: Use Quick Demo option - it's fastest and shows everything working!**
