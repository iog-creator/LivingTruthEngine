# Cursor Rules Consolidated

**Generated:** 2025-08-16 09:30:09
**Total Rules:** 34

## Purpose
This file contains all active Cursor rules from `.cursor/rules/` folder,
consolidated for refactoring and reorganization purposes.

## Rules Index

1. **Canon** (`00-global.mdc`)
   - Phase: 9.5.7.4.10
   - Scope: N/A
   - Summary: No summary available

2. **docker/docker-compose.yml** (`ai_integration.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: {e}")

3. **Analysis Scripts and MCP-First Batching** (`analysis_batching.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

4. **API Contracts** (`api_contracts.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

5. **Automated Development Management** (`automated_development_management.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

6. **Coding Standards for AI-Assisted Development** (`coding_standards.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: string;

7. **Complete Analysis Pipeline** (`complete_analysis_pipeline.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

8. **Core Workflow (Phase 9)** (`core_workflow.mdc`)
   - Phase: 1) `validate_cursor_rules`
   - Scope: N/A
   - Summary: No summary available

9. **Cursor AppArmor Fix for Ubuntu** (`cursor_apparmor_fix.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

10. **Database Schema Consistency** (`database_schema_consistency.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

11. **Docker Best Practices for Living Truth Engine** (`docker_best_practices.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

12. **Docker Health Check Best Practices** (`docker_health_checks.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

13. **Compose Rules** (`docker_management.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

14. **Error Handling and Testing Standards** (`error_handling_and_testing.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

15. **Fallbacks & Health** (`fallbacks_and_health.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

16. **How to Build Cursor Rules - Complete Guide** (`how_to_make_a_cursor_rule.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

17. **Living Truth Agent Integration Process** (`living_truth_agent_integration.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

18. **Master Log Rebuild Rule** (`master_log.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: **

19. **SSOT Requirement (hard fail)** (`mcp_enforcement.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

20. **MCP Hub Server - Current Status and Usage** (`mcp_hub_server_status.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

21. **MCP-First Development** (`mcp_integration.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

22. **MCP-first Operations** (`mcp_ops.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

23. **MCP Server Integration and Best Practices** (`mcp_server_integration.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

24. **Models & Embeddings (SSOT)** (`models_and_embeddings.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

25. **Project Overview** (`project_overview.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

26. **Resilience Dashboard UI Development** (`resilience_dashboard_ui.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

27. **Policy** (`ssot_meta_index.mdc`)
   - Phase: 9.5.7.4.12
   - Scope: N/A
   - Summary: No summary available

28. **System Integration Status** (`system_integration_status.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

29. **System Management and Automation** (`system_management.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

30. **System Status (Updated: 2025-08-13 21:30:00)** (`system_status.mdc`)
   - Phase: 9.5.4 - Performance Gates
   - Scope: N/A
   - Summary: No summary available

31. **Testing Standards** (`testing_standards.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

32. **UI Policy** (`ui_policy.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

33. **Veritas Generalist Ingestion Runner - Development Guidelines** (`veritas_runs.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

34. **Visualization System Integration** (`visualization_system.mdc`)
   - Phase: N/A
   - Scope: N/A
   - Summary: No summary available

---

## Consolidated Rules Content

### 1. Canon
**File:** `00-global.mdc`

**Metadata:**
- phase: 9.5.7.4.10

**Content:**
```mdc
---
description: 00-Global rule for Living Truth Engine
alwaysApply: true
---

### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'always',
 'checksum': '070121f881cc1e43d36fbc3d6d206cfd15282d5e5d442a5dbf8f08145a63ac29',
 'enforcement': 'strict',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': '00-global',
 'scope': 'all',
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: 00-global',
 'updated': '2025-08-15',
 'version': 1}
```

### SSOT Meta

```yaml
owner: researcher-ssot
severity: critical
tags: [ssot, global, enforcement, rules]
phase: 9.5.7.4.10
dependsOn: [verify-complete-ssot, mcp-router-check]
autofixAllowed: false
notes: "Global rule that enforces SSOT gates on every commit"
```

# Canon
- **SSOT bundle (root only)**: `README.md`, `project_master_log.md`, `MCP_REQUIREMENTS_REFERENCE.md`,
  `SERVICES_MANIFEST.md`, and all `PHASE_*_COMPLETION_SUMMARY.md`.
- **Envelope**: APIs/tools return `{status, data?, error?}`.
- **Commit-complete**: code + tests + docs + rules updated together.

## SSOT Enforcement (permanent)
- **Before edits**: load SSOT files into context and run:
```bash
python scripts/verify_ssot_bundle.py
```
- **After edits**: re-run the same command. On failure: stop and fix.
- **Commit message**: include `[SSOT Verified]` once checks pass.

## ENFORCED WORKFLOW (CRITICAL)
**MANDATORY STEPS - NO EXCEPTIONS:**
1. **Pre-change validation**: `python scripts/verify_complete_ssot_system.py --fix`
2. **Make changes** (code, docs, rules)
3. **Post-change validation**: `python scripts/verify_complete_ssot_system.py --fix`
4. **Only then commit**: `git commit -m "[SSOT Verified] <message>"`
5. **Block completion** if any validation fails

**VIOLATION = IMMEDIATE STOP AND FIX**

## Tool Rituals (run & show output)
- **Complete SSOT System** (REQUIRED for all changes):
  - `python scripts/verify_complete_ssot_system.py` (comprehensive validation + auto-fix)
- **Repo health** (if needed):
  - `python scripts/verify_compose_healthchecks.py || true`
  - `python scripts/audit_models.py || true`
- **UI / Playwright** (any UI change):
  - `npx playwright test --reporter=list` (use `data-testid` selectors)

## Branch & PR Discipline (fork-first)
- Work on feature branches in the **fork**; open PRs to fork default branch.
- PRs must show green for **SSOT Guard** and **Repo Health** workflows.
- Use `PULL_REQUEST_TEMPLATE.md` checklist.

## What NOT to do
- No duplicate SSOT files under `docs/` or `archive/docs/`.
- No UI changes without Playwright specs.
- No phase closeouts without updated SSOT + `[SSOT Verified]` commit.

## LM Studio Helper (Local Only)
- **Purpose**: LM Studio is a **helper agent** for analysis and patch drafting
- **Safety**: LM Studio is **read-only** - it suggests changes but never applies them
- **Integration Methods**:
  1. **HTTP Bridge** (`make lm-tools`): For tool-based analysis
  2. **MCP Server** (`make lm-mcp`): For conversational interaction  
  3. **SSOT Agent** (`make ssot-agent`): For automated workflows
- **Workflow**: LM Studio analyzes → Cursor applies → SSOT validates → Commit
- **Never apply writes from LM Studio**. All edits must pass:
```bash
python scripts/verify_complete_ssot_system.py
```
and commit with `[SSOT Verified]`.

## SSOT Scope Discipline
- Pre-edit check: `python scripts/verify_complete_ssot_system.py --scope fast`
- Post-fix gate: `python scripts/verify_complete_ssot_system.py --scope full` (local) or CI nightly full.
- # SSOT Requirement (hard fail)
- Command to run **before** approving/merging:
```bash
python scripts/verify_complete_ssot_system.py --fix
```
- On any failure: **stop** and remediate. Approvals are blocked until PASS.

# Commit Discipline
- Require `[SSOT Verified]` in commit message once SSOT checks pass.

# Prohibited
- Duplicate SSOT files outside root.
- Merging with failing SSOT Guard or Repo Health checks.
```bash
python scripts/verify_complete_ssot_system.py
```
and commit with `[SSOT Verified]`.

## SSOT Scope Discipline
- Pre-edit check: `python scripts/verify_complete_ssot_system.py --scope fast`
- Post-fix gate: `python scripts/verify_complete_ssot_system.py --scope full` (local) or CI nightly full.

## SSOT Scope Discipline
- Pre-edit check: `python scripts/verify_complete_ssot_system.py --scope fast`
- Post-fix gate: `python scripts/verify_complete_ssot_system.py --scope full` (local) or CI nightly full.
```

---

### 2. docker/docker-compose.yml
**File:** `ai_integration.mdc`

**Metadata:**
- summary: {e}")

**Content:**
```mdc
---
description: Ai Integration rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'ac0c3ddda2a4156b66487927d40d02d47d8c9a42ee7abcaeec5f243da7e05345',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'ai_integration',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: ai_integration',
 'updated': '2025-08-15',
 'version': 1}
```

#AI Integration Patterns

## Overview
The Living Truth Engine integrates with desktop LM Studio for real AI analysis, providing actual LLM generation instead of pattern matching.

## 🎯 **Key Components**

### **LM Studio Integration**
- **Desktop Version**: Port 1234 for real AI generation
- **Docker Version**: Port 1235 for containerized inference
- **Network Configuration**: `host.docker.internal:1234` for container-to-desktop communication
- **Model**: `qwen/qwen3-8b` for text generation

### **MCP Tools**
- **`analyze_veritas_summary`**: Real AI-powered document summarization
- **`analyze_veritas_claims`**: AI-powered claim extraction and categorization
- **`generate_lm_studio_text`**: Direct LLM text generation
- **`create_3d_network_visualization`**: AI-enhanced visualization generation

### **API Endpoints**
- **`/api/ai/chat`**: Direct chat with LM Studio models
- **`/api/execute`**: Execute MCP tools with AI capabilities
- **`/api/health/full`**: System health including AI service status

## 🔧 **Configuration**

### **Docker Configuration**
```yaml
# docker/docker-compose.yml
services:
  dashboard:
    environment:
      - LM_STUDIO_ENDPOINT=http://host.docker.internal:1234
    extra_hosts:
      - "host.docker.internal:host-gateway"
  
  lm-studio:
    ports:
      - "1235:1234"  # Docker version on different port
```

### **Environment Variables**
```bash
# .env
LM_STUDIO_ENDPOINT=http://localhost:1234  # Desktop version
DOCKER_ENVIRONMENT=false  # Use localhost vs container names
```

## 🚀 **Usage Patterns**

### **Real AI Analysis**
```python
def _generate_ai_summary(self, text: str, title: str) -> dict:
    """Generate AI-powered summary using real LLM generation."""
    try:
        prompt = f"""Please analyze this survivor testimony and provide a comprehensive summary.

Title: {title}
Text: {text[:2000]}

Please provide:
1. A concise summary (2-3 sentences)
2. 3-5 key points
3. Overall sentiment (Positive/Negative/Neutral)

Format your response as JSON:
{{
    "summary": "brief summary here",
    "key_points": ["point 1", "point 2", "point 3"],
    "sentiment": "Positive/Negative/Neutral"
}}"""

        response = requests.post(
            f"{self.lm_studio_endpoint}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "qwen/qwen3-8b",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                parsed = json.loads(content)
                return {
                    "summary": parsed.get("summary", "AI analysis completed"),
                    "key_points": parsed.get("key_points", []),
                    "sentiment": parsed.get("sentiment", "Neutral")
                }
            except json.JSONDecodeError:
                return self._fallback_summary(text, title)
        else:
            return self._fallback_summary(text, title)
            
    except Exception as e:
        logger.error(f"Error generating AI summary: {e}")
        return self._fallback_summary(text, title)
```

### **AI Chat Integration**
```python
@self.app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """Chat with AI using LM Studio."""
    try:
        message = request.get("message", "")
        model = request.get("model", "qwen/qwen3-8b")
        max_tokens = request.get("max_tokens", 1000)
        
        # Call MCP tool for AI generation
        result = await self.execute_mcp_tool(
            "generate_lm_studio_text",
            {
                "prompt": message,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
        )
        
        return {"status": "ok", "data": result}
    except Exception as e:
        return {"status": "error", "error": {"code": "ai_chat_failed", "msg": str(e)}}
```

### **Frontend AI Integration**
```javascript
// AI Chat
async function sendChatMessage() {
    const message = CHAT_INPUT.value.trim();
    if (!message) return;
    
    try {
        addStatus('🤖 AI processing...', 'info');
        const result = await apiCall('/api/ai/chat', 'POST', {
            message: message,
            model: 'qwen/qwen3-8b',
            max_tokens: 1000
        });
        
        addStatus('✅ AI response received', 'success');
        OUTPUT.innerHTML = `<h3>🤖 AI Chat Response</h3><pre>${JSON.stringify(result, null, 2)}</pre>`;
        
    } catch (error) {
        addStatus('❌ AI chat failed', 'error');
        OUTPUT.innerHTML = `<h3>❌ AI Chat Error</h3><pre>${error}</pre>`;
    }
}

// Complete Analysis Pipeline
async function startCompleteAnalysis() {
    try {
        addStatus('🚀 Starting complete analysis pipeline...', 'info');
        
        // Step 1: Start the analysis
        const analysisData = { channel_url: channelUrl, limit: 1, sort: 'oldest', max_depth: 1 };
        await apiCall('/api/runs/youtube/start', 'POST', analysisData);
        
        // Step 2: Generate AI Summary
        const summaryResult = await apiCall('/api/execute', 'POST', { 
            tool_name: 'analyze_veritas_summary', 
            params: { run_id: latestRun.run_id } 
        });
        
        // Step 3: Generate AI Claims
        const claimsResult = await apiCall('/api/execute', 'POST', { 
            tool_name: 'analyze_veritas_claims', 
            params: { run_id: latestRun.run_id } 
        });
        
        // Step 4: Create visualization
        const vizResult = await apiCall('/api/execute', 'POST', { 
            tool_name: 'create_3d_network_visualization', 
            params: { graph_data: graphData } 
        });
        
        addStatus('✅ Complete analysis finished!', 'success');
        
    } catch (error) {
        addStatus('❌ Analysis failed', 'error');
        OUTPUT.innerHTML = `<h3>❌ Analysis Error</h3><pre>${error}</pre>`;
    }
}
```

## 📊 **AI Features**

### **Real LLM Generation**
- **No Pattern Matching**: All analysis uses actual LLM calls
- **Structured Output**: JSON-formatted responses for consistency
- **Error Handling**: Graceful fallbacks if AI service unavailable
- **Confidence Scores**: AI-generated confidence metrics

### **Document Analysis**
- **Summarization**: AI-powered document summaries
- **Claim Extraction**: Identifies and categorizes claims
- **Sentiment Analysis**: Determines overall sentiment
- **Key Points**: Extracts important information

### **Interactive Chat**
- **Direct Communication**: Real-time chat with AI models
- **Context Awareness**: Maintains conversation context
- **Model Selection**: Choose different AI models
- **Parameter Control**: Adjust temperature, max tokens

## 🔗 **API Integration**

### **AI Endpoints**
- **`/api/ai/chat`**: Direct chat with LM Studio
- **`/api/execute`**: Execute AI-powered MCP tools
- **`/api/health/full`**: AI service health status

### **Response Format**
```python
# Success Response
{
    "status": "ok",
    "data": "AI-generated content or analysis results"
}

# Error Response
{
    "status": "error",
    "error": {
        "code": "ai_service_unavailable",
        "msg": "LM Studio connection failed"
    }
}
```

## 🧪 **Testing**

### **AI Service Testing**
- **Connection Test**: Verify LM Studio accessibility
- **Model Availability**: Check for required models
- **Response Validation**: Ensure proper JSON responses
- **Error Handling**: Test with invalid requests

### **Integration Testing**
- **MCP Tool Execution**: Test AI tools via `/api/execute`
- **Chat Functionality**: Verify real-time chat
- **Analysis Pipeline**: Test complete AI workflow
- **Performance**: Check response times

## 🚨 **Common Issues**

### **Connection Refused**
- **Cause**: LM Studio not running or wrong port
- **Solution**: Start desktop LM Studio on port 1234
- **Prevention**: Health checks before AI operations

### **Model Not Found**
- **Cause**: Required model not loaded in LM Studio
- **Solution**: Load `qwen/qwen3-8b` model
- **Prevention**: Model availability checks

### **Timeout Errors**
- **Cause**: Long generation times or network issues
- **Solution**: Increase timeout values
- **Prevention**: Progress indicators and timeouts

### **JSON Parse Errors**
- **Cause**: AI returns malformed JSON
- **Solution**: Implement fallback parsing
- **Prevention**: Structured prompts and validation

## 📋 **Best Practices**

### **Service Management**
- **Health Checks**: Regular AI service monitoring
- **Error Recovery**: Graceful fallbacks for failures
- **Resource Limits**: Prevent excessive API calls
- **Caching**: Cache results when appropriate

### **Prompt Engineering**
- **Structured Output**: Request JSON format for consistency
- **Clear Instructions**: Specific, unambiguous prompts
- **Context Provision**: Include relevant background
- **Error Handling**: Specify fallback behavior

### **Performance**
- **Async Operations**: Non-blocking AI calls
- **Batch Processing**: Group related requests
- **Timeout Management**: Reasonable timeouts
- **Resource Monitoring**: Track API usage

### **User Experience**
- **Progress Indicators**: Show AI processing status
- **Error Messages**: Clear feedback for failures
- **Response Formatting**: Consistent output display
- **Loading States**: Visual feedback during processing

## 🔄 **Workflow Integration**

### **Complete Analysis Pipeline**
1. **Document Ingestion**: Process source documents
2. **AI Analysis**: Generate summaries and claims
3. **Entity Extraction**: Identify key entities
4. **Visualization**: Create interactive graphs
5. **Results Display**: Present comprehensive analysis

### **Individual AI Operations**
- **Document Summarization**: AI-powered summaries
- **Claim Extraction**: Identify and categorize claims
- **Interactive Chat**: Real-time AI conversation
- **Content Generation**: AI-assisted content creation
```

---

### 3. Analysis Scripts and MCP-First Batching
**File:** `analysis_batching.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Analysis Batching rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '10443b77b4a284d1b8f53c8752ff8f5678292110c3cf738379281c4d0f057942',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'analysis_batching',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: analysis_batching',
 'updated': '2025-08-15',
 'version': 1}
```

# Analysis Scripts and MCP-First Batching

## Analysis scripts location
```text
- All analysis/archive scripts are in `scripts/analyze/`
  - Examples: `scripts/analyze/analyze_imagination_podcast_*.py`, `scripts/analyze/archive_imagination_podcast*.py`
- Prefer MCP Hub meta-tools with batching instead of invoking scripts directly.
- Phase 8.1: Use unified dashboard interface at http://localhost:8050 for analysis
```

## MCP-first batching usage
```text
- Analysis: use `batch_execute_tools` or `execute_category_tools('analysis', ...)` for grouped operations
- GitHub via Hub: use `execute_github_tool` or `execute_category_tools('github', ...)`
  - Allowed GitHub tools: list_repositories, search_repositories, create_issue, get_github_status
```

## Phase 8.1 Dashboard Integration
```text
- Unified Interface: All analysis functionality accessible via dashboard at http://localhost:8050
- Quick Start: Pre-filled defaults for immediate analysis (10 videos, oldest first, depth 3)
- Run Management: Browse and manage analysis results with detailed bundle views
- Advanced Controls: Expert toggles and raw MCP tool access
- Progressive Disclosure: Simple defaults with expandable advanced options
 - Fallbacks: Dashboard reads runs, details, and corpus from data/runs when MCP is unavailable in container
```

## Checklist additions
- Trigger analysis through MCP when possible (batching preferred)
- Use unified dashboard interface for user-friendly analysis workflows
- Verify script paths under `scripts/analyze/` in docs/tests
```

---

### 4. API Contracts
**File:** `api_contracts.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Api Contracts rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '0f140a86dd977e05152389fd3c5dd9b15c5e3c9b2e311f1102c7048cce31df95',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'api_contracts',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: api_contracts',
 'updated': '2025-08-15',
 'version': 1}
```

# API Contracts

## 🎯 **Envelope Format (Required)**

All API responses MUST use the standard envelope format:
```json
{
  "status": "ok" | "error",
  "data": any,
  "error": {
    "code": number,
    "message": string
  }
}
```

### **Error Code Standards**
- **502**: Upstream model error (LLM, embedding service unavailable)
- **503**: Dependencies down (database, external services)
- **500**: Internal server error (unexpected exceptions)
- **409**: Conflict (constraint violations, duplicate data)
- **404**: Not found (resources not available)

## 📋 **Testing Requirements**

### **Envelope Validation**
- Tests must assert envelope format for all endpoints
- Validate `status` field presence and values
- Check error codes match expected ranges (502/503/500)

### **Zod Schema Integration (Phase 9.4.7)**
- Add zod schemas in UI for type-safe API responses
- Validate envelope structure at runtime
- Provide TypeScript types from schemas

## 🚨 **Breaking Changes**

### **Contract Updates**
- Breaking changes require plan amendment
- Update contract tests for all affected endpoints
- Maintain backward compatibility where possible
- Document migration path for consumers

### **Version Management**
- Use semantic versioning for API changes
- Deprecate old endpoints before removal
- Provide migration guides for breaking changes

## ✅ **Implementation Checklist**

- [ ] All endpoints return proper envelope format
- [ ] Error codes follow standard conventions
- [ ] Tests validate envelope structure
- [ ] Zod schemas defined for UI integration
- [ ] Documentation updated with contract details

## 🔧 **Examples**

### **Success Response**
```json
{
  "status": "ok",
  "data": {
    "runs": [...],
    "total": 10
  }
}
```

### **Error Response**
```json
{
  "status": "error",
  "error": {
    "code": 503,
    "message": "Database connection failed"
  }
}
```

### **Constraint Violation Response**
```json
{
  "status": "error",
  "error": {
    "code": 409,
    "message": "Graph building failed due to constraint violation. Try using ?rebuild=1 to clear existing data: duplicate key value violates unique constraint"
  },
  "data": {
    "code": "graph_build_conflict",
    "hint": "Use ?rebuild=1 to clear existing data"
  }
}
```

## 📚 **References**
- Phase 9.3 plan & tests for envelope implementation
- Phase 9.4.7 for zod schema integration
- @core_workflow.mdc for development protocol
```

---

### 5. Automated Development Management
**File:** `automated_development_management.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Automated Development Management rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '508671902505d317dc0b19dcbbb9cd7ecb5a196008c25a9de593947e0ff71213',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'automated_development_management',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: automated_development_management',
 'updated': '2025-08-15',
 'version': 1}
```

# Automated Development Management

## Description
This rule establishes automated processes for detecting development needs, adding tools, updating documentation, and managing cursor rules without manual intervention.

## 🎯 **Automated Tool Detection and Addition**

### **Tool Detection Patterns**
```python
# ✅ Automatic tool detection triggers
TRIGGER_PATTERNS = {
    "new_api_endpoint": r"http://localhost:\d+",
    "new_service": r"docker.*up.*-d",
    "new_functionality": r"def\s+\w+.*->\s*\w+:",
    "new_mcp_tool": r"@mcp\.tool\(\)",
    "new_environment_var": r"export\s+\w+=",
    "new_configuration": r"config.*=.*{",
    "new_dependency": r"pip install|npm install|yarn add"
}

# ✅ Automatic tool addition workflow
def auto_add_tool(detected_need: str, context: dict) -> None:
    """Automatically add tools when needs are detected."""
    # 1. Detect tool need
    # 2. Create MCP tool
    # 3. Update documentation
    # 4. Update cursor rules
    # 5. Validate configuration
    pass
```

### **Automatic Tool Categories**
- **API Integration Tools**: Detect new endpoints, add API tools
- **Service Management Tools**: Detect new services, add management tools
- **Data Processing Tools**: Detect new data sources, add processing tools
- **Configuration Tools**: Detect new configs, add management tools
- **Monitoring Tools**: Detect new services, add health check tools

## 📋 **Automated Documentation Updates**

### **Documentation Update Triggers**
```python
# ✅ Automatic documentation triggers
DOC_UPDATE_TRIGGERS = {
    "new_tool_added": ["update_mcp_server_docs", "update_cursor_rules"],
    "service_status_changed": ["update_current_status", "update_readme"],
    "configuration_changed": ["update_environment_docs", "update_setup_guides"],
    "new_feature": ["create_feature_docs", "update_overview"],
    "bug_fix": ["update_troubleshooting", "update_changelog"]
}

# ✅ Automatic documentation workflow
def auto_update_docs(change_type: str, details: dict) -> None:
    """Automatically update all relevant documentation."""
    # 1. Identify affected documents
    # 2. Update each document
    # 3. Maintain consistency
    # 4. Update cross-references
    # 5. Validate documentation
    pass
```

### **Documentation Files to Update**
- **`CURRENT_STATUS.md`**: Service status, achievements, fixes
- **`README.md`**: Overview, setup, features
- **`docs/CURRENT_SYSTEM_STATUS.md`**: Comprehensive system state
- **`myenvironment.txt`**: Environment variables, configuration
- **Feature-specific docs**: New documentation for new features

## 🔧 **Automated Cursor Rule Management**

### **Cursor Rule Update Triggers**
```python
# ✅ Automatic cursor rule triggers
CURSOR_RULE_TRIGGERS = {
    "new_pattern": ["update_best_practices", "add_examples"],
    "new_tool": ["update_mcp_integration", "add_tool_patterns"],
    "new_service": ["update_system_management", "add_service_patterns"],
    "new_workflow": ["update_development_workflow", "add_automation"],
    "new_issue": ["add_troubleshooting", "update_prevention"]
}

# ✅ Automatic cursor rule workflow
def auto_update_cursor_rules(change_type: str, details: dict) -> None:
    """Automatically update relevant cursor rules."""
    # 1. Identify affected rules
    # 2. Update rule content
    # 3. Add new patterns/examples
    # 4. Maintain consistency
    # 5. Validate rule syntax
    pass
```

### **Cursor Rules to Update**
- **`current_working_state.mdc`**: Current status, achievements
- **`mcp_server_best_practices.mdc`**: Tool patterns, integration
- **`docker_best_practices.mdc`**: Service management, configuration
- **`system_management.mdc`**: Environment, automation
- **`coding_standards.mdc`**: Patterns, conventions

## 🤖 **MCP Server Automation Functions**

### **Automated Management Tools**
```python
@mcp.tool()
def auto_detect_and_add_tools() -> str:
    """Automatically detect development needs and add tools."""
    # Scan codebase for patterns
    # Identify missing tools
    # Add tools automatically
    # Update documentation
    # Update cursor rules
    pass

@mcp.tool()
def auto_update_all_documentation() -> str:
    """Automatically update all documentation based on current state."""
    # Update CURRENT_STATUS.md
    # Update README.md
    # Update system status docs
    # Update environment config
    # Validate consistency
    pass

@mcp.tool()
def auto_update_cursor_rules() -> str:
    """Automatically update cursor rules based on current patterns."""
    # Update working state
    # Update best practices
    # Update integration patterns
    # Add new examples
    # Validate rules
    pass

@mcp.tool()
def auto_validate_system_state() -> str:
    """Automatically validate and report system state."""
    # Check all services
    # Validate configurations
    # Test MCP servers
    # Generate status report
    # Update documentation
    pass
```

## 🔄 **Automated Workflow Integration**

### **Development Workflow Automation**
```python
# ✅ Pre-commit automation
def pre_commit_automation() -> None:
    """Automated pre-commit checks and updates."""
    auto_detect_and_add_tools()
    auto_update_all_documentation()
    auto_update_cursor_rules()
    auto_validate_system_state()

# ✅ Post-change automation
def post_change_automation(change_type: str, details: dict) -> None:
    """Automated post-change updates."""
    if change_type in DOC_UPDATE_TRIGGERS:
        auto_update_docs(change_type, details)
    if change_type in CURSOR_RULE_TRIGGERS:
        auto_update_cursor_rules(change_type, details)
    auto_validate_system_state()
```

### **Continuous Monitoring**
```python
# ✅ Continuous monitoring triggers
MONITORING_TRIGGERS = {
    "service_status": ["check_health", "update_status"],
    "tool_usage": ["analyze_patterns", "suggest_improvements"],
    "documentation_gaps": ["identify_gaps", "create_docs"],
    "rule_violations": ["detect_violations", "suggest_fixes"]
}
```

## 📊 **Automated Quality Assurance**

### **Validation Checks**
```python
# ✅ Automated validation
def auto_validate_everything() -> dict:
    """Comprehensive automated validation."""
    return {
        "services": validate_services(),
        "mcp_servers": validate_mcp_servers(),
        "documentation": validate_documentation(),
        "cursor_rules": validate_cursor_rules(),
        "configurations": validate_configurations()
    }

# ✅ Automated consistency checks
def auto_check_consistency() -> dict:
    """Check consistency across all components."""
    return {
        "port_mappings": check_port_consistency(),
        "endpoint_urls": check_endpoint_consistency(),
        "tool_names": check_tool_naming_consistency(),
        "documentation": check_doc_consistency()
    }
```

## 🚀 **Implementation Requirements**

### **Automatic Triggers**
- **Code changes**: Detect new functions, APIs, services
- **Configuration changes**: Detect new env vars, settings
- **Service changes**: Detect new containers, endpoints
- **Tool usage**: Detect missing tools, suggest additions

### **Automatic Updates**
- **Documentation**: Update all relevant docs automatically
- **Cursor rules**: Update rules with new patterns
- **MCP tools**: Add tools when needs detected
- **Configuration**: Update configs when services change

### **Automatic Validation**
- **System health**: Continuous health monitoring
- **Consistency**: Cross-component consistency checks
- **Quality**: Automated quality assurance
- **Compliance**: Rule compliance validation

## 📋 **Automated Management Checklist**

### **Before Any Development**
- [ ] **Auto-detect tool needs** based on code patterns
- [ ] **Auto-add missing tools** to MCP servers
- [ ] **Auto-update documentation** for new features
- [ ] **Auto-update cursor rules** with new patterns

### **During Development**
- [ ] **Auto-monitor changes** and trigger updates
- [ ] **Auto-validate consistency** across components
- [ ] **Auto-suggest improvements** based on patterns
- [ ] **Auto-detect issues** and suggest fixes

### **After Development**
- [ ] **Auto-update all documentation** with changes
- [ ] **Auto-update cursor rules** with new patterns
- [ ] **Auto-validate system state** and report
- [ ] **Auto-generate status reports** for review

## 🎯 **Success Metrics**
- ✅ **100% automated tool detection** and addition
- ✅ **100% automated documentation updates** on changes
- ✅ **100% automated cursor rule updates** with patterns
- ✅ **100% automated validation** of system state
- ✅ **0% manual intervention** required for maintenance
```

---

### 6. Coding Standards for AI-Assisted Development
**File:** `coding_standards.mdc`

**Metadata:**
- summary: string;

**Content:**
```mdc
---
description: Coding Standards rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '429ff29679cfdc092c602f150d909c7c06a61fe55cc88237d2f8497667c2d122',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'coding_standards',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: coding_standards',
 'updated': '2025-08-15',
 'version': 1}
```

# Coding Standards for AI-Assisted Development

## Description
This rule establishes coding standards optimized for AI-assisted development, ensuring code quality, consistency, and AI understanding.

## 🎯 **AI-Optimized Coding Standards**

### **Python Standards**

#### **Type Hints (Required)**
```python
# ✅ Good - AI can understand types
def analyze_transcript(transcript_name: str, anonymize: bool = False) -> dict[str, Any]:
    """Analyze a transcript file with optional anonymization."""
    pass

# ❌ Bad - AI can't understand types
def analyze_transcript(transcript_name, anonymize=False):
    pass
```

#### **Docstrings (Required)**
```python
def query_langflow(query: str, output_type: str = "summary") -> str:
    """
    Query the Langflow workflow for survivor testimony analysis.
    
    Args:
        query: The query string or analysis request
        output_type: Type of output (summary, study_guide, timeline, audio)
    
    Returns:
        Analysis results as formatted string
        
    Raises:
        ValueError: If query is empty or invalid
        ConnectionError: If Langflow service is unavailable
    """
    pass
```

#### **Naming Conventions**
- **Functions**: `snake_case` (e.g., `analyze_transcript`)
- **Classes**: `PascalCase` (e.g., `LivingTruthEngine`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_MODEL`)
- **Variables**: `snake_case` (e.g., `transcript_data`)

### **JavaScript/TypeScript Standards**

#### **Type Definitions**
```typescript
// ✅ Good - Clear types for AI
interface AnalysisResult {
  confidence: number;
  sources: string[];
  summary: string;
  timestamp: Date;
}

// ❌ Bad - No types
function analyzeData(data) {
  return { confidence: 0.8, sources: [], summary: "" };
}
```

#### **Function Documentation**
```typescript
/**
 * Analyzes transcript data for survivor testimony patterns
 * @param transcriptData - Raw transcript text
 * @param options - Analysis options
 * @returns Promise<AnalysisResult> - Analysis results
 */
async function analyzeTranscript(
  transcriptData: string, 
  options: AnalysisOptions
): Promise<AnalysisResult> {
  // Implementation
}
```

## 📋 **Code Quality Checklist**

### **Before Committing**
- [ ] **Type hints** added to all functions
- [ ] **Docstrings** with Args/Returns/Raises
- [ ] **Consistent naming** conventions
- [ ] **Error handling** implemented
- [ ] **Logging** for debugging
- [ ] **Tests** written for new functions

### **AI Understanding**
- [ ] **Clear function names** that describe purpose
- [ ] **Descriptive variable names** (not `x`, `data`, `result`)
- [ ] **Comments** for complex logic
- [ ] **Modular functions** (single responsibility)
- [ ] **Consistent patterns** across codebase

## 🔧 **Best Practices**

### **Function Design**
```python
# ✅ Good - Single responsibility, clear purpose
def extract_evidence_references(text: str) -> list[dict[str, str]]:
    """Extract evidence references from text."""
    pass

def validate_reference(reference: dict[str, str]) -> bool:
    """Validate an evidence reference."""
    pass

# ❌ Bad - Multiple responsibilities, unclear purpose
def process_text(text):
    """Process text and do various things."""
    # Too many responsibilities
    pass
```

### **Error Handling**
```python
# ✅ Good - Specific error handling
try:
    result = query_langflow(query)
except requests.ConnectionError:
    logger.error("Langflow service unavailable")
    return "Service temporarily unavailable"
except ValueError as e:
    logger.error(f"Invalid query: {e}")
    return f"Invalid query: {e}"
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return "An error occurred during analysis"
```

### **Logging**
```python
import logging

logger = logging.getLogger(__name__)

def analyze_transcript(transcript_name: str) -> dict[str, Any]:
    logger.info(f"Starting analysis of transcript: {transcript_name}")
    
    try:
        # Analysis logic
        logger.debug("Analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise
```

## 🎨 **Code Organization**

### **File Structure**
```python
# ✅ Good - Clear organization
"""
Living Truth Engine - Transcript Analysis Module

This module provides functions for analyzing transcript data
for survivor testimony corroboration and evidence analysis.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

class TranscriptAnalyzer:
    """Analyzes transcript data for survivor testimony patterns."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def analyze(self, transcript_path: Path) -> Dict[str, Any]:
        """Analyze a transcript file."""
        pass
```

### **Import Organization**
```python
# Standard library imports
import logging
import os
from pathlib import Path
from typing import Dict, Any, List

# Third-party imports
import requests
from dotenv import load_dotenv

# Local imports
from .utils import validate_input
from .models import AnalysisResult
```

## 🚨 **Common Mistakes to Avoid**

### **AI Confusion Issues**
- ❌ **Generic variable names**: `data`, `result`, `x`
- ❌ **No type hints**: AI can't understand data structures
- ❌ **Complex functions**: Multiple responsibilities confuse AI
- ❌ **Inconsistent patterns**: AI can't learn from examples
- ❌ **Missing documentation**: AI lacks context

### **Code Quality Issues**
- ❌ **Magic numbers**: Use constants with descriptive names
- ❌ **Deep nesting**: Keep functions flat and readable
- ❌ **Long functions**: Break into smaller, focused functions
- ❌ **Hardcoded values**: Use configuration files
- ❌ **Silent failures**: Always handle errors explicitly

## 📊 **Success Metrics**

- ✅ **Type coverage**: 100% of functions have type hints
- ✅ **Documentation**: All functions have docstrings
- ✅ **Test coverage**: >90% code coverage
- ✅ **AI understanding**: Clear, consistent patterns
- ✅ **Maintainability**: Modular, readable code
```

---

### 7. Complete Analysis Pipeline
**File:** `complete_analysis_pipeline.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Complete Analysis Pipeline rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '1c9c115317d812d6928513f96ad3b60da653bbd1e21923708fc9486d27ca276c',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'complete_analysis_pipeline',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: complete_analysis_pipeline',
 'updated': '2025-08-15',
 'version': 1}
```

# Complete Analysis Pipeline

## Overview
The Living Truth Engine provides a complete analysis pipeline that orchestrates document ingestion, AI analysis, and visualization generation in a single workflow.

## 🎯 **Pipeline Components**

### **Start Complete Analysis**
- **Single Button**: Orchestrates entire workflow
- **Step-by-Step Progress**: Visual indicators for each stage
- **Comprehensive Results**: Summary, claims, and visualization
- **Error Handling**: Graceful failure with clear feedback

### **Pipeline Stages**
1. **Document Ingestion**: Start YouTube analysis
2. **AI Summary**: Generate document summaries
3. **AI Claims**: Extract and categorize claims
4. **Entity Extraction**: Identify key entities
5. **Visualization**: Create 3D network graphs
6. **Results Display**: Present comprehensive analysis

## 🚀 **Implementation**

### **Frontend Orchestration**
```javascript
async function startCompleteAnalysis() {
    try {
        addStatus('🚀 Starting complete analysis pipeline...', 'info');
        OUTPUT.innerHTML = '<h3>🚀 Living Truth Engine - Complete Analysis</h3><p>Starting comprehensive analysis pipeline...</p>';

        // Step 1: Start the analysis
        addStatus('Step 1: Starting YouTube analysis...', 'info');
        const channelUrl = 'https://www.youtube.com/@imaginationpodcastofficial';
        const analysisData = { channel_url: channelUrl, limit: 1, sort: 'oldest', max_depth: 1 };
        await apiCall('/api/runs/youtube/start', 'POST', analysisData);
        addStatus('✅ Analysis started successfully', 'success');
        
        // Step 2: Wait for completion and get run ID
        addStatus('Step 2: Waiting for analysis completion...', 'info');
        await new Promise(resolve => setTimeout(resolve, 5000));
        await refreshRuns();
        const runsResponse = await fetch(`${API_BASE.value}/api/runs`);
        const runsData = await runsResponse.json();
        const latestRun = runsData.data[0];
        if (!latestRun) { throw new Error('No analysis runs found'); }
        addStatus(`✅ Analysis completed: ${latestRun.run_id}`, 'success');
        
        // Step 3: Generate AI Summary
        addStatus('Step 3: Generating AI summary...', 'info');
        const summaryResult = await apiCall('/api/execute', 'POST', { 
            tool_name: 'analyze_veritas_summary', 
            params: { run_id: latestRun.run_id } 
        });
        
        // Step 4: Generate AI Claims
        addStatus('Step 4: Generating AI claims...', 'info');
        const claimsResult = await apiCall('/api/execute', 'POST', { 
            tool_name: 'analyze_veritas_claims', 
            params: { run_id: latestRun.run_id } 
        });
        
        // Step 5: Create visualization
        addStatus('Step 5: Creating advanced visualization...', 'info');
        const graphData = { /* dynamic graph data */ };
        const vizResult = await apiCall('/api/execute', 'POST', { 
            tool_name: 'create_3d_network_visualization', 
            params: { graph_data: graphData } 
        });
        
        // Step 6: Present complete results
        addStatus('✅ Complete analysis finished!', 'success');
        OUTPUT.innerHTML = `
            <h3>🎯 Living Truth Engine - Complete Analysis Results</h3>
            <div style="margin-bottom: 20px; padding: 15px; background: #1a1a1a; border-radius: 8px;">
                <h4>📊 Analysis Overview</h4>
                <p><strong>Run ID:</strong> ${latestRun.run_id}</p>
                <p><strong>Topic:</strong> ${latestRun.topic || 'Unknown'}</p>
                <p><strong>Status:</strong> ✅ Complete</p>
                <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
            </div>
            <div style="margin-bottom: 20px; padding: 15px; background: #1a1a1a; border-radius: 8px;">
                <h4>🤖 AI Summary</h4>
                <div style="white-space: pre-wrap; color: #e0e0e0;">${summaryResult}</div>
            </div>
            <div style="margin-bottom: 20px; padding: 15px; background: #1a1a1a; border-radius: 8px;">
                <h4>🔍 AI Claims Analysis</h4>
                <div style="white-space: pre-wrap; color: #e0e0e0;">${claimsResult}</div>
            </div>
            <div style="margin-bottom: 20px; padding: 15px; background: #1a1a1a; border-radius: 8px;">
                <h4>🎨 Advanced 3D Network Visualization</h4>
                <p><strong>Nodes:</strong> ${graphData.nodes.length} | <strong>Edges:</strong> ${graphData.edges.length}</p>
                <div style="width: 100%; height: 600px; border: 1px solid #ccc; background: white; overflow: auto;" id="viz-container">
                    ${vizHtml || '<p style="color: #666; text-align: center; padding: 20px;">Visualization loading...</p>'}
                </div>
            </div>
        `;
        
    } catch (error) {
        addStatus('❌ Complete analysis failed', 'error');
        OUTPUT.innerHTML = `<h3>❌ Analysis Error</h3><pre>${error}</pre>`;
    }
}
```

### **Status Management**
```javascript
// Status indicators for pipeline progress
const st = {
    llm: { box: document.getElementById("llm"), dot: document.getElementById("llm-dot"), txt: document.getElementById("llm-txt") },
    embedding: { box: document.getElementById("embedding"), dot: document.getElementById("embedding-dot"), txt: document.getElementById("embedding-txt") },
    progress: { box: document.getElementById("progress"), dot: document.getElementById("progress-dot"), txt: document.getElementById("progress-txt") },
    status: { box: document.getElementById("status"), dot: document.getElementById("status-dot"), txt: document.getElementById("status-txt") }
};

function setActive(which, on, label) {
    const o = st[which];
    o.box.classList.toggle("flash", !!on);
    if (o.dot) o.dot.style.background = on ? "var(--ok)" : "var(--muted)";
    if (o.txt) o.txt.textContent = label || (on ? "working…" : "idle");
}

function addStatus(message, type = 'info') {
    const statusDiv = document.getElementById('status-stack');
    const statusItem = document.createElement('div');
    statusItem.className = `status-item ${type}`;
    statusItem.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
    statusDiv.appendChild(statusItem);
    statusDiv.scrollTop = statusDiv.scrollHeight;
}
```

## 📊 **Pipeline Features**

### **Orchestration**
- **Single Entry Point**: One button starts entire workflow
- **Sequential Execution**: Steps execute in proper order
- **Progress Tracking**: Visual feedback for each stage
- **Error Recovery**: Graceful handling of failures

### **Real-time Updates**
- **Status Indicators**: Live updates during processing
- **Progress Steps**: Visual progress through pipeline
- **Result Display**: Immediate presentation of results
- **Error Feedback**: Clear error messages and recovery

### **Comprehensive Results**
- **AI Summary**: Document analysis and key points
- **AI Claims**: Extracted claims with categorization
- **Visualization**: Interactive 3D network graphs
- **Metadata**: Run information and timestamps

## 🔗 **API Integration**

### **Pipeline Endpoints**
- **`/api/runs/youtube/start`**: Start document ingestion
- **`/api/runs`**: Get available runs
- **`/api/execute`**: Execute AI analysis tools
- **`/api/visualizations/{filename}`**: Serve visualizations

### **MCP Tools Used**
- **`analyze_veritas_summary`**: Generate document summaries
- **`analyze_veritas_claims`**: Extract and categorize claims
- **`create_3d_network_visualization`**: Create interactive graphs

## 🧪 **Testing**

### **Pipeline Testing**
- **End-to-End**: Complete workflow verification
- **Step-by-Step**: Individual stage validation
- **Error Scenarios**: Failure handling tests
- **Performance**: Timing and resource usage

### **Integration Testing**
- **API Endpoints**: Verify all required endpoints
- **MCP Tools**: Test tool execution and responses
- **UI Updates**: Confirm real-time status updates
- **Result Display**: Validate comprehensive output

## 🚨 **Common Issues**

### **Pipeline Failures**
- **Cause**: Missing dependencies or services
- **Solution**: Health checks before starting
- **Prevention**: Comprehensive error handling

### **Timeout Issues**
- **Cause**: Long-running operations
- **Solution**: Appropriate timeouts and progress indicators
- **Prevention**: Async operations and status updates

### **Data Dependencies**
- **Cause**: Steps depend on previous results
- **Solution**: Proper sequencing and validation
- **Prevention**: Clear data flow and error handling

## 📋 **Best Practices**

### **Pipeline Design**
- **Modular Steps**: Independent, testable components
- **Clear Dependencies**: Explicit step ordering
- **Error Handling**: Graceful failure at each stage
- **Progress Tracking**: Visual feedback throughout

### **User Experience**
- **Single Action**: One button for complete workflow
- **Real-time Updates**: Live status and progress
- **Comprehensive Results**: All analysis in one view
- **Error Recovery**: Clear guidance for failures

### **Performance**
- **Async Operations**: Non-blocking pipeline execution
- **Resource Management**: Efficient memory and CPU usage
- **Timeout Handling**: Reasonable timeouts for operations
- **Caching**: Reuse results when possible

### **Maintainability**
- **Clear Structure**: Well-organized pipeline code
- **Error Logging**: Comprehensive error tracking
- **Configuration**: Configurable pipeline parameters
- **Testing**: Comprehensive test coverage

## 🔄 **Workflow Integration**

### **Complete Analysis Pipeline**
1. **Start Analysis**: Begin document ingestion
2. **Wait for Completion**: Monitor run status
3. **Generate Summary**: AI-powered document analysis
4. **Extract Claims**: AI-powered claim identification
5. **Create Visualization**: Generate interactive graphs
6. **Display Results**: Present comprehensive analysis

### **Individual Components**
- **Document Ingestion**: Standalone document processing
- **AI Analysis**: Individual summary and claims generation
- **Visualization**: Independent graph creation
- **Result Display**: Flexible result presentation
```

---

### 8. Core Workflow (Phase 9)
**File:** `core_workflow.mdc`

**Metadata:**
- phase: 1) `validate_cursor_rules`

**Content:**
```mdc
---
description: Core Workflow rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '663599e6373317b02c42aa45925579bcad6a53e260012092be56328ee13d4a19',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'core_workflow',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: core_workflow',
 'updated': '2025-08-15',
 'version': 1}
```

# Core Workflow (Phase 9)

## 🎯 **Phase 9 Development Protocol**

### **One PR per sub-phase** in `PHASE_9_MASTER_PLAN.md` order.
- **Commit format:** `phase<subphase>: <summary> [verified]`
- **On PR merge (MANDATORY):**
  1) Write `PHASE_<subphase>_COMPLETION_SUMMARY.md` (root).
  2) Run sub-phase smoke (if present).
  3) `python build_master_log.py append`.

### **Never change** the `{status,data?,error?}` API envelope or error-code policy unless explicitly planned.
- References: Phase 9.3 plan & tests
- Envelope format: `{status: "ok"|"error", data?: any, error?: {code, message}}`
- Error codes: 502 upstream model error, 503 deps-down, 500 internal

## 🚨 **Critical: Fix Root Issues, Don't Work Around Them**

### **When You Encounter Errors**
- **❌ DON'T**: Work around errors or ignore them
- **❌ DON'T**: Create fallback mechanisms that hide the real problem
- **❌ DON'T**: Assume the error is "expected" without investigation
- **✅ DO**: Investigate and fix the root cause
- **✅ DO**: Update database schemas if there are type mismatches
- **✅ DO**: Fix missing functionality rather than creating workarounds

### **Common Root Issues to Fix**
- **Database Schema Mismatches**: Update table schemas to match code expectations
- **Missing Database Storage**: Implement proper database storage in runners
- **Type Mismatches**: Fix data type inconsistencies (UUID vs VARCHAR, etc.)
- **Missing Dependencies**: Add required imports and dependencies
- **Configuration Issues**: Fix configuration files and environment variables

### **Investigation Process**
1. **Check the actual error message** - don't assume it's "expected"
2. **Verify database schema** with `\d table_name` commands
3. **Check if data is actually being stored** in the database
4. **Test the specific failing functionality** in isolation
5. **Fix the root cause** rather than adding error handling

## 1) BUILD
- `docker compose -f docker/docker-compose.yml up -d --build`
- Rebuild any changed services; no UI edits unless the phase explicitly says so.

## 2) VERIFY
- Run health gates: `bash scripts/proof_of_life.sh` (Phase 8) + `bash scripts/p9_1_smoke.sh`
- Run tests: `pytest -q`; exit on first failure.
- **Bundle Check**: Verify `.veritasrun` folder exists with `manifest.json`, `corpus.jsonl`, `merkle.json`, `metrics.json`
- **Database Check**: Verify documents are actually stored in database
- **Documentation**: Update docs (`README.md`, `PHASE_*`, `CONSOLIDATED_COMPLETION_SUMMARY.md`)

## 3) ITERATE
- Fix only the failing step; re-run BUILD & VERIFY.
- **Fix root causes** - don't work around errors
- Update docs & rules before merging.
- **Commit with message**: `phaseX.Y: <brief change> [verified]`
- **Paste test outputs** in PR or chat for traceability

# Fallback Exceptions (allowed)
- YouTube captions/transcripts fallback when MCP fetch fails.
- Reranker CPU execution when GPU is occupied (log the switch).
- Local dev data only when `ALLOW_FALLBACKS=true` (dev).
- In-memory search fallback if pgvector is unavailable (dev only).
(These exceptions are allowed and MUST be logged; no other fallbacks.)

# UI Targeting
- Do NOT modify `src/dashboard/static/ui_status_chat.html` unless a phase plan explicitly says so.
- Main dashboard `/` edits allowed only when the phase defines them.
- Phase 9.4.0 introduces a reverse proxy; root `/` must serve the new UI shell.

# MCP Integration
- Use MCP tools: `validate_cursor_rules()`, `fix_cursor_rule_frontmatter()` before/after changes
- Required MCP operations in every phase:
  1) `validate_cursor_rules`
  2) `fix_cursor_rule_frontmatter`
  3) `ruleset_archive_outdated`
  4) `ruleset_apply_templates`
  5) `run_smoke_and_tests`
  6) `generate_phase_completion_summary`

# Compose Rules
- Healthchecks for all services; fail fast if any gate fails.
- Use `host.docker.internal:1234/v1` for LM Studio from containers.

# Init DB (pgvector)
- Mount `docker/initdb/` to Postgres; `002_pgvector.sql` must exist.

## 📋 **Root Issue Fixing Checklist**

### **When Investigating Errors**
- [ ] **Read the full error message** - don't truncate or ignore
- [ ] **Check database schema** with `\d table_name` commands
- [ ] **Verify data is being stored** in the expected tables
- [ ] **Test the specific functionality** that's failing
- [ ] **Check for type mismatches** (UUID vs VARCHAR, etc.)
- [ ] **Verify all dependencies** are properly imported
- [ ] **Check configuration files** for missing settings

### **Before Claiming "It Works"**
- [ ] **Database is actually populated** with test data
- [ ] **API endpoints return expected data** (not just 200 status)
- [ ] **No error messages** in logs that are being ignored
- [ ] **Schema consistency** across all related tables
- [ ] **Performance requirements** are actually met
- [ ] **Error handling** works for edge cases

### **Documentation Updates**
- [ ] **Update completion summary** with actual fixes made
- [ ] **Create cursor rules** for lessons learned
- [ ] **Update master log** with current status
- [ ] **Document schema changes** and their rationale
- [ ] **Note any workarounds** that were implemented
```

---

### 9. Cursor AppArmor Fix for Ubuntu
**File:** `cursor_apparmor_fix.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Cursor Apparmor Fix rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '73954c227c3100ff1fbf101d8509c038a2c6ca88a7c33327cae43437a292f9a7',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'cursor_apparmor_fix',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: cursor_apparmor_fix',
 'updated': '2025-08-15',
 'version': 1}
```

# Cursor AppArmor Fix for Ubuntu

## Description
This rule provides the solution for fixing "Cursor is not responding" pauses on Ubuntu caused by AppArmor security restrictions interfering with Cursor AppImage.

## 🎯 **Problem**
- **AppArmor restrictions** on AppImage execution causing freezes
- **Sandbox errors** in Electron framework
- **High resource usage** during AI operations leading to unresponsiveness
- **Common on Ubuntu 22.04+** with stricter AppArmor policies

## 🔧 **Solution**

### **Automated Fix**
```bash
# Run the automated fix script
./scripts/setup/fix_cursor_apparmor.sh
```

### **Manual Steps**
1. **Install dependencies**: `sudo apt install libfuse2t64 -y`
2. **Move AppImage**: Copy to `~/Applications/cursor.AppImage`
3. **Create AppArmor profile**: `/etc/apparmor.d/cursor-appimage` with unconfined mode
4. **Apply profile**: `sudo apparmor_parser -r /etc/apparmor.d/cursor-appimage`
5. **Create desktop entry**: `/usr/share/applications/cursor.desktop` with `--no-sandbox`
6. **Clean up old references**: Remove old desktop entries and launch scripts

### **AppArmor Profile**
```bash
profile cursor /home/mccoy/Applications/cursor*.AppImage flags=(unconfined) {
  userns,
  include if exists <local/cursor>
}
```

### **Desktop Entry**
```ini
[Desktop Entry]
Name=Cursor
Exec=/home/mccoy/Applications/cursor.AppImage --no-sandbox
Icon=/home/mccoy/.local/share/cursor/cursor.png
Type=Application
Categories=Development;
Comment=AI-first code editor
```

## 📋 **Verification**

### **Check AppArmor Profile**
```bash
sudo aa-status | grep cursor
```

### **Test Cursor Launch**
```bash
~/Applications/cursor.AppImage --no-sandbox
```

### **Monitor Resources**
```bash
htop
```

## 🚨 **Troubleshooting**

### **If Issues Persist**
1. **Add GPU disable flag**: `--no-sandbox --disable-gpu`
2. **Check for updates**: Download latest from cursor.com/downloads
3. **Monitor resources**: Use `htop` during AI operations
4. **Test network**: Cursor Settings > Network > Run Diagnostics

### **Emergency Recovery**
```bash
# Restart AppArmor
sudo systemctl restart apparmor

# Remove profile if needed
sudo rm /etc/apparmor.d/cursor-appimage
sudo apparmor_parser -r /etc/apparmor.d/cursor-appimage
```

## 🎯 **Expected Results**
- ✅ **No more freezing** during AI operations
- ✅ **Smooth Cursor behavior** on Ubuntu
- ✅ **Reliable AI assistant** functionality
- ✅ **Better performance** during resource-intensive tasks

## 📊 **System Requirements**
- **Ubuntu 22.04+** (tested on Ubuntu 25.04)
- **libfuse2t64** package installed
- **8GB+ RAM** recommended for AI operations
- **Stable internet connection** for AI features
```

---

### 10. Database Schema Consistency
**File:** `database_schema_consistency.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Database Schema Consistency rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'c58b6f892b074334e5eb30913daa45eea5cc6e5750594d4a0b375f84d7b1dfcd',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'database_schema_consistency',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: database_schema_consistency',
 'updated': '2025-08-15',
 'version': 1}
```

# Database Schema Consistency

## 🎯 **Core Principle**
Maintain consistent data types and relationships across all database tables to prevent runtime errors and ensure proper API functionality.

## 📋 **Critical Schema Rules**

### **Run ID Format Consistency**
- **Use VARCHAR(255) for run_id columns** across all tables
- **Never use UUID type** for run_id columns
- **String format**: `YYYYMMDD_HHMMSS_topic-name` (e.g., `20250813_205443_youtube-analysis--https---www-youtube-co`)

### **Required Schema Updates**
```sql
-- Always use these data types for consistency
ALTER TABLE lte.documents ALTER COLUMN run_id TYPE VARCHAR(255);
ALTER TABLE lte.graph_snapshots ALTER COLUMN run_id TYPE VARCHAR(255);
ALTER TABLE lte.claims ALTER COLUMN doc_id TYPE INTEGER;
```

### **Document Storage Schema**
```sql
-- lte.documents table structure
CREATE TABLE lte.documents (
    id INTEGER PRIMARY KEY,
    run_id VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    uri TEXT,
    title TEXT,
    published_at TIMESTAMP,
    shard_no INTEGER DEFAULT 1,
    text_len INTEGER,
    sha256 VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 **Implementation Requirements**

### **VeritasRunner Database Integration**
- **Always store documents** in database after bundle creation
- **Use proper field mapping** from canonicalized documents to database schema
- **Handle errors gracefully** without failing the entire run

```python
# Required database storage in VeritasRunner.start()
try:
    from src.storage.pgvector_store import PgVectorStore
    from src.config.living_truth_config import LivingTruthConfig
    
    # Initialize pgvector store
    config = LivingTruthConfig()
    dsn = f"postgresql://postgres:pass@postgres:5432/living_truth_engine"
    pgvector_store = PgVectorStore(dsn, embedder=None)
    
    # Convert canonicalized docs to database format
    db_docs = []
    for doc in canonicalized_docs:
        db_doc = {
            "id": doc.get("id", ""),
            "source_type": doc.get("source_type", "unknown"),
            "uri": doc.get("uri", ""),
            "title": doc.get("title", ""),
            "text": doc.get("text", "")
        }
        db_docs.append(db_doc)
    
    # Store documents in database
    if db_docs:
        pgvector_store.upsert_docs(run_id, db_docs)
        logger.info(f"Stored {len(db_docs)} documents in database for run {run_id}")
        
except Exception as e:
    logger.error(f"Failed to store documents in database: {e}")
    # Don't fail the run, just log the error
```

### **PgVectorStore upsert_docs Method**
- **Match actual database schema** in SQL queries
- **Use correct column names** and data types
- **Handle conflicts properly** with ON CONFLICT clauses

```python
def upsert_docs(self, run_id: str, docs: List[Dict[str, Any]]):
    """Upsert documents and their embeddings to pgvector store"""
    with self.db.cursor() as cur:
        for d in docs:
            # Insert document using actual schema columns
            cur.execute(
                "INSERT INTO lte.documents(run_id,source_type,uri,title,text_len,sha256) "
                "VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (run_id,source_type,uri,shard_no) DO UPDATE SET title=EXCLUDED.title,text_len=EXCLUDED.text_len,sha256=EXCLUDED.sha256",
                (run_id, d["source_type"], d.get("uri", ""), d.get("title", ""), len(d.get("text", "")), d.get("id", ""))
            )
```

## 🚨 **Common Issues to Avoid**

### **UUID Format Mismatch**
- ❌ **Don't use UUID type** for run_id columns
- ❌ **Don't assume** database schema matches code expectations
- ✅ **Always verify** schema before implementing storage code
- ✅ **Use VARCHAR(255)** for run_id columns consistently

### **Missing Database Storage**
- ❌ **Don't create bundles** without storing documents in database
- ❌ **Don't ignore** database storage errors
- ✅ **Always implement** database storage in VeritasRunner
- ✅ **Log errors** but don't fail the entire run

### **Schema Mismatch**
- ❌ **Don't assume** column names and types
- ❌ **Don't use hardcoded** schema expectations
- ✅ **Check actual schema** with `\d table_name`
- ✅ **Update code** to match actual database structure

## ✅ **Validation Checklist**

### **Before Implementing Database Storage**
- [ ] **Check actual schema** with `\d table_name` command
- [ ] **Verify data types** match code expectations
- [ ] **Test database connection** and permissions
- [ ] **Validate field mapping** from source data to database columns

### **After Implementation**
- [ ] **Test document storage** with actual run data
- [ ] **Verify API endpoints** work with stored data
- [ ] **Check error handling** for database failures
- [ ] **Validate performance** of database operations

## 📊 **Testing Requirements**

### **Schema Validation**
```bash
# Check actual table schema
docker exec living-truth-postgres psql -U postgres -d living_truth_engine -c "\d lte.documents"

# Verify run_id format
docker exec living-truth-postgres psql -U postgres -d living_truth_engine -c "SELECT DISTINCT run_id FROM lte.documents LIMIT 5;"
```

### **Storage Validation**
```bash
# Create test run
curl -s -X POST http://localhost:8050/api/runs/youtube/start -H 'Content-Type: application/json' -d '{"channel_url":"https://www.youtube.com/@imaginationpodcastofficial","limit":1,"sort":"oldest","max_depth":1}'

# Verify documents stored
docker exec living-truth-postgres psql -U postgres -d living_truth_engine -c "SELECT COUNT(*) FROM lte.documents WHERE run_id LIKE '%youtube%';"
```

## 📚 **References**

- **Phase 9.5.3**: Database schema fixes and document storage implementation
- **PgVectorStore**: Database storage implementation
- **VeritasRunner**: Bundle creation and database integration
- **API Endpoints**: Timeline and graph API functionality
```

---

### 11. Docker Best Practices for Living Truth Engine
**File:** `docker_best_practices.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Docker Best Practices rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '07ce04dc1cb3cac9fb68558caabcae9e4afeabcecc6a5ca668c03e6b58d4cf01',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'docker_best_practices',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: docker_best_practices',
 'updated': '2025-08-15',
 'version': 1}
```

# Docker Best Practices for Living Truth Engine

## Description
This rule establishes Docker best practices for the Living Truth Engine project, ensuring modern, secure, and efficient containerization.

## 🐳 **Docker Configuration Standards**

### **Docker Compose v2 (Required)**
```yaml
# ✅ Good - Modern Docker Compose v2 syntax
services:
  langflow:
    image: langflowai/langflow:latest
    container_name: living_truth_langflow
    ports:
      - "7860:7860"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    restart: unless-stopped
    networks:
      - living-truth-network

# ❌ Bad - Deprecated v1 syntax
version: '3.8'
services:
  langflow:
    image: langflowai/langflow
    ports:
      - "7860:7860"
```

### **Security Best Practices**
```dockerfile
# ✅ Good - Non-root user, security hardening
FROM python:3.12-slim

# Install system dependencies with cleanup
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### **Volume and Network Configuration**
```yaml
# ✅ Good - Explicit networks, read-only volumes
services:
  living-truth-mcp:
    volumes:
      - ../data/sources:/app/data/sources:ro  # Read-only
      - ../data/outputs/logs:/app/data/outputs/logs
      - ../.env:/app/.env:ro  # Read-only
    networks:
      - living-truth-network

networks:
  living-truth-network:
    driver: bridge
    name: living-truth-network

volumes:
  postgres_data:
    driver: local
    name: living-truth-postgres-data
```

## 📋 **Docker Configuration Checklist**

### **Before Creating Dockerfile**
- [ ] **Use slim base images** (e.g., `python:3.12-slim`)
- [ ] **Install dependencies before code copy** (layer caching)
- [ ] **Create non-root user** for security
- [ ] **Add health checks** for monitoring
- [ ] **Use .dockerignore** to exclude unnecessary files

### **Before Creating docker-compose.yml**
- [ ] **Use Docker Compose v2** syntax (no `version` field)
- [ ] **Specify image tags** (e.g., `:latest`, `:17-alpine`)
- [ ] **Add container names** for easy identification
- [ ] **Configure health checks** for all services
- [ ] **Set restart policies** (`unless-stopped`, `always`)
- [ ] **Use explicit networks** and volumes
- [ ] **Make sensitive volumes read-only** (`:ro`)

### **Before Deploying**
- [ ] **Validate compose file** with `docker compose config`
- [ ] **Test health checks** manually
- [ ] **Verify environment variables** are loaded
- [ ] **Check port conflicts** before starting
- [ ] **Run validation script** (`./scripts/setup/validate_docker.sh`)

## 🔧 **Docker Commands and Scripts**

### **Service Management**
```bash
# ✅ Use Docker Compose v2 commands
docker compose -f docker/docker-compose.yml up -d
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml logs -f

# ✅ Use project scripts
./scripts/setup/start_services.sh
./scripts/setup/stop_services.sh
./scripts/setup/validate_docker.sh
```

### **Build Optimization**
```bash
# ✅ Enable BuildKit for faster builds
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml build

# ✅ Use BuildKit inline cache
docker build --build-arg BUILDKIT_INLINE_CACHE=1 .
```

### **System Maintenance**
```bash
# ✅ Clean up unused resources
docker image prune -f
docker system prune
docker volume prune

# ✅ Update system components
./scripts/setup/update_system.sh
```

## 🚨 **Common Docker Mistakes to Avoid**

### **Security Issues**
- ❌ **Running as root** in containers
- ❌ **Mounting volumes without read-only** for sensitive data
- ❌ **Using latest tags** without pinning versions
- ❌ **Exposing unnecessary ports**
- ❌ **Not using health checks**

### **Performance Issues**
- ❌ **Not using .dockerignore** (large build context)
- ❌ **Copying code before dependencies** (poor layer caching)
- ❌ **Not using BuildKit** (slower builds)
- ❌ **Using full base images** instead of slim
- ❌ **Not cleaning up** apt cache in Dockerfile

### **Configuration Issues**
- ❌ **Using Docker Compose v1** syntax
- ❌ **Not specifying restart policies**
- ❌ **Missing health checks**
- ❌ **Not using explicit networks**
- ❌ **Hardcoded values** instead of environment variables

## 📊 **Docker Best Practices Metrics**

- ✅ **Security**: 100% non-root containers
- ✅ **Performance**: BuildKit enabled, slim images
- ✅ **Reliability**: Health checks on all services
- ✅ **Maintainability**: Clear naming, documentation
- ✅ **Modern**: Docker Compose v2, latest practices

## 🎯 **Docker Development Workflow**

### **1. Development Setup**
```bash
# Start development environment
./scripts/setup/start_services.sh

# Validate configuration
./scripts/setup/validate_docker.sh
```

### **2. Testing**
```bash
# Test services individually
curl -f http://localhost:7860/health  # Langflow
curl -f http://localhost:8000/health  # MCP Server
pg_isready -h localhost -p 5432  # PostgreSQL
```

### **3. Deployment**
```bash
# Build and deploy
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml up -d --build

# Monitor deployment
docker compose -f docker/docker-compose.yml logs -f
```
```

---

### 12. Docker Health Check Best Practices
**File:** `docker_health_checks.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Docker Health Checks rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '231c2b40992c305680b7ef09fb57a850acc5de654db83f27c20affd818e84f37',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'docker_health_checks',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: docker_health_checks',
 'updated': '2025-08-15',
 'version': 1}
```

# Docker Health Check Best Practices

## Description
This rule defines Docker health check best practices and troubleshooting procedures for the Living Truth Engine project.

## 🎯 **Health Check Standards**

### **Health Check Requirements**
- **All services must have health checks** configured
- **Health checks must be lightweight** and fast
- **Use appropriate tools** available in the container
- **Avoid external dependencies** when possible
- **Set reasonable timeouts** and retry intervals

### **Health Check Patterns**

#### **HTTP Services**
```yaml
# ✅ Good - HTTP health check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s

# ✅ Good - Dashboard health check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8050/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

#### **TCP Services**
```yaml
# ✅ Good - TCP connection test (when curl not available)
healthcheck:
  test: ["CMD-SHELL", "timeout 10 bash -c '</dev/tcp/localhost/1234' || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

#### **Database Services**
```yaml
# ✅ Good - Database-specific health check
healthcheck:
  test: ["CMD", "pg_isready", "-U", "postgres", "-d", "living_truth_engine"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

## 🚨 **Common Health Check Issues**

### **Tool Availability Issues**
- ❌ **Using curl when not available**: LM Studio container doesn't have curl
- ❌ **Using wget when not available**: Some containers lack wget
- ❌ **Using python when not available**: Minimal containers may not have Python

### **Port Mapping Issues**
- ❌ **Wrong port in health check**: Using internal port instead of external
- ❌ **Port conflicts**: Multiple services using same port
- ❌ **Network issues**: Health check can't reach service

### **Configuration Issues**
- ❌ **Missing health check**: Service has no health check configured
- ❌ **Incorrect test command**: Health check command doesn't work
- ❌ **Wrong timeout values**: Too short or too long timeouts

## 🔧 **Health Check Troubleshooting**

### **Diagnosing Health Check Failures**
```bash
# Check container health status
docker inspect <container_name> --format='{{.State.Health.Status}}'

# View health check logs
docker inspect <container_name> --format='{{range .State.Health.Log}}{{.Output}}{{end}}'

# Test health check manually
docker exec <container_name> <health_check_command>
```

### **Common Fixes**

#### **LM Studio Health Check Fix**
```yaml
# ❌ Bad - Uses curl (not available)
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:1234/v1/models"]

# ✅ Good - Uses TCP connection test
healthcheck:
  test: ["CMD-SHELL", "timeout 10 bash -c '</dev/tcp/localhost/1234' || exit 1"]
```

#### **PostgreSQL Health Check Fix**
```yaml
# ❌ Bad - Generic health check
healthcheck:
  test: ["CMD", "pg_isready"]

# ✅ Good - Specific database check
healthcheck:
  test: ["CMD", "pg_isready", "-U", "postgres", "-d", "living_truth_engine"]
```

## 📋 **Health Check Checklist**

### **Before Deploying**
- [ ] **Verify tool availability** in container
- [ ] **Test health check command** manually
- [ ] **Set appropriate timeouts** and intervals
- [ ] **Configure start period** for slow-starting services
- [ ] **Use container-specific tools** when available

### **After Deployment**
- [ ] **Monitor health status** for all containers
- [ ] **Check health check logs** for failures
- [ ] **Verify service functionality** despite health status
- [ ] **Update health checks** if needed

### **Troubleshooting Steps**
- [ ] **Check container logs** for startup issues
- [ ] **Test health check manually** inside container
- [ ] **Verify port mappings** and network connectivity
- [ ] **Update health check configuration** if needed
- [ ] **Restart container** to apply changes

## 🎯 **Service-Specific Health Checks**

### **LM Studio**
```yaml
healthcheck:
  test: ["CMD-SHELL", "timeout 10 bash -c '</dev/tcp/localhost/1234' || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

### **PostgreSQL**
```yaml
healthcheck:
  test: ["CMD", "pg_isready", "-U", "postgres", "-d", "living_truth_engine"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

### **Neo4j**
```yaml
healthcheck:
  test: ["CMD-SHELL", "cypher-shell -u neo4j -p livingtruth123 'RETURN 1'"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### **Redis**
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### **Langflow**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

## 📊 **Health Check Metrics**
- ✅ **100% health check coverage** for all services
- ✅ **Appropriate tool usage** for each container
- ✅ **Reasonable timeout values** and intervals
- ✅ **Proper error handling** and retry logic
- ✅ **Container-specific optimizations**
```

---

### 13. Compose Rules
**File:** `docker_management.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Docker Management rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'bd639545ff5b28570d669b7173c20ea8d95adaefb179099837eb9d20489d9162',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'docker_management',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: docker_management',
 'updated': '2025-08-15',
 'version': 1}
```

# Compose Rules
- Healthchecks for all services; fail fast if any gate fails.
- Use `host.docker.internal:1234/v1` for LM Studio from containers.

# Init DB (pgvector)
- Mount `docker/initdb/` to Postgres; `002_pgvector.sql` must exist.
```

---

### 14. Error Handling and Testing Standards
**File:** `error_handling_and_testing.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Error Handling And Testing rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '2ce138ff4e6e469ff37287ba15437b5e072ffc8cde81b02b3e8a667d16acb06a',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'error_handling_and_testing',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: error_handling_and_testing',
 'updated': '2025-08-15',
 'version': 1}
```

# Error Handling and Testing Standards

## Description
This rule establishes error handling and testing standards for the Living Truth Engine project, ensuring proper error reporting and comprehensive testing.

## 🚫 **No Fallback Mechanisms**

### **Fail-Fast Principle**
- **❌ NO FALLBACKS**: Never create placeholder files or silent fallbacks
- **✅ THROW ERRORS**: If something fails, throw a clear error immediately
- **✅ CLEAR MESSAGING**: Error messages should explain exactly what failed and why
- **✅ PROPER EXCEPTIONS**: Use appropriate exception types (RuntimeError, ValueError, etc.)

### **Examples of Bad Error Handling**
```python
# ❌ BAD - Silent fallback
try:
    result = some_operation()
except Exception as e:
    # Creates placeholder file instead of throwing error
    create_placeholder_file()
    return "Warning: Operation failed but created placeholder"

# ❌ BAD - Generic error handling
try:
    result = some_operation()
except Exception as e:
    return f"Error: {e}"  # Too generic
```

### **Examples of Good Error Handling**
```python
# ✅ GOOD - Clear error with context
try:
    result = some_operation()
except FileNotFoundError as e:
    raise RuntimeError(f"Required file not found: {e}")
except ConnectionError as e:
    raise RuntimeError(f"Service connection failed: {e}")
except Exception as e:
    raise RuntimeError(f"Unexpected error in some_operation: {e}")

# ✅ GOOD - Specific error types
def generate_audio(text: str) -> str:
    try:
        voice = PiperVoice.load("en_US-lessac-medium.onnx")
        voice.synthesize(text, output_path)
        return f"✅ Audio generated successfully: {output_path}"
    except FileNotFoundError as e:
        raise RuntimeError(f"Piper TTS voice model not found: {e}")
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")
```

## 🧪 **Functional Testing Standards**

### **Test Categories**
1. **Service Functionality**: Test actual service capabilities, not just health checks
2. **Data Processing**: Verify real data processing and analysis
3. **Integration**: Test service interactions and dependencies
4. **Error Conditions**: Test proper error handling and reporting
5. **Performance**: Verify response times and resource usage

### **Functional Test Requirements**
```python
# ✅ GOOD - Tests actual functionality
def test_audio_generation_functionality(self):
    """Test audio generation can create actual audio files"""
    try:
        result = self.engine.generate_audio("Test text")
        
        # Verify actual audio file was created
        audio_files = list(Path("data/outputs/audio").glob("*.wav"))
        if not audio_files:
            return False
            
        latest_audio = max(audio_files, key=lambda x: x.stat().st_mtime)
        file_size = latest_audio.stat().st_size
        
        # Real audio files should be substantial
        if file_size < 1000:
            return False
            
        return True
    except Exception as e:
        # If audio generation fails, it should throw an error
        logger.error(f"Audio generation test failed: {e}")
        return False

# ❌ BAD - Only tests health checks
def test_audio_generation(self):
    """Test audio generation health check"""
    response = requests.get("http://localhost:8050/health")
    return response.status_code == 200  # This doesn't test actual audio generation
```

### **Test Coverage Requirements**
- **100% Core Functionality**: All main features must have functional tests
- **Error Path Testing**: Test error conditions and proper error handling
- **Integration Testing**: Test service interactions and dependencies
- **Performance Testing**: Verify response times and resource usage
- **Data Validation**: Verify output data quality and structure

## 📊 **Testing Metrics**

### **Functional Test Results**
- **✅ 6/7 Tests Passing**: Core functionality working
- **❌ 1/7 Tests Failing**: Audio generation needs piper-tts models
- **🎯 85% Coverage**: Most functionality verified

### **Current Test Categories**
1. **✅ Langflow Workflow**: API accessible, health checks pass
2. **✅ Dashboard Visualization**: Interface loads, data validation works
3. **✅ LM Studio Models**: Model availability and API access verified
4. **❌ Audio Generation**: Fails due to missing piper-tts voice models
5. **✅ Transcript Analysis**: Real data processing verified
6. **✅ Visualization Generation**: Network graph creation verified
7. **✅ MCP Server Tools**: Core MCP functionality verified

## 🔧 **Error Handling Implementation**

### **Current Error Handling**
- **✅ Audio Generation**: Throws RuntimeError when piper-tts models missing
- **✅ Langflow Workflow**: Throws NotImplementedError for unimplemented features
- **✅ MCP Server**: Proper error propagation and logging
- **✅ Database Operations**: Clear error messages for connection issues

### **Error Handling Checklist**
- [ ] **No silent failures** - All errors are logged and reported
- [ ] **Clear error messages** - Errors explain what failed and why
- [ ] **Proper exception types** - Use appropriate exception classes
- [ ] **Error context** - Include relevant context in error messages
- [ ] **No fallback mechanisms** - Don't create placeholder data
- [ ] **Fail fast** - Throw errors immediately when operations fail

## 🎯 **Best Practices**

### **Error Handling**
1. **Be Specific**: Use specific exception types and clear error messages
2. **Include Context**: Provide relevant context about what failed
3. **Log Errors**: Always log errors with appropriate detail
4. **Fail Fast**: Don't continue with invalid state
5. **No Placeholders**: Never create placeholder or dummy data

### **Testing**
1. **Test Functionality**: Test what the service actually does, not just if it's running
2. **Test Error Paths**: Verify proper error handling and reporting
3. **Test Real Data**: Use real data and verify actual processing
4. **Test Integration**: Verify service interactions work correctly
5. **Test Performance**: Ensure response times meet requirements

### **Quality Assurance**
1. **Run Functional Tests**: Execute comprehensive functional tests regularly
2. **Monitor Error Rates**: Track and analyze error patterns
3. **Validate Output**: Verify output data quality and structure
4. **Performance Monitoring**: Monitor response times and resource usage
5. **Documentation**: Keep error handling and testing documentation current

## 🗄️ **Database Constraint Violation Handling**

### **UPSERT Pattern for Idempotent Operations**
- **Use `ON CONFLICT` clauses** for all database insertions that may have duplicates
- **Transaction safety** - Wrap related operations in database transactions
- **Clear error messages** - Provide specific guidance for constraint violations
- **Rebuild functionality** - Support clearing existing data for clean rebuilds

### **Examples of Good Constraint Handling**
```python
# ✅ GOOD - UPSERT with conflict handling
def store_entity(self, doc_id: int, entity: Dict[str, Any]) -> int:
    """Store an entity and return its ID. Uses UPSERT to handle duplicates."""
    with self.db.cursor() as cur:
        cur.execute(
            "INSERT INTO lte.entities (doc_id, type, value, span_start, span_end, conf) "
            "VALUES (%s, %s, %s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING RETURNING id",
            (doc_id, entity['type'], entity['value'], entity.get('span_start'),
             entity.get('span_end'), entity.get('conf', 1.0))
        )
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            # If conflict occurred, get the existing ID
            cur.execute(
                "SELECT id FROM lte.entities WHERE doc_id = %s AND type = %s AND value = %s",
                (doc_id, entity['type'], entity['value'])
            )
            return cur.fetchone()[0]

# ✅ GOOD - Transaction management
def process_run(self, run_id: str, documents: List[Dict[str, Any]], rebuild: bool = False):
    """Process a complete run through the linking pipeline."""
    try:
        # Start transaction
        self.pgvector_store.db.autocommit = False
        
        try:
            # Clear existing data if rebuild requested
            if rebuild:
                self.pgvector_store.clear_run_data(run_id)
            
            # Process documents and store data
            # ... processing logic ...
            
            # Commit transaction
            self.pgvector_store.db.commit()
            return results
            
        except Exception as e:
            # Rollback transaction on error
            self.pgvector_store.db.rollback()
            raise
            
        finally:
            # Restore autocommit
            self.pgvector_store.db.autocommit = True
            
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}
```

### **API Error Response Standards**
```python
# ✅ GOOD - Specific error codes for constraint violations
if 'duplicate key value violates unique constraint' in error_msg:
    return envelope_err(
        f"Graph building failed due to constraint violation. Try using ?rebuild=1 to clear existing data: {error_msg}", 
        409,
        {"code": "graph_build_conflict", "hint": "Use ?rebuild=1 to clear existing data"}
    )
```

### **JSON Serialization Handling**
```python
# ✅ GOOD - DateTime conversion for JSON serialization
def convert_datetime(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return obj

# Convert all datetime fields before JSON serialization
for doc in documents:
    if 'created_at' in doc and doc['created_at']:
        doc['created_at'] = convert_datetime(doc['created_at'])
```


**Follow these standards to ensure robust error handling and comprehensive testing throughout the Living Truth Engine project.**

alwaysApply: false

alwaysApply: false

alwaysApply: false

alwaysApply: false
```

---

### 15. Fallbacks & Health
**File:** `fallbacks_and_health.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Fallbacks And Health rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'e340914c927b7ff71200923817ba7a26314361b2fe9a2e903e67c584bdb9e9a0',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'fallbacks_and_health',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: fallbacks_and_health',
 'updated': '2025-08-15',
 'version': 1}
```

# Fallbacks & Health

## 🚨 **Allowed Fallbacks Only**

### **Explicitly Permitted Fallbacks**
- **YouTube captions/transcripts**: When MCP fetch fails
- **Reranker CPU execution**: When GPU is occupied (log the switch)
- **Dev-only in-memory search**: When pgvector is unavailable (dev environment only)

### **Fallback Requirements**
- **Log every fallback** with timestamp and reason
- **Expose short summary** in `/api/health/full`
- **No silent fallbacks** - all must be observable
- **Fail fast** if no fallback is available

## 📊 **Health Monitoring**

### **Health Endpoint Requirements**
- `/api/health/full` must include fallback event summary
- Track last N fallback events with timestamps
- Provide fallback frequency metrics
- Include system state indicators

### **Fallback Event Structure**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "type": "youtube_captions|reranker_cpu|in_memory_search",
  "reason": "MCP fetch failed|GPU occupied|pgvector unavailable",
  "duration_ms": 1500
}
```

## 🔧 **Implementation Standards**

### **Logging Requirements**
```python
# ✅ Good - Explicit fallback logging
logger.warning(f"Using CPU reranker fallback: {reason}")

# ❌ Bad - Silent fallback
# No logging of fallback usage
```

### **Health Integration**
- Centralize fallback guards and logging
- Expose last N events in health endpoint
- Provide fallback statistics and trends

### **Error Handling**
- Clear error messages when fallbacks unavailable
- Graceful degradation when possible
- User notification of fallback usage

## 📋 **Monitoring Requirements**

### **Fallback Metrics**
- Count of fallback events by type
- Average duration of fallback operations
- Success rate of fallback mechanisms
- Impact on overall system performance

### **Health Checks**
- Verify fallback mechanisms are available
- Check fallback event logs for anomalies
- Monitor fallback frequency trends
- Alert on excessive fallback usage

## ✅ **Implementation Checklist**

- [ ] Only allowed fallbacks implemented
- [ ] All fallbacks logged with timestamps
- [ ] Health endpoint includes fallback summary
- [ ] Fallback events exposed in monitoring
- [ ] Error handling for unavailable fallbacks
- [ ] Documentation of fallback policies

## 🔧 **Examples**

### **Fallback Logging**
```python
import logging

logger = logging.getLogger(__name__)

def process_with_fallback():
    try:
        return process_primary()
    except Exception as e:
        logger.warning(f"Using CPU reranker fallback: {e}")
        return process_cpu_fallback()
```

### **Health Response**
```json
{
  "status": "ok",
  "data": {
    "fallback_events": [
      {
        "timestamp": "2024-01-01T12:00:00Z",
        "type": "reranker_cpu",
        "reason": "GPU occupied",
        "duration_ms": 1500
      }
    ],
    "fallback_stats": {
      "total_events": 5,
      "cpu_reranker": 3,
      "youtube_captions": 2
    }
  }
}
```

## 📚 **References**
- Phase 9.3 for fallback policy carry-over
- Phase 9.5.2 for expanded fallback monitoring
- @api_contracts.mdc for health endpoint format
- @core_workflow.mdc for development protocol
description:
globs:
alwaysApply: false
```

---

### 16. How to Build Cursor Rules - Complete Guide
**File:** `how_to_make_a_cursor_rule.mdc`

**Metadata:**

**Content:**
```mdc
---
description: How To Make A Cursor Rule rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '69ed3d1144831c5312fbd5db341ca2dbb09a261391e35855304205178903e101',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'how_to_make_a_cursor_rule',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: how_to_make_a_cursor_rule',
 'updated': '2025-08-15',
 'version': 1}
```

# How to Build Cursor Rules - Complete Guide

## Description
This rule provides comprehensive guidance on creating effective Cursor rules, including proper structure, metadata, content organization, and best practices for different rule types.

## 🔧 **Cursor Rule Validation Tools**

### **Available MCP Tools**
The Living Truth Engine provides automated tools for validating and fixing cursor rule frontmatter:

1. **`validate_cursor_rules()`** - Validates all `.mdc` files in `.cursor/rules/` for proper frontmatter
2. **`fix_cursor_rule_frontmatter(filename)`** - Fixes frontmatter for a specific `.mdc` file

### **Usage Examples**
```python
# Validate all cursor rules
result = engine.validate_cursor_rules()
print(result)

# Fix a specific file
result = engine.fix_cursor_rule_frontmatter('my_rule.mdc')
print(result)
```

### **Validation Checks**
The validation tool checks for:
- ✅ YAML frontmatter presence
- ✅ Required fields: `description`, `globs`, `alwaysApply`
- ✅ Valid YAML syntax
- ✅ Proper structure and formatting

### **When to Use Validation Tools**
- **Before committing** cursor rule changes
- **When troubleshooting** cursor rule issues
- **After manual edits** to ensure proper formatting
- **During development** to catch frontmatter errors early

## 🎯 **What Are Cursor Rules?**

Cursor rules are **long-term memory** that you and your team can access. They capture:
- Domain-specific context and workflows
- Formatting and coding conventions
- Architecture decisions and patterns
- Project-specific knowledge and automation

## 📋 **Rule Anatomy - Required Structure**

### **Frontmatter (Required)**
Every rule MUST have proper frontmatter:

```yaml
```

### **Rule Types and Properties**

| Rule Type | Description | Properties |
|-----------|-------------|------------|
| **Always** | Always included in model context | `alwaysApply: true` |
| **Auto Attached** | Included when files match glob patterns | `globs: ["*.ts", "*.js"]` |
| **Agent Requested** | AI decides whether to include | `description: "required"` |
| **Manual** | Only when explicitly mentioned | `@ruleName` |

## 🏗️ **Creating Rules - Step-by-Step Process**

### **1. Choose Rule Type**
- **Always**: For critical, project-wide rules (coding standards, architecture)
- **Auto Attached**: For file-type specific rules (React patterns, API conventions)
- **Agent Requested**: For contextual rules (debugging, testing patterns)
- **Manual**: For specialized rules (deployment, specific workflows)

### **2. Define Scope with Globs**
```yaml
globs: 
  - "*.ts"                    # All TypeScript files
  - "**/components/**"        # All component directories
  - "src/**/*.js"            # JavaScript files in src
  - ".cursor/**"             # Cursor configuration files
  - "**/mcp*.json"           # MCP configuration files
```

### **3. Write Clear Description**
- **Be specific** about what the rule covers
- **Include keywords** for AI discovery
- **Mention file types** or contexts where it applies

### **4. Structure Content Properly**

#### **Header Section**
```markdown
# Rule Title

## Description
What this rule does and why it's important.

## 🎯 **Key Objectives**
- Primary goal 1
- Primary goal 2
```

#### **Main Content**
```markdown
## 📋 **Requirements**
- [ ] Requirement 1
- [ ] Requirement 2

## ✅ **Best Practices**
- Do this
- Don't do that

## 🔧 **Examples**
```code
// Good example
const goodCode = "example";

// Bad example  
const badCode = "avoid";
```
```

#### **Footer**
```markdown
## 📚 **References**
- Link to documentation
- Related rules

@coding_standards.mdc
```

## 📁 **File Organization**

### **Project Structure**
```
project/
├── .cursor/
│   ├── rules/
│   │   ├── coding_standards.mdc
│   │   ├── architecture.mdc
│   │   └── workflows.mdc
│   └── settings.json
├── backend/
│   └── .cursor/
│       └── rules/
│           └── api_conventions.mdc
└── frontend/
    └── .cursor/
        └── rules/
            └── react_patterns.mdc
```

### **Naming Conventions**
- **Use descriptive names**: `api_conventions.mdc`, `react_patterns.mdc`
- **Use underscores**: `coding_standards.mdc` (not `coding-standards.mdc`)
- **Be specific**: `mcp_server_troubleshooting.mdc` (not `troubleshooting.mdc`)

## 🎨 **Content Best Practices**

### **Use Clear Headers**
```markdown
## 🚨 **CRITICAL** - Must follow
## ✅ **Best Practices** - Recommended
## ⚠️ **Warnings** - Be careful
## 🔧 **Examples** - Code samples
## 📋 **Checklist** - Step-by-step
```

### **Include Code Examples**
```markdown
#### **Good Example**
```typescript
// ✅ Correct way
const apiResponse = await fetch('/api/data');
```

#### **Bad Example**
```typescript
// ❌ Avoid this
const response = fetch('/api/data'); // Missing await
```
```

### **Use Checklists**
```markdown
#### **Before Creating New Feature**
- [ ] Check existing implementations
- [ ] Follow naming conventions
- [ ] Add proper error handling
- [ ] Write tests
- [ ] Update documentation
```

### **Reference Other Rules**
```markdown
## 📚 **Related Rules**
- @coding_standards.mdc - For general coding practices
- @mcp_server_integration.mdc - For MCP server patterns
```

## 🔧 **Creating Rules from Conversations**

### **Using `/Generate Cursor Rules`**
1. **Have a detailed conversation** about a topic
2. **Use `/Generate Cursor Rules`** command
3. **Review and edit** the generated rule
4. **Add proper frontmatter** and structure
5. **Test the rule** in a new conversation

### **Manual Creation Process**
1. **Identify recurring patterns** from conversations
2. **Create rule file** in `.cursor/rules/`
3. **Add proper frontmatter**
4. **Write comprehensive content**
5. **Test with `@ruleName`**

## 📊 **Rule Effectiveness Checklist**

### **Before Publishing**
- [ ] **Clear frontmatter** with proper description and globs
- [ ] **Specific scope** - not too broad or narrow
- [ ] **Actionable content** - tells what to do, not just what to avoid
- [ ] **Code examples** - shows good and bad practices
- [ ] **Proper formatting** - uses headers, lists, code blocks
- [ ] **Tested functionality** - works when referenced

### **After Publishing**
- [ ] **Test with `@ruleName`** in conversation
- [ ] **Verify auto-attachment** works for glob patterns
- [ ] **Check team adoption** - others can use it
- [ ] **Update as needed** - rules evolve with projects

## 🚨 **Common Mistakes to Avoid**

### **Frontmatter Issues**
- ❌ **Missing frontmatter** - rule won't be recognized
- ❌ **Vague description** - AI can't understand purpose
- ❌ **Incorrect globs** - rule won't apply to intended files
- ❌ **Missing `alwaysApply`** - unclear when rule should be used

### **Content Issues**
- ❌ **Too broad scope** - rule becomes irrelevant
- ❌ **No examples** - hard to understand and follow
- ❌ **Negative focus** - only says what not to do
- ❌ **Outdated information** - rule becomes misleading

### **Organization Issues**
- ❌ **Poor naming** - hard to find and reference
- ❌ **No cross-references** - rules don't work together
- ❌ **Inconsistent structure** - hard to maintain

## 🎯 **Advanced Techniques**

### **Conditional Rules**
```yaml
```

### **Nested Rules**
```
project/
├── .cursor/rules/
│   ├── general.mdc          # Project-wide rules
│   └── frontend/
│       ├── react.mdc        # React-specific rules
│       └── styling.mdc      # CSS/styling rules
```

### **Rule Dependencies**
```markdown
## 📚 **Prerequisites**
- @coding_standards.mdc - General coding practices
- @mcp_server_integration.mdc - MCP server patterns

## 📚 **Related Rules**
- @testing_standards.mdc - Testing conventions
- @docker_management.mdc - Deployment workflows
```

## 📈 **Measuring Rule Success**

### **Success Metrics**
- ✅ **Consistent application** across team
- ✅ **Reduced errors** in codebase
- ✅ **Faster onboarding** for new team members
- ✅ **Better code quality** and maintainability
- ✅ **Reduced repetitive questions** in conversations

### **Maintenance Schedule**
- **Weekly**: Review rule usage and effectiveness
- **Monthly**: Update rules based on project evolution
- **Quarterly**: Audit and consolidate related rules
```

---

### 17. Living Truth Agent Integration Process
**File:** `living_truth_agent_integration.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Living Truth Agent Integration rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'a77dcfb8e810ef7547ae5a8647a8e53dab586c9c48ad4f11dceb5b934a4f7991',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'living_truth_agent_integration',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: living_truth_agent_integration',
 'updated': '2025-08-15',
 'version': 1}
```

# Living Truth Agent Integration Process

## Description
This rule defines the systematic process for integrating Living Truth Agent functionality into LivingTruthEngine while building MCP tools for each component.

## 🎯 **Integration Process Standards**

### **Phase-Based Integration**
1. **Phase 1**: Core System Integration ✅ **COMPLETED**
   - Configuration system migrated
   - Hybrid retrieval system migrated
   - Research analysis system migrated

2. **Phase 2**: Advanced Features Integration 🔄 **IN PROGRESS**
   - Notebook Agent System
   - AGI Integration Layer
   - Channel Archiver System

3. **Phase 3**: MCP Integration Enhancement
   - Enhanced MCP tools for all components
   - Tool registry updates
   - Performance monitoring

### **MCP-First Development Pattern**
For every component migrated, follow this pattern:

1. **Create Component**: Migrate the core functionality
2. **Build MCP Tools**: Create MCP tools for the component
3. **Update Registry**: Add tools to tool_registry.json
4. **Test Integration**: Verify MCP tools work correctly
5. **Document**: Update cursor rules and documentation

## 📋 **MCP Tool Development Checklist**

### **Before Creating Any Component**
- [ ] **Check existing MCP tools** in tool_registry.json
- [ ] **Plan MCP tool structure** for the component
- [ ] **Define tool parameters** and return types
- [ ] **Consider tool categories** (analysis, system, langflow, etc.)

### **During Component Migration**
- [ ] **Create component file** with proper imports
- [ ] **Add MCP tool decorators** for key functions
- [ ] **Integrate with existing config** system
- [ ] **Follow error handling** patterns
- [ ] **Add logging** for debugging

### **After Component Creation**
- [ ] **Update tool registry** with new tools
- [ ] **Test MCP tools** via hub server
- [ ] **Update cursor rules** if needed
- [ ] **Document tool usage** examples

## 🔧 **MCP Tool Categories**

### **Analysis Tools** (Biblical Forensic)
- `analyze_biblical_evidence` - Biblical forensic analysis
- `extract_claims` - Claims extraction and verification
- `map_entities` - Entity relationship mapping
- `conduct_research_analysis` - Comprehensive research analysis

### **Notebook Agent Tools** (Document Processing)
- `process_documents` - Universal document processing
- `generate_study_guide` - Study guide generation
- `summarize_documents` - Document summarization
- `conduct_web_research` - Web research capabilities

### **AGI Integration Tools** (Advanced AI)
- `integrate_agi_analysis` - AGI system integration
- `cross_validate_findings` - Cross-validation of results
- `generate_confidence_scores` - Confidence scoring
- `create_integrated_insights` - Integrated insights generation

### **Processing Tools** (Content Management)
- `process_youtube_content` - YouTube content processing
- `archive_channel_content` - Channel archiving
- `extract_transcripts` - Transcript extraction
- `organize_content` - Content organization

## 🚨 **Integration Standards**

### **Required Patterns**
- **MCP-First**: Every component must have MCP tools
- **Error Handling**: No fallback mechanisms, fail-fast approach
- **Configuration**: Use centralized config system
- **Logging**: Comprehensive logging for all operations
- **Testing**: MCP tool testing for all functionality

### **File Organization**
```
LivingTruthEngine/src/
├── analysis/
│   ├── notebook_agent.py          # Notebook agent with MCP tools
│   ├── agi_integration.py         # AGI integration with MCP tools
│   └── channel_archiver.py        # Channel archiver with MCP tools
├── mcp_servers/
│   └── living_truth_fastmcp_server.py  # Enhanced with new tools
└── config/
    └── tool_registry.json         # Updated with new tools
```

### **MCP Tool Schema**
```json
{
  "name": "tool_name",
  "description": "Tool description",
  "server": "living_truth_fastmcp_server",
  "module": "src.mcp_servers.living_truth_fastmcp_server",
  "function": "tool_function",
  "params_schema": {
    "param_name": {
      "type": "string",
      "required": true,
      "description": "Parameter description"
    }
  }
}
```

## 🎯 **Integration Workflow**

### **1. Component Analysis**
```python
# Analyze source component
source_file = "living_truth_agent/core/component.py"
# Identify key functions for MCP tools
# Plan integration approach
```

### **2. Component Migration**
```python
# Create target component
target_file = "LivingTruthEngine/src/analysis/component.py"
# Migrate with MCP tool integration
# Follow LivingTruthEngine patterns
```

### **3. MCP Tool Creation**
```python
# Add MCP tools to living_truth_fastmcp_server.py
@mcp.tool()
def component_tool(param: str) -> str:
    """MCP tool for component functionality."""
    return component_instance.function(param)
```

### **4. Registry Update**
```json
// Update config/tool_registry.json
{
  "name": "component_tool",
  "description": "Component functionality",
  "server": "living_truth_fastmcp_server",
  "module": "src.mcp_servers.living_truth_fastmcp_server",
  "function": "component_tool"
}
```

### **5. Testing and Validation**
```python
# Test MCP tool via hub server
result = mcp_mcp_hub_server_execute_tool("component_tool", {"param": "test"})
# Validate functionality
# Update documentation
```

## 📊 **Integration Metrics**

### **Success Criteria**
- ✅ **100% MCP Coverage**: Every component has MCP tools
- ✅ **100% Tool Registry**: All tools documented in registry
- ✅ **100% Error Handling**: Proper error handling in all tools
- ✅ **100% Testing**: All MCP tools tested and working
- ✅ **100% Documentation**: All tools documented

### **Quality Standards**
- **Tool Response Time**: <1s for individual tools
- **Error Rate**: <5% in tool execution
- **Documentation**: Complete parameter descriptions
- **Testing**: Comprehensive test coverage

## 🚀 **Next Steps**

### **Phase 2.1: Notebook Agent System**
1. **Migrate notebook_agent.py** with MCP tools
2. **Create MCP tools** for document processing
3. **Update tool registry** with new tools
4. **Test integration** via MCP hub server

### **Phase 2.2: AGI Integration Layer**
1. **Migrate agi_integration.py** with MCP tools
2. **Create MCP tools** for AGI operations
3. **Update tool registry** with new tools
4. **Test integration** via MCP hub server

### **Phase 2.3: Channel Archiver System**
1. **Migrate channel_archiver.py** with MCP tools
2. **Create MCP tools** for content processing
3. **Update tool registry** with new tools
4. **Test integration** via MCP hub server
```

---

### 18. Master Log Rebuild Rule
**File:** `master_log.mdc`

**Metadata:**
- summary: **

**Content:**
```mdc
---
description: Master Log rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '5e118d3e0e2fc93d53208c2f1b994f6478d1c8fb8eccbe64687e5339c2269d05',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'master_log',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: master_log',
 'updated': '2025-08-15',
 'version': 1}
```

# Master Log Rebuild Rule

**When you create or modify any PHASE_* plan or completion summary:**

1. Run:
   - `scripts/rebuild_master_log.sh`
   - Verify `docs/project_master_log.md` updated.
2. Include the updated file in the same commit.
3. In PR/Delivery, paste the line `MasterLog: UPDATED` with the commit SHA.

**Do not** hand-edit `docs/project_master_log.md`. It's generated by `build_master_log.py`.
```

---

### 19. SSOT Requirement (hard fail)
**File:** `mcp_enforcement.mdc`

**Metadata:**

**Content:**
```mdc
---
description: MCP enforcement rules for Living Truth Engine. Enforce SSOT verification
  and rule validity.
globs:
- '**/*'
alwaysApply: true
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'bf0d0ee853f24c258cf3c07017a6d5f41dfcf7f81a87226b9fced65525e967fd',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'mcp_enforcement',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: mcp_enforcement',
 'updated': '2025-08-15',
 'version': 1}
```

# SSOT Requirement (hard fail)
- Command to run **before** approving/merging:
```bash
python scripts/verify_complete_ssot_system.py --fix
```
- On any failure: **stop** and remediate. Approvals are blocked until PASS.

# Commit Discipline
- Require `[SSOT Verified]` in commit message once SSOT checks pass.

# Prohibited
- Duplicate SSOT files outside root.
- Merging with failing SSOT Guard or Repo Health checks.
```

---

### 20. MCP Hub Server - Current Status and Usage
**File:** `mcp_hub_server_status.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Mcp Hub Server Status rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '68a2312d37c321203745816fd1f19d2c9a8b02d8701d0de79e487a315b4ebab3',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'mcp_hub_server_status',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: mcp_hub_server_status',
 'updated': '2025-08-15',
 'version': 1}
```

# MCP Hub Server - Current Status and Usage

## Description
This rule documents the current operational status of the MCP Hub Server, including available tools, usage patterns, and troubleshooting information.

## 🎯 **Current Status**

### **✅ MCP Hub Server Operational**
- **Status**: Healthy and running
- **Meta-Tools**: 15 tools exposed to Cursor
- **Underlying Tools**: 63 tools across 8 servers
- **Registry**: Loaded with complete tool definitions
- **Path Resolution**: Fixed with absolute paths

### **📋 Available Meta-Tools (15 total)**

#### **Tool Discovery and Management**
1. **`list_tools(query: str = "", server: str = "")`** - List available tools with filtering
2. **`get_tool_details(tool_name: str)`** - Get detailed tool information and schema
3. **`search_tools(query: str)`** - Semantic search across tool descriptions
4. **`get_tool_categories()`** - Get available tool categories

#### **Tool Execution**
5. **`execute_tool(tool_name: str, params: dict)`** - Execute any tool by name
6. **`batch_execute_tools(tools: list)`** - Execute multiple tools in sequence
7. **`execute_analysis_tool(tool_name: str, params: dict)`** - Execute analysis tools
8. **`execute_system_tool(tool_name: str, params: dict)`** - Execute system tools
9. **`execute_langflow_tool(tool_name: str, params: dict)`** - Execute Langflow tools
10. **`execute_category_tools(category: str, tools: list)`** - Execute tools by category

#### **Hub Server Management**
11. **`get_status()`** - Get hub server health and status
12. **`reload_registry()`** - Reload tool registry from file

#### **Tool Management**
13. **`build_tool(tool_def: dict)`** - Build and add new tool to registry
14. **`update_tool(tool_name: str, updates: dict)`** - Update existing tool in registry
15. **`delete_tool(tool_name: str)`** - Delete tool from registry

## 🔧 **Usage Patterns**

### **Tool Discovery**
```python
# List all available underlying tools
mcp_mcp_hub_server_list_tools()

# Search for specific tools
mcp_mcp_hub_server_search_tools("analysis")

# Get tool details
mcp_mcp_hub_server_get_tool_details("query_langflow")

# Get tool categories
mcp_mcp_hub_server_get_tool_categories()
```

### **Tool Execution**
```python
# Execute any underlying tool
mcp_mcp_hub_server_execute_tool("query_langflow", {"query": "test query"})

# Execute category-specific tools
mcp_mcp_hub_server_execute_analysis_tool("analyze_transcript", {"transcript_name": "test"})
mcp_mcp_hub_server_execute_langflow_tool("query_langflow", {"query": "test"})
mcp_mcp_hub_server_execute_system_tool("get_status", {})

# Batch execution
mcp_mcp_hub_server_batch_execute_tools([
    {"tool": "get_status", "params": {}},
    {"tool": "list_sources", "params": {}}
])
```

### **Hub Server Management**
```python
# Check hub server status
mcp_mcp_hub_server_get_status()

# Reload tool registry
mcp_mcp_hub_server_reload_registry()

### **Tool Management**
```python
# Build new tool
mcp_mcp_hub_server_build_tool({
    "name": "new_tool",
    "description": "Test tool",
    "server": "living_truth_fastmcp_server",
    "module": "src.mcp_servers.living_truth_fastmcp_server",
    "function": "new_function",
    "params_schema": {"param1": {"type": "string"}}
})

# Update existing tool
mcp_mcp_hub_server_update_tool("existing_tool", {"description": "Updated description"})

# Delete tool
mcp_mcp_hub_server_delete_tool("old_tool")
```

## 📊 **Current Metrics**

### **Tool Availability**
- ✅ **Meta-tools**: 15 (under Cursor's 40-tool limit)
- ✅ **Underlying tools**: 63 accessible via meta-tools
- ✅ **Servers**: 8 underlying MCP servers
- ✅ **Registry**: Complete with all tool definitions

### **Performance**
- ✅ **Response time**: <1s for tool execution
- ✅ **Registry loading**: Successful with absolute paths
- ✅ **Module loading**: Dynamic loading working correctly
- ✅ **Error handling**: Proper error reporting and logging

### **Categories Available**
- **Analysis**: query_langflow, analyze_transcript, generate_viz, batch_analysis_operations
- **System**: get_status, list_sources, get_lm_studio_models, batch_system_operations
- **Langflow**: query_langflow, create_langflow, export_flow_to_file, load_flow_from_file, get_langflow_status
- **GitHub**: list_repositories, create_issue
- **Database**: test_connection, list_tables, execute_query
- **Models**: search_models, get_model_info, generate_lm_studio_text
- **Documentation**: crawl_docs, retrieve_docs
- **Workflow**: query_rulego_chain, list_rulego_chains
- **Solver**: solve_constraint, route_llm

## 🚨 **Recent Fixes**

### **Path Resolution Issue**
- **Problem**: Server couldn't find registry file due to relative paths
- **Solution**: Updated to use absolute paths based on `__file__` location
- **Result**: Registry loads correctly regardless of working directory

### **Recursion Error**
- **Problem**: `execute_tool` method calling itself recursively
- **Solution**: Renamed internal method to `_execute_tool_internal`
- **Result**: Tool execution works correctly

### **Tool Count Correction**
- **Previous**: Documented as 15 meta-tools
- **Current**: Actually 12 meta-tools (corrected in all documentation)
- **Result**: Accurate documentation matching actual implementation

## 🎯 **Benefits Achieved**

### **Cursor Compliance**
- **Before**: 63 tools causing limit warning
- **After**: 12 meta-tools, well under 40-tool limit
- **Result**: No more warnings, optimal performance

### **Full Functionality Preserved**
- **All 63 tools**: Still accessible via meta-tools
- **Dynamic execution**: Tools loaded on-demand
- **Category organization**: Tools grouped by function
- **Batch operations**: Multiple tools can be executed together

### **Future-Proof Architecture**
- **Unlimited development**: Can add unlimited tools behind the scenes
- **Controlled exposure**: Only essential meta-tools exposed to Cursor
- **Scalable**: Easy to add new tools and categories

## 📚 **Related Rules**
- **@mcp_server_integration.mdc** - Integration patterns and best practices
- **@project_overview.mdc** - Project architecture overview
```

---

### 21. MCP-First Development
**File:** `mcp_integration.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Mcp Integration rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '58b901c8ddc742bf7d730ac7ab316b11c9685a441014b687611fc4952be68c2a',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'mcp_integration',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: mcp_integration',
 'updated': '2025-08-15',
 'version': 1}
```

# MCP-First Development

## 🎯 **Core Principle**
Use MCP tools to:
- validate rules, archive old ones, create/update rule files,
- run smoke tests, and generate completion summaries.

## 📋 **Required MCP Operations in Every Phase**
1) `validate_cursor_rules`
2) `fix_cursor_rule_frontmatter`
3) `ruleset_archive_outdated`
4) `ruleset_apply_templates`
5) `run_smoke_and_tests`
6) `generate_phase_completion_summary`

# Cursor Hooks (Phase 9)

## 🔄 **Before Coding a Sub-phase**
- `mcp.project.rules.validate` - Validate cursor rules
- `mcp.lte.health.get_full` - Record health snapshot in PR
- `mcp.lte.models.registry_show` - Verify model configuration

## 🔧 **After Coding**
- Run sub-phase smoke via `mcp.lte.smoke.run_phase`
- `mcp.lte.ui.contracts.validate_envelopes` (if UI touched)
- `mcp.lte.pgvector.db_dim` + `mcp.lte.models.assert_embedding_dim` (if storage touched)

## ✅ **On Completion**
- `mcp.project.rules.fix_frontmatter` - Fix rule metadata
- `mcp.project.rules.archive_outdated` (if any superseded rules)
- `generate_phase_completion_summary()` → writes `PHASE_<subphase>_COMPLETION_SUMMARY.md`
- `python build_master_log.py append` - Update master log

## 🛠️ **MCP Tool Namespaces**

### **Project Management**
- `mcp.project.rules.*` - Rule validation and management
- `mcp.lte.smoke.*` - Smoke test execution

### **System Health**
- `mcp.lte.health.*` - Health monitoring and validation
- `mcp.lte.models.*` - Model registry management
- `mcp.lte.gpu.*` - GPU status and allocation

### **Infrastructure**
- `mcp.lte.pgvector.*` - Database dimension management
- `mcp.lte.proxy.*` - Reverse proxy validation
- `mcp.lte.adapters.*` - Adapter pipeline testing

### **UI & Contracts**
- `mcp.lte.ui.contracts.*` - UI contract validation
- `mcp.lte.timeline.*` - Timeline endpoint validation

## 📚 **References**
- @mcp_ops.mdc for detailed MCP operations
- @core_workflow.mdc for development protocol
- @api_contracts.mdc for contract validation
```

---

### 22. MCP-first Operations
**File:** `mcp_ops.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Mcp Ops rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'c3683ba0e704e404562a4bd43f1d13a0e95696ff88f7522459ca9f4546f53469',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'mcp_ops',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: mcp_ops',
 'updated': '2025-08-15',
 'version': 1}
```

# MCP-first Operations

## 🎯 **Required MCP Operations**

### **Pre-coding Operations**
- `validate_cursor_rules()` - Validate all cursor rules
- `mcp.lte.health.get_full()` - Get system health snapshot
- `mcp.lte.models.registry_show()` - Show model registry status

### **Post-coding Operations**
- `fix_cursor_rule_frontmatter()` - Fix rule metadata
- `ruleset_archive_outdated()` - Archive superseded rules
- `ruleset_apply_templates()` - Apply rule templates

### **Completion Operations**
- `generate_phase_completion_summary()` - Generate completion summary
- `mcp.lte.smoke.run_phase()` - Run phase-specific smoke tests
- `python build_master_log.py append` - Update master log

## 📋 **Phase Workflow Integration**

### **Before Each Sub-phase**
1. **Validate Environment**
   - `mcp.project.rules.validate` - Check cursor rules
   - `mcp.lte.health.get_full` - Record health snapshot
   - `mcp.lte.models.registry_show` - Verify model configuration

2. **Prepare Development**
   - `mcp.lte.pgvector.db_dim` - Check database dimensions
   - `mcp.lte.models.assert_embedding_dim` - Validate SSOT

### **During Development**
1. **Code Quality**
   - `mcp.project.rules.fix_frontmatter` - Maintain rule metadata
   - `mcp.lte.ui.contracts.validate_envelopes` - Validate API contracts

2. **Testing**
   - `mcp.lte.smoke.run_phase` - Execute smoke tests
   - `mcp.lte.adapters.test_sources` - Test adapter pipelines

### **After Completion**
1. **Documentation**
   - `generate_phase_completion_summary()` - Write completion summary
   - `mcp.project.rules.archive_outdated` - Clean up old rules

2. **Integration**
   - `mcp.lte.proxy.smoke` - Verify reverse proxy
   - `mcp.lte.gpu.status` - Check GPU allocation

## 🔧 **MCP Tool Categories**

### **Project Management**
- `mcp.project.rules.*` - Rule validation and management
- `mcp.lte.smoke.*` - Smoke test execution
- `generate_phase_completion_summary()` - Documentation generation

### **System Health**
- `mcp.lte.health.*` - Health monitoring and validation
- `mcp.lte.models.*` - Model registry management
- `mcp.lte.gpu.*` - GPU status and allocation

### **Infrastructure**
- `mcp.lte.pgvector.*` - Database dimension management
- `mcp.lte.proxy.*` - Reverse proxy validation
- `mcp.lte.adapters.*` - Adapter pipeline testing

### **UI & Contracts**
- `mcp.lte.ui.contracts.*` - UI contract validation
- `mcp.lte.timeline.*` - Timeline endpoint validation

## ✅ **Implementation Checklist**

- [ ] All required MCP operations implemented
- [ ] Pre-coding validation workflow established
- [ ] Post-coding quality checks automated
- [ ] Completion documentation automated
- [ ] Integration with phase workflow complete

## 🔧 **Examples**

### **Pre-coding Validation**
```python
# Validate cursor rules
result = mcp.project.rules.validate()
if not result["valid"]:
    raise Exception("Cursor rules validation failed")

# Get health snapshot
health = mcp.lte.health.get_full()
print(f"System health: {health['status']}")
```

### **Completion Workflow**
```python
# Generate completion summary
summary = generate_phase_completion_summary("9.4.2")
with open("PHASE_9_4_2_COMPLETION_SUMMARY.md", "w") as f:
    f.write(summary)

# Update master log
subprocess.run(["python", "build_master_log.py", "append"])
```

## 📚 **References**
- Phase 9.3 for MCP operations pattern
- @core_workflow.mdc for development protocol
- @api_contracts.mdc for contract validation
- @models_and_embeddings.mdc for SSOT validation
description:
globs:
alwaysApply: false
```

---

### 23. MCP Server Integration and Best Practices
**File:** `mcp_server_integration.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Mcp Server Integration rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '7d65cc37659469698ba25893d2fb08d7852850541793a71a4be72ca0efb13366',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'mcp_server_integration',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: mcp_server_integration',
 'updated': '2025-08-15',
 'version': 1}
```

# MCP Server Integration and Best Practices

## Description
This rule defines MCP (Model Context Protocol) server integration practices for the Living Truth Engine, ensuring proper tool usage and system integration.

## 🔧 **MCP Server Configuration**

### **MCP Hub Server Setup**
```json
// ✅ Good - Single MCP Hub Server configuration solving 63-tool limit issue
{
  "mcpServers": {
    "mcp_hub_server": {
      "command": "python3",
      "args": [
        "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/src/mcp_servers/mcp_hub_server.py"
      ],
      "env": {
        "LANGFLOW_API_ENDPOINT": "http://localhost:7860",
        "LANGFLOW_API_KEY": "${LANGFLOW_API_KEY}",
        "LANGFLOW_PROJECT_ID": "399a0977-d08a-4d61-ba52-fd9811676762",
        "LM_STUDIO_ENDPOINT": "http://localhost:1234",
        "PYTHONPATH": "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/src"
      },
      "description": "MCP Hub Server - Consolidated tool gateway providing access to all 63 tools via 15 meta-tools, avoiding Cursor's 40-tool limit"
    }
  }
}
```

### **MCP Hub Server Architecture**
- **✅ Single Gateway**: One MCP server exposing 15 meta-tools to Cursor
- **✅ Underlying Tools**: 63 tools across 8 servers accessible via hub routing
- **✅ Registry Management**: `config/tool_registry.json` with complete tool definitions
- **✅ Dynamic Loading**: Tools loaded on-demand using `importlib`
- **✅ Proxy Execution**: Hub routes calls to appropriate underlying servers
- **✅ Tool Categories**: Tools organized by function (analysis, system, langflow, etc.)

### **MCP Hub Server Tool Usage**
```python
# ✅ Good - Use MCP Hub Server meta-tools (15 total)
mcp_mcp_hub_server_list_tools()
mcp_mcp_hub_server_get_tool_details("query_langflow")
mcp_mcp_hub_server_execute_tool("query_langflow", {"query": "test"})
mcp_mcp_hub_server_search_tools("analysis")
mcp_mcp_hub_server_batch_execute_tools([{"tool": "get_status", "params": {}}])

# ✅ Good - Category-specific execution
mcp_mcp_hub_server_execute_analysis_tool("analyze_transcript", {"transcript_name": "test"})
mcp_mcp_hub_server_execute_langflow_tool("query_langflow", {"query": "test"})
mcp_mcp_hub_server_execute_system_tool("get_status", {})

# ❌ Bad - Direct tool calls (not available through hub)
mcp_living_truth_fastmcp_server_query_langflow()  # Use hub instead
mcp_langflow_mcp_server_query_langflow()         # Use hub instead
```

## 📋 **MCP Integration Checklist**

### **Before Using MCP Hub Server**
- [ ] **Verify MCP Hub Server is running** and accessible
- [ ] **Check tool availability** with `list_tools()` call
- [ ] **Validate input parameters** before calling tools
- [ ] **Handle errors gracefully** with proper fallbacks
- [ ] **Use appropriate meta-tool** for the task
- [ ] **Use batch operations** for efficiency when available
- [ ] **Use category-specific tools** for better organization
- [ ] **Check tool details** with `get_tool_details()` before execution

### **MCP Hub Server Operations**
- [ ] **Start MCP Hub Server** before development work (`python3 src/mcp_servers/mcp_hub_server.py`)
- [ ] **Monitor hub server health** during operations
- [ ] **Restart hub server** if tools become unresponsive
- [ ] **Update tool registry** when adding new tools (`config/tool_registry.json`)
- [ ] **Test meta-tool functionality** after changes
- [ ] **Reload registry** if needed (`reload_registry()`)

### **MCP Hub Server Best Practices**
- [ ] **Use MCP Hub Server meta-tools** for all operations
- [ ] **Use batch operations** for efficiency (e.g., `batch_execute_tools`)
- [ ] **Use category-specific tools** for better organization
- [ ] **Search tools first** with `search_tools()` to find appropriate tools
- [ ] **Get tool details** with `get_tool_details()` before execution
- [ ] **Document tool usage** in code and documentation
- [ ] **Handle tool errors** with appropriate messaging
- [ ] **Validate tool outputs** before using results
- [ ] **Use registry management** for tool discovery and organization

## 🔧 **MCP Hub Server Meta-Tools (15 total)**

### **Tool Discovery and Management**
```python
# ✅ Tool discovery and information
mcp_mcp_hub_server_list_tools()                    # List all available tools
mcp_mcp_hub_server_get_tool_details("tool_name")   # Get tool details and schema
mcp_mcp_hub_server_search_tools("query")           # Search tools by description
mcp_mcp_hub_server_get_tool_categories()           # Get tool categories
```

### **Tool Execution**
```python
# ✅ General tool execution
mcp_mcp_hub_server_execute_tool("tool_name", params)  # Execute any tool by name
mcp_mcp_hub_server_batch_execute_tools(tools_list)    # Execute multiple tools

# ✅ Category-specific execution
mcp_mcp_hub_server_execute_analysis_tool("analyze_transcript", {"transcript_name": "test"})
mcp_mcp_hub_server_execute_system_tool("get_status", {})
mcp_mcp_hub_server_execute_langflow_tool("query_langflow", {"query": "test"})
mcp_mcp_hub_server_execute_category_tools("analysis", tools_list)

# ✅ Proxy execution examples
result = mcp_mcp_hub_server_execute_tool(tool_name="query_langflow", params={"query": "Analyze patterns"})
result = mcp_mcp_hub_server_execute_tool(tool_name="analyze_transcript", params={"transcript_name": "test", "anonymize": True})

#### **Performance Monitoring**
```python
import time
start = time.time()
result = mcp_mcp_hub_server_execute_tool("query_langflow", {"query": "test"})
duration = time.time() - start
if duration > 1:
    print("Warning: Slow tool execution")
```

### **Tool Management**
```python
# ✅ Build new tool
mcp_mcp_hub_server_build_tool({
    "name": "new_tool",
    "description": "Test tool",
    "server": "living_truth_fastmcp_server",
    "module": "src.mcp_servers.living_truth_fastmcp_server",
    "function": "new_function",
    "params_schema": {"param1": {"type": "string"}}
})

# ✅ Update existing tool
mcp_mcp_hub_server_update_tool("existing_tool", {"description": "Updated description"})

# ✅ Delete tool
mcp_mcp_hub_server_delete_tool("old_tool")
```

### **Hub Server Management**
```python
# ✅ Hub server operations
mcp_mcp_hub_server_get_status()                    # Get hub server health
mcp_mcp_hub_server_reload_registry()               # Reload tool registry
```

## 🎯 **MCP Hub Server Standards**

### **Required Patterns**
- **Use MCP Hub Server** as the single gateway for all tool access
- **Update tool registry** - add new tools to `config/tool_registry.json`
- **Follow FastMCP patterns** - for underlying server implementations
- **Use proper naming conventions** - snake_case for methods, descriptive names
- **Organize by categories** - group tools by function (analysis, system, langflow, etc.)

### **Tool Registry Schema**
```json
{
  "name": "tool_name",
  "description": "Tool description",
  "server": "server_name",
  "module": "module.path",
  "function": "function_name",
  "params_schema": {
    "param_name": {"type": "string", "required": true},
    "optional_param": {"type": "integer", "default": 1000}
  }
}
```

**Registry Validation Example**:
```python
def validate_registry(registry: Dict) -> bool:
    """Validate tool registry structure and content."""
    required_keys = ['name', 'description', 'server']
    for tool in registry.get('tools', []):
        if not all(key in tool for key in required_keys):
            raise ValueError(f"Missing required keys in tool entry: {tool.get('name', 'unknown')}")
        
        # Validate params_schema if present
        if 'params_schema' in tool:
            for param_name, param_def in tool['params_schema'].items():
                if 'type' not in param_def:
                    raise ValueError(f"Parameter {param_name} missing type definition")
    
    return True

# Usage
try:
    with open('config/tool_registry.json', 'r') as f:
        registry = json.load(f)
    validate_registry(registry)
    print("✅ Registry validation passed")
except Exception as e:
    print(f"❌ Registry validation failed: {e}")

**Registry Backup**: Copy to `.bak` on load for corruption recovery.

### **Tool Management**
```python
# Build new tool
mcp_mcp_hub_server_build_tool({
    "name": "new_tool", 
    "description": "Test tool", 
    "server": "living_truth_fastmcp_server", 
    "module": "src.mcp_servers.living_truth_fastmcp_server", 
    "function": "new_function",
    "params_schema": {"param1": {"type": "string", "required": True}}
})

# Update existing tool
mcp_mcp_hub_server_update_tool("existing_tool", {"description": "Updated description"})

# Delete tool
mcp_mcp_hub_server_delete_tool("old_tool")
```

### **Performance Monitoring**
```python
import time

def measure_tool_performance(tool_name: str, params: Dict) -> Tuple[Any, float]:
    start = time.time()
    result = mcp_mcp_hub_server_execute_tool(tool_name, params)
    duration = time.time() - start
    if duration > 1:
        logger.warning(f"Slow execution: {duration}s for {tool_name}")
    if duration > 2:
        logger.error(f"Alert: Execution exceeded 2s for {tool_name}")
        # Optional: send_alert("slow_execution", tool_name, duration)
    return result, duration
```

### **Tool Registry Schema**
- **Valid Types**: 'string', 'int', 'float', 'bool', 'list', 'dict', 'any'—enforced in validation
- **Registry Size**: Maximum 200 tools with automatic warnings
- **Recovery Testing**: Test backup and recovery functionality

### **Integration Patterns**

#### **Adding New Tools to Hub Server**
```python
# ✅ Good - Add tool to underlying server
class LivingTruthEngine:
    def new_functionality(self, param: str) -> str:
        """Add new functionality to existing class."""
        # Implementation
        return result

# ✅ Good - Add tool to registry (config/tool_registry.json)
{
  "name": "new_functionality",
  "description": "New functionality for analysis",
  "server": "living_truth_fastmcp_server",
  "module": "src.mcp_servers.living_truth_fastmcp_server",
  "function": "new_functionality",
  "params_schema": {
    "param": {"type": "string", "required": true}
  }
}

# ✅ Good - Access via hub server
mcp_mcp_hub_server_execute_tool("new_functionality", {"param": "value"})
```

#### **LM Studio Integration Pattern**
```python
# ✅ Good - LM Studio method in LivingTruthEngine class
def get_lm_studio_models(self) -> str:
    """Get list of available models in LM Studio."""
    try:
        response = requests.get(f"{self.lm_studio_endpoint}/v1/models")
        if response.status_code == 200:
            models = response.json()
            return f"✅ Available models in LM Studio:\n{json.dumps(models, indent=2)}"
        else:
            return f"❌ Failed to get models: {response.status_code}"
    except Exception as e:
        return f"❌ Error accessing LM Studio: {e}"

# ✅ Good - Corresponding MCP tool
@mcp.tool()
def get_lm_studio_models() -> str:
    """Get list of available models in LM Studio."""
    return engine.get_lm_studio_models()
```

## 🚨 **Common MCP Issues**

### **JSON Syntax Errors**
- ❌ **Trailing commas** - Causes all MCP servers to disappear
- ❌ **Missing quotes** - Invalid JSON syntax
- ❌ **Wrong brackets** - Malformed JSON structure

### **Pattern Violations**
- ❌ **Using standard MCP** instead of FastMCP
- ❌ **Creating separate servers** when integration is possible
- ❌ **Not following existing structure** - inconsistent patterns

### **Configuration Issues**
- ❌ **Wrong file paths** - MCP servers can't find files
- ❌ **Missing environment variables** - Servers can't connect
- ❌ **Incorrect endpoints** - Wrong service ports

## 🔧 **MCP Troubleshooting**

### **Diagnosing MCP Hub Server Issues**
```bash
# Validate JSON syntax
python3 -m json.tool .cursor/mcp.json
python3 -m json.tool config/tool_registry.json

# Check MCP Hub Server status in Cursor
# Look for green dots (working) vs red dots (errors)

# Test MCP Hub Server manually
python3 src/mcp_servers/mcp_hub_server.py

# Check tool registry
python3 -c "import json; data=json.load(open('config/tool_registry.json')); print(f'Total tools: {data[\"total_tools\"]}')"
```

### **Hub-Specific Issues**
- **Hub Registry Load Failure**: Check config/tool_registry.json permissions; run `reload_registry()`
- **Proxy Errors**: Ensure underlying servers running; test with `get_status()`
- **Tool Not Found**: Verify tool exists in registry; check `list_tools()` output
- **Import Errors**: Verify module path in registry; check PYTHONPATH

### **Common Fixes**

#### **JSON Syntax Fix**
```json
# ❌ Bad - Trailing comma
{
  "mcpServers": {
    "server1": { ... },
    "server2": { ... },  // <- This comma causes issues
  }
}

# ✅ Good - No trailing comma
{
  "mcpServers": {
    "server1": { ... },
    "server2": { ... }   // <- No trailing comma
  }
}
```

#### **Integration Fix**
```python
# ❌ Bad - Separate MCP server
class NewMCPServer:
    def __init__(self):
        self.server = Server("new_server")

# ✅ Good - Integrate into existing
class LivingTruthEngine:
    def new_functionality(self) -> str:
        # Add to existing class
        pass

@mcp.tool()
def new_functionality() -> str:
    return engine.new_functionality()
```

## 📋 **MCP Development Checklist**

### **Before Adding New Tools**
- [ ] **Check existing tools** in registry for similar functionality
- [ ] **Add to underlying server** using FastMCP pattern
- [ ] **Update tool registry** in `config/tool_registry.json`
- [ ] **Follow naming conventions** consistently
- [ ] **Organize by category** (analysis, system, langflow, etc.)
- [ ] **Test via hub server** using `execute_tool()` or category-specific methods

### **When Adding New Tools**
- [ ] **Add method to underlying server** first
- [ ] **Add tool to registry** in `config/tool_registry.json`
- [ ] **Update total_tools count** in registry
- [ ] **Test tool via hub server** using `execute_tool()`
- [ ] **Verify tool appears** in `list_tools()` output

### **Before Updating Configuration**
- [ ] **Validate JSON syntax** with python3 -m json.tool
- [ ] **Check file paths** are correct
- [ ] **Verify environment variables** are set
- [ ] **Test hub server startup** manually
- [ ] **Validate tool registry** structure and completeness

## 🎯 **Current MCP Hub Server Architecture**

### **MCP Hub Server** (15 meta-tools)
- **File**: `src/mcp_servers/mcp_hub_server.py`
- **Pattern**: FastMCP with proxy/gateway architecture
- **Registry**: `config/tool_registry.json` with 63 tools across 8 servers
- **Meta-Tools**: list_tools, get_tool_details, execute_tool, search_tools, batch_execute_tools
- **Category Tools**: execute_analysis_tool, execute_system_tool, execute_langflow_tool
- **Management Tools**: get_status, reload_registry, get_tool_categories, execute_category_tools

### **Underlying Servers** (63 tools total)
1. **Living Truth FastMCP Server** (22 tools): LM Studio, Core, Batch, Utility, Automation
2. **Langflow MCP Server** (12 tools): JSON import/export, workflow management
3. **GitHub MCP Server** (4 tools): Repository management
4. **PostgreSQL MCP Server** (6 tools): Database operations
5. **Hugging Face MCP Server** (5 tools): Model access
6. **DevDocs MCP Server** (4 tools): Document retrieval
7. **Rulego MCP Server** (5 tools): Workflow orchestration
8. **MCP Solver Server** (5 tools): Constraint solving

### **Benefits**
- **Cursor Compliance**: Only 15 tools exposed, well under 40-tool limit
- **Full Access**: All 63 tools accessible via hub routing
- **Scalability**: Unlimited tool development behind scenes
- **Organization**: Tools categorized by function
- **Performance**: Optimal Cursor performance with reduced tool exposure

## 📊 **MCP Hub Server Metrics**
- ✅ **100% Cursor compliance** - Only 15 meta-tools exposed (under 40-tool limit)
- ✅ **100% tool access** - All 63 underlying tools accessible via hub
- ✅ **100% registry management** - Complete tool registry with definitions
- ✅ **100% category organization** - Tools organized by function
- ✅ **100% dynamic loading** - Tools loaded on-demand for efficiency
- ✅ **100% error handling** - All tools include proper error handling

## 🚀 **Best Practices Summary**

### **1. Always Check Existing**
- Look for existing MCP servers first
- Integrate into existing structure when possible
- Follow established patterns and naming

### **2. Use FastMCP Library**
- All MCP servers must use FastMCP
- Add methods to existing classes
- Create corresponding @mcp.tool() decorators

### **3. Validate Configuration**
- Always validate JSON syntax
- Check file paths and environment variables
- Test server startup manually

### **4. Follow Integration Patterns**
- Add functionality to existing classes
- Create corresponding MCP tools
- Update tool lists and documentation
mcp_living_truth_fastmcp_server_test_tool("message")
mcp_langflow_mcp_server_test_tool("message")
```

### **Langflow Integration Tools**
```python
# ✅ Query Langflow workflow
mcp_living_truth_fastmcp_server_query_langflow(
    query="Analyze this transcript for corroborating evidence",
    output_type="summary",
    anonymize=False
)
```

### **Langflow Integration Tools**
```python
# ✅ Query Langflow workflow
mcp_langflow_mcp_server_query_langflow(
    query="Analyze this transcript for Biblical patterns",
    output_type="summary",
    anonymize=False
)

# ✅ Create or update Langflow workflows
mcp_langflow_mcp_server_create_langflow(
    flow_config={
        "name": "Test Workflow",
        "data": {"nodes": [], "edges": []}
    }
)

# ✅ Living Truth Engine Flow
# Access: http://localhost:7860/flows/90d0cc9d-d590-4734-813e-5664c95f907a
# Test: "Investigate Entity A connections, output as network"
# Schema-based generation: Uses `config/langflow_schemas.json` from local Langflow code
# Direct MCP: Use `mcp_lf-cursor_*` tools for direct Langflow operations

# ✅ Langflow operations
mcp_langflow_mcp_server_list_langflow_tools()
```

### **Data Analysis Tools**
```python
# ✅ Transcript analysis
mcp_living_truth_fastmcp_server_analyze_transcript("transcript_name")

# ✅ Source management
mcp_living_truth_fastmcp_server_list_sources()

# ✅ Batch operations for efficiency
mcp_living_truth_fastmcp_server_batch_system_operations()
mcp_living_truth_fastmcp_server_batch_analysis_operations("query", "transcript_name")
```
mcp_living_truth_fastmcp_server_list_sources()

# ✅ Visualization generation
mcp_living_truth_fastmcp_server_generate_viz(viz_type="network")
```

## 🚨 **Common MCP Issues to Avoid**

### **Configuration Issues**
- ❌ **Using dashes in tool names** (use underscores)
- ❌ **Tool names over 60 characters** (causes filtering)
- ❌ **Incorrect server paths** or environment variables
- ❌ **Missing PYTHONPATH** configuration
- ❌ **Conflicting MCP configurations** across projects

### **Usage Issues**
- ❌ **Not checking server status** before using tools
- ❌ **Ignoring tool errors** without fallback
- ❌ **Using wrong tool** for the task
- ❌ **Not validating tool outputs**
- ❌ **Hardcoding tool calls** without error handling

### **Integration Issues**
- ❌ **Not using MCP tools** when available
- ❌ **Bypassing MCP** for operations it can handle
- ❌ **Inconsistent tool usage** patterns
- ❌ **Not documenting tool dependencies**
- ❌ **Ignoring MCP server health**

## 📊 **MCP Integration Metrics**

- ✅ **Tool Exposure**: 100% compliance with 15 meta-tools (under 40-tool limit)
- ✅ **Proxy Response Time**: <1s for execution (monitor with `measure_tool_performance`)
- ✅ **Registry Size**: Unlimited, tested up to 100 tools
- ✅ **Error Rate**: <5% in proxy calls (log via logger.error)
- ✅ **Server Uptime**: 99%+ MCP Hub Server availability
- ✅ **Tool Usage**: 90%+ operations use MCP when available
- ✅ **Documentation**: 100% of tools documented
- ✅ **Tool Count**: 63 tools correctly loaded and validated
- ✅ **Performance Monitoring**: Active with timing and warnings
- ✅ **Backup System**: Automatic registry backup and recovery

## 🎯 **MCP Development Workflow**

### **1. Development Setup**
```python
# ✅ Start MCP server
# Ensure living_truth_fastmcp_server.py is running

# ✅ Check server status
mcp_living_truth_fastmcp_server_get_status()

# ✅ Validate tool availability
mcp_living_truth_fastmcp_server_test_tool("MCP server ready")
```

### **2. Tool Usage Pattern**
```python
# ✅ Always check status first
try:
    status = mcp_living_truth_fastmcp_server_get_status()
    if status.get("status") == "healthy":
        # Use MCP tools
        result = mcp_living_truth_fastmcp_server_query_langflow("query")
    else:
        # Fall back to direct operations
        result = perform_direct_operation("query")
except Exception as e:
    # Handle MCP errors gracefully
    logger.error(f"MCP tool error: {e}")
    result = perform_fallback_operation("query")
```

### **3. Error Handling**
```python
# ✅ Comprehensive error handling
def safe_mcp_operation(operation_func, *args, **kwargs):
    """Safely execute MCP operation with fallback."""
    try:
        return operation_func(*args, **kwargs)
    except ConnectionError:
        logger.warning("MCP server unavailable, using fallback")
        return fallback_operation(*args, **kwargs)
    except ValueError as e:
        logger.error(f"Invalid MCP operation parameters: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected MCP error: {e}")
        return fallback_operation(*args, **kwargs)
```

## 🔍 **MCP Server Monitoring**

### **Health Checks**
```python
# ✅ Regular status checks
def check_mcp_health():
    try:
        status = mcp_living_truth_fastmcp_server_get_status()
        return status.get("status") == "healthy"
    except Exception:
        return False

# ✅ Tool availability validation
def validate_tools():
    tools = [
        "get_status",
        "query_langflow", 
        "analyze_transcript",
        "list_sources"
    ]
    available_tools = []
    for tool in tools:
        try:
            # Test tool availability
            pass
        except Exception:
            logger.warning(f"Tool {tool} not available")
    return available_tools
```

### **Performance Monitoring**
```python
# ✅ Tool response times
import time

def measure_tool_performance(tool_func, *args, **kwargs):
    start_time = time.time()
    try:
        result = tool_func(*args, **kwargs)
        response_time = time.time() - start_time
        logger.info(f"Tool {tool_func.__name__} completed in {response_time:.2f}s")
        return result
    except Exception as e:
        logger.error(f"Tool {tool_func.__name__} failed after {time.time() - start_time:.2f}s: {e}")
        raise
```

## 🛠️ **MCP Troubleshooting**

### **Common Problems**
1. **Server not running**: Start `living_truth_fastmcp_server.py`
2. **Tool not found**: Check tool name spelling and availability
3. **Connection errors**: Verify server configuration and network
4. **Permission issues**: Check file permissions and user access
5. **Environment issues**: Verify PYTHONPATH and dependencies

### **Hub-Specific Issues**
- **Hub Registry Load Failure**: Check permissions (`ls -la config/tool_registry.json`); if invalid, validate with `validate_registry()`; reload with `reload_registry()`
- **Proxy Errors**: Ensure underlying server running (`mcp_hub_server_get_status()`); test import: `importlib.import_module(tool['module'])`
- **Tool Not Found**: Search registry first (`search_tools(tool_name)`); if missing, build with `build_tool()`
- **Performance Issues**: If >1s, check logs (`tail -f data/logs/hub.log`); optimize with batch tools
- **Registry Overflow**: If >100 tools, paginate `list_tools(page: int = 1, size: int = 20)`
- **Dynamic Build Failure**: If `build_tool()` fails (invalid code), log and return error details

### **Recovery Procedures**
```python
# ✅ Server restart procedure
def restart_mcp_server():
    try:
        # Stop current server
        stop_mcp_server()
        # Start new server
        start_mcp_server()
        # Validate restart
        status = mcp_living_truth_fastmcp_server_get_status()
        return status.get("status") == "healthy"
    except Exception as e:
        logger.error(f"Failed to restart MCP server: {e}")
        return False

# ✅ Tool recovery
def recover_tool_usage():
    if not check_mcp_health():
        restart_mcp_server()
    return check_mcp_health()
```
```

---

### 24. Models & Embeddings (SSOT)
**File:** `models_and_embeddings.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Models And Embeddings rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'ca070e1efab5b010c2679e3bb6fd20f52b150567639e2e3bde04eee6c608fcb9',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'models_and_embeddings',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: models_and_embeddings',
 'updated': '2025-08-15',
 'version': 1}
```

# Models & Embeddings (SSOT)

## 🎯 **Single Source of Truth (SSOT)**

### **Embedding dimension is SSOT-driven via ModelRegistry**
- No magic numbers in code (replacing hard-coded 768)
- All embedding dimensions sourced from `ModelRegistry`
- Database schema must match registry configuration

### **Health Endpoint Requirements**
- `/api/health/full` must surface `embedding_model` and `embedding_dim`
- Provide `dim_mismatch` boolean when registry vs DB differ
- Enable monitoring of configuration consistency

## 🔧 **Implementation Requirements**

### **ModelRegistry Integration**
```python
# ✅ Good - SSOT-driven
dim = ModelRegistry.embedding().extra["dim"]

# ❌ Bad - Magic number
dim = 768
```

### **Database Migrations**
- Migrations must re-create vector columns using configured **dim**
- Validate schema matches registry on startup
- Fail fast with remediation instructions on mismatch

### **Configuration Validation**
- Start-time check in `pgvector_store.py`
- Query DB vector column length and compare with registry
- Provide clear error messages with migration instructions

## 📋 **Health Contract**

### **Required Health Fields**
```json
{
  "embedding_model": "string",
  "embedding_dim": 1536,
  "dim_mismatch": false,
  "fallback_events": [...]
}
```

### **Validation Logic**
- Compare `ModelRegistry.embedding().extra["dim"]` with DB schema
- Report `dim_mismatch: true` when values differ
- Include remediation instructions in health response

## 🚨 **Error Handling**

### **Dimension Mismatch**
- Fail fast with clear error message
- Include migration script name in error
- Provide step-by-step remediation instructions

### **Registry Validation**
- Validate registry configuration on startup
- Check all required fields are present
- Log configuration details for debugging

## ✅ **Implementation Checklist**

- [ ] ModelRegistry configured with SSOT embedding dimensions
- [ ] Health endpoint includes embedding_model and embedding_dim
- [ ] Database migrations use registry dimensions
- [ ] Start-time validation implemented
- [ ] Error handling for dimension mismatches
- [ ] Documentation updated with SSOT approach

## 🔧 **Examples**

### **Health Endpoint Response**
```json
{
  "status": "ok",
  "data": {
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dim": 384,
    "dim_mismatch": false,
    "llm_model": "gpt-4",
    "reverse_proxy": true,
    "ui_origin": "http://localhost:3000"
  }
}
```

### **Migration Script**
```sql
-- docker/initdb/003b_graph_dim.sql
ALTER TABLE lte.doc_embeddings 
ALTER COLUMN embedding TYPE vector(384);
```

## 📚 **References**
- Phase 9.3.1 hotfix for embedding dimension issues
- Phase 9.5.1 for partitioned embeddings by model/dim
- @api_contracts.mdc for health endpoint format
- @core_workflow.mdc for development protocol
description:
globs:
alwaysApply: false
```

---

### 25. Project Overview
**File:** `project_overview.mdc`

**Content:**
```mdc
---
description: Project Overview rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '6f34d4464dea5cf836009411210171ee59b0f427c271631a06565b1f81370dae',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'project_overview',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: project_overview',
 'updated': '2025-08-15',
 'version': 1}
```

## 🎯 **Project Overview**

### **Living Truth Engine**
The Living Truth Engine is an AI-powered system for survivor testimony corroboration and evidence analysis. It combines multiple technologies to provide comprehensive analysis capabilities, using multiple sources (including but not limited to Biblical references) to find supporting evidence and make connections.

### **Core Components**
- **Langflow**: Primary AI workflow orchestration platform
- **PostgreSQL**: Primary database for data storage with langflow database
- **Neo4j**: Graph database for relationship analysis
- **Redis**: Caching and session management
- **Unified Dashboard**: Guided interface for all operations (Phase 8.1 complete)
- **MCP Hub Server**: Consolidated tool gateway providing access to all 63 tools via 15 meta-tools
- **Python Backend**: Core analysis and processing logic
- **Docker**: Containerized deployment and development

## 🏗️ **Architecture**

### **Service Architecture**
```
┌─────────────────┐
│ Cursor AI       │
└─────────────────┘
        │ (15 meta-tools)
        ▼
┌─────────────────┐
│ MCP Hub Server  │
│ (Registry: 63+  │
│  tools)         │
└─────────────────┘
        │ (Proxy calls)
        ▼
┌─────────────────┬─────────────────┬─────────────────┐
│ Living Truth   │ Langflow MCP    │ Other Servers   │
│ FastMCP Server │ Server          │ (GitHub, DB,    │
│ (22 tools)     │ (12 tools)      │ HF, DevDocs,    │
│                │                 │ Rulego, Solver) │
└─────────────────┴─────────────────┴─────────────────┘
        │                       │
        ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│ Unified Dashboard│    │   PostgreSQL    │
│   (Port 8050)   │    │   (Port 5432)   │
│                 │    │                 │
│ • Guided UI     │    │ • Data Storage  │
│ • Quick Start   │    │ • Langflow DB   │
│ • Analysis      │    │ • Analysis Data │
└─────────────────┘    └─────────────────┘
        │
        ▼
┌─────────────────┐
│   Langflow      │
│   (Port 7860)   │
│                 │
│ • Multi-Agent   │
│ • Python Native │
│ • Workflow UI   │
└─────────────────┘
```

### **Data Flow**
1. **Input**: Transcripts, videos, documents
2. **Processing**: AI analysis, pattern recognition
3. **Storage**: PostgreSQL database
4. **Output**: Analysis reports, visualizations, summaries

## 📁 **Project Structure**

### **Directory Organization**
```
LivingTruthEngine/
├── docker/                    # Docker configuration
│   ├── docker-compose.yml    # Service orchestration
│   └── .dockerignore         # Build exclusions
├── scripts/                   # Automation scripts
│   ├── setup/                # Setup and configuration
│   ├── testing/              # Test automation
│   └── deployment/           # Deployment scripts
├── src/                      # Source code
│   ├── mcp_servers/          # MCP server implementations
│   ├── analysis/             # Analysis modules
│   └── utils/                # Utility functions
├── data/                     # Data storage
│   ├── sources/              # Input data sources
│   ├── outputs/              # Analysis outputs
│   └── logs/                 # Application logs
├── config/                   # Configuration files
│   └── tool_registry.json   # MCP Hub Server tool registry
├── tests/                    # Test suite
├── docs/                     # Documentation
└── .cursor/                  # Cursor IDE configuration
    ├── rules/                # Development rules
    └── mcp.json             # MCP Hub Server configuration
```

## 🔧 **Technology Stack**

### **Core Technologies**
- **Python 3.13**: Primary programming language
- **PostgreSQL 17**: Database system with langflow database
- **Neo4j 5.15.0**: Graph database for relationship analysis
- **Redis 7.2**: Caching and session management
- **Docker**: Containerization platform
- **Docker Compose v2**: Service orchestration

### **AI and ML**
- **LangChain**: AI framework for LLM integration
- **Hugging Face**: Model hosting and inference
- **OpenAI**: Language model API
- **SpaCy**: Natural language processing

### **MCP Integration**
- **MCP Hub Server**: Consolidated tool gateway with 15 meta-tools
- **Tool Registry**: Central registry of 63 tools across 8 servers
- **FastMCP**: Framework for MCP server implementation
- **Dynamic Loading**: On-demand tool loading for efficiency
- **Piper TTS**: Text-to-speech synthesis
- **Dash/Plotly**: Interactive data visualizations

#### **MCP Hub Server Components Table**
| Component | Description | Location |
|-----------|-------------|----------|
| Tool Registry | JSON for all tools | config/tool_registry.json (.bak for backup) |
| Meta-Tools | 15 exposed functions | src/mcp_servers/mcp_hub_server.py |
| Proxy Logic | Dynamic execution | importlib in execute_tool() |
| Underlying Servers | 8 servers with 63 tools | src/mcp_servers/*.py |
| Performance Monitoring | Timing and warnings | Built into execute_tool() |
| Backup System | Automatic backup/recovery | Built into load_registry() |
| Registry Validation | Enhanced error reporting | Built into validate_registry() |
| Tool Management | CRUD operations | build_tool, update_tool, delete_tool |
| Performance Alerts | Warn on >2s executions | logger in execute_tool |
| Registry Recovery | Test backup and recovery | test_registry_recovery |

#### **Testing Integration**
- Run functional tests: `./scripts/testing/functional_tests.py` (aim for 100%; integrate timing checks in tests for <1s)
- Test MCP Hub Server: `python3 src/mcp_servers/mcp_hub_server.py`
- Validate registry: Use `validate_registry()` function from @mcp_server_integration.mdc
- Performance monitoring: Use `measure_tool_performance()` for response time tracking
- Registry recovery testing: Use `test_registry_recovery()` for backup validation
- Enhanced validation: Test with invalid parameter types to verify constraints

### **Development Tools**
- **Cursor IDE**: AI-assisted development environment
- **MCP**: Model Context Protocol for tool integration
- **FastAPI**: Web framework for APIs
- **Uvicorn**: ASGI server

## 📋 **Development Guidelines**

### **Code Standards**
- **Type Hints**: Required for all Python functions
- **Docstrings**: Comprehensive documentation
- **Naming**: Consistent snake_case for Python, camelCase for JavaScript
- **Error Handling**: Explicit error handling with logging
- **Testing**: 90%+ code coverage required

### **Docker Best Practices**
- **Docker Compose v2**: Modern syntax, no version field
- **Security**: Non-root users, read-only volumes
- **Performance**: BuildKit, slim base images, layer optimization
- **Health Checks**: Comprehensive monitoring
- **Networking**: Explicit network configuration

### **System Management**
- **Environment**: Virtual environment for all Python operations
- **Automation**: Scripts for common operations
- **Monitoring**: Health checks and logging
- **Updates**: Regular system component updates
- **Backup**: Data backup and recovery procedures

## 🚀 **Development Workflow**

### **Daily Development**
1. **Environment Setup**: Activate virtual environment
2. **Service Start**: Start Docker services
3. **Development**: Code with AI assistance
4. **Testing**: Run tests and validation
5. **Documentation**: Update docs as needed

### **Weekly Maintenance**
1. **System Updates**: Update components
2. **Resource Cleanup**: Remove unused Docker resources
3. **Configuration Validation**: Verify all configurations
4. **Performance Review**: Monitor system performance

### **Monthly Review**
1. **Security Updates**: Check for security patches
2. **Documentation Review**: Update project documentation
3. **Rule Updates**: Review and update cursor rules
4. **Architecture Review**: Assess system architecture

## 🎯 **Key Features**

### **Analysis Capabilities**
- **Transcript Analysis**: Pattern recognition in survivor testimony
- **Multi-Source Evidence Analysis**: Connecting survivor stories with supporting evidence from various sources
- **Biblical References**: One source among many for finding supporting evidence and connections
- **Entity Recognition**: Named entity extraction and linking
- **Relationship Mapping**: Network analysis of relationships and connections
- **Visualization**: Interactive 3D and 2D visualizations

### **Integration Features**
- **MCP Tools**: Comprehensive tool integration
- **API Endpoints**: RESTful API for external access
- **Web Interface**: Langflow-based workflow editor
- **Data Import**: Multiple input format support
- **Export Options**: Various output formats

## 📊 **Quality Metrics**

### **Code Quality**
- **Type Coverage**: 100% type hints
- **Documentation**: 100% docstring coverage
- **Test Coverage**: >90% code coverage
- **Linting**: Zero linting errors
- **Security**: No security vulnerabilities

### **System Performance**
- **Uptime**: 99%+ service availability
- **Response Time**: <2s for API calls
- **Resource Usage**: <80% CPU/memory utilization
- **Build Time**: <5 minutes for full build
- **Deployment**: <2 minutes for deployment

## 🔍 **Monitoring and Logging**

### **Health Monitoring**
- **Service Health**: Docker health checks
- **API Health**: Endpoint monitoring
- **Database Health**: Connection monitoring
- **Resource Monitoring**: CPU, memory, disk usage
- **Error Tracking**: Comprehensive error logging

### **Logging Strategy**
- **Application Logs**: Structured logging with levels
- **Access Logs**: API access and usage tracking
- **Error Logs**: Detailed error information
- **Performance Logs**: Response time and resource usage
- **Audit Logs**: Security and compliance tracking

## 🛠️ **Troubleshooting**

### **Common Issues**
1. **Service Startup**: Port conflicts, missing dependencies
2. **Database Issues**: Connection problems, data corruption
3. **MCP Server**: Configuration errors, tool availability
4. **Performance**: Resource constraints, slow queries
5. **Security**: Permission issues, authentication problems

### **Recovery Procedures**
- **Service Restart**: Automated restart procedures
- **Data Recovery**: Backup and restore procedures
- **Configuration Reset**: Reset to known good state
- **Environment Reset**: Complete environment rebuild
- **Emergency Procedures**: Critical issue response
```

---

### 26. Resilience Dashboard UI Development
**File:** `resilience_dashboard_ui.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Resilience Dashboard Ui rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '9b72370766c881c34924a892901171ba646c977a2f916e782988476e87303701',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'resilience_dashboard_ui',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: resilience_dashboard_ui',
 'updated': '2025-08-15',
 'version': 1}
```

# Resilience Dashboard UI Development

## 🎯 **Phase 9.5.7 Objective**
Build an interactive dashboard to visualize resilience metrics, chaos test results, and predictive monitoring alerts with real-time updates and CI validation hooks.

## 📋 **Core Requirements**

### **Dashboard Components**
- **Resilience Overview**: Real-time gauge with component breakdown
- **Chaos Test Results**: Filterable table with scenario/date filters
- **Predictive Monitoring**: Live anomaly feed with severity indicators
- **Historical Trends**: Time-series graphs with CI threshold overlays

### **Technical Stack**
- **Frontend**: React + Tailwind + shadcn/ui
- **Charts**: `react-gauge-chart` + `recharts`
- **Backend**: FastAPI resilience endpoints
- **Real-time**: WebSockets or long-polling (<2s latency)

## 🔧 **Development Standards**

### **API Endpoints**
```python
# Required endpoints in src/api/resilience.py
@router.get("/api/resilience/score")
async def get_resilience_score() -> dict:
    """Get current resilience score and historical breakdown."""
    return {"status": "ok", "data": {...}}

@router.get("/api/resilience/chaos")
async def get_chaos_tests(limit: int = 50) -> dict:
    """Get chaos test history with filtering."""
    return {"status": "ok", "data": {...}}

@router.get("/api/resilience/anomalies")
async def get_anomalies(severity: str = None) -> dict:
    """Get anomaly and prediction history."""
    return {"status": "ok", "data": {...}}
```

### **MCP Tools**
```python
# Required MCP tools in src/mcp_tools/resilience_dashboard_tools.py
@mcp.tool()
def get_resilience_dashboard_data(view: str, params: dict = None) -> dict:
    """Get structured data for dashboard panels."""
    pass

@mcp.tool()
def export_resilience_report(format: str, window_hours: int = 24) -> dict:
    """Export resilience report in specified format."""
    pass
```

### **Frontend Components**
```typescript
// Required components in ui/components/
interface ResilienceDashboardProps {
  refreshInterval?: number;
  showRealTime?: boolean;
}

interface ResilienceGaugeProps {
  score: number;
  threshold: number;
  components: Record<string, number>;
}
```

## ✅ **Acceptance Criteria**

### **Performance Requirements**
- [ ] Dashboard loads in <2.5s with all panels populated
- [ ] Real-time updates <2s after backend change
- [ ] API response time <500ms
- [ ] Memory usage <100MB

### **Functionality Requirements**
- [ ] CI gate: resilience score ≥80% for last 24h
- [ ] MCP tools return correct data for each view
- [ ] Historical trends match DB data
- [ ] Chaos table filters and sorts correctly

### **Quality Requirements**
- [ ] 100% test coverage for new code
- [ ] All accessibility standards met
- [ ] Mobile responsiveness verified
- [ ] 0 critical security vulnerabilities

## 🧪 **Testing Strategy**

### **Unit Tests**
- API endpoint validation
- MCP tool functionality
- Component rendering
- Data transformation logic

### **Integration Tests**
- Dashboard data flow
- Real-time update mechanism
- Database query performance
- WebSocket connectivity

### **UI Tests (Playwright)**
```typescript
test('resilience dashboard loads and displays data', async ({ page }) => {
  await page.goto('/dashboard/resilience');
  
  // Verify gauge renders
  await expect(page.locator('[data-testid="resilience-gauge"]')).toBeVisible();
  
  // Verify chaos table populates
  await expect(page.locator('[data-testid="chaos-table"]')).toHaveCount(1);
  
  // Verify trend graph shows history
  await expect(page.locator('[data-testid="trend-graph"]')).toBeVisible();
});
```

## 🔒 **Security & Validation**

### **Input Validation**
- Sanitize all dashboard parameters
- Validate time ranges and filters
- Rate limit API endpoints
- Authenticate dashboard access

### **Data Validation**
- Verify resilience score calculations
- Validate chaos test data integrity
- Check anomaly detection accuracy
- Ensure historical data consistency

## 🚨 **Error Handling**

### **Fail-Fast Pattern**
- No fallback mechanisms
- Explicit error handling
- Structured error responses
- Comprehensive logging

### **Graceful Degradation**
- Real-time updates fail → fallback to polling
- Large dataset performance → implement pagination
- WebSocket connectivity → graceful degradation
- Chart rendering issues → fallback to simple displays

## 📊 **Monitoring & Alerting**

### **Dashboard Health**
- Monitor dashboard load times
- Track real-time update latency
- Alert on failed data fetches
- Log user interactions

### **Resilience Metrics**
- Track resilience score trends
- Monitor chaos test success rates
- Alert on anomaly detection
- Validate predictive accuracy

## 🔄 **Development Workflow**

### **Before Coding**
1. Run `validate_cursor_rules()` to check current state
2. Read `PHASE_9_5_7_PLAN.md` for requirements
3. Check existing resilience infrastructure
4. Plan MCP tool integration

### **During Development**
1. Follow BUILD → VERIFY → ITERATE workflow
2. Implement API endpoints with proper envelope responses
3. Build UI components with TypeScript types
4. Add comprehensive error handling
5. Write tests for all new functionality

### **After Completion**
1. Run `enforce_mcp_compliance(phase)` to validate requirements
2. Update `MCP_REQUIREMENTS_REFERENCE.md` with new tools
3. Validate all MCP tools and rules
4. Update master log and completion summaries
5. Run full CI validation

## 📁 **File Structure**

### **Backend Files**
- `src/api/resilience.py` - New resilience API endpoints
- `src/mcp_tools/resilience_dashboard_tools.py` - MCP tool implementations
- `specs/resilience_dashboard_tools.json` - MCP tool specifications

### **Frontend Files**
- `ui/components/ResilienceDashboard.tsx` - Main dashboard component
- `ui/components/ResilienceGauge.tsx` - Gauge visualization
- `ui/components/ChaosTestTable.tsx` - Chaos test results table
- `ui/components/PredictiveAlerts.tsx` - Anomaly feed component
- `ui/components/HistoricalTrends.tsx` - Time-series graphs

### **CI/CD Files**
- `scripts/resilience_dashboard_test.sh` - Dashboard validation script
- `tests/ui/resilience_dashboard.spec.ts` - Playwright UI tests
- `.github/workflows/resilience-dashboard.yml` - CI workflow

## 📚 **References**
- @core_workflow.mdc - Development protocol
- @api_contracts.mdc - API envelope format
- @mcp_server_integration.mdc - MCP tool patterns
- @testing_standards.mdc - Testing requirements
```

---

### 27. Policy
**File:** `ssot_meta_index.mdc`

**Metadata:**
- phase: 9.5.7.4.12

**Content:**
```mdc
---
description: Ensure SSOT metadata index exists, validates, and stays fresh
alwaysApply: true
---

# Policy
- The file `reports/ssot_meta_index.json` must exist and parse as JSON.
- It must validate (schema + suggested types) and be **fresh** relative to rules/docs.
- `make reports` runs `meta-index` and `meta-validate`.

# How to comply
```bash
make meta-index
make meta-validate
```

### SSOT Meta

```yaml
owner: researcher-ssot
severity: high
tags: [ssot, metadata, validation]
phase: 9.5.7.4.12
dependsOn: [meta-index, meta-validate]
autofixAllowed: true
```

```

---

### 28. System Integration Status
**File:** `system_integration_status.mdc`

**Metadata:**

**Content:**
```mdc
---
description: System Integration Status rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'ca8a10be39fcde82bf88ecd1ccf6934904a6caa5c2c5e0510bc8682bf6cd36fd',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'system_integration_status',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: system_integration_status',
 'updated': '2025-08-15',
 'version': 1}
```

# System Integration Status

## Overview
The Living Truth Engine is **FULLY OPERATIONAL** with complete AI integration, advanced visualization, and comprehensive analysis pipeline.

## ✅ **System Status - VERIFIED**

### **Core Services**
- ✅ **Dashboard**: Single-file UI at `http://localhost:8050/static/ui_status_chat.html`
- ✅ **API Endpoints**: All endpoints responding with proper envelope format
- ✅ **MCP Server**: Living Truth FastMCP Server with 20+ tools
- ✅ **AI Integration**: Desktop LM Studio on port 1234 for real LLM generation
- ✅ **Visualization**: Advanced 3D network graphs with Plotly
- ✅ **Complete Pipeline**: Single-button orchestration of entire workflow

### **Docker Configuration**
- ✅ **Dashboard Container**: Running and serving UI
- ✅ **LM Studio**: Desktop version (port 1234) + Docker version (port 1235)
- ✅ **Network**: `host.docker.internal:1234` for container-to-desktop communication
- ✅ **Environment**: Proper endpoint configuration

### **API Verification**
```bash
# All endpoints verified working
✅ /api/health - {"status": "ok"}
✅ /api/health/full - Complete system status
✅ /api/tools - 9 categories of MCP tools
✅ /api/runs - Available analysis runs
✅ /api/execute - MCP tool execution
✅ /api/ai/chat - Direct AI chat
✅ /api/visualizations - Visualization serving
```

## 🎯 **Key Achievements**

### **Real AI Integration**
- **No Pattern Matching**: All analysis uses actual LLM generation
- **Desktop LM Studio**: Direct integration with port 1234
- **AI Tools**: `analyze_veritas_summary`, `analyze_veritas_claims`, `generate_lm_studio_text`
- **Structured Output**: JSON-formatted AI responses

### **Advanced Visualization**
- **3D Network Graphs**: Interactive Plotly visualizations
- **Entity Extraction**: JavaScript-based entity identification
- **Dynamic Generation**: Real-time graph creation from analysis data
- **HTML Rendering**: Proper visualization serving and embedding

### **Complete Analysis Pipeline**
- **Single Button**: "Start Complete Analysis" orchestrates entire workflow
- **Step-by-Step Progress**: Visual indicators for each stage
- **Comprehensive Results**: Summary, claims, and visualization in one view
- **Real-time Updates**: Live status and progress tracking

### **Modern UI**
- **Single File**: Complete UI in `ui_status_chat.html`
- **Dark Theme**: Modern design with grid background
- **Responsive**: Works on desktop and mobile
- **Status Stack**: Real-time system status indicators

## 🔧 **Technical Implementation**

### **Frontend Technologies**
- **Pure HTML/CSS/JavaScript**: No frameworks, single file
- **CSS Grid**: Responsive layout with status stack and output panels
- **Fetch API**: Modern async/await for API calls
- **Plotly.js**: Embedded for 3D network visualizations

### **Backend Integration**
- **FastAPI**: RESTful API with proper envelope format
- **MCP Protocol**: Tool execution via Model Context Protocol
- **Docker**: Containerized services with proper networking
- **Real AI**: Desktop LM Studio integration

### **Data Flow**
1. **Document Ingestion**: Veritas runs create `.veritasrun` bundles
2. **AI Analysis**: Real LLM generation via desktop LM Studio
3. **Entity Extraction**: JavaScript-based entity identification
4. **Visualization**: Dynamic graph generation from analysis results
5. **UI Display**: Interactive presentation of all results

## 🧪 **Verification Procedures**

### **Quick Health Check**
```bash
# Verify all endpoints
curl -s http://localhost:8050/api/health | jq .
curl -s http://localhost:8050/api/health/full | jq .
curl -s http://localhost:8050/api/tools | jq .
curl -s http://localhost:8050/api/runs | jq .

# Verify UI accessibility
curl -s http://localhost:8050/static/ui_status_chat.html | head -5
```

### **Complete Workflow Test**
1. **Open UI**: Navigate to `http://localhost:8050/static/ui_status_chat.html`
2. **Test System**: Click "Proof-of-Life" for complete verification
3. **Start Analysis**: Click "Start Complete Analysis" for full pipeline
4. **Verify Results**: Check for AI summary, claims, and visualization
5. **Test Chat**: Use AI chat interface for direct interaction

### **AI Integration Test**
```bash
# Test AI chat endpoint
curl -X POST http://localhost:8050/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?", "model": "qwen/qwen3-8b"}' | jq .

# Test MCP tool execution
curl -X POST http://localhost:8050/api/execute \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_lm_studio_status"}' | jq .
```

## 🚨 **Known Issues - RESOLVED**

### **Previously Fixed**
- ❌ **Missing `/api/health/full` endpoint**: ✅ **RESOLVED** - Implemented endpoint
- ❌ **Timeout issues**: ✅ **RESOLVED** - Increased timeouts
- ❌ **AI using pattern matching**: ✅ **RESOLVED** - Real LLM integration
- ❌ **Visualization showing blank grid**: ✅ **RESOLVED** - Schema normalization
- ❌ **HTML not rendering**: ✅ **RESOLVED** - HTMLResponse with proper media_type

### **Current Status**
- ✅ **All endpoints working**: Verified with smoke tests
- ✅ **AI integration complete**: Real LLM generation confirmed
- ✅ **Visualization system operational**: 3D graphs rendering correctly
- ✅ **Complete pipeline functional**: Single-button workflow working
- ✅ **UI fully accessible**: Single-file interface operational

## 📋 **Maintenance Procedures**

### **Regular Health Checks**
```bash
# Daily verification
bash scripts/smoke_envelope.sh

# Weekly comprehensive test
curl -s http://localhost:8050/static/ui_status_chat.html > /dev/null && echo "UI accessible" || echo "UI issue"
curl -s http://localhost:8050/api/health | jq -e '.status == "ok"' && echo "API healthy" || echo "API issue"
```

### **System Monitoring**
- **Dashboard Status**: Monitor container health
- **AI Service**: Verify LM Studio connectivity
- **API Endpoints**: Regular endpoint testing
- **UI Functionality**: Periodic workflow verification

### **Update Procedures**
1. **Code Changes**: Rebuild dashboard container
2. **Configuration**: Update environment variables
3. **Dependencies**: Update requirements.txt
4. **Verification**: Run smoke tests after changes

## 🎯 **Success Metrics**

### **All Requirements Met**
- ✅ **Single File UI**: Complete interface in one HTML file
- ✅ **Real AI**: Uses desktop LM Studio for actual LLM generation
- ✅ **Advanced Visualization**: Interactive 3D network graphs
- ✅ **Complete Pipeline**: Single-button orchestration
- ✅ **Systematic Testing**: Comprehensive verification procedures
- ✅ **No Fallbacks**: Clean error handling without silent failures

### **Quality Assurance**
- ✅ **Documentation**: Complete usage instructions and cursor rules
- ✅ **Testing**: Comprehensive verification scripts
- ✅ **Maintainability**: Clean, well-structured code
- ✅ **Integration**: Seamless system integration

## 🚀 **Next Steps**

The system is **production-ready** and provides a solid foundation for:

1. **Feature Expansion**: Easy to add new analysis tools
2. **UI Enhancements**: Simple to modify styling and layout
3. **Integration**: Ready for additional MCP tools
4. **Deployment**: Single file makes deployment straightforward
5. **Advanced Analytics**: Foundation for sophisticated analysis workflows

## 📝 **Conclusion**

The Living Truth Engine is **FULLY OPERATIONAL** with:
- ✅ Complete AI integration using real LLM generation
- ✅ Advanced 3D visualization system
- ✅ Comprehensive analysis pipeline
- ✅ Modern, responsive UI
- ✅ Systematic testing and verification
- ✅ Production-ready deployment

**The system is ready for immediate use and further development!** 🚀

**Last Verified**: $(date)
**Status**: ✅ **FULLY OPERATIONAL**
```

---

### 29. System Management and Automation
**File:** `system_management.mdc`

**Metadata:**

**Content:**
```mdc
---
description: System Management rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '5bbf48bedab3afdd66a9b7be4a479f46290f807b5d9e08966ac4329bc7d0b277',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'system_management',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: system_management',
 'updated': '2025-08-15',
 'version': 1}
```

# System Management and Automation

## Description
This rule defines system management practices for the Living Truth Engine, including environment setup, automation, and monitoring.

## 🖥️ **System Configuration Standards**

### **Environment Management**
```bash
# ✅ Good - Use virtual environment
source living_venv/bin/activate

# ✅ Good - Environment-driven configuration
export AGI_DASHBOARD_PORT=8050
export AGI_LOG_LEVEL=INFO
export AGI_ENVIRONMENT=development
```

### **Python Environment**
```bash
# ✅ Good - Canonical environment usage
# Always use living_venv for all operations
source living_venv/bin/activate

# ✅ Good - Environment validation
python -c "import sys; print('Environment:', sys.executable)"
```

### **System Updates**
```bash
# ✅ Good - Automated system updates
./scripts/setup/update_system.sh

# ✅ Good - Component-specific updates
# Docker: Latest Engine, Compose v2, BuildKit
# Node.js: Latest LTS version
# Python: Latest packages and dependencies
```

## 📋 **System Management Checklist**

### **Environment Setup**
- [ ] **Activate virtual environment** before any Python operations
- [ ] **Use environment variables** for configuration
- [ ] **Validate environment** before operations
- [ ] **Check dependencies** are installed
- [ ] **Verify MCP server** is running

### **System Maintenance**
- [ ] **Update system components** regularly
- [ ] **Clean up unused resources** (Docker, logs, cache)
- [ ] **Monitor system resources** (CPU, memory, disk)
- [ ] **Backup important data** regularly
- [ ] **Validate configurations** after updates

### **Development Workflow**
- [ ] **Check for existing files** before creating new ones
- [ ] **Use MCP server** for operations when possible
- [ ] **Follow cursor rules** for all operations
- [ ] **Update documentation** as you go
- [ ] **Run compliance checks** regularly

## 🔧 **Automation Scripts**

### **Service Management**
```bash
# ✅ Start all services (LivingTruthEngine group)
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine
docker compose -f docker/docker-compose.yml up -d

# ✅ Stop all services
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine
docker compose -f docker/docker-compose.yml down

# ✅ Validate Docker setup
./scripts/setup/validate_docker.sh

# ✅ Update system components
./scripts/setup/update_system.sh
```

### **Development Automation**
```bash
# ✅ Check system status
./scripts/setup/check_system.sh

# ✅ Run tests
./scripts/testing/run_tests.sh
./scripts/testing/trace_performance.sh
./scripts/testing/simple_performance_test.sh
./scripts/testing/functional_tests.py  # Comprehensive functional testing

# ✅ Deploy application
./scripts/deployment/deploy.sh
```

### **MCP Server Integration**
```bash
# ✅ Use MCP tools for operations
mcp_living_truth_fastmcp_server_get_status()
mcp_living_truth_fastmcp_server_query_langflow("query")
mcp_living_truth_fastmcp_server_analyze_transcript("transcript_name")
```

## 🚨 **Common System Issues to Avoid**

### **Environment Issues**
- ❌ **Not activating virtual environment** before Python operations
- ❌ **Using system Python** instead of project environment
- ❌ **Hardcoding configuration** instead of environment variables
- ❌ **Not validating environment** before operations
- ❌ **Mixing environments** across different projects

### **Automation Issues**
- ❌ **Manual operations** that could be automated
- ❌ **Not using MCP server** for available operations
- ❌ **Inconsistent script usage** across team
- ❌ **Not updating documentation** with changes
- ❌ **Skipping validation steps**

### **System Maintenance Issues**
- ❌ **Not updating components** regularly
- ❌ **Accumulating unused resources** (Docker images, logs)
- ❌ **Not monitoring system health**
- ❌ **No backup strategy** for important data
- ❌ **Ignoring security updates**

## 📊 **System Management Metrics**

- ✅ **Environment consistency**: 100% virtual environment usage
- ✅ **Automation coverage**: 90%+ operations automated
- ✅ **System updates**: Monthly component updates
- ✅ **Resource efficiency**: <10% unused resources
- ✅ **Documentation**: 100% operations documented

## 🎯 **System Management Workflow**

### **1. Daily Operations**
```bash
# Start development environment
source living_venv/bin/activate
./scripts/setup/start_services.sh

# Check system status
./scripts/setup/check_system.sh
```

### **2. Weekly Maintenance**
```bash
# Update system components
./scripts/setup/update_system.sh

# Clean up resources
docker system prune
docker image prune -f

# Validate configurations
./scripts/setup/validate_docker.sh
```

### **3. Monthly Review**
```bash
# Comprehensive system check
./scripts/setup/check_system.sh
./scripts/setup/validate_docker.sh

# Update documentation
# Review and update cursor rules
# Check for security updates
```

## 🔍 **Monitoring and Validation**

### **System Health Checks**
```bash
# ✅ Service status
docker compose -f docker/docker-compose.yml ps

# ✅ Environment validation
python -c "import sys; print('Python:', sys.version)"
node --version
docker --version

# ✅ MCP server status
mcp_living_truth_fastmcp_server_get_status()
```

### **Performance Monitoring**
```bash
# ✅ Resource usage
docker stats
df -h
free -h

# ✅ Service response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3000/
```

### **Log Analysis**
```bash
# ✅ Service logs
docker compose -f docker/docker-compose.yml logs -f

# ✅ Application logs
tail -f logs/application.log

# ✅ Error monitoring
grep -i error logs/*.log
```

## 🛠️ **Troubleshooting Guide**

### **Common Problems**
1. **Environment not activated**: `source living_venv/bin/activate`
2. **Port conflicts**: Stop conflicting services, check `netstat -tulpn`
3. **Docker issues**: Restart Docker daemon, validate compose file
4. **MCP server errors**: Check configuration, restart server
5. **Permission issues**: Check file permissions, use correct user

### **Recovery Procedures**
```bash
# ✅ Full system restart
./scripts/setup/stop_services.sh
./scripts/setup/start_services.sh

# ✅ Environment reset
deactivate
source living_venv/bin/activate

# ✅ Docker reset
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d
```
```

---

### 30. System Status (Updated: 2025-08-13 21:30:00)
**File:** `system_status.mdc`

**Metadata:**
- phase: 9.5.4 - Performance Gates

**Content:**
```mdc
---
description: System Status rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '12b79407f24396be479065db411d16eb2bce372c6a030fe4e01954c597522244',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'system_status',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: system_status',
 'updated': '2025-08-15',
 'version': 1}
```

# System Status (Updated: 2025-08-13 21:30:00)

✅ Dashboard: Healthy
✅ LM Studio: Healthy
✅ Langflow: Healthy
✅ Graph Build: Fixed (constraint violations resolved)

## Phase 9.5.3 - Timeline API + Graph Polish: ✅ COMPLETED
- **Timeline API**: 25ms response time (<1s requirement)
- **Graph UX**: Enhanced with filters, pinning, and selection
- **Graph Build**: Fixed constraint violations with UPSERT support
- **Performance**: All APIs meeting timing requirements

## Rule System Status
- **Core Workflow**: ✅ Operational
- **MCP Integration**: ✅ Operational  
- **Docker Management**: ✅ Operational
- **Testing Standards**: ✅ Operational
- **API Contracts**: ✅ Operational
- **Error Handling**: ✅ Enhanced with constraint violation handling

## Archived Rules
- build_verify_iterate.mdc
- workflow.mdc
- current_working_state.mdc
- cursor_rule_management.mdc
- mcp_hub_server.mdc
- mcp_red_dot.mdc
- phase_8_1_implementation.mdc
- migrated_functionality.mdc

## Next Phase: 9.5.4 - Performance Gates
- Performance harness with p95 latencies
- LCP budget enforcement
- Bundle size optimization
- CI gates for performance regressions

- mcp_hub_server.mdc
- mcp_red_dot.mdc
- phase_8_1_implementation.mdc
- migrated_functionality.mdc
```

---

### 31. Testing Standards
**File:** `testing_standards.mdc`

**Content:**
```mdc
---
description: Testing Standards rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '012795a0836aa6fe2103bca4b1493eafe7282a094a3f6859759777a996ba6f40',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'testing_standards',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: testing_standards',
 'updated': '2025-08-15',
 'version': 1}
```

- Smoke: `scripts/p9_1_smoke.sh`
- Envelope lint: assert `status` present; `error` on non-2xx paths.
- Health gates: LM Studio, Langflow, MCP Hub, Rulego, pgvector.
- No flaky tests; mark @skip only with issue link.
```

---

### 32. UI Policy
**File:** `ui_policy.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Ui Policy rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': '0eed8078c6874d187fdf7fd4a95f74ba50c630da7ad48fa9249a52aa0b0b8fce',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'ui_policy',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: ui_policy',
 'updated': '2025-08-15',
 'version': 1}
```

# UI Policy

## 🚨 **Legacy UI Protection**

### **Do NOT edit legacy Dash templates**
- Keep `/status` functional for now
- No modifications to `src/dashboard/templates/` unless explicitly planned
- Legacy UI serves as fallback during transition

## 🔄 **Reverse Proxy Requirements (Phase 9.4.0)**

### **Root `/` must serve the new UI shell**
- Phase 9.4.0 introduces reverse proxy configuration
- Root endpoint must return new UI shell, not legacy dashboard
- Maintain backward compatibility for existing API endpoints

### **API Integration**
- UI fetches go through `apiClient` with zod-validated envelopes
- All API calls must handle envelope format: `{status, data?, error?}`
- Implement proper error boundaries for failed requests

## 🛡️ **Error Handling Requirements**

### **Error Boundary Required (Phase 9.4.6)**
- Implement React error boundaries for all major components
- Graceful degradation for API failures
- User-friendly error messages with retry options

### **No "Dead Buttons"**
- All interactive elements must have proper loading states
- Disable buttons during async operations
- Provide visual feedback for user actions

## 📋 **Development Standards**

### **Component Architecture**
- Use functional components with hooks
- Implement proper TypeScript types
- Follow React best practices for state management

### **Testing Requirements**
- E2E tests for all major user flows
- Unit tests for complex components
- Accessibility testing for all interactive elements

## ✅ **Implementation Checklist**

- [ ] Legacy templates protected from modifications
- [ ] Reverse proxy configuration implemented
- [ ] API client with envelope validation
- [ ] Error boundaries implemented
- [ ] Loading states for all async operations
- [ ] E2E tests for critical user flows

## 🔧 **Examples**

### **API Client Usage**
```typescript
const { data, error, isLoading } = useQuery({
  queryKey: ['runs'],
  queryFn: () => apiClient.get('/api/runs'),
  select: (response) => response.data // envelope.data
});
```

### **Error Boundary Implementation**
```typescript
<ErrorBoundary fallback={<ErrorFallback />}>
  <ComponentWithAsyncOperations />
</ErrorBoundary>
```

## 📚 **References**
- Phase 9.4.0 for reverse proxy implementation
- Phase 9.4.6 for error boundary requirements
- @api_contracts.mdc for envelope format
- @core_workflow.mdc for development protocol
```

---

### 33. Veritas Generalist Ingestion Runner - Development Guidelines
**File:** `veritas_runs.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Veritas Runs rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'de92bcfcdecbba61db4ffd1266feb94e9714e185dba138c176e2fe255b84582c',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'veritas_runs',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: veritas_runs',
 'updated': '2025-08-15',
 'version': 1}
```

# Veritas Generalist Ingestion Runner - Development Guidelines

## Overview
Implements the Generalist Ingestion Runner and Job Runs UI. Enforce local-only by default.

## Core Principles

### Function Design
- **Prefer small, single-purpose functions with type hints**
- **Fail-fast pattern**: No fallback mechanisms, explicit error handling
- **Local-first**: No external network calls unless explicitly configured
- **Bundle-centric**: All operations produce verifiable .veritasrun bundles

### Network and External Services
- **No Hugging Face/network bursts unless HF_BURST=="on"**
- **OCR default off**: Only set OCR_REQUIRED="true" to allow downstream handling
- **Local processing**: Prefer local processing over external API calls
- **Rate limiting**: Implement appropriate rate limiting for any external calls

### Bundle Structure
- **Produce .veritasrun bundles under data/outputs/runs/<ts>_<slug>.veritasrun**
- **Each bundle must include**:
  - `manifest.json`: Run metadata, flags, document list
  - `corpus.jsonl`: Canonicalized documents in JSONL format
  - `proofs/*.sha256`: Individual SHA-256 proof files for each document
  - `merkle.json`: Merkle tree with root hash and leaf hashes
  - `metrics.json`: Run statistics (doc count, bytes, duration, errors)

### MCP Integration
- **Expose MCP tools**: start_veritas_run, get_veritas_run_status, list_veritas_runs, open_veritas_bundle
- **Tool registry**: Register all tools in config/tool_registry.json
- **Error handling**: Return structured error responses, not exceptions
- **Performance**: Target <1s response time for tool execution

## Implementation Guidelines

### VeritasRunner Class
```python
class VeritasRunner:
    """Coordinates a verifiable, local-first ingestion run and writes a .veritasrun bundle."""
    
    def start(self, topic: str, max_docs: int = 10, sources: Optional[List[str]] = None) -> VeritasRunStatus:
        """Start a new ingestion run and create bundle."""
        
    def get_status(self, run_id: str) -> VeritasRunStatus:
        """Get status of a specific run."""
        
    def list_runs(self, limit: int = 20) -> List[str]:
        """List available runs."""
        
    def open_bundle(self, run_id: str) -> Dict[str, Any]:
        """Open and parse a bundle."""
```

### Bundle Writing
```python
def write_bundle(run_dir: str, docs: List[Dict[str, Any]], flags: Dict[str, Any]) -> Dict[str, Any]:
    """Write a complete .veritasrun bundle with all required components."""
```

### Document Processing
```python
def to_canonical(raw: dict) -> dict:
    """Convert raw document to canonical format."""
    
def sha256_text(text: str) -> str:
    """Generate SHA-256 hash of text content."""
    
def build_merkle(leaves: List[str]) -> dict:
    """Build merkle tree from document hashes."""
```

## Testing Requirements

### Test Coverage
- **Add tests/test_phase7_veritas.py** to assert bundle layout and MCP listing
- **Bundle structure validation**: Verify all required files exist
- **MCP tool testing**: Test all four Veritas MCP tools
- **Flag validation**: Ensure flags match config/veritas_flags.toml
- **Performance testing**: Verify response times meet targets

### Test Structure
```python
def test_phase7_smoke_run():
    """Test basic Veritas run creation and bundle structure."""
    
def test_veritas_mcp_tools():
    """Test MCP tools for Veritas operations."""
    
def test_bundle_structure():
    """Test complete bundle structure and validation."""
```

## Dashboard Integration

### Job Runs Tab
- **Enumerate bundles**: List all .veritasrun bundles in data/outputs/runs/
- **Bundle viewer**: Display manifest, metrics, and merkle root
- **Health checks**: Verify dashboard health endpoint
- **Error handling**: Graceful handling of missing or corrupted bundles

## Configuration

### Flags File
- **config/veritas_flags.toml**: Central configuration for all flags
- **Default values**: Conservative defaults for local-only operation
- **Flag validation**: Validate flags on startup and during operations

## Error Handling

### Fail-Fast Pattern
- **No fallbacks**: Either work or throw explicit error
- **Structured errors**: Return error objects, not exceptions
- **Logging**: Comprehensive logging for debugging
- **Validation**: Validate inputs and outputs at each step

## Performance Targets

### Response Times
- **Bundle creation**: <2s for typical runs
- **MCP tool execution**: <1s response time
- **Dashboard loading**: <1s for Job Runs tab
- **Test execution**: <30s for complete test suite

## Security and Privacy

### Data Handling
- **PII scrubbing**: Standard PII scrubbing enabled by default
- **Local storage**: All data stored locally in bundles
- **No external transmission**: No data sent to external services unless configured
- **Access control**: Proper file permissions for bundle directories

## Maintenance

### Code Quality
- **Type hints**: Required for all functions
- **Docstrings**: Comprehensive documentation
- **Error handling**: Explicit error handling patterns
- **Testing**: 100% test coverage for new functionality

# Veritas Generalist Ingestion Runner - Development Guidelines

## Overview
Implements the Generalist Ingestion Runner and Job Runs UI. Enforce local-only by default.

## Core Principles

### Function Design
- **Prefer small, single-purpose functions with type hints**
- **Fail-fast pattern**: No fallback mechanisms, explicit error handling
- **Local-first**: No external network calls unless explicitly configured
- **Bundle-centric**: All operations produce verifiable .veritasrun bundles

### Network and External Services
- **No Hugging Face/network bursts unless HF_BURST=="on"**
- **OCR default off**: Only set OCR_REQUIRED="true" to allow downstream handling
- **Local processing**: Prefer local processing over external API calls
- **Rate limiting**: Implement appropriate rate limiting for any external calls

### Bundle Structure
- **Produce .veritasrun bundles under data/outputs/runs/<ts>_<slug>.veritasrun**
- **Each bundle must include**:
  - `manifest.json`: Run metadata, flags, document list
  - `corpus.jsonl`: Canonicalized documents in JSONL format
  - `proofs/*.sha256`: Individual SHA-256 proof files for each document
  - `merkle.json`: Merkle tree with root hash and leaf hashes
  - `metrics.json`: Run statistics (doc count, bytes, duration, errors)

### MCP Integration
- **Expose MCP tools**: start_veritas_run, get_veritas_run_status, list_veritas_runs, open_veritas_bundle
- **Tool registry**: Register all tools in config/tool_registry.json
- **Error handling**: Return structured error responses, not exceptions
- **Performance**: Target <1s response time for tool execution

## Implementation Guidelines

### VeritasRunner Class
```python
class VeritasRunner:
    """Coordinates a verifiable, local-first ingestion run and writes a .veritasrun bundle."""
    
    def start(self, topic: str, max_docs: int = 10, sources: Optional[List[str]] = None) -> VeritasRunStatus:
        """Start a new ingestion run and create bundle."""
        
    def get_status(self, run_id: str) -> VeritasRunStatus:
        """Get status of a specific run."""
        
    def list_runs(self, limit: int = 20) -> List[str]:
        """List available runs."""
        
    def open_bundle(self, run_id: str) -> Dict[str, Any]:
        """Open and parse a bundle."""
```

### Bundle Writing
```python
def write_bundle(run_dir: str, docs: List[Dict[str, Any]], flags: Dict[str, Any]) -> Dict[str, Any]:
    """Write a complete .veritasrun bundle with all required components."""
```

### Document Processing
```python
def to_canonical(raw: dict) -> dict:
    """Convert raw document to canonical format."""
    
def sha256_text(text: str) -> str:
    """Generate SHA-256 hash of text content."""
    
def build_merkle(leaves: List[str]) -> dict:
    """Build merkle tree from document hashes."""
```

## Testing Requirements

### Test Coverage
- **Add tests/test_phase7_veritas.py** to assert bundle layout and MCP listing
- **Bundle structure validation**: Verify all required files exist
- **MCP tool testing**: Test all four Veritas MCP tools
- **Flag validation**: Ensure flags match config/veritas_flags.toml
- **Performance testing**: Verify response times meet targets

### Test Structure
```python
def test_phase7_smoke_run():
    """Test basic Veritas run creation and bundle structure."""
    
def test_veritas_mcp_tools():
    """Test MCP tools for Veritas operations."""
    
def test_bundle_structure():
    """Test complete bundle structure and validation."""
```

## Dashboard Integration

### Job Runs Tab
- **Enumerate bundles**: List all .veritasrun bundles in data/outputs/runs/
- **Bundle viewer**: Display manifest, metrics, and merkle root
- **Health checks**: Verify dashboard health endpoint
- **Error handling**: Graceful handling of missing or corrupted bundles

## Configuration

### Flags File
- **config/veritas_flags.toml**: Central configuration for all flags
- **Default values**: Conservative defaults for local-only operation
- **Flag validation**: Validate flags on startup and during operations

## Error Handling

### Fail-Fast Pattern
- **No fallbacks**: Either work or throw explicit error
- **Structured errors**: Return error objects, not exceptions
- **Logging**: Comprehensive logging for debugging
- **Validation**: Validate inputs and outputs at each step

## Performance Targets

### Response Times
- **Bundle creation**: <2s for typical runs
- **MCP tool execution**: <1s response time
- **Dashboard loading**: <1s for Job Runs tab
- **Test execution**: <30s for complete test suite

## Security and Privacy

### Data Handling
- **PII scrubbing**: Standard PII scrubbing enabled by default
- **Local storage**: All data stored locally in bundles
- **No external transmission**: No data sent to external services unless configured
- **Access control**: Proper file permissions for bundle directories

## Maintenance

### Code Quality
- **Type hints**: Required for all functions
- **Docstrings**: Comprehensive documentation
- **Error handling**: Explicit error handling patterns
- **Testing**: 100% test coverage for new functionality
```

---

### 34. Visualization System Integration
**File:** `visualization_system.mdc`

**Metadata:**

**Content:**
```mdc
---
description: Visualization System rule for Living Truth Engine
---
### Meta (migrated from nonstandard frontmatter)

```yaml
{'applies': 'phase',
 'checksum': 'd8bc4397fdcef4e4481400fee9c31c2de9d69111e688156501066ddb0c1adf31',
 'enforcement': 'advisory',
 'links': [],
 'owner': 'researcher-ssot',
 'phase': '9.5.7.4.6',
 'rule_id': 'visualization_system',
 'scope': ['**/*'],
 'summary': 'Rule autogenerated/normalized by SSOT fixer; please refine summary.',
 'title': 'Cursor Rule: visualization_system',
 'updated': '2025-08-15',
 'version': 1}
```

# Visualization System Integration

## Overview
The Living Truth Engine includes a sophisticated visualization system for creating interactive 3D network graphs from analysis data.

## 🎯 **Key Components**

### **AdvancedVisualizer Class**
- **Location**: `src/visualization/advanced_viz.py`
- **Purpose**: Creates interactive 3D network graphs using Plotly
- **Features**: Entity extraction, dynamic graph generation, HTML export

### **MCP Integration**
- **Tool**: `create_3d_network_visualization`
- **Location**: `src/mcp_servers/living_truth_fastmcp_server.py`
- **Purpose**: Exposes visualization capabilities via MCP protocol

### **UI Integration**
- **Location**: `src/dashboard/static/ui_status_chat.html`
- **Purpose**: Embeds visualizations in the web interface
- **Features**: Dynamic graph generation, entity extraction, HTML rendering

## 🔧 **Data Schema**

### **Expected Graph Data Format**
```python
{
    "nodes": {
        "node_id": {
            "label": "Node Label",
            "type": "entity_type",
            "confidence": 0.8,
            "description": "Node description"
        }
    },
    "edges": [
        {
            "source": "node_id_1",
            "target": "node_id_2",
            "attributes": {
                "type": "relationship_type",
                "weight": 1.0
            }
        }
    ]
}
```

### **Schema Normalization**
The MCP tool automatically normalizes incoming data:
- **List nodes** → **Dict nodes** keyed by ID
- **Edge fields** → **source/target** format
- **Missing attributes** → **Default values**

## 🚀 **Usage Patterns**

### **Frontend Graph Generation**
```javascript
// Extract entities from document text
const entities = [];
const words = text.split(/\s+/);
for (let i = 0; i < words.length && entities.length < 10; i++) {
    const word = words[i];
    const cleanWord = word.replace(/[^\w]/g, '');
    
    if (cleanWord.length > 2 && 
        /^[A-Z]/.test(cleanWord) && 
        !stopWords.includes(cleanWord)) {
        entities.push(cleanWord);
    }
}

// Create graph data
const graphData = {
    nodes: documentNodes.concat(entityNodes),
    edges: entityEdges
};

// Generate visualization
const vizResult = await apiCall('/api/execute', 'POST', {
    tool_name: 'create_3d_network_visualization',
    params: { graph_data: graphData }
});
```

### **Backend Visualization Creation**
```python
def create_3d_network_visualization(self, graph_data: dict) -> str:
    """Create 3D network visualization using advanced visualizer."""
    try:
        if not self.visualizer:
            return "❌ Advanced visualizer not initialized"
        
        # Normalize incoming graph data
        normalized = self._normalize_graph_data(graph_data)
        
        # Create 3D network graph
        fig = self.visualizer.create_interactive_3d_network_graph(normalized)
        
        # Save visualization
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"3d_network_visualization_{timestamp}.html"
        output_path = self.visualizer.output_dir / output_file
        
        # Save the Plotly figure as HTML
        fig.write_html(str(output_path))
        
        return f"✅ 3D network visualization created successfully\nOutput file: {output_file}"
        
    except Exception as e:
        return f"❌ 3D network visualization error: {str(e)}"
```

## 📊 **Visualization Features**

### **3D Network Graphs**
- **Interactive**: Zoom, pan, rotate, hover
- **Color-coded**: Different colors for entity types
- **Size-scaled**: Node size based on importance/confidence
- **Edge visualization**: Relationship lines between entities

### **Entity Extraction**
- **JavaScript-based**: Client-side entity extraction
- **Capitalized words**: Identifies potential entities
- **Stop word filtering**: Removes common words
- **Configurable limits**: Maximum entities per document

### **HTML Rendering**
- **Direct HTML**: Served as raw HTML content
- **Embedded**: Displays within UI container
- **External link**: "Open in new window" option
- **Responsive**: Adapts to container size

## 🔗 **API Integration**

### **Visualization Endpoints**
- **`/api/visualizations`**: List available visualization files
- **`/api/visualizations/{filename}`**: Serve specific HTML file
- **`/api/execute`**: Create new visualizations via MCP tools

### **Response Format**
```python
# HTML Response (for visualization files)
from fastapi.responses import HTMLResponse
return HTMLResponse(content=html_content, media_type="text/html")

# JSON Response (for MCP tool results)
return f"✅ 3D network visualization created successfully\nOutput file: {filename}"
```

## 🧪 **Testing**

### **Visualization Testing**
- **File generation**: Verify HTML files are created
- **Content validation**: Check for Plotly JavaScript
- **Rendering test**: Confirm graphs display correctly
- **Schema validation**: Ensure data normalization works

### **Integration Testing**
- **MCP tool execution**: Test via `/api/execute`
- **UI embedding**: Verify visualization displays in UI
- **Error handling**: Test with invalid data
- **Performance**: Check generation time

## 🚨 **Common Issues**

### **Blank Grid Display**
- **Cause**: Empty data arrays or schema mismatch
- **Solution**: Normalize graph data format
- **Prevention**: Validate data before visualization

### **Missing Nodes/Edges**
- **Cause**: Entity extraction too restrictive
- **Solution**: Adjust extraction parameters
- **Prevention**: Test with various document types

### **HTML Not Rendering**
- **Cause**: Content-Type mismatch
- **Solution**: Use HTMLResponse with proper media_type
- **Prevention**: Consistent response format

## 📋 **Best Practices**

### **Data Preparation**
- **Normalize schemas**: Ensure consistent data format
- **Validate inputs**: Check for required fields
- **Handle errors**: Graceful fallbacks for missing data
- **Limit size**: Reasonable node/edge counts

### **Performance**
- **Batch processing**: Generate multiple visualizations efficiently
- **Caching**: Reuse generated visualizations when possible
- **Async operations**: Non-blocking visualization generation
- **Resource limits**: Prevent excessive memory usage

### **User Experience**
- **Loading indicators**: Show progress during generation
- **Error messages**: Clear feedback for failures
- **Multiple views**: Both embedded and external options
- **Responsive design**: Adapt to different screen sizes

## 🔄 **Workflow Integration**

### **Complete Analysis Pipeline**
1. **Start Analysis**: Begin document processing
2. **Extract Entities**: Identify key entities from text
3. **Generate Graph**: Create visualization data
4. **Render Visualization**: Produce interactive HTML
5. **Display Results**: Show in UI with other analysis

### **Individual Components**
- **Entity Extraction**: Standalone entity identification
- **Graph Generation**: Create visualization from existing data
- **Visualization Display**: Show existing visualizations
- **Data Export**: Save visualization data for reuse
```

---
