#!/usr/bin/env python3
"""Test Phase 3 providers: AlignUI, 21st.dev, BentoGrids, Next.js Design."""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_ui_aggregator.providers.registry import registry
from mcp_ui_aggregator.providers.alignui import AlignUIProvider
from mcp_ui_aggregator.providers.twenty_first import TwentyFirstProvider
from mcp_ui_aggregator.providers.bentogrids import BentoGridsProvider
from mcp_ui_aggregator.providers.nextjs_design import NextJSDesignProvider


async def test_phase3_providers():
    """Test the Phase 3 providers."""
    print("🧪 Testing Phase 3 providers")
    print("=" * 60)
    
    # Test AlignUI Provider
    print("\n🎨 Testing AlignUI Provider (Base + Pro)")
    print("-" * 45)
    
    try:
        alignui = AlignUIProvider()
        components = await alignui.list_components(limit=5)
        print(f"✅ AlignUI: Found {len(components)} components")
        
        for comp in components:
            print(f"  - {comp.name} ({comp.id})")
            print(f"    📝 {comp.description}")
            print(f"    🏷️  Tags: {', '.join(comp.tags[:3])}...")
            print(f"    📦 License: {comp.license.type.value}")
            print(f"    💎 Pro: {comp.access.pro}")
            print()
    
    except Exception as e:
        print(f"❌ AlignUI error: {e}")
    
    # Test 21st.dev Provider
    print("\n📂 Testing 21st.dev Provider (Directory)")
    print("-" * 42)
    
    try:
        twenty_first = TwentyFirstProvider()
        components = await twenty_first.list_components(limit=4)
        print(f"✅ 21st.dev: Found {len(components)} components")
        
        for comp in components:
            print(f"  - {comp.name} ({comp.id})")
            print(f"    📝 {comp.description}")
            print(f"    🏷️  Tags: {', '.join(comp.tags)}")
            print(f"    🔗 External URL: {comp.source.url}")
            print()
    
    except Exception as e:
        print(f"❌ 21st.dev error: {e}")
    
    # Test BentoGrids Provider
    print("\n🍱 Testing BentoGrids Provider (Specialized)")
    print("-" * 47)
    
    try:
        bentogrids = BentoGridsProvider()
        components = await bentogrids.list_components(limit=4)
        print(f"✅ BentoGrids: Found {len(components)} components")
        
        for comp in components:
            print(f"  - {comp.name} ({comp.id})")
            print(f"    📝 {comp.description}")
            print(f"    🏷️  Tags: {', '.join(comp.tags)}")
            print(f"    🎯 Category: {comp.category}")
            print()
    
    except Exception as e:
        print(f"❌ BentoGrids error: {e}")
    
    # Test Next.js Design Provider
    print("\n⚡ Testing Next.js Design Provider (Templates)")
    print("-" * 50)
    
    try:
        nextjs_design = NextJSDesignProvider()
        components = await nextjs_design.list_components(limit=4)
        print(f"✅ Next.js Design: Found {len(components)} components")
        
        for comp in components:
            print(f"  - {comp.name} ({comp.id})")
            print(f"    📝 {comp.description}")
            print(f"    🏷️  Tags: {', '.join(comp.tags[:3])}...")
            print(f"    ⚛️  Next.js: {comp.framework.next}")
            print()
    
    except Exception as e:
        print(f"❌ Next.js Design error: {e}")
    
    # Test registry with all providers
    print("\n📋 Testing Complete Provider Registry")
    print("-" * 40)
    
    total_components = 0
    print("All available providers:")
    for provider_name in registry.list_providers():
        provider = registry.get_provider(provider_name)
        if provider:
            components_count = len(await provider.list_components(limit=1000))
            total_components += components_count
            print(f"  - {provider_name}: {components_count} components")
    
    print(f"\n🎉 Phase 3 Testing completed!")
    print(f"📊 Total components across all providers: {total_components}")


if __name__ == "__main__":
    asyncio.run(test_phase3_providers())