#!/usr/bin/env python3
"""Test new providers: React Bits and Aceternity UI."""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_ui_aggregator.providers.registry import registry
from mcp_ui_aggregator.providers.reactbits import ReactBitsProvider
from mcp_ui_aggregator.providers.aceternity import AceternityProvider


async def test_providers():
    """Test the new providers."""
    print("🧪 Testing new providers: React Bits and Aceternity UI")
    print("=" * 60)
    
    # Test React Bits Provider
    print("\n🚀 Testing React Bits Provider")
    print("-" * 30)
    
    try:
        reactbits = ReactBitsProvider()
        components = await reactbits.list_components(limit=5)
        print(f"✅ React Bits: Found {len(components)} components")
        
        for comp in components:
            print(f"  - {comp.name} ({comp.id})")
            print(f"    📝 {comp.description}")
            print(f"    🏷️  Tags: {', '.join(comp.tags)}")
            print(f"    📦 License: {comp.license.type.value}")
            print(f"    ⚛️  Framework: React={comp.framework.react}, Next={comp.framework.next}")
            print()
    
    except Exception as e:
        print(f"❌ React Bits error: {e}")
    
    # Test Aceternity Provider
    print("\n✨ Testing Aceternity UI Provider")
    print("-" * 35)
    
    try:
        aceternity = AceternityProvider()
        components = await aceternity.list_components(limit=5)
        print(f"✅ Aceternity: Found {len(components)} components")
        
        for comp in components:
            print(f"  - {comp.name} ({comp.id})")
            print(f"    📝 {comp.description}")
            print(f"    🏷️  Tags: {', '.join(comp.tags)}")
            print(f"    📦 License: {comp.license.type.value}")
            print(f"    💎 Pro: {comp.access.pro}")
            print()
    
    except Exception as e:
        print(f"❌ Aceternity error: {e}")
    
    # Test registry
    print("\n📋 Testing Provider Registry")
    print("-" * 30)
    
    print("Available providers:")
    for provider_name in registry.list_providers():
        provider = registry.get_provider(provider_name)
        if provider:
            components_count = len(await provider.list_components(limit=1000))
            print(f"  - {provider_name}: {components_count} components")
    
    print("\n🎉 Testing completed!")


if __name__ == "__main__":
    asyncio.run(test_providers())