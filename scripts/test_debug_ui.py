#!/usr/bin/env python3
"""
Debug UI Proof-of-Life Test
Simulates the browser-based Debug UI to verify frontend-backend integration
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8050"

async def get(session: aiohttp.ClientSession, path: str, init: Dict[str, Any] = None) -> Dict[str, Any]:
    """Simulate the Debug UI's get function"""
    if init is None:
        init = {}
    
    headers = {'Accept': 'application/json'}
    if 'headers' in init:
        headers.update(init['headers'])
    
    method = init.get('method', 'GET')
    data = init.get('body')
    
    async with session.request(method, f"{BASE_URL}{path}", headers=headers, data=data) as r:
        j = await r.json()
        # Envelope format validation - all endpoints must use {status, data?, error?}
        if 'status' in j and ('data' in j or 'error' in j):
            return j
        raise Exception(f'envelope mismatch {path}')

async def run_proof_of_life():
    """Run the Proof-of-Life test"""
    print("Running Proof-of-Life test...")
    
    async with aiohttp.ClientSession() as session:
        try:
            print("GET /api/health")
            health = await get(session, '/api/health')
            print(json.dumps(health, indent=2))
            
            print("GET /api/health/full")
            health_full = await get(session, '/api/health/full')
            print(json.dumps(health_full, indent=2))
            
            print("GET /api/runs")
            runs = await get(session, '/api/runs')
            print(json.dumps(runs, indent=2))
            
            rid = runs.get('data', [{}])[0].get('run_id') if runs.get('data') else None
            if rid:
                print("POST /api/analyze/summary")
                summary = await get(session, '/api/analyze/summary', {
                    'method': 'POST',
                    'body': json.dumps({'run_id': rid}),
                    'headers': {'Content-Type': 'application/json'}
                })
                print(json.dumps(summary, indent=2))
                
                print("POST /api/analyze/claims")
                claims = await get(session, '/api/analyze/claims', {
                    'method': 'POST',
                    'body': json.dumps({'run_id': rid}),
                    'headers': {'Content-Type': 'application/json'}
                })
                print(json.dumps(claims, indent=2))
            else:
                print("No runs found; skipping analyze endpoints.")
            
            print("GET /api/tools")
            tools = await get(session, '/api/tools')
            print(json.dumps(tools, indent=2))
            
            print("\nPoL SUCCESS ✅")
            return True
            
        except Exception as e:
            print(f"\nPoL FAIL ❌ {str(e)}")
            return False

if __name__ == "__main__":
    success = asyncio.run(run_proof_of_life())
    sys.exit(0 if success else 1)
