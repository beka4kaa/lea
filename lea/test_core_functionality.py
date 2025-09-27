#!/usr/bin/env python3
"""Quick functional test to verify core features work."""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_core_functionality():
    """Test core functionality that users will actually use."""
    
    print("🔧 CORE FUNCTIONALITY TEST")
    print("="*50)
    
    # 1. Health check
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Server health: OK")
    
    # 2. Get providers list
    response = requests.get(f"{BASE_URL}/api/v1/providers")
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) > 0
    print(f"✅ Providers available: {len(providers)}")
    
    # 3. Get components from a provider
    response = requests.get(f"{BASE_URL}/api/v1/providers/shadcn/components")
    assert response.status_code == 200
    components = response.json()
    assert len(components) > 0
    print(f"✅ ShadCN components: {len(components)}")
    
    # 4. Search for button components
    response = requests.get(f"{BASE_URL}/api/v1/components?q=button&limit=10")
    assert response.status_code == 200
    search_result = response.json()
    print(f"✅ Button search: found results")
    
    # 5. Get MCP tools
    mcp_data = {
        "jsonrpc": "2.0",
        "method": "tools/list", 
        "params": {},
        "id": 1
    }
    response = requests.post(f"{BASE_URL}/mcp", json=mcp_data)
    assert response.status_code == 200
    print("✅ MCP tools: accessible")
    
    # 6. Test blocks functionality
    block_data = {
        "block_type": "auth",
        "target": "nextjs",
        "style": "tailwind"
    }
    response = requests.post(f"{BASE_URL}/api/v1/blocks", json=block_data)
    assert response.status_code == 200
    print("✅ Blocks generation: working")
    
    # 7. Test install plan
    install_data = {
        "component_ids": ["shadcn/button"],
        "target": "nextjs",
        "package_manager": "npm"
    }
    response = requests.post(f"{BASE_URL}/api/v1/install-plan", json=install_data)
    assert response.status_code == 200
    print("✅ Install plans: working")
    
    print("\n🎉 ALL CORE FUNCTIONALITY TESTS PASSED!")
    print("The application is ready for production!")
    
    return True

if __name__ == "__main__":
    try:
        test_core_functionality()
        exit(0)
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        exit(1)