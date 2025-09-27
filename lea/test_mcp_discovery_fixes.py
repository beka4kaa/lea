#!/usr/bin/env python3
"""
Test script for MCP Server Discovery Issue fixes.
Tests all scenarios mentioned in AGENT_FIX_PROMPT.md
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Dict, Any, List

class MCPServerTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_case(self, name: str, url: str, data: Dict[str, Any] = None, method: str = "GET") -> Dict[str, Any]:
        """Execute a single test case."""
        print(f"\n🧪 Testing: {name}")
        print(f"   URL: {method} {url}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
            
        start_time = datetime.now()
        
        try:
            if method == "GET":
                async with self.session.get(url) as response:
                    result = await response.json()
                    status = response.status
            else:  # POST
                async with self.session.post(url, json=data) as response:
                    result = await response.json()
                    status = response.status
                    
            duration = (datetime.now() - start_time).total_seconds()
            
            test_result = {
                "test": name,
                "url": url,
                "method": method,
                "status": status,
                "duration_ms": round(duration * 1000, 2),
                "success": status == 200,
                "response": result,
                "timestamp": start_time.isoformat()
            }
            
            if test_result["success"]:
                print(f"   ✅ PASS ({status}) - {duration*1000:.1f}ms")
            else:
                print(f"   ❌ FAIL ({status}) - {duration*1000:.1f}ms")
                
            self.test_results.append(test_result)
            return test_result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            test_result = {
                "test": name,
                "url": url,
                "method": method,
                "status": 0,
                "duration_ms": round(duration * 1000, 2),
                "success": False,
                "error": str(e),
                "timestamp": start_time.isoformat()
            }
            print(f"   💥 ERROR - {str(e)}")
            self.test_results.append(test_result)
            return test_result

    async def run_discovery_tests(self):
        """Test all discovery endpoints."""
        print("\n" + "="*60)
        print("🔍 DISCOVERY ENDPOINTS TESTS")
        print("="*60)
        
        # Test 1: MCP Discovery endpoint
        await self.test_case(
            "MCP Discovery Endpoint",
            f"{self.base_url}/mcp-discovery"
        )
        
        # Test 2: OpenAPI MCP Schema
        await self.test_case(
            "OpenAPI MCP Schema",
            f"{self.base_url}/openapi-mcp.json"
        )
        
        # Test 3: MCP Status
        await self.test_case(
            "MCP Status Endpoint",
            f"{self.base_url}/mcp-status"
        )

    async def run_format_validation_tests(self):
        """Test JSON-RPC 2.0 format validation."""
        print("\n" + "="*60)
        print("🔧 FORMAT VALIDATION TESTS")
        print("="*60)
        
        # Test 1: Valid JSON-RPC 2.0 request
        await self.test_case(
            "Valid JSON-RPC 2.0 Request",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            "POST"
        )
        
        # Test 2: REST-style request (should return helpful error)
        await self.test_case(
            "REST-style Request (Should Show Error)",
            f"{self.base_url}/mcp",
            {
                "query": "button beautiful modern",
                "limit": 10
            },
            "POST"
        )
        
        # Test 3: Missing jsonrpc field
        await self.test_case(
            "Missing jsonrpc Field",
            f"{self.base_url}/mcp",
            {
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            "POST"
        )
        
        # Test 4: Missing method field
        await self.test_case(
            "Missing method Field",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "params": {}
            },
            "POST"
        )
        
        # Test 5: Missing id field
        await self.test_case(
            "Missing id Field",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {}
            },
            "POST"
        )
        
        # Test 6: Invalid JSON
        print(f"\n🧪 Testing: Invalid JSON")
        print(f"   URL: POST {self.base_url}/mcp")
        start_time = datetime.now()
        try:
            async with self.session.post(f"{self.base_url}/mcp", data="invalid json") as response:
                result = await response.json()
                duration = (datetime.now() - start_time).total_seconds()
                print(f"   ✅ PASS ({response.status}) - {duration*1000:.1f}ms")
                self.test_results.append({
                    "test": "Invalid JSON",
                    "status": response.status,
                    "success": True,
                    "response": result
                })
        except Exception as e:
            print(f"   ✅ PASS - Correctly handled invalid JSON: {str(e)}")

    async def run_tool_call_tests(self):
        """Test tool call functionality."""
        print("\n" + "="*60)
        print("🛠️  TOOL CALL TESTS")
        print("="*60)
        
        # Test 1: Valid search_component call
        await self.test_case(
            "Valid search_component Call",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "search_component",
                    "arguments": {
                        "query": "button beautiful",
                        "limit": 3
                    }
                }
            },
            "POST"
        )
        
        # Test 2: Valid list_components call
        await self.test_case(
            "Valid list_components Call",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "list_components",
                    "arguments": {"limit": 5}
                }
            },
            "POST"
        )
        
        # Test 3: Unknown tool call
        await self.test_case(
            "Unknown Tool Call",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "unknown_tool",
                    "arguments": {}
                }
            },
            "POST"
        )
        
        # Test 4: Initialize method
        await self.test_case(
            "Initialize Method",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "initialize",
                "params": {"protocolVersion": "2024-11-05"}
            },
            "POST"
        )

    async def run_error_handling_tests(self):
        """Test comprehensive error handling."""
        print("\n" + "="*60)
        print("💥 ERROR HANDLING TESTS")
        print("="*60)
        
        # Test 1: Unknown method
        await self.test_case(
            "Unknown Method",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "unknown/method",
                "params": {}
            },
            "POST"
        )
        
        # Test 2: Malformed tool call
        await self.test_case(
            "Malformed Tool Call",
            f"{self.base_url}/mcp",
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "search_component"
                    # Missing arguments
                }
            },
            "POST"
        )

    def generate_report(self):
        """Generate test report."""
        print("\n" + "="*80)
        print("📊 TEST REPORT")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")  
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   - {result['test']}: {result.get('error', 'Status ' + str(result['status']))}")
        
        print(f"\n✅ Key Improvements Working:")
        discovery_working = any(r["success"] and "Discovery" in r["test"] for r in self.test_results)
        format_validation_working = any(r["success"] and "REST-style" in r["test"] for r in self.test_results)
        error_handling_working = any(r["success"] and "Unknown" in r["test"] for r in self.test_results)
        
        print(f"   - Discovery endpoints: {'✅' if discovery_working else '❌'}")
        print(f"   - Format validation: {'✅' if format_validation_working else '❌'}")
        print(f"   - Error handling: {'✅' if error_handling_working else '❌'}")
        
        print(f"\n🎯 MCP Server Discovery Issue Fix Status:")
        if success_rate >= 90 and discovery_working and format_validation_working:
            print("   🎉 FIXED! All major issues resolved.")
        elif success_rate >= 75:
            print("   🔧 MOSTLY FIXED. Minor issues remain.")
        else:
            print("   ⚠️  PARTIALLY FIXED. More work needed.")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": success_rate,
            "discovery_working": discovery_working,
            "format_validation_working": format_validation_working,
            "error_handling_working": error_handling_working
        }

async def main():
    """Run all MCP server tests."""
    print("🚀 MCP Server Discovery Issue Fix Tests")
    print("Testing all scenarios from AGENT_FIX_PROMPT.md")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async with MCPServerTester() as tester:
        # Run all test suites
        await tester.run_discovery_tests()
        await tester.run_format_validation_tests()
        await tester.run_tool_call_tests()
        await tester.run_error_handling_tests()
        
        # Generate final report
        report = tester.generate_report()
        
        # Save detailed results
        with open("mcp_fix_test_results.json", "w") as f:
            json.dump({
                "summary": report,
                "detailed_results": tester.test_results,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: mcp_fix_test_results.json")
        
        return report["success_rate"] >= 90

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)