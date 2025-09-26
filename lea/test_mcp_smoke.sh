#!/bin/bash

# MCP Bridge Smoke Tests
# This script tests the MCP JSON-RPC bridge functionality with curl

echo "🚀 Starting MCP Bridge Smoke Tests..."
echo "=================================="

BASE_URL="http://localhost:8000"
FAILED_TESTS=0
TOTAL_TESTS=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
run_test() {
    local test_name="$1"
    local request_data="$2"
    local expected_pattern="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Testing $test_name... "
    
    # Make request and capture response
    response=$(curl -s -X POST "$BASE_URL/mcp" \
        -H "Content-Type: application/json" \
        -d "$request_data")
    
    # Check if pattern exists in response
    if echo "$response" | grep -q "$expected_pattern"; then
        echo -e "${GREEN}✓ PASS${NC}"
        echo "  Response: $(echo "$response" | jq -c '.')"
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Expected pattern: $expected_pattern"
        echo "  Actual response: $response"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo
}

# Health check first
echo "🏥 Health Check"
echo "==============="
health_response=$(curl -s "$BASE_URL/mcp/health")
if echo "$health_response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ MCP endpoint is healthy${NC}"
    echo "  Response: $(echo "$health_response" | jq -c '.')"
else
    echo -e "${RED}✗ MCP endpoint is not healthy${NC}"
    echo "  Response: $health_response"
    exit 1
fi
echo

echo "🔧 MCP Protocol Tests"
echo "===================="

# Test 1: Initialize
run_test "MCP Initialize" \
'{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "Smoke Test",
      "version": "1.0.0"
    }
  }
}' \
'"Lea UI Components"'

# Test 2: Tools List
run_test "Tools List" \
'{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}' \
'"list_components"'

# Test 3: Search Components
run_test "Search Components" \
'{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "search_component",
    "arguments": {
      "query": "button",
      "limit": 3
    }
  }
}' \
'"components"'

# Test 4: List Components
run_test "List Components" \
'{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "list_components",
    "arguments": {
      "limit": 5,
      "offset": 0
    }
  }
}' \
'"total"'

# Test 5: Get Component Code
run_test "Get Component Code" \
'{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "get_component_code",
    "arguments": {
      "component_id": "shadcn/button",
      "format": "tsx"
    }
  }
}' \
'"code"'

# Test 6: Get UI Block
run_test "Get UI Block" \
'{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "get_block",
    "arguments": {
      "block_type": "auth",
      "target": "nextjs",
      "style": "tailwind"
    }
  }
}' \
'"Authentication Form"'

# Test 7: Install Plan
run_test "Install Plan" \
'{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "install_plan",
    "arguments": {
      "component_ids": ["shadcn/button", "magicui/animated-beam"],
      "target": "nextjs",
      "package_manager": "npm"
    }
  }
}' \
'"commands"'

# Test 8: Verify Code
run_test "Verify Code" \
'{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "tools/call",
  "params": {
    "name": "verify",
    "arguments": {
      "code": "import React from '\''react'\''; export default function Test() { return <div>Hello</div>; }",
      "framework": "react",
      "check_imports": true,
      "check_syntax": true
    }
  }
}' \
'"is_valid"'

# Test 9: Error Handling - Invalid Method
run_test "Invalid Method Error" \
'{
  "jsonrpc": "2.0",
  "id": 9,
  "method": "invalid_method",
  "params": {}
}' \
'"Method not found"'

# Test 10: Error Handling - Invalid Tool
run_test "Invalid Tool Error" \
'{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "invalid_tool",
    "arguments": {}
  }
}' \
'"error"'

echo "📊 Test Results Summary"
echo "======================"
PASSED_TESTS=$((TOTAL_TESTS - FAILED_TESTS))
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed! MCP bridge is working correctly.${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Check the output above for details.${NC}"
    exit 1
fi