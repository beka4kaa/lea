"""Tests for MCP JSON-RPC bridge functionality."""

import json
import pytest
import httpx
from fastapi.testclient import TestClient
from typing import Dict, Any

# Test data
SAMPLE_MCP_REQUESTS = {
    "initialize": {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "Test Client",
                "version": "1.0.0"
            }
        }
    },
    "tools_list": {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    },
    "search_components": {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "search_component",
            "arguments": {
                "query": "button",
                "limit": 5
            }
        }
    },
    "get_component_code": {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "get_component_code",
            "arguments": {
                "component_id": "shadcn/button",
                "format": "tsx"
            }
        }
    },
    "get_block": {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "get_block",
            "arguments": {
                "block_type": "auth",
                "target": "nextjs",
                "style": "tailwind"
            }
        }
    }
}


class TestMCPBridge:
    """Test MCP JSON-RPC bridge functionality."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        from mcp_ui_aggregator.api.app import app
        return TestClient(app)
    
    def test_mcp_initialize(self, client):
        """Test MCP initialize request."""
        response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["initialize"])
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert "result" in data
        
        result = data["result"]
        assert result["protocolVersion"] == "2024-11-05"
        assert result["serverInfo"]["name"] == "Lea UI Components"
        assert result["serverInfo"]["version"] == "1.0.0"
        assert "capabilities" in result
    
    def test_mcp_tools_list(self, client):
        """Test MCP tools/list request."""
        response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["tools_list"])
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        assert "result" in data
        
        result = data["result"]
        assert "tools" in result
        assert len(result["tools"]) > 0
        
        # Check required tools are present
        tool_names = [tool["name"] for tool in result["tools"]]
        expected_tools = [
            "list_components",
            "search_component", 
            "get_component_code",
            "get_component_docs",
            "get_block",
            "install_plan",
            "verify"
        ]
        
        for tool in expected_tools:
            assert tool in tool_names
    
    def test_mcp_search_components(self, client):
        """Test MCP search_component tool call."""
        response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["search_components"])
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 3
        assert "result" in data
        
        result = data["result"]
        assert "content" in result
        assert len(result["content"]) > 0
        assert result["content"][0]["type"] == "text"
        
        # Parse the JSON content
        content_json = json.loads(result["content"][0]["text"])
        assert "query" in content_json
        assert content_json["query"] == "button"
        assert "components" in content_json
    
    def test_mcp_get_component_code(self, client):
        """Test MCP get_component_code tool call."""
        response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["get_component_code"])
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 4
        assert "result" in data
        
        result = data["result"]
        assert "content" in result
        assert len(result["content"]) > 0
        
        # Parse the JSON content
        content_json = json.loads(result["content"][0]["text"])
        assert "component_id" in content_json
        assert content_json["component_id"] == "shadcn/button"
        assert "code" in content_json
        assert "format" in content_json
    
    def test_mcp_get_block(self, client):
        """Test MCP get_block tool call."""
        response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["get_block"])
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 5
        assert "result" in data
        
        result = data["result"]
        assert "content" in result
        assert len(result["content"]) > 0
        
        # Parse the JSON content
        content_json = json.loads(result["content"][0]["text"])
        assert "name" in content_json
        assert "files" in content_json
        assert "dependencies" in content_json
        assert "commands" in content_json
    
    def test_mcp_invalid_method(self, client):
        """Test MCP request with invalid method."""
        invalid_request = {
            "jsonrpc": "2.0",
            "id": 999,
            "method": "invalid_method",
            "params": {}
        }
        
        response = client.post("/mcp", json=invalid_request)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 999
        assert "error" in data
        assert data["error"]["code"] == -32601
        assert "Method not found" in data["error"]["message"]
    
    def test_mcp_invalid_tool(self, client):
        """Test MCP tool call with invalid tool name."""
        invalid_tool_request = {
            "jsonrpc": "2.0",
            "id": 888,
            "method": "tools/call",
            "params": {
                "name": "invalid_tool",
                "arguments": {}
            }
        }
        
        response = client.post("/mcp", json=invalid_tool_request)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 888
        assert "result" in data
        
        # Parse the error content
        content_json = json.loads(data["result"]["content"][0]["text"])
        assert "error" in content_json
        assert "Unknown tool" in content_json["error"]
    
    def test_mcp_health_endpoint(self, client):
        """Test MCP health endpoint."""
        response = client.get("/mcp/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "server_info" in data
        assert data["server_info"]["name"] == "Lea UI Components"
        assert "tools_count" in data
        assert data["tools_count"] > 0
        assert "timestamp" in data


class TestMCPEndToEnd:
    """End-to-end MCP workflow tests."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        from mcp_ui_aggregator.api.app import app
        return TestClient(app)
    
    def test_mcp_full_workflow(self, client):
        """Test complete MCP workflow: initialize → list tools → search → get code."""
        
        # Step 1: Initialize
        init_response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["initialize"])
        assert init_response.status_code == 200
        init_data = init_response.json()
        assert "result" in init_data
        
        # Step 2: List tools
        tools_response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["tools_list"])
        assert tools_response.status_code == 200
        tools_data = tools_response.json()
        assert "result" in tools_data
        assert len(tools_data["result"]["tools"]) > 0
        
        # Step 3: Search components
        search_response = client.post("/mcp", json=SAMPLE_MCP_REQUESTS["search_components"])
        assert search_response.status_code == 200
        search_data = search_response.json()
        
        # Parse search results
        search_content = json.loads(search_data["result"]["content"][0]["text"])
        assert len(search_content["components"]) > 0
        
        # Step 4: Get component code (use first component from search)
        first_component = search_content["components"][0]
        component_id = f"{first_component['provider']}/{first_component['name'].lower().replace(' ', '-')}"
        
        get_code_request = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "get_component_code",
                "arguments": {
                    "component_id": component_id,
                    "format": "tsx"
                }
            }
        }
        
        code_response = client.post("/mcp", json=get_code_request)
        assert code_response.status_code == 200
        code_data = code_response.json()
        
        # Verify we got code
        code_content = json.loads(code_data["result"]["content"][0]["text"])
        assert "code" in code_content
        assert len(code_content["code"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])