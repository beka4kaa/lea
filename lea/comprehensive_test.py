#!/usr/bin/env python3
"""
Comprehensive test suite for LEA UI Components MCP Server
Tests all endpoints and validates functionality
"""

import requests
import json
import time
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TestResult:
    endpoint: str
    method: str
    success: bool
    response_time: float
    status_code: int
    error: str = ""

class LEAUITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[TestResult] = []
        
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None) -> TestResult:
        """Test a single endpoint and return results"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, params=data, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response_time = time.time() - start_time
            
            result = TestResult(
                endpoint=endpoint,
                method=method,
                success=response.status_code == 200,
                response_time=response_time,
                status_code=response.status_code,
                error="" if response.status_code == 200 else response.text[:200]
            )
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print(f"✅ {method} {endpoint} - {response.status_code} ({response_time:.2f}s)")
                    if endpoint == "/components" and isinstance(response_data, dict):
                        print(f"   📊 Found {response_data.get('total', 0)} components")
                    elif endpoint.startswith("/blocks/"):
                        print(f"   📦 Block: {response_data.get('name', 'Unknown')}")
                    elif endpoint.startswith("/components/search"):
                        print(f"   🔍 Search results: {len(response_data.get('components', []))}")
                except:
                    print(f"✅ {method} {endpoint} - {response.status_code} ({response_time:.2f}s) [Non-JSON response]")
            else:
                print(f"❌ {method} {endpoint} - {response.status_code} ({response_time:.2f}s)")
                print(f"   Error: {result.error}")
                
        except Exception as e:
            response_time = time.time() - start_time
            result = TestResult(
                endpoint=endpoint,
                method=method,
                success=False,
                response_time=response_time,
                status_code=0,
                error=str(e)
            )
            print(f"❌ {method} {endpoint} - Exception ({response_time:.2f}s)")
            print(f"   Error: {str(e)}")
            
        self.results.append(result)
        return result
        
    def run_comprehensive_tests(self):
        """Run all tests systematically"""
        print("🚀 Starting Comprehensive LEA UI Components MCP Server Tests")
        print("=" * 70)
        
        # Test 1: Basic Health Check
        print("\n📋 Test 1: Basic Health Check")
        self.test_endpoint("/")
        self.test_endpoint("/health")
        self.test_endpoint("/mcp-status")
        
        # Test 2: Component Listing
        print("\n📋 Test 2: Component Listing")
        self.test_endpoint("/api/v1/components")
        self.test_endpoint("/api/v1/components", data={"limit": 10})
        self.test_endpoint("/api/v1/components", data={"provider": "shadcn"})
        self.test_endpoint("/api/v1/components", data={"category": "buttons"})
        self.test_endpoint("/api/v1/components", data={"framework": "react"})
        
        # Test 3: Component Search
        print("\n📋 Test 3: Component Search")
        self.test_endpoint("/api/v1/components/search", data={"query": "button"})
        self.test_endpoint("/api/v1/components/search", data={"query": "card"})
        self.test_endpoint("/api/v1/components/search", data={"query": "form"})
        self.test_endpoint("/api/v1/components/search", data={"query": "navigation"})
        self.test_endpoint("/api/v1/components/search", data={"query": "modal"})
        
        # Test 4: Provider Information
        print("\n📋 Test 4: Provider Information")
        self.test_endpoint("/api/v1/providers")
        self.test_endpoint("/api/v1/providers/shadcn")
        self.test_endpoint("/api/v1/providers/daisyui")
        self.test_endpoint("/api/v1/providers/magicui")
        
        # Test 5: UI Blocks
        print("\n📋 Test 5: UI Blocks")
        blocks_to_test = ["auth", "navbar", "hero", "pricing", "footer"]
        for block in blocks_to_test:
            self.test_endpoint(f"/api/v1/blocks/{block}")
            
        # Test 6: Component Code (if working)
        print("\n📋 Test 6: Component Code Retrieval")
        components_to_test = [
            "shadcn/button",
            "daisyui/btn",
            "alignui/button",
        ]
        for component in components_to_test:
            self.test_endpoint(f"/api/v1/components/{component}/code")
            
        # Test 7: Component Documentation
        print("\n📋 Test 7: Component Documentation")
        for component in components_to_test:
            self.test_endpoint(f"/api/v1/components/{component}/docs")
            
        # Test 8: Installation Plans
        print("\n📋 Test 8: Installation Plans")
        self.test_endpoint("/api/v1/install-plan", "POST", {
            "component_ids": ["shadcn/button", "daisyui/btn"],
            "target": "nextjs",
            "package_manager": "npm"
        })
        
        # Test 9: Component Verification
        print("\n📋 Test 9: Component Verification")
        test_code = '''
import React from 'react';

export default function TestButton({ children, onClick }) {
  return (
    <button 
      onClick={onClick}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      {children}
    </button>
  );
}
'''
        self.test_endpoint("/api/v1/verify", "POST", {
            "code": test_code,
            "framework": "react"
        })
        
        # Test 10: Edge Cases and Error Handling
        print("\n📋 Test 10: Edge Cases and Error Handling")
        self.test_endpoint("/api/v1/components/nonexistent-component")
        self.test_endpoint("/api/v1/blocks/nonexistent-block")
        self.test_endpoint("/api/v1/components/search", data={"query": ""})
        self.test_endpoint("/api/v1/components", data={"limit": 1000})
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        
        avg_response_time = sum(r.response_time for r in self.results) / total_tests if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "average_response_time": avg_response_time
            },
            "details": {
                "successful": [r for r in self.results if r.success],
                "failed": [r for r in self.results if not r.success]
            }
        }
        
        return report
        
    def print_summary(self):
        """Print test summary"""
        report = self.generate_report()
        summary = report["summary"]
        
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful: {summary['successful_tests']} ✅")
        print(f"Failed: {summary['failed_tests']} ❌")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Average Response Time: {summary['average_response_time']:.2f}s")
        
        if report["details"]["failed"]:
            print("\n❌ FAILED TESTS:")
            for failed in report["details"]["failed"]:
                print(f"   {failed.method} {failed.endpoint} - {failed.error[:100]}")
                
        print("\n🎯 PERFORMANCE METRICS:")
        fastest = min(self.results, key=lambda x: x.response_time)
        slowest = max(self.results, key=lambda x: x.response_time)
        print(f"   Fastest: {fastest.endpoint} ({fastest.response_time:.2f}s)")
        print(f"   Slowest: {slowest.endpoint} ({slowest.response_time:.2f}s)")
        
        # Component statistics
        component_tests = [r for r in self.results if r.endpoint.startswith("/components") and r.success]
        if component_tests:
            print(f"\n📦 COMPONENT TESTS:")
            print(f"   Successfully tested {len(component_tests)} component endpoints")
            
        # Block statistics  
        block_tests = [r for r in self.results if r.endpoint.startswith("/blocks") and r.success]
        if block_tests:
            print(f"\n🧱 BLOCK TESTS:")
            print(f"   Successfully tested {len(block_tests)} block types")

def main():
    """Main test execution"""
    tester = LEAUITester()
    
    print("🔥 LEA UI Components MCP Server - Comprehensive Test Suite")
    print("Testing server at: http://localhost:8000")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester.run_comprehensive_tests()
    tester.print_summary()
    
    print(f"\n✨ Testing completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()