"""Test script for component providers."""

import asyncio
import json
from mcp_ui_aggregator.providers import registry, get_provider
from mcp_ui_aggregator.models.component_manifest import (
    Provider,
    ComponentSearchFilter,
    ComponentCategory
)


async def test_providers():
    """Test all registered providers."""
    print("🚀 Testing Component Providers")
    print("=" * 50)
    
    # List all providers
    providers = registry.list_providers()
    print(f"📋 Registered providers: {[p.value for p in providers]}")
    print()
    
    for provider_name in providers:
        print(f"🔍 Testing {provider_name.value.upper()} provider...")
        
        try:
            provider = get_provider(provider_name)
            
            # Test listing components
            print(f"   📦 Getting components...")
            components = await provider.list_components(limit=5)
            print(f"   ✅ Found {len(components)} components")
            
            if components:
                # Show first component details
                first_component = components[0]
                print(f"   📝 Sample component: {first_component.name}")
                print(f"      - ID: {first_component.id}")
                print(f"      - Category: {first_component.category}")
                print(f"      - Tags: {', '.join(first_component.tags[:3])}")
                print(f"      - License: {first_component.license.type}")
                print(f"      - Runtime deps: {', '.join(first_component.runtime_deps[:3])}")
                
                # Test getting specific component
                try:
                    specific = await provider.get_component(first_component.slug)
                    print(f"   ✅ Successfully retrieved specific component")
                except Exception as e:
                    print(f"   ❌ Failed to get specific component: {e}")
            
            # Test search
            print(f"   🔎 Testing search...")
            search_filter = ComponentSearchFilter(
                provider=provider_name,
                limit=3,
                query="button"
            )
            
            search_result = await provider.search_components(search_filter)
            print(f"   ✅ Search found {len(search_result.components)} components")
            
        except Exception as e:
            print(f"   ❌ Error testing {provider_name.value}: {e}")
        
        print()
    
    # Test cross-provider search
    print("🌐 Testing cross-provider search...")
    try:
        # This would be done through the API, but let's simulate it
        all_components = []
        for provider_name in providers:
            try:
                provider = get_provider(provider_name)
                components = await provider.list_components(limit=10)
                all_components.extend(components)
            except:
                continue
        
        print(f"✅ Total components across all providers: {len(all_components)}")
        
        # Group by category
        by_category = {}
        for comp in all_components:
            category = comp.category
            by_category[category] = by_category.get(category, 0) + 1
        
        print("📊 Components by category:")
        for category, count in sorted(by_category.items()):
            print(f"   {category}: {count}")
        
        # Group by provider
        by_provider = {}
        for comp in all_components:
            provider = comp.provider
            by_provider[provider] = by_provider.get(provider, 0) + 1
        
        print("📊 Components by provider:")
        for provider, count in sorted(by_provider.items()):
            print(f"   {provider}: {count}")
            
    except Exception as e:
        print(f"❌ Error in cross-provider test: {e}")


async def test_install_plan():
    """Test install plan generation."""
    print("\n" + "=" * 50)
    print("🛠️  Testing Install Plan Generation")
    print("=" * 50)
    
    try:
        # Get a Magic UI component
        magicui = get_provider(Provider.MAGICUI)
        components = await magicui.list_components(limit=1)
        
        if components:
            component = components[0]
            print(f"📦 Component: {component.name}")
            print(f"🔧 Install plan:")
            print(f"   Dependencies: {', '.join(component.runtime_deps)}")
            print(f"   Peer deps: {', '.join(component.peer_deps)}")
            
            if component.install.npm:
                print(f"   NPM commands: {', '.join(component.install.npm)}")
            
            if component.access.cli:
                print(f"   CLI command: {component.access.cli}")
            
            if component.tailwind:
                print(f"   Tailwind version: {component.tailwind.version}")
                if component.tailwind.plugin_deps:
                    print(f"   Tailwind plugins: {', '.join(component.tailwind.plugin_deps)}")
        
    except Exception as e:
        print(f"❌ Error testing install plan: {e}")


async def main():
    """Main test function."""
    await test_providers()
    await test_install_plan()
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())