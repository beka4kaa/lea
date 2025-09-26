#!/usr/bin/env python3
"""Test Phase 4 providers - HyperUI and Tailwind Components Gallery."""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_ui_aggregator.providers.registry import get_all_providers
from mcp_ui_aggregator.models.component_manifest import Provider

async def test_phase4_providers():
    """Test Phase 4 providers (HyperUI and Tailwind Components Gallery)."""
    print("🧪 Testing Phase 4 providers")
    print("=" * 60)
    
    # Get all providers
    providers = get_all_providers()
    
    # Test HyperUI Provider
    hyperui_provider = next((p for p in providers if p.provider_name == Provider.HYPERUI), None)
    if hyperui_provider:
        print("\n🎨 Testing HyperUI Provider (Free Tailwind Components)")
        print("-" * 60)
        try:
            components = await hyperui_provider.list_components(limit=10)
            print(f"✅ HyperUI: Found {len(components)} components")
            
            for comp in components[:5]:  # Show first 5
                print(f"  - {comp.name} ({comp.id})")
                print(f"    📝 {comp.description}")
                print(f"    🏷️  Tags: {', '.join(comp.tags[:3])}...")
                print(f"    🎯 Category: {comp.category}")
                print(f"    🌐 Free: {comp.access.free}")
                print()
            
        except Exception as e:
            print(f"❌ Error testing HyperUI: {e}")
    else:
        print("❌ HyperUI provider not found")
    
    # Test Tailwind Components Gallery Provider
    tailwind_provider = next((p for p in providers if p.provider_name == Provider.TAILWIND_COMPONENTS), None)
    if tailwind_provider:
        print("\n🎨 Testing Tailwind Components Gallery Provider")
        print("-" * 60)
        try:
            components = await tailwind_provider.list_components(limit=10)
            print(f"✅ Tailwind Components: Found {len(components)} components")
            
            for comp in components[:5]:  # Show first 5
                print(f"  - {comp.name} ({comp.id})")
                print(f"    📝 {comp.description}")
                print(f"    🏷️  Tags: {', '.join(comp.tags[:3])}...")
                print(f"    🎯 Category: {comp.category}")
                print(f"    🔧 Complexity: {comp.tags[-1] if comp.tags else 'unknown'}")
                if comp.runtime_deps:
                    print(f"    📦 Runtime deps: {', '.join(comp.runtime_deps)}")
                print()
            
        except Exception as e:
            print(f"❌ Error testing Tailwind Components: {e}")
    else:
        print("❌ Tailwind Components provider not found")
    
    # Test complete registry
    print("\n📋 Testing Complete Provider Registry")
    print("-" * 40)
    print("All available providers:")
    
    total_components = 0
    for provider in providers:
        try:
            components_count = len(await provider.list_components(limit=1000))
            total_components += components_count
            print(f"  - {provider.provider_name}: {components_count} components")
        except Exception as e:
            print(f"  - {provider.provider_name}: Error - {e}")
    
    print(f"\n🎉 Phase 4 Testing completed!")
    print(f"📊 Total components across all providers: {total_components}")

if __name__ == "__main__":
    asyncio.run(test_phase4_providers())