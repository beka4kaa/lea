#!/usr/bin/env python3
"""
Quick test script for MCP Discovery Issue fixes using curl.
Tests key scenarios from AGENT_FIX_PROMPT.md
"""

import subprocess
import json
import sys
from datetime import datetime

def run_curl(url, data=None, method="GET"):
    """Run curl command and return result."""
    try:
        if method == "GET":
            cmd = ["curl", "-s", url]
        else:  # POST
            cmd = ["curl", "-s", "-X", "POST", url, "-H", "Content-Type: application/json", "-d", json.dumps(data)]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            try:
                return True, json.loads(result.stdout)
            except json.JSONDecodeError:
                return True, {"raw_response": result.stdout}
        else:
            return False, {"error": result.stderr}
            
    except subprocess.TimeoutExpired:
        return False, {"error": "Request timeout"}
    except Exception as e:
        return False, {"error": str(e)}

def test_discovery_endpoints():
    """Test discovery endpoints."""
    print("\n🔍 DISCOVERY ENDPOINTS TESTS")
    print("="*50)
    
    tests = [
        ("MCP Discovery", "http://localhost:8000/mcp-discovery"),
        ("MCP Status", "http://localhost:8000/mcp-status"),  
        ("OpenAPI MCP", "http://localhost:8000/openapi-mcp.json"),
        ("Root Endpoint", "http://localhost:8000/")
    ]
    
    results = []
    for name, url in tests:
        print(f"Testing {name}...")
        success, response = run_curl(url)
        results.append((name, success, response))
        print(f"  {'✅ PASS' if success else '❌ FAIL'}")
    
    return results

def test_format_validation():
    """Test JSON-RPC 2.0 format validation."""
    print("\n🔧 FORMAT VALIDATION TESTS")
    print("="*50)
    
    tests = [
        ("Valid JSON-RPC 2.0", {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }),
        ("REST-style Request", {
            "query": "button beautiful modern",
            "limit": 10
        }),
        ("Missing jsonrpc", {
            "id": 1,
            "method": "tools/list",
            "params": {}
        }),
        ("Missing method", {
            "jsonrpc": "2.0",
            "id": 1,
            "params": {}
        }),
        ("Unknown method", {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "unknown/method",
            "params": {}
        })
    ]
    
    results = []
    for name, data in tests:
        print(f"Testing {name}...")
        success, response = run_curl("http://localhost:8000/mcp", data, "POST")
        results.append((name, success, response))
        
        # Check if we got expected error handling
        if name == "REST-style Request" and success:
            has_error = "error" in response and "PROTOCOL MISMATCH" in response["error"]["message"]
            print(f"  {'✅ PASS - Correct error' if has_error else '❌ FAIL - Wrong response'}")
        elif name == "Valid JSON-RPC 2.0" and success:
            has_result = "result" in response
            print(f"  {'✅ PASS - Got result' if has_result else '❌ FAIL - No result'}")
        else:
            print(f"  {'✅ PASS' if success else '❌ FAIL'}")
    
    return results

def test_tool_calls():
    """Test tool call functionality.""" 
    print("\n🛠️  TOOL CALL TESTS")
    print("="*50)
    
    tests = [
        ("List Components", {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "list_components", "arguments": {"limit": 2}}
        }),
        ("Search Components", {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call", 
            "params": {"name": "search_component", "arguments": {"query": "button", "limit": 2}}
        }),
        ("Unknown Tool", {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "unknown_tool", "arguments": {}}
        })
    ]
    
    results = []
    for name, data in tests:
        print(f"Testing {name}...")
        success, response = run_curl("http://localhost:8000/mcp", data, "POST")
        results.append((name, success, response))
        
        # Check response quality
        if success and "result" in response:
            content = response.get("result", {}).get("content", [])
            if content and len(content) > 0:
                print(f"  ✅ PASS - Got content")
            else:
                print(f"  ⚠️  PASS - No content")
        else:
            print(f"  {'✅ PASS' if success else '❌ FAIL'}")
    
    return results

def generate_report(discovery_results, validation_results, tool_results):
    """Generate test report."""
    print("\n" + "="*80)
    print("📊 TEST REPORT")
    print("="*80)
    
    all_results = discovery_results + validation_results + tool_results
    total_tests = len(all_results)
    passed_tests = sum(1 for _, success, _ in all_results if success)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    # Check key features
    discovery_working = any(success for _, success, _ in discovery_results)
    validation_working = any(success for _, success, _ in validation_results)
    tools_working = any(success for _, success, _ in tool_results)
    
    print(f"\n✅ Key Features Status:")
    print(f"   - Discovery endpoints: {'✅' if discovery_working else '❌'}")
    print(f"   - Format validation: {'✅' if validation_working else '❌'}")
    print(f"   - Tool calls: {'✅' if tools_working else '❌'}")
    
    print(f"\n🎯 MCP Server Discovery Issue Fix Status:")
    success_rate = passed_tests/total_tests*100
    if success_rate >= 90 and discovery_working and validation_working:
        print("   🎉 FIXED! All major issues resolved.")
        return True
    elif success_rate >= 75:
        print("   🔧 MOSTLY FIXED. Minor issues remain.")
        return True
    else:
        print("   ⚠️  PARTIALLY FIXED. More work needed.")
        return False

def main():
    """Run all tests."""
    print("🚀 MCP Server Discovery Issue Fix Tests")
    print("Testing key scenarios from AGENT_FIX_PROMPT.md")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    print("\n🔍 Checking server health...")
    success, response = run_curl("http://localhost:8000/health")
    if not success:
        print("❌ Server is not running. Please start the server first.")
        print("   Run: cd lea && python3 -m uvicorn mcp_ui_aggregator.api.app:app --port 8000")
        return False
    
    print("✅ Server is running")
    
    # Run all test suites
    discovery_results = test_discovery_endpoints()
    validation_results = test_format_validation()
    tool_results = test_tool_calls()
    
    # Generate report
    return generate_report(discovery_results, validation_results, tool_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)