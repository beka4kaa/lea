#!/usr/bin/env python3
"""Comprehensive test suite for all MCP UI Aggregator endpoints."""

import requests
import json
import time
import sys
from typing import Dict, List, Any
from datetime import datetime

BASE_URL = "http://localhost:8000"

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"✅ {test_name}")
        
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"❌ {test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success rate: {(self.passed/total)*100:.1f}%" if total > 0 else "No tests run")
        
        if self.errors:
            print(f"\nFAILED TESTS:")
            for error in self.errors:
                print(f"  - {error}")
                
        return self.failed == 0

def test_endpoint(test_result: TestResult, test_name: str, url: str, method: str = "GET", data: Dict = None, expected_status: int = 200):
    """Test a single endpoint."""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            test_result.add_fail(test_name, f"Unsupported method: {method}")
            return None
            
        if response.status_code == expected_status:
            test_result.add_pass(test_name)
            return response.json() if response.content else None
        else:
            test_result.add_fail(test_name, f"Expected {expected_status}, got {response.status_code}")
            return None
            
    except Exception as e:
        test_result.add_fail(test_name, f"Exception: {str(e)}")
        return None

def main():
    """Run all endpoint tests."""
    test_result = TestResult()
    
    print("🧪 TESTING MCP UI AGGREGATOR ENDPOINTS")
    print("="*60)
    
    # Root and health endpoints
    test_endpoint(test_result, "Root endpoint", f"{BASE_URL}/")
    test_endpoint(test_result, "Health Check", f"{BASE_URL}/health")
    
    # API v1 endpoints
    print(f"\n📡 API v1 Endpoints:")
    
    # Providers
    providers_data = test_endpoint(test_result, "Get Providers", f"{BASE_URL}/api/v1/providers")
    
    # Stats
    test_endpoint(test_result, "Get Stats", f"{BASE_URL}/api/v1/stats")
    
    # Components
    components_data = test_endpoint(test_result, "Get Components", f"{BASE_URL}/api/v1/components")
    
    # Components with query
    test_endpoint(test_result, "Search Components", f"{BASE_URL}/api/v1/components?q=button&limit=5")
    
    # Test individual provider endpoints if providers are available
    if providers_data and isinstance(providers_data, list):
        print(f"\n🏪 Provider-specific endpoints:")
        for provider_name in providers_data[:3]:  # Test first 3 providers
            test_endpoint(test_result, f"Provider {provider_name} components", 
                        f"{BASE_URL}/api/v1/providers/{provider_name}/components")
    
    # Test specific component by ID - try with a pattern that likely exists
    print(f"\n🧩 Component-specific endpoints:")
    test_endpoint(test_result, f"Specific component", 
                f"{BASE_URL}/api/v1/components/shadcn/button")
    
    # Blocks endpoints (POST methods)
    print(f"\n🧱 Blocks endpoints:")
    
    # Test blocks with POST method
    block_data = {
        "block_type": "auth",
        "target": "nextjs",
        "style": "tailwind"
    }
    test_endpoint(test_result, "Get auth block (POST)", f"{BASE_URL}/api/v1/blocks", "POST", block_data)
    
    # Test install plan
    install_data = {
        "component_ids": ["shadcn/button"],
        "target": "nextjs",
        "package_manager": "npm"
    }
    test_endpoint(test_result, "Get install plan", f"{BASE_URL}/api/v1/install-plan", "POST", install_data)
    
    # Test code verification
    verify_data = {
        "code": "import React from 'react'; export default function Button() { return <button>Click me</button>; }",
        "framework": "react"
    }
    test_endpoint(test_result, "Verify code", f"{BASE_URL}/api/v1/verify", "POST", verify_data)
    
    # MCP endpoints
    print(f"\n🔗 MCP Bridge endpoints:")
    test_endpoint(test_result, "MCP Health", f"{BASE_URL}/mcp/health")
    
    # Test MCP bridge with valid data
    mcp_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 1
    }
    test_endpoint(test_result, "MCP Tools List", f"{BASE_URL}/mcp", "POST", mcp_data)
    
    # Provider-specific tests
    print(f"\n🎨 UI Component Provider Tests:")
    
    # Test providers individually
    if providers_data and isinstance(providers_data, list):
        for provider_name in providers_data[:3]:
            # Get components for each provider
            provider_components = test_endpoint(test_result, 
                f"Get {provider_name} components", 
                f"{BASE_URL}/api/v1/providers/{provider_name}/components")
    
    # Performance test
    print(f"\n⚡ Performance Tests:")
    start_time = time.time()
    test_endpoint(test_result, "Performance test (components)", f"{BASE_URL}/api/v1/components?limit=10")
    end_time = time.time()
    
    response_time = end_time - start_time
    if response_time < 5.0:  # Should respond within 5 seconds
        test_result.add_pass(f"Response time ({response_time:.2f}s)")
    else:
        test_result.add_fail(f"Response time ({response_time:.2f}s)", "Too slow (>5s)")
    
    # Test error handling
    print(f"\n🚨 Error Handling Tests:")
    test_endpoint(test_result, "Non-existent provider", f"{BASE_URL}/api/v1/providers/non-existent/components", expected_status=404)
    test_endpoint(test_result, "Invalid component ID", f"{BASE_URL}/api/v1/components/invalid/component-id", expected_status=404)
    
    # Final summary
    success = test_result.summary()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED! Ready for GitHub push.")
        return 0
    else:
        print(f"\n💥 SOME TESTS FAILED! Please fix issues before pushing.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)