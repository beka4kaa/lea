#!/usr/bin/env python3
"""Тестирование MCP сервера - отправляем различные запросы."""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def send_mcp_request(method: str, params: Dict = None, request_id: int = 1) -> Dict[Any, Any]:
    """Отправка MCP запроса."""
    mcp_data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": request_id
    }
    
    print(f"📤 Отправляем MCP запрос:")
    print(f"   Method: {method}")
    print(f"   Params: {json.dumps(params, indent=2) if params else 'None'}")
    
    try:
        response = requests.post(f"{BASE_URL}/mcp", json=mcp_data, timeout=10)
        print(f"📥 Ответ (HTTP {response.status_code}):")
        
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        else:
            print(f"❌ Ошибка: {response.text}")
            return {"error": response.text}
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return {"error": str(e)}

def main():
    """Основная функция тестирования."""
    print("🧪 ТЕСТИРОВАНИЕ MCP СЕРВЕРА")
    print("=" * 60)
    
    # 1. Список доступных инструментов
    print("\n1️⃣ Получаем список инструментов MCP:")
    print("-" * 40)
    send_mcp_request("tools/list")
    
    time.sleep(1)
    
    # 2. Поиск компонентов
    print("\n2️⃣ Поиск компонентов кнопок:")
    print("-" * 40)
    search_params = {
        "name": "search_component",
        "arguments": {
            "query": "button",
            "limit": 5
        }
    }
    send_mcp_request("tools/call", search_params, 2)
    
    time.sleep(1)
    
    # 3. Список всех компонентов
    print("\n3️⃣ Список компонентов:")
    print("-" * 40)
    list_params = {
        "name": "list_components",
        "arguments": {
            "limit": 3,
            "provider": "shadcn"
        }
    }
    send_mcp_request("tools/call", list_params, 3)
    
    time.sleep(1)
    
    # 4. Получение кода компонента
    print("\n4️⃣ Получение кода компонента:")
    print("-" * 40)
    code_params = {
        "name": "get_component_code",
        "arguments": {
            "component_id": "shadcn/button"
        }
    }
    send_mcp_request("tools/call", code_params, 4)
    
    time.sleep(1)
    
    # 5. Получение блока
    print("\n5️⃣ Получение блока:")
    print("-" * 40)
    block_params = {
        "name": "get_block",
        "arguments": {
            "block_type": "auth",
            "target": "nextjs",
            "style": "tailwind"
        }
    }
    send_mcp_request("tools/call", block_params, 5)
    
    time.sleep(1)
    
    # 6. План установки
    print("\n6️⃣ План установки:")
    print("-" * 40)
    install_params = {
        "name": "install_plan",
        "arguments": {
            "component_ids": ["shadcn/button", "shadcn/input"],
            "target": "nextjs",
            "package_manager": "npm"
        }
    }
    send_mcp_request("tools/call", install_params, 6)
    
    time.sleep(1)
    
    # 7. Проверка кода
    print("\n7️⃣ Проверка кода:")
    print("-" * 40)
    verify_params = {
        "name": "verify",
        "arguments": {
            "code": "import React from 'react'; export default function Button({ children }) { return <button className='px-4 py-2 bg-blue-500 text-white rounded'>{children}</button>; }",
            "framework": "react"
        }
    }
    send_mcp_request("tools/call", verify_params, 7)
    
    print("\n" + "=" * 60)
    print("✅ Тестирование MCP сервера завершено!")

if __name__ == "__main__":
    main()