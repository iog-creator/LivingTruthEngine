# Living Truth Engine - Troubleshooting Guide

## Overview

This troubleshooting guide covers common issues and solutions for the Living Truth Engine project, including environment setup, MCP server problems, Flowise integration, and general development issues.

## Environment Issues

### Virtual Environment Problems

#### Issue: Wrong Python Environment
**Symptoms**: Using system Python instead of `living_venv`
```
$ which python
/usr/bin/python3  # Should be /path/to/living_venv/bin/python
```

**Solution**:
```bash
# Activate the correct environment
source living_venv/bin/activate

# Verify activation
which python
# Should show: /path/to/LivingTruthEngine/living_venv/bin/python
```

#### Issue: Missing Dependencies
**Symptoms**: Import errors or missing packages
```
ModuleNotFoundError: No module named 'langchain'
```

**Solution**:
```bash
# Ensure environment is activated
source living_venv/bin/activate

# Install dependencies
pip install langchain langchain-huggingface langchain-openai langchain-community yt_dlp spacy plotly psycopg2-binary dash piper-tts serpapi requests python-dotenv

# Install spacy model
python -m spacy download en_core_web_sm
```

#### Issue: Environment Variables Not Loading
**Symptoms**: MCP server can't find API keys
```
ERROR: FLOWISE_API_KEY and FLOWISE_CHATFLOW_ID must be set in .env
```

**Solution**:
```bash
# Check .env file exists and has correct values
cat .env

# Ensure python-dotenv is installed
pip install python-dotenv

# Verify .env file is in the correct location
ls -la .env
```

## MCP Server Issues

### MCP Server Not Detected

#### Issue: MCP Server Not Appearing in Cursor
**Symptoms**: MCP server not listed in Cursor's tools

**Solution**:
1. **Check global MCP configuration**:
   ```bash
   cat ~/.cursor/mcp.json
   ```

2. **Verify MCP server path**:
   ```json
   {
     "flowise-mcp-server": {
       "command": "${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/living_venv/bin/python",
       "args": ["${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/flowise_mcp_server.py"]
     }
   }
   ```

3. **Restart Cursor IDE** to reload MCP configuration

4. **Test MCP server manually**:
   ```bash
   echo '{"method": "tools.list", "params": []}' | python flowise_mcp_server.py
   ```

#### Issue: MCP Server Tools Not Working
**Symptoms**: Tools listed but execution fails

**Solution**:
1. **Check environment variables**:
   ```bash
   source living_venv/bin/activate
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API_KEY:', os.getenv('FLOWISE_API_KEY'))"
   ```

2. **Test individual tools**:
   ```bash
   echo '{"method": "tools.execute", "params": ["get_status"]}' | python flowise_mcp_server.py
   ```

3. **Check logs**:
   ```bash
   tail -f mcp_server.log
   ```

### MCP Server Communication Errors

#### Issue: JSON-RPC Protocol Errors
**Symptoms**: Invalid JSON or protocol errors

**Solution**:
1. **Check JSON format**:
   ```bash
   echo '{"method": "tools.list", "params": []}' | python -m json.tool
   ```

2. **Verify MCP server implementation**:
   ```python
   # Check handle_request method in flowise_mcp_server.py
   def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
       # Ensure proper method handling
   ```

## Flowise Integration Issues

### Flowise Not Running

#### Issue: Flowise Installation Problems
**Symptoms**: `npm install -g flowise` fails or hangs

**Solution**:
1. **Check Node.js version**:
   ```bash
   node --version  # Should be 18.15.0+
   npm --version
   ```

2. **Use sudo for global installation**:
   ```bash
   sudo npm install -g flowise
   ```

3. **Alternative: Use Docker**:
   ```bash
   docker run -d --name flowise -p 3000:3000 flowiseai/flowise
   ```

#### Issue: Flowise Not Starting
**Symptoms**: `flowise start` fails or port 3000 unavailable

**Solution**:
1. **Check port availability**:
   ```bash
   netstat -tulpn | grep :3000
   lsof -i :3000
   ```

2. **Kill conflicting processes**:
   ```bash
   sudo kill -9 <PID>
   ```

3. **Start Flowise with specific port**:
   ```bash
   flowise start --port 3001
   ```

### Flowise API Issues

#### Issue: API Authentication Errors
**Symptoms**: 401 Unauthorized errors

**Solution**:
1. **Check API key in Flowise UI**:
   - Go to http://localhost:3000
   - Check API keys in settings
   - Copy correct API key to `.env`

2. **Verify chatflow ID**:
   - Import `living_truth_full_flow.json`
   - Copy chatflow ID to `.env`

3. **Test API manually**:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        http://localhost:3000/api/v1/chatflows
   ```

#### Issue: Graph Import Problems
**Symptoms**: Flowise graph not loading or errors

**Solution**:
1. **Check JSON format**:
   ```bash
   python -m json.tool living_truth_full_flow.json
   ```

2. **Import manually in Flowise UI**:
   - Go to http://localhost:3000
   - Click "Import" and select the JSON file
   - Configure credentials and variables

3. **Check node compatibility**:
   - Ensure all nodes are available in Flowise
   - Update to latest Flowise version

## Database Issues

### PostgreSQL Connection Problems

#### Issue: Database Connection Failed
**Symptoms**: Connection refused or authentication errors

**Solution**:
1. **Check PostgreSQL service**:
   ```bash
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   ```

2. **Verify database exists**:
   ```bash
   psql -U postgres -l | grep living_truth_engine
   ```

3. **Create database if missing**:
   ```bash
   createdb -U postgres living_truth_engine
   psql -U postgres -d living_truth_engine -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```

4. **Check connection settings in `.env`**:
   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=living_truth_engine
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=pass
   ```

### PGVector Extension Issues

#### Issue: Vector Extension Not Available
**Symptoms**: `pgvector` extension not found

**Solution**:
1. **Install pgvector**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql-14-pgvector

   # Or compile from source
   git clone https://github.com/pgvector/pgvector.git
   cd pgvector
   make
   sudo make install
   ```

2. **Enable extension**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

## Model and AI Issues

### LM Studio Problems

#### Issue: LM Studio Not Responding
**Symptoms**: Model inference errors or timeouts

**Solution**:
1. **Check LM Studio service**:
   - Ensure LM Studio is running on localhost:1234
   - Verify models are loaded

2. **Test LM Studio API**:
   ```bash
   curl http://localhost:1234/models
   ```

3. **Check model configuration**:
   - Verify Qwen3-0.6B and Qwen3-8B models are loaded
   - Check model compatibility

### Model Loading Issues

#### Issue: Models Not Found
**Symptoms**: Model loading errors or missing models

**Solution**:
1. **Download required models**:
   - text-embedding-qwen3-embedding-0.6b
   - qwen.qwen3-reranker-0.6b
   - qwen/qwen3-8b

2. **Check model paths**:
   - Verify model files are in correct location
   - Check file permissions

## Performance Issues

### Slow Query Processing

#### Issue: Long Response Times
**Symptoms**: Queries taking too long to process

**Solution**:
1. **Check system resources**:
   ```bash
   htop
   free -h
   df -h
   ```

2. **Optimize database**:
   ```sql
   ANALYZE;
   VACUUM;
   ```

3. **Check vector store indexing**:
   - Ensure proper indexes on vector columns
   - Consider batch processing for large datasets

### Memory Issues

#### Issue: Out of Memory Errors
**Symptoms**: Memory exhaustion or crashes

**Solution**:
1. **Monitor memory usage**:
   ```bash
   ps aux | grep python
   ```

2. **Optimize batch sizes**:
   - Reduce `AGI_EMBED_BATCH_SIZE` in environment
   - Process documents in smaller batches

3. **Check for memory leaks**:
   - Monitor memory usage over time
   - Restart services if needed

## Logging and Debugging

### Enable Debug Logging

#### Issue: Insufficient Log Information
**Symptoms**: Hard to diagnose problems

**Solution**:
1. **Increase log level**:
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Add more logging**:
   ```python
   logger.debug(f"Processing query: {query}")
   logger.info(f"API response: {response.status_code}")
   ```

3. **Check log files**:
   ```bash
   tail -f mcp_server.log
   tail -f logs/flowise.log
   ```

### Common Error Messages

#### "ModuleNotFoundError"
**Solution**: Install missing package in `living_venv`

#### "Connection refused"
**Solution**: Check if service is running and port is available

#### "Permission denied"
**Solution**: Check file permissions and user access

#### "Invalid JSON"
**Solution**: Validate JSON format and syntax

## Getting Help

### Self-Diagnosis Steps
1. **Check environment**: Ensure `living_venv` is activated
2. **Verify services**: Confirm all services are running
3. **Check logs**: Review error logs for specific issues
4. **Test components**: Test individual components separately
5. **Validate configuration**: Check all configuration files

### External Resources
- **Flowise Documentation**: https://docs.flowiseai.com/
- **LangChain Documentation**: https://python.langchain.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Cursor Documentation**: https://docs.cursor.com/

### Support Channels
- **Project Issues**: Create issue in project repository
- **Community Forums**: Check relevant community forums
- **Documentation**: Review project documentation
- **Logs**: Share relevant log files for debugging 