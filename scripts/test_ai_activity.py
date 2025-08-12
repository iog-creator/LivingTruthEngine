#!/usr/bin/env python3
"""
Test script to simulate AI activity WebSocket messages
Demonstrates the enhanced AI Activity Panel functionality
"""

import asyncio
import websockets
import json
import time

async def test_ai_activity():
    """Test the AI Activity Panel with simulated WebSocket messages"""
    
    uri = "ws://localhost:8050/ws/ai-activity"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to AI Activity WebSocket")
            
            # Test 1: Start LLM inference
            print("\n1. Starting LLM inference...")
            await websocket.send(json.dumps({
                "ai_type": "llm",
                "status": "working",
                "current_activity": "Processing user query with LLM",
                "progress_step": 1
            }))
            
            await asyncio.sleep(2)
            
            # Test 2: Start embedding
            print("2. Starting embedding...")
            await websocket.send(json.dumps({
                "ai_type": "embedder", 
                "status": "working",
                "current_activity": "Generating embeddings for documents",
                "progress_step": 2
            }))
            
            await asyncio.sleep(2)
            
            # Test 3: Start OCR
            print("3. Starting OCR...")
            await websocket.send(json.dumps({
                "ai_type": "ocr",
                "status": "working", 
                "current_activity": "Extracting text from images",
                "progress_step": 3
            }))
            
            await asyncio.sleep(2)
            
            # Test 4: Complete all tasks
            print("4. Completing all tasks...")
            await websocket.send(json.dumps({
                "ai_type": "llm",
                "status": "done",
                "current_activity": "Analysis complete",
                "progress_step": 3
            }))
            
            await websocket.send(json.dumps({
                "ai_type": "embedder",
                "status": "done"
            }))
            
            await websocket.send(json.dumps({
                "ai_type": "ocr", 
                "status": "done"
            }))
            
            await asyncio.sleep(1)
            
            # Test 5: Reset to idle
            print("5. Resetting to idle...")
            await websocket.send(json.dumps({
                "current_activity": "Idle",
                "progress_step": 0
            }))
            
            print("\nAI Activity Panel test completed!")
            
    except websockets.exceptions.ConnectionRefused:
        print("❌ WebSocket connection refused. Make sure the dashboard is running and WebSocket endpoint is available.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧠 Testing Enhanced AI Activity Panel")
    print("=" * 40)
    print("This test simulates the AI activity monitoring system")
    print("Open http://localhost:8050 in your browser to see the activity panel")
    print("=" * 40)
    
    asyncio.run(test_ai_activity())
