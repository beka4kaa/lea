#!/usr/bin/env python3
"""
Final comprehensive test and validation report for LEA UI Components MCP Server
Validates all functionality and creates a detailed report
"""

import requests
import json
import time
from typing import Dict, List, Any
import sys

class LEAUIValidator:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        
    def test_endpoint(self, name: str, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> Dict:
        """Test endpoint and return structured result"""
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
            success = response.status_code == expected_status
            
            result = {
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "success": success,
                "status_code": response.status_code,
                "response_time": response_time,
                "data_length": len(response.text),
                "error": "" if success else response.text[:200]
            }
            
            if success and response.status_code == 200:
                try:
                    json_data = response.json()
                    if isinstance(json_data, dict):
                        if "components" in json_data:
                            result["components_count"] = len(json_data["components"])
                            result["total_components"] = json_data.get("total", 0)
                        elif "name" in json_data and "files" in json_data:
                            result["block_name"] = json_data["name"]
                            result["files_count"] = len(json_data["files"])
                        elif "providers" in json_data:
                            result["providers_count"] = len(json_data["providers"])
                except:
                    pass
                    
            print(f"{'✅' if success else '❌'} {name}: {response.status_code} ({response_time:.3f}s)")
            if not success:
                print(f"   Error: {result['error']}")
                
        except Exception as e:
            response_time = time.time() - start_time
            result = {
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "data_length": 0,
                "error": str(e)
            }
            print(f"❌ {name}: Exception ({response_time:.3f}s) - {str(e)}")
            
        self.results.append(result)
        return result
        
    def run_validation_suite(self):
        """Run comprehensive validation"""
        print("🚀 LEA UI Components MCP Server - Final Validation Suite")
        print("=" * 80)
        print(f"Testing server: {self.base_url}")
        print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. Health Check
        print("🔍 1. Health & Status Endpoints")
        self.test_endpoint("Root Health", "GET", "/")
        self.test_endpoint("Health Check", "GET", "/health")
        self.test_endpoint("MCP Status", "GET", "/mcp-status")
        print()
        
        # 2. Component Discovery
        print("🔍 2. Component Discovery & Search")
        self.test_endpoint("List All Components", "GET", "/api/v1/components")
        self.test_endpoint("Limited Components", "GET", "/api/v1/components", {"limit": 10})
        self.test_endpoint("Search by Query", "GET", "/api/v1/components", {"query": "button"})
        self.test_endpoint("Filter by Provider", "GET", "/api/v1/components", {"provider": "shadcn"})
        self.test_endpoint("Filter by Category", "GET", "/api/v1/components", {"category": "buttons"})
        self.test_endpoint("Framework Filter", "GET", "/api/v1/components", {"framework": "react"})
        print()
        
        # 3. Provider Management
        print("🔍 3. Provider Information")
        self.test_endpoint("List Providers", "GET", "/api/v1/providers")
        print()
        
        # 4. Component Details
        print("🔍 4. Component Code & Documentation")
        components_to_test = [
            ("daisyui/btn", "DaisyUI Button"),
            ("alignui/button", "AlignUI Button"),
            ("shadcn/button", "Shadcn Button")
        ]
        
        for comp_id, name in components_to_test:
            provider, component = comp_id.split("/")
            self.test_endpoint(f"{name} Code", "GET", f"/api/v1/components/{provider}/{component}/code")
            self.test_endpoint(f"{name} Docs", "GET", f"/api/v1/components/{provider}/{component}/docs")
        print()
        
        # 5. UI Blocks (All Types)
        print("🔍 5. UI Blocks Generation")
        block_types = ["auth", "navbar", "hero", "pricing", "footer", "features", "testimonials", "cta", "dashboard", "landing"]
        
        for block_type in block_types:
            self.test_endpoint(f"{block_type.title()} Block", "POST", "/api/v1/blocks", {"block_type": block_type})
        print()
        
        # 6. Component Installation
        print("🔍 6. Installation & Verification")
        self.test_endpoint("Installation Plan", "POST", "/api/v1/install-plan", {
            "component_ids": ["shadcn/button", "daisyui/btn"],
            "target": "nextjs",
            "package_manager": "npm"
        })
        
        # Test code verification
        test_code = '''import React from 'react';

export default function TestButton({ children, onClick }) {
  return (
    <button 
      onClick={onClick}
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      {children}
    </button>
  );
}'''
        
        self.test_endpoint("Code Verification", "POST", "/api/v1/verify", {
            "code": test_code,
            "framework": "react"
        })
        print()
        
        # 7. Performance & Edge Cases
        print("🔍 7. Performance & Edge Cases")
        self.test_endpoint("Large Limit Test", "GET", "/api/v1/components", {"limit": 200})
        self.test_endpoint("Empty Query", "GET", "/api/v1/components", {"query": ""})
        self.test_endpoint("Invalid Block Type", "POST", "/api/v1/blocks", {"block_type": "invalid"}, 400)
        print()
        
    def generate_final_report(self):
        """Generate comprehensive final report"""
        successful = [r for r in self.results if r["success"]]
        failed = [r for r in self.results if not r["success"]]
        
        total_tests = len(self.results)
        success_rate = (len(successful) / total_tests * 100) if total_tests > 0 else 0
        avg_response_time = sum(r["response_time"] for r in self.results) / total_tests
        
        print("=" * 80)
        print("📊 FINAL COMPREHENSIVE VALIDATION REPORT")
        print("=" * 80)
        
        # Summary Statistics
        print(f"🎯 SUMMARY STATISTICS")
        print(f"   Total Tests Executed: {total_tests}")
        print(f"   Successful Tests: {len(successful)} ✅")
        print(f"   Failed Tests: {len(failed)} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Response Time: {avg_response_time:.3f}s")
        print()
        
        # Component Statistics
        component_results = [r for r in successful if r.get("components_count") or r.get("total_components")]
        if component_results:
            main_result = component_results[0]
            print(f"📦 COMPONENT STATISTICS")
            print(f"   Total Components Available: {main_result.get('total_components', 'Unknown')}")
            print(f"   Component Retrieval Tests: {len([r for r in successful if 'Component' in r['name']])}")
            print()
        
        # Block Statistics
        block_results = [r for r in successful if r.get("block_name")]
        if block_results:
            print(f"🧱 UI BLOCKS STATISTICS")
            print(f"   Successful Block Generations: {len(block_results)}")
            print(f"   Block Types Working: {', '.join([r['block_name'] for r in block_results[:5]])}")
            if len(block_results) > 5:
                print(f"   ... and {len(block_results) - 5} more")
            print()
        
        # Provider Statistics
        provider_results = [r for r in successful if r.get("providers_count")]
        if provider_results:
            print(f"🏢 PROVIDER STATISTICS")
            print(f"   Active Providers: {provider_results[0].get('providers_count', 'Unknown')}")
            print()
        
        # Performance Metrics
        fastest = min(self.results, key=lambda x: x["response_time"])
        slowest = max(self.results, key=lambda x: x["response_time"])
        
        print(f"⚡ PERFORMANCE METRICS")
        print(f"   Fastest Response: {fastest['name']} ({fastest['response_time']:.3f}s)")
        print(f"   Slowest Response: {slowest['name']} ({slowest['response_time']:.3f}s)")
        print(f"   Performance Grade: {'A+' if avg_response_time < 0.1 else 'A' if avg_response_time < 0.5 else 'B' if avg_response_time < 1.0 else 'C'}")
        print()
        
        # Functionality Assessment
        print(f"🔧 FUNCTIONALITY ASSESSMENT")
        
        # Component Management
        component_tests = len([r for r in successful if any(word in r['name'].lower() for word in ['component', 'search', 'filter'])])
        component_grade = "✅ EXCELLENT" if component_tests >= 8 else "⚠️ GOOD" if component_tests >= 5 else "❌ NEEDS WORK"
        print(f"   Component Management: {component_grade} ({component_tests}/10 tests passed)")
        
        # Block Generation
        block_tests = len([r for r in successful if 'block' in r['name'].lower()])
        block_grade = "✅ EXCELLENT" if block_tests >= 8 else "⚠️ GOOD" if block_tests >= 5 else "❌ NEEDS WORK"
        print(f"   UI Block Generation: {block_grade} ({block_tests}/10 tests passed)")
        
        # Documentation & Code
        docs_tests = len([r for r in successful if any(word in r['name'].lower() for word in ['code', 'docs', 'install', 'verify'])])
        docs_grade = "✅ EXCELLENT" if docs_tests >= 6 else "⚠️ GOOD" if docs_tests >= 4 else "❌ NEEDS WORK"
        print(f"   Documentation & Code: {docs_grade} ({docs_tests}/8 tests passed)")
        print()
        
        # Overall System Health
        overall_grade = "A+" if success_rate >= 90 else "A" if success_rate >= 80 else "B" if success_rate >= 70 else "C" if success_rate >= 60 else "F"
        print(f"🏆 OVERALL SYSTEM GRADE: {overall_grade}")
        print()
        
        # Recommendations
        print(f"💡 RECOMMENDATIONS")
        if failed:
            print("   Issues to Address:")
            for failure in failed[:3]:  # Show top 3 failures
                print(f"   - Fix: {failure['name']} ({failure['error'][:50]}...)")
        else:
            print("   ✅ System is performing excellently!")
            print("   ✅ All core functionality is working")
            print("   ✅ Ready for production use")
        
        print()
        print(f"✨ Validation completed: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        return {
            "total_tests": total_tests,
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "grade": overall_grade
        }

def main():
    """Run validation suite"""
    try:
        validator = LEAUIValidator()
        validator.run_validation_suite()
        report = validator.generate_final_report()
        
        # Return appropriate exit code
        sys.exit(0 if report["success_rate"] >= 80 else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Validation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()