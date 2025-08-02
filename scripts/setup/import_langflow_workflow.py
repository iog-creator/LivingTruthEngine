#!/usr/bin/env python3
"""
Living Truth Engine - Langflow Workflow Import Script
Imports the Survivor Testimony Analysis workflow into Langflow
"""

import os
import sys
import json
import requests
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LangflowWorkflowImporter:
    """Imports workflows into Langflow service."""
    
    def __init__(self):
        """Initialize the Langflow workflow importer."""
        self.langflow_url = os.getenv('LANGFLOW_API_ENDPOINT', 'http://localhost:3100')
        self.username = os.getenv('LANGFLOW_SUPERUSER', 'admin')
        self.password = os.getenv('LANGFLOW_SUPERUSER_PASSWORD', 'admin')
        self.session = requests.Session()
        
        logger.info(f"Langflow importer initialized for {self.langflow_url}")
    
    def login(self) -> bool:
        """Login to Langflow and get authentication token."""
        try:
            login_url = f"{self.langflow_url}/api/v1/auth/login"
            login_data = {
                "username": self.username,
                "password": self.password
            }
            
            response = self.session.post(login_url, json=login_data, timeout=30)
            
            if response.status_code == 200:
                token = response.json().get('access_token')
                if token:
                    self.session.headers.update({'Authorization': f'Bearer {token}'})
                    logger.info("Successfully logged into Langflow")
                    return True
                else:
                    logger.error("No access token received from Langflow")
                    return False
            else:
                logger.error(f"Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def import_workflow(self, workflow_file: Path) -> bool:
        """Import a workflow JSON file into Langflow."""
        try:
            if not workflow_file.exists():
                logger.error(f"Workflow file not found: {workflow_file}")
                return False
            
            # Read workflow JSON
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # Import workflow
            import_url = f"{self.langflow_url}/api/v1/flows"
            
            response = self.session.post(
                import_url, 
                json=workflow_data, 
                timeout=60
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                flow_id = result.get('id')
                logger.info(f"Successfully imported workflow: {flow_id}")
                return True
            else:
                logger.error(f"Import failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Import error: {e}")
            return False
    
    def list_workflows(self) -> Optional[list]:
        """List all workflows in Langflow."""
        try:
            list_url = f"{self.langflow_url}/api/v1/flows"
            
            response = self.session.get(list_url, timeout=30)
            
            if response.status_code == 200:
                workflows = response.json()
                logger.info(f"Found {len(workflows)} workflows")
                return workflows
            else:
                logger.error(f"List workflows failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"List workflows error: {e}")
            return None
    
    def delete_workflow(self, flow_id: str) -> bool:
        """Delete a workflow from Langflow."""
        try:
            delete_url = f"{self.langflow_url}/api/v1/flows/{flow_id}"
            
            response = self.session.delete(delete_url, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"Successfully deleted workflow: {flow_id}")
                return True
            else:
                logger.error(f"Delete failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Delete error: {e}")
            return False

def main():
    """Main function to import the Survivor Testimony Analysis workflow."""
    try:
        # Initialize importer
        importer = LangflowWorkflowImporter()
        
        # Login to Langflow
        if not importer.login():
            logger.error("Failed to login to Langflow")
            sys.exit(1)
        
        # Get workflow file path
        project_root = Path(__file__).parent.parent.parent
        workflow_file = project_root / "LivingTruthEngine_ForensicAnalysis_Langflow.json"
        
        # Check if workflow already exists
        existing_workflows = importer.list_workflows()
        if existing_workflows:
            for workflow in existing_workflows:
                if workflow.get('name') == 'Living Truth Engine Forensic Analysis':
                    logger.info("Workflow already exists, deleting old version")
                    importer.delete_workflow(workflow['id'])
                    break
        
        # Import workflow
        if importer.import_workflow(workflow_file):
            logger.info("✅ Forensic Analysis workflow imported successfully!")
            
            # List workflows to confirm
            workflows = importer.list_workflows()
            if workflows:
                logger.info("Available workflows:")
                for workflow in workflows:
                    logger.info(f"  - {workflow.get('name', 'Unknown')} (ID: {workflow.get('id', 'Unknown')})")
        else:
            logger.error("❌ Failed to import workflow")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Script error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 