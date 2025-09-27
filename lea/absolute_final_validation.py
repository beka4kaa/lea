#!/usr/bin/env python3
"""
ABSOLUTE FINAL COMPREHENSIVE VALIDATION - EVERYTHING CHECKED
Tests every single endpoint, edge case, and functionality
"""

import requests
import json
import time
from typing import Dict, List, Any
import sys

class AbsoluteFinalValidator:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.critical_issues = []
        self.warnings = []
        
    def test_endpoint(self, name: str, method: str, endpoint: str, data: Dict = None, expected_status: int = 200, critical: bool = True) -> Dict:
        """Test endpoint with critical/non-critical classification"""
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
                "critical": critical,
                "data_length": len(response.text),
                "error": "" if success else response.text[:200]
            }
            
            # Parse response data for additional info
            if success and response.status_code == 200:
                try:
                    json_data = response.json()
                    if isinstance(json_data, dict):
                        result["response_keys"] = list(json_data.keys())
                        # Component stats
                        if "total_components" in json_data:
                            result["total_components"] = json_data["total_components"]
                        if "providers" in json_data:
                            result["providers_count"] = json_data["providers"]
                        # Component data
                        if "components" in json_data:
                            result["components_count"] = len(json_data["components"])
                        if "code" in json_data:
                            result["has_code"] = bool(json_data["code"])
                        if "name" in json_data and "files" in json_data:
                            result["block_generated"] = True
                    elif isinstance(json_data, list):
                        result["list_length"] = len(json_data)
                except:
                    pass
                    
            # Track critical issues
            if not success and critical:
                self.critical_issues.append(f"{name}: {response.status_code} - {result['error']}")
            elif not success and not critical:
                self.warnings.append(f"{name}: {response.status_code} - {result['error']}")
                    
            status_icon = "✅" if success else ("🔥" if critical else "⚠️")
            print(f"{status_icon} {name}: {response.status_code} ({response_time:.3f}s)")
            if not success:
                print(f"   {'CRITICAL' if critical else 'WARNING'}: {result['error']}")
                
        except Exception as e:
            response_time = time.time() - start_time
            result = {
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "critical": critical,
                "data_length": 0,
                "error": str(e)
            }
            
            if critical:
                self.critical_issues.append(f"{name}: Exception - {str(e)}")
            else:
                self.warnings.append(f"{name}: Exception - {str(e)}")
                
            status_icon = "🔥" if critical else "⚠️"
            print(f"{status_icon} {name}: Exception ({response_time:.3f}s) - {str(e)}")
            
        self.results.append(result)
        return result
        
    def run_absolute_final_validation(self):
        """Run EVERYTHING - no stone unturned"""
        print("🔥 ABSOLUTE FINAL COMPREHENSIVE VALIDATION")
        print("=" * 80)
        print(f"Testing server: {self.base_url}")
        print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 GOAL: Test EVERY SINGLE endpoint and functionality")
        print()
        
        # 1. CRITICAL SYSTEM HEALTH
        print("🔥 1. CRITICAL SYSTEM HEALTH")
        self.test_endpoint("Root Health", "GET", "/", critical=True)
        self.test_endpoint("Health Check", "GET", "/health", critical=True)
        self.test_endpoint("MCP Status", "GET", "/mcp-status", critical=True)
        self.test_endpoint("MCP Discovery", "GET", "/mcp-discovery", critical=True)
        self.test_endpoint("MCP Health", "GET", "/mcp/health", critical=True)
        print()
        
        # 2. CORE COMPONENT FUNCTIONALITY  
        print("🔥 2. CORE COMPONENT FUNCTIONALITY")
        self.test_endpoint("List All Components", "GET", "/api/v1/components", critical=True)
        self.test_endpoint("Component Stats", "GET", "/api/v1/stats", critical=True)
        self.test_endpoint("Search Buttons", "GET", "/api/v1/components", {"query": "button"}, critical=True)
        self.test_endpoint("Filter by Provider", "GET", "/api/v1/components", {"provider": "daisyui"}, critical=True)
        self.test_endpoint("Filter by Category", "GET", "/api/v1/components", {"category": "buttons"}, critical=True)
        self.test_endpoint("Framework Filter", "GET", "/api/v1/components", {"framework": "react"}, critical=True)
        self.test_endpoint("Free Components Only", "GET", "/api/v1/components", {"free_only": True}, critical=False)
        self.test_endpoint("Pagination Test", "GET", "/api/v1/components", {"limit": 50, "offset": 10}, critical=True)
        print()
        
        # 3. PROVIDER MANAGEMENT
        print("🔥 3. PROVIDER MANAGEMENT")
        self.test_endpoint("List All Providers", "GET", "/api/v1/providers", critical=True)
        
        # Test each provider
        providers = ["daisyui", "shadcn", "magicui", "alignui", "reactbits"]
        for provider in providers:
            self.test_endpoint(f"{provider.title()} Components", "GET", f"/api/v1/providers/{provider}/components", critical=True)
            self.test_endpoint(f"{provider.title()} Sync", "POST", f"/api/v1/providers/{provider}/sync", critical=False)
        print()
        
        # 4. COMPONENT CODE & DOCS (CRITICAL TEST)
        print("🔥 4. COMPONENT CODE & DOCUMENTATION")
        critical_components = [
            ("daisyui/btn", "DaisyUI Button"),
            ("alignui/button", "AlignUI Button"), 
            ("reactbits/magnetic-button", "ReactBits Magnetic"),
            ("aceternity/3d-card-effect", "Aceternity 3D Card"),
        ]
        
        for comp_id, name in critical_components:
            provider, component = comp_id.split("/")
            self.test_endpoint(f"{name} Code", "GET", f"/api/v1/components/{provider}/{component}/code", critical=True)
            self.test_endpoint(f"{name} Docs", "GET", f"/api/v1/components/{provider}/{component}/docs", critical=True)
            
        # Test format fallback with a component that has code
        self.test_endpoint("Format Fallback Test", "GET", "/api/v1/components/aceternity/3d-card-effect/code?format=vue", critical=True)
        self.test_endpoint("Shadcn Button Docs", "GET", "/api/v1/components/shadcn/button/docs", critical=True)
        print()
        
        # 5. UI BLOCKS (ALL TYPES)
        print("🔥 5. UI BLOCKS GENERATION")
        block_types = ["auth", "navbar", "hero", "pricing", "footer", "features", "testimonials", "cta", "dashboard", "landing"]
        
        for block_type in block_types:
            self.test_endpoint(f"{block_type.title()} Block", "POST", "/api/v1/blocks", {"block_type": block_type}, critical=True)
        
        # Test invalid block
        self.test_endpoint("Invalid Block Type", "POST", "/api/v1/blocks", {"block_type": "nonexistent"}, 404, critical=False)
        print()
        
        # 6. INSTALLATION & VERIFICATION
        print("🔥 6. INSTALLATION & VERIFICATION")
        self.test_endpoint("Single Component Install", "POST", "/api/v1/install-plan", {
            "component_ids": ["daisyui/btn"],
            "target": "nextjs",
            "package_manager": "npm"
        }, critical=True)
        
        self.test_endpoint("Multi Component Install", "POST", "/api/v1/install-plan", {
            "component_ids": ["daisyui/btn", "alignui/button", "reactbits/magnetic-button"],
            "target": "react",
            "package_manager": "yarn"
        }, critical=True)
        
        # Test code verification
        valid_code = '''import React from 'react';

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
        
        self.test_endpoint("Valid Code Verification", "POST", "/api/v1/verify", {
            "code": valid_code,
            "framework": "react"
        }, critical=True)
        
        invalid_code = "import React from 'react'; export default function Bad({ }) { return <button>; }"
        self.test_endpoint("Invalid Code Verification", "POST", "/api/v1/verify", {
            "code": invalid_code,
            "framework": "react"
        }, 400, critical=False)
        print()
        
        # 7. EDGE CASES & STRESS TESTS
        print("🔥 7. EDGE CASES & STRESS TESTS")
        self.test_endpoint("Empty Query Search", "GET", "/api/v1/components", {"query": ""}, critical=False)
        self.test_endpoint("Very Long Query", "GET", "/api/v1/components", {"query": "a" * 100}, critical=False)
        self.test_endpoint("Special Characters", "GET", "/api/v1/components", {"query": "!@#$%^&*()"}, critical=False)
        self.test_endpoint("Large Limit", "GET", "/api/v1/components", {"limit": 500}, critical=False)
        self.test_endpoint("Invalid Provider", "GET", "/api/v1/components", {"provider": "nonexistent"}, critical=False)
        self.test_endpoint("Invalid Framework", "GET", "/api/v1/components", {"framework": "nonexistent"}, critical=False)
        
        # Test nonexistent components
        self.test_endpoint("Nonexistent Component Code", "GET", "/api/v1/components/fake/component/code", 404, critical=False)
        self.test_endpoint("Nonexistent Component Docs", "GET", "/api/v1/components/fake/component/docs", 404, critical=False)
        print()
        
        # 8. MCP-SPECIFIC FUNCTIONALITY  
        print("🔥 8. MCP-SPECIFIC FUNCTIONALITY")
        self.test_endpoint("MCP Root", "GET", "/mcp", critical=True)
        self.test_endpoint("OpenAPI MCP Schema", "GET", "/openapi-mcp.json", critical=True)
        self.test_endpoint("OpenAPI Main Schema", "GET", "/openapi.json", critical=True)
        print()
        
    def generate_absolute_final_report(self):
        """Generate the ultimate comprehensive report"""
        successful = [r for r in self.results if r["success"]]
        failed = [r for r in self.results if not r["success"]]
        critical_failed = [r for r in failed if r["critical"]]
        warnings_failed = [r for r in failed if not r["critical"]]
        
        total_tests = len(self.results)
        success_rate = (len(successful) / total_tests * 100) if total_tests > 0 else 0
        critical_success_rate = ((len([r for r in self.results if r["critical"]]) - len(critical_failed)) / len([r for r in self.results if r["critical"]]) * 100) if len([r for r in self.results if r["critical"]]) > 0 else 0
        
        print("=" * 80)
        print("🔥 ABSOLUTE FINAL COMPREHENSIVE REPORT")
        print("=" * 80)
        
        # CRITICAL STATUS
        print(f"🎯 CRITICAL SYSTEM STATUS")
        if len(critical_failed) == 0:
            print(f"   ✅ ALL CRITICAL FUNCTIONALITY: WORKING PERFECTLY")
        else:
            print(f"   🔥 CRITICAL ISSUES FOUND: {len(critical_failed)}")
            
        print(f"   Total Tests: {total_tests}")
        print(f"   Overall Success: {len(successful)}/{total_tests} ({success_rate:.1f}%)")
        print(f"   Critical Success: {critical_success_rate:.1f}%")
        print(f"   Critical Issues: {len(critical_failed)} 🔥")
        print(f"   Warnings: {len(warnings_failed)} ⚠️")
        print()
        
        # DETAILED ANALYSIS
        if len(critical_failed) > 0:
            print(f"🔥 CRITICAL ISSUES (MUST FIX):")
            for issue in self.critical_issues[:5]:
                print(f"   🔥 {issue}")
            if len(self.critical_issues) > 5:
                print(f"   ... and {len(self.critical_issues) - 5} more critical issues")
            print()
            
        if len(warnings_failed) > 0:
            print(f"⚠️ WARNINGS (NICE TO FIX):")
            for warning in self.warnings[:5]:
                print(f"   ⚠️ {warning}")
            if len(self.warnings) > 5:
                print(f"   ... and {len(self.warnings) - 5} more warnings")
            print()
        
        # FUNCTIONALITY BREAKDOWN
        component_tests = len([r for r in successful if any(word in r['name'].lower() for word in ['component', 'search', 'provider', 'code', 'docs'])])
        block_tests = len([r for r in successful if 'block' in r['name'].lower()])
        system_tests = len([r for r in successful if any(word in r['name'].lower() for word in ['health', 'status', 'mcp'])])
        
        print(f"📊 FUNCTIONALITY BREAKDOWN")
        print(f"   Component System: {component_tests} tests ✅")
        print(f"   UI Block Generation: {block_tests} tests ✅")
        print(f"   System Health: {system_tests} tests ✅")
        print()
        
        # FINAL VERDICT
        if len(critical_failed) == 0:
            verdict = "🏆 SYSTEM IS FULLY OPERATIONAL"
            grade = "A+"
            recommendation = "✅ READY FOR PRODUCTION USE"
        elif len(critical_failed) <= 2:
            verdict = "⚠️ SYSTEM IS MOSTLY OPERATIONAL"
            grade = "A-"
            recommendation = "⚠️ FIX CRITICAL ISSUES BEFORE PRODUCTION"
        else:
            verdict = "🔥 SYSTEM HAS SIGNIFICANT ISSUES"
            grade = "C"
            recommendation = "🔥 REQUIRES IMMEDIATE ATTENTION"
            
        print(f"🏆 FINAL VERDICT: {verdict}")
        print(f"📈 SYSTEM GRADE: {grade}")
        print(f"💡 RECOMMENDATION: {recommendation}")
        print()
        
        # COMPONENT STATISTICS
        stats_results = [r for r in successful if r.get("total_components")]
        if stats_results:
            print(f"📦 COMPONENT ECOSYSTEM STATUS")
            print(f"   Total Components: {stats_results[0].get('total_components', 'Unknown')}")
            print(f"   Active Providers: {stats_results[0].get('providers_count', 'Unknown')}")
            print()
        
        print(f"✨ Absolute final validation completed: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 CONCLUSION: Every endpoint, functionality, and edge case tested!")
        print("=" * 80)
        
        return {
            "total_tests": total_tests,
            "successful": len(successful),
            "critical_failed": len(critical_failed),
            "warnings": len(warnings_failed),
            "success_rate": success_rate,
            "critical_success_rate": critical_success_rate,
            "grade": grade,
            "fully_operational": len(critical_failed) == 0
        }

def main():
    """Run absolute final validation"""
    try:
        validator = AbsoluteFinalValidator()
        validator.run_absolute_final_validation()
        report = validator.generate_absolute_final_report()
        
        # Return appropriate exit code
        sys.exit(0 if report["fully_operational"] else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Validation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()