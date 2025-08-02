#!/usr/bin/env python3
"""
PostgreSQL MCP Server for Living Truth Engine
Provides database access and querying capabilities
"""

import os
import sys
import json
import logging
import psycopg2
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP("PostgreSQL MCP Server")

class PostgreSQLIntegration:
    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST', 'localhost')
        self.port = os.getenv('POSTGRES_PORT', '5432')
        self.database = os.getenv('POSTGRES_DB', 'living_truth_engine')
        self.user = os.getenv('POSTGRES_USER', 'postgres')
        self.password = os.getenv('POSTGRES_PASSWORD', 'pass')
        
        self.connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        
        logger.info(f"PostgreSQL integration initialized for database: {self.database}")

    def _get_connection(self):
        """Get database connection."""
        try:
            return psycopg2.connect(self.connection_string)
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def test_connection(self) -> str:
        """Test database connection."""
        try:
            conn = self._get_connection()
            conn.close()
            return "✅ Database connection successful"
        except Exception as e:
            return f"❌ Database connection failed: {str(e)}"

    def list_tables(self) -> str:
        """List all tables in the database."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            tables = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if tables:
                result = "📋 **Database Tables:**\n\n"
                for table_name, table_type in tables:
                    result += f"- **{table_name}** ({table_type})\n"
                return result
            else:
                return "📋 No tables found in the database"
                
        except Exception as e:
            logger.error(f"Error listing tables: {e}")
            return f"❌ Error: {str(e)}"

    def describe_table(self, table_name: str) -> str:
        """Describe table structure."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position
            """, (table_name,))
            
            columns = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if columns:
                result = f"📋 **Table Structure: {table_name}**\n\n"
                result += "| Column | Type | Nullable | Default |\n"
                result += "|--------|------|----------|--------|\n"
                for col_name, data_type, is_nullable, col_default in columns:
                    nullable = "YES" if is_nullable == "YES" else "NO"
                    default = col_default or "NULL"
                    result += f"| {col_name} | {data_type} | {nullable} | {default} |\n"
                return result
            else:
                return f"❌ Table '{table_name}' not found"
                
        except Exception as e:
            logger.error(f"Error describing table: {e}")
            return f"❌ Error: {str(e)}"

    def execute_query(self, query: str, limit: int = 10) -> str:
        """Execute a SQL query safely."""
        try:
            # Basic security check - only allow SELECT queries
            query_lower = query.strip().lower()
            if not query_lower.startswith('select'):
                return "❌ Only SELECT queries are allowed for security reasons"
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Add LIMIT if not present
            if 'limit' not in query_lower:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            cursor.close()
            conn.close()
            
            if results:
                result = f"📊 **Query Results** (showing up to {limit} rows):\n\n"
                result += "| " + " | ".join(column_names) + " |\n"
                result += "|" + "|".join(["---"] * len(column_names)) + "|\n"
                
                for row in results:
                    result += "| " + " | ".join(str(cell) for cell in row) + " |\n"
                return result
            else:
                return "📊 Query executed successfully but returned no results"
                
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return f"❌ Query error: {str(e)}"

    def get_table_count(self, table_name: str) -> str:
        """Get row count for a table."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM %s", (table_name,))
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return f"📊 Table '{table_name}' contains {count} rows"
            
        except Exception as e:
            logger.error(f"Error getting table count: {e}")
            return f"❌ Error: {str(e)}"

# MCP Tool Definitions
@mcp.tool()
def test_connection() -> str:
    """Test PostgreSQL database connection."""
    db = PostgreSQLIntegration()
    return db.test_connection()

@mcp.tool()
def list_tables() -> str:
    """List all tables in the database."""
    db = PostgreSQLIntegration()
    return db.list_tables()

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Describe the structure of a specific table."""
    db = PostgreSQLIntegration()
    return db.describe_table(table_name)

@mcp.tool()
def execute_query(query: str, limit: int = 10) -> str:
    """Execute a SELECT query on the database (read-only for security)."""
    db = PostgreSQLIntegration()
    return db.execute_query(query, limit)

@mcp.tool()
def get_table_count(table_name: str) -> str:
    """Get the number of rows in a specific table."""
    db = PostgreSQLIntegration()
    return db.get_table_count(table_name)

@mcp.tool()
def get_database_status() -> str:
    """Get database connection status and configuration."""
    db = PostgreSQLIntegration()
    status = {
        "host": db.host,
        "port": db.port,
        "database": db.database,
        "user": db.user,
        "connection_status": db.test_connection()
    }
    return json.dumps(status, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio") 