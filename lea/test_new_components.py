#!/usr/bin/env python3
"""Test script to verify new interactive components are working."""

import asyncio
import sys
sys.path.append('/Users/bekzhan/Documents/projects/mcp/lea')

from mcp_ui_aggregator.providers.magicui import MagicUIProvider

async def test_new_components():
    """Test that new interactive components are available."""
    
    print("🎯 Testing New Interactive Components")
    print("=" * 50)
    
    magicui = MagicUIProvider()
    
    # Test new components
    new_components = ["contact-form", "modal-dialog", "image-gallery", 
                     "loading-spinner", "tooltip", "calculator"]
    
    for component_slug in new_components:
        try:
            component = await magicui.get_component(component_slug)
            print(f"✅ {component.name} ({component_slug})")
            print(f"   Category: {component.category}")
            print(f"   Has TSX code: {'✅ Yes' if component.code.tsx else '❌ No'}")
            if component.code.tsx:
                code_length = len(component.code.tsx)
                print(f"   Code length: {code_length} characters")
                if code_length > 100:
                    print(f"   Code preview: {component.code.tsx[:100]}...")
            print(f"   Dependencies: {component.runtime_deps}")
            print(f"   Description: {component.description}")
            print("")
        except Exception as e:
            print(f"❌ Error getting {component_slug}: {e}")
            print("")
    
    # Test component count
    try:
        all_components = await magicui.list_components(limit=1000)
        print(f"📊 Total components available: {len(all_components)}")
        
        # Count by category
        categories = {}
        for comp in all_components:
            cat = str(comp.category)
            categories[cat] = categories.get(cat, 0) + 1
        
        print("📈 Components by category:")
        for cat, count in sorted(categories.items()):
            print(f"   {cat}: {count}")
        
    except Exception as e:
        print(f"❌ Error listing components: {e}")
    
    print("\n🎯 New Interactive Components Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_new_components())