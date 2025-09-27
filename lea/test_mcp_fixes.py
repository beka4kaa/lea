#!/usr/bin/env python3
"""Тестирование исправленных MCP функций."""

import requests
import json

BASE_URL = "http://localhost:8000"

def send_mcp_request(method: str, params: dict = None, request_id: int = 1):
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
            if 'result' in result and 'content' in result['result']:
                # Извлекаем содержимое из MCP ответа
                content = result['result']['content'][0]['text']
                try:
                    parsed_content = json.loads(content)
                    print(json.dumps(parsed_content, indent=2, ensure_ascii=False))
                    return parsed_content
                except json.JSONDecodeError:
                    print(content)
                    return content
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return result
        else:
            print(f"❌ Ошибка: {response.text}")
            return {"error": response.text}
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return {"error": str(e)}

def main():
    """Тестирование исправленных функций."""
    print("🔧 ТЕСТИРОВАНИЕ ИСПРАВЛЕННЫХ MCP ФУНКЦИЙ")
    print("=" * 60)
    
    # 1. Поиск компонентов
    print("\n1️⃣ Поиск компонентов кнопок:")
    print("-" * 40)
    search_params = {
        "name": "search_component",
        "arguments": {
            "query": "button",
            "limit": 3
        }
    }
    result1 = send_mcp_request("tools/call", search_params, 1)
    
    # 2. Список компонентов
    print("\n2️⃣ Список компонентов:")
    print("-" * 40)
    list_params = {
        "name": "list_components",
        "arguments": {
            "limit": 3,
            "provider": "shadcn"
        }
    }
    result2 = send_mcp_request("tools/call", list_params, 2)
    
    # 3. Получение кода компонента (попробуем другой подход)
    print("\n3️⃣ Получение кода компонента:")
    print("-" * 40)
    code_params = {
        "name": "get_component_code",
        "arguments": {
            "component_id": "shadcn/button"
        }
    }
    result3 = send_mcp_request("tools/call", code_params, 3)
    
    print("\n" + "=" * 60)
    
    # Проверим результаты
    success_count = 0
    total_count = 3
    
    if result1 and not result1.get("error"):
        print("✅ Поиск компонентов: ИСПРАВЛЕН")
        success_count += 1
    else:
        print("❌ Поиск компонентов: все еще есть проблемы")
    
    if result2 and not result2.get("error"):
        print("✅ Список компонентов: ИСПРАВЛЕН")  
        success_count += 1
    else:
        print("❌ Список компонентов: все еще есть проблемы")
        
    if result3 and not result3.get("error"):
        print("✅ Получение кода: ИСПРАВЛЕН")
        success_count += 1
    else:
        print("❌ Получение кода: все еще есть проблемы")
    
    print(f"\nРезультат: {success_count}/{total_count} функций исправлены!")
    
    if success_count == total_count:
        print("🎉 ВСЕ MCP ФУНКЦИИ РАБОТАЮТ!")
    else:
        print("🔧 Нужны дополнительные исправления")

if __name__ == "__main__":
    main()