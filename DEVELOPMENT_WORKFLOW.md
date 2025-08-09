# Development Workflow for Experimentation

## 🎯 **Branching Strategy**

### **Current Branches**
- **`master`**: Stable, production-ready code
- **`dev/experimentation`**: Active development and experimentation

### **Branch Protection**
- **`master`**: Protected - requires pull request and review
- **`dev/experimentation`**: Open for experimentation and breaking changes

## 🔄 **Development Workflow**

### **Starting New Experiments**
```bash
# Ensure you're on the experimentation branch
git checkout dev/experimentation

# Create feature-specific branches for major experiments
git checkout -b feature/experiment-name

# Make your changes and experiment freely
# ... experiment and break things ...

# Commit your changes
git add .
git commit -m "feat: Experiment with [description]"

# Push to remote
git push origin feature/experiment-name
```

### **Merging Successful Experiments**
```bash
# When experiment is successful, merge back to dev/experimentation
git checkout dev/experimentation
git merge feature/experiment-name

# Push updates
git push origin dev/experimentation

# Clean up feature branch
git branch -d feature/experiment-name
git push origin --delete feature/experiment-name
```

### **Promoting to Master**
```bash
# When dev/experimentation is stable, create pull request to master
# Via GitHub: https://github.com/iog-creator/LivingTruthEngine/pull/new/dev/experimentation

# Or via command line (after PR approval)
git checkout master
git merge dev/experimentation
git push origin master
```

## 🧪 **Experimentation Guidelines**

### **Safe Experimentation Practices**
1. **Always work on `dev/experimentation` or feature branches**
2. **Never experiment directly on `master`**
3. **Commit frequently** with descriptive messages
4. **Test thoroughly** before merging back
5. **Document your experiments** in commit messages

### **Breaking Changes Protocol**
1. **Create feature branch** for major breaking changes
2. **Update documentation** to reflect changes
3. **Test thoroughly** before merging
4. **Communicate changes** in commit messages
5. **Consider rollback strategy** for major changes

### **MCP Hub Server Experimentation**
```bash
# Test MCP Hub Server changes
python3 src/mcp_servers/mcp_hub_server.py

# Validate registry after changes
python3 scripts/setup/regenerate_tool_registry.py

# Test enhanced features
python3 -c "import sys; sys.path.append('src'); from mcp_servers.mcp_hub_server import MCPHubServer; server = MCPHubServer(); print('✅ Server loaded successfully')"
```

## 📋 **Current Experimentation Status**

### **Branch Status**
- **Current Branch**: `dev/experimentation`
- **Base Branch**: `master` (stable)
- **Status**: Ready for experimentation

### **Safe to Experiment With**
- ✅ MCP Hub Server features and tools
- ✅ Docker configurations and services
- ✅ Langflow workflows and integrations
- ✅ Cursor rules and documentation
- ✅ Testing scripts and validation

### **Protected Areas**
- ⚠️ Core database schemas (backup first)
- ⚠️ Production environment variables
- ⚠️ Critical service configurations

## 🚀 **Quick Start for Experiments**

### **1. Start Experimenting**
```bash
# You're already on dev/experimentation branch
# Start making changes and breaking things!
```

### **2. Test Your Changes**
```bash
# Test MCP Hub Server
python3 src/mcp_servers/mcp_hub_server.py

# Test Docker services
docker compose -f docker/docker-compose.yml up -d

# Test functional tests
python3 scripts/testing/functional_tests.py
```

### **3. Commit Your Experiments**
```bash
git add .
git commit -m "experiment: [describe what you're testing]"
git push origin dev/experimentation
```

### **4. Rollback if Needed**
```bash
# If experiment goes wrong, reset to last good state
git reset --hard HEAD~1
git push --force origin dev/experimentation
```

## 📊 **Experiment Tracking**

### **Current Experiments**
- [ ] List your experiments here
- [ ] Track progress and results
- [ ] Document successful approaches

### **Experiment Log**
```bash
# View experiment history
git log --oneline dev/experimentation

# View specific experiment changes
git show <commit-hash>
```

---

**🎯 Ready to Start Experimenting!**

You're now on the `dev/experimentation` branch and can safely break things without affecting the stable `master` branch. Go ahead and start experimenting with new features, breaking changes, and innovative approaches! 