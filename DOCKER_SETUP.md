# Living Truth Engine - Docker Setup Guide

## 🐳 Overview

This guide provides step-by-step instructions for setting up the Living Truth Engine using Docker containers. This approach ensures consistent environments across different systems and simplifies deployment.

## 📋 Prerequisites

- Linux system (Ubuntu/Debian recommended)
- User with sudo privileges
- Internet connection for downloading Docker images

## 🚀 Quick Start

### 1. Run the Setup Script

```bash
# Make sure you're in the LivingTruthEngine directory
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine

# Activate the virtual environment
source living_venv/bin/activate

# Run the Docker setup script
./setup_docker.sh
```

### 2. Manual Setup (if script fails)

If the automated script doesn't work, follow these manual steps:

#### Install Docker
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Important**: Log out and back in after adding user to docker group.

#### Create Directories
```bash
mkdir -p logs config tests docs scripts models .flowise
```

#### Update Environment Variables
Edit the `.env` file with your actual API keys:
```bash
nano .env
```

#### Start Services
```bash
docker-compose up -d --build
```

## 🏗️ Architecture

The Docker setup includes the following services:

### Core Services
- **Flowise** (Port 3000): AI workflow orchestration
- **PostgreSQL** (Port 5432): Database with pgvector extension
- **LM Studio** (Port 1234): Local model inference
- **Dashboard** (Port 8050): Web-based monitoring interface

### Supporting Services
- **MCP Server**: Model Context Protocol server
- **Redis**: Caching and session management

## 📁 Directory Structure

```
LivingTruthEngine/
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Python application container
├── requirements.txt            # Python dependencies
├── setup_docker.sh            # Automated setup script
├── dashboard.py               # Dash web dashboard
├── flowise_mcp_server.py      # MCP server implementation
├── living_truth_full_flow.json # Flowise workflow
├── living_truth_config.json   # Application configuration
├── .env                       # Environment variables
├── .cursor/                   # Cursor IDE configuration
├── sources/                   # Data sources
├── visualizations/            # Generated visualizations
├── logs/                      # Application logs
├── config/                    # Configuration files
├── tests/                     # Test files
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── models/                    # AI models
└── .flowise/                  # Flowise data
```

## 🔧 Configuration

### Environment Variables

The following environment variables need to be configured in `.env`:

#### Required API Keys
- `FLOWISE_API_KEY`: Your Flowise API key
- `LANGCHAIN_API_KEY`: Your LangSmith API key
- `SERP_API_KEY`: Your SerpAPI key

#### Service Configuration
- `FLOWISE_CHATFLOW_ID`: ID of your Flowise chatflow
- `POSTGRES_PASSWORD`: Database password
- `DASHBOARD_PORT`: Dashboard port (default: 8050)

### Service URLs

Once running, services will be available at:
- **Flowise**: http://localhost:3000
- **Dashboard**: http://localhost:8050
- **LM Studio**: http://localhost:1234
- **PostgreSQL**: localhost:5432

## 🛠️ Management Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs flowise
docker-compose logs postgres
docker-compose logs dashboard
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild Services
```bash
docker-compose up -d --build
```

### Check Service Status
```bash
docker-compose ps
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### 2. Port Already in Use
```bash
# Check what's using the port
sudo netstat -tulpn | grep :3000

# Stop conflicting service or change port in docker-compose.yml
```

#### 3. Docker Service Not Running
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### 4. Insufficient Disk Space
```bash
# Clean up Docker images
docker system prune -a

# Check disk usage
df -h
```

### Health Checks

Each service includes health checks. Monitor them with:
```bash
docker-compose ps
```

### Log Analysis

Check logs for errors:
```bash
# Recent logs
docker-compose logs --tail=100

# Follow logs in real-time
docker-compose logs -f
```

## 🔄 Development Workflow

### 1. Code Changes
Make changes to your Python files in the project directory.

### 2. Rebuild and Restart
```bash
docker-compose up -d --build
```

### 3. Test Changes
Access the dashboard at http://localhost:8050

### 4. View Logs
```bash
docker-compose logs -f dashboard
```

## 📊 Monitoring

### Dashboard
Access the web dashboard at http://localhost:8050 for:
- System health monitoring
- Performance metrics
- Real-time logs
- Service status

### Health Checks
All services include health checks that monitor:
- Service availability
- Response times
- Error rates
- Resource usage

## 🔐 Security

### Network Security
- Services are isolated in Docker networks
- Only necessary ports are exposed
- Internal communication uses Docker networking

### Data Security
- Database passwords are stored in environment variables
- API keys are kept secure in `.env` file
- Volumes are properly mounted for data persistence

### Access Control
- Services run with minimal required privileges
- User permissions are properly configured
- Docker group membership is required

## 🚀 Production Deployment

For production deployment:

1. **Update Environment Variables**
   - Use strong passwords
   - Configure proper API keys
   - Set appropriate log levels

2. **Configure Reverse Proxy**
   - Set up nginx or Apache
   - Configure SSL certificates
   - Set up proper domain names

3. **Monitoring and Logging**
   - Configure external monitoring
   - Set up log aggregation
   - Configure alerts

4. **Backup Strategy**
   - Configure database backups
   - Set up volume backups
   - Test recovery procedures

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review service logs
3. Verify environment configuration
4. Check Docker and system resources

For additional help, refer to the main project documentation or create an issue in the project repository. 