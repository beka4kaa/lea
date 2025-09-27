#!/usr/bin/env python3
"""Test script to verify enhanced component templates are working."""

import asyncio
import sys
sys.path.append('/Users/bekzhan/Documents/projects/mcp/lea')

from mcp_ui_aggregator.providers.shadcn import ShadcnUIProvider
from mcp_ui_aggregator.providers.magicui import MagicUIProvider

async def test_enhanced_components():
    """Test that enhanced components return proper code."""
    
    print("🧪 Testing Enhanced Component Templates")
    print("=" * 50)
    
    # Test Shadcn provider
    print("\n📦 Testing Shadcn Provider...")
    shadcn = ShadcnUIProvider()
    
    try:
        button_manifest = await shadcn.get_component("button")
        print(f"✅ Button component found: {button_manifest.name}")
        print(f"   Has TSX code: {'✅ Yes' if button_manifest.code.tsx else '❌ No'}")
        if button_manifest.code.tsx:
            code_length = len(button_manifest.code.tsx)
            print(f"   Code length: {code_length} characters")
            if code_length > 100:
                print(f"   Code preview: {button_manifest.code.tsx[:100]}...")
        print(f"   Dependencies: {button_manifest.runtime_deps}")
    except Exception as e:
        print(f"❌ Error getting button component: {e}")
    
    try:
        card_manifest = await shadcn.get_component("card")
        print(f"✅ Card component found: {card_manifest.name}")
        print(f"   Has TSX code: {'✅ Yes' if card_manifest.code.tsx else '❌ No'}")
        if card_manifest.code.tsx:
            code_length = len(card_manifest.code.tsx)
            print(f"   Code length: {code_length} characters")
    except Exception as e:
        print(f"❌ Error getting card component: {e}")
    
    # Test MagicUI provider
    print("\n✨ Testing MagicUI Provider...")
    magicui = MagicUIProvider()
    
    try:
        magic_button_manifest = await magicui.get_component("magic-button")
        print(f"✅ Magic button component found: {magic_button_manifest.name}")
        print(f"   Has TSX code: {'✅ Yes' if magic_button_manifest.code.tsx else '❌ No'}")
        if magic_button_manifest.code.tsx:
            code_length = len(magic_button_manifest.code.tsx)
            print(f"   Code length: {code_length} characters")
            if code_length > 100:
                print(f"   Code preview: {magic_button_manifest.code.tsx[:100]}...")
        print(f"   Dependencies: {magic_button_manifest.runtime_deps}")
    except Exception as e:
        print(f"❌ Error getting magic-button component: {e}")
    
    try:
        marquee_manifest = await magicui.get_component("marquee")
        print(f"✅ Marquee component found: {marquee_manifest.name}")
        print(f"   Has TSX code: {'✅ Yes' if marquee_manifest.code.tsx else '❌ No'}")
        if marquee_manifest.code.tsx:
            code_length = len(marquee_manifest.code.tsx)
            print(f"   Code length: {code_length} characters")
    except Exception as e:
        print(f"❌ Error getting marquee component: {e}")
    
    print("\n🎯 Enhanced Component Template Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_components())