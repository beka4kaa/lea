#!/usr/bin/env python3
"""Script to get code for the top 5 beautiful button components."""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_ui_aggregator.providers.registry import get_all_providers
from mcp_ui_aggregator.models.component_manifest import Provider

async def get_component_codes():
    """Get the code for the top 5 beautiful button components."""
    
    top_components = [
        ("magicui", "magic-button"),
        ("magicui", "rainbow-button"), 
        ("hyperui", "newsletter-signup"),
        ("hyperui", "button-group"),
        ("shadcn", "button")
    ]
    
    providers = get_all_providers()
    provider_map = {p.provider_name.value.lower(): p for p in providers}
    
    print("🎨 TOP 5 BEAUTIFUL BUTTON COMPONENTS - CODE EXAMPLES")
    print("=" * 80)
    
    for i, (provider_name, component_slug) in enumerate(top_components, 1):
        print(f"\n{i}. {provider_name.upper()} - {component_slug}")
        print("-" * 60)
        
        try:
            provider = provider_map.get(provider_name)
            if provider:
                component = await provider.get_component(component_slug)
                
                print(f"Name: {component.name}")
                print(f"Description: {component.description}")
                
                # Get code from the component manifest
                if component.code.tsx:
                    print(f"\n📝 TSX Code:")
                    print("```tsx")
                    print(component.code.tsx[:1000] + "..." if len(component.code.tsx) > 1000 else component.code.tsx)
                    print("```")
                elif component.code.jsx:
                    print(f"\n📝 JSX Code:")
                    print("```jsx")
                    print(component.code.jsx[:1000] + "..." if len(component.code.jsx) > 1000 else component.code.jsx)
                    print("```")
                elif component.code.html:
                    print(f"\n📝 HTML Code:")
                    print("```html")
                    print(component.code.html[:1000] + "..." if len(component.code.html) > 1000 else component.code.html)
                    print("```")
                elif component.code.vue:
                    print(f"\n📝 Vue Code:")
                    print("```vue")
                    print(component.code.vue[:1000] + "..." if len(component.code.vue) > 1000 else component.code.vue)
                    print("```")
                else:
                    print("\n📝 Code not available in component manifest")
                    # Try to get code from provider-specific method if available
                    try:
                        if hasattr(provider, '_get_component_code'):
                            code_content = await provider._get_component_code(component_slug)
                            print("```typescript")
                            print(code_content[:1000] + "..." if len(code_content) > 1000 else code_content)
                            print("```")
                    except Exception as code_err:
                        print(f"Could not fetch code: {code_err}")
                
                # Installation info
                if hasattr(component, 'runtime_deps') and component.runtime_deps:
                    print(f"\n📦 Dependencies: {', '.join(component.runtime_deps)}")
                    
                if hasattr(component, 'tags') and component.tags:
                    print(f"🏷️ Tags: {', '.join(component.tags)}")
                    
        except Exception as e:
            print(f"❌ Error getting component: {e}")
            import traceback
            print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(get_component_codes())