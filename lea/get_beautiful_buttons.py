#!/usr/bin/env python3
"""Script to find the most beautiful button components from LEA UI aggregator."""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from mcp_ui_aggregator.providers.registry import get_all_providers
from mcp_ui_aggregator.models.component_manifest import Provider

async def get_beautiful_buttons():
    """Get the top 5 most beautiful button components."""
    
    print("🔍 Searching for beautiful button components...")
    print("=" * 60)
    
    beautiful_buttons = []
    
    # Get all providers
    providers = get_all_providers()
    
    for provider in providers:
        print(f"\n📦 Checking {provider.provider_name.value} provider...")
        
        try:
            # Get all components from this provider
            components = await provider.list_components(limit=100)
            
            # Filter for button components
            button_components = []
            for component in components:
                if any(keyword in component.name.lower() or 
                      keyword in component.description.lower() or
                      (hasattr(component, 'tags') and any(keyword in tag.lower() for tag in component.tags))
                      for keyword in ['button', 'btn']):
                    button_components.append(component)
            
            if button_components:
                print(f"   Found {len(button_components)} button components")
                for btn in button_components:
                    print(f"   - {btn.name}: {btn.description}")
                    beautiful_buttons.append({
                        'provider': provider.provider_name.value,
                        'component': btn,
                        'beauty_score': calculate_beauty_score(btn, provider.provider_name.value)
                    })
            else:
                print("   No button components found")
                
        except Exception as e:
            print(f"   Error loading components: {e}")
    
    # Sort by beauty score and get top 5
    beautiful_buttons.sort(key=lambda x: x['beauty_score'], reverse=True)
    top_5 = beautiful_buttons[:5]
    
    print("\n" + "=" * 60)
    print("🏆 TOP 5 MOST BEAUTIFUL BUTTON COMPONENTS")
    print("=" * 60)
    
    for i, btn_data in enumerate(top_5, 1):
        component = btn_data['component']
        provider = btn_data['provider']
        score = btn_data['beauty_score']
        
        print(f"\n{i}. {component.name} ({provider})")
        print(f"   Beauty Score: {score}/10")
        print(f"   Description: {component.description}")
        print(f"   Component ID: {provider.lower()}/{component.slug}")
        
        if hasattr(component, 'tags') and component.tags:
            print(f"   Tags: {', '.join(component.tags)}")
            
        # Try to get code preview
        try:
            code_data = await get_component_code_preview(component, provider)
            if code_data:
                print(f"   Preview: {code_data[:100]}...")
        except:
            pass
            
        print(f"   URL: https://lea-production.up.railway.app/components/{provider.lower()}/{component.slug}")

def calculate_beauty_score(component, provider_name):
    """Calculate a beauty score for a button component."""
    score = 5.0  # Base score
    
    # Provider-based scoring (some providers focus more on beautiful designs)
    provider_scores = {
        'magicui': 3.0,      # Known for magical animations
        'aceternity': 2.5,   # Modern animated components  
        'shadcn': 1.5,       # Clean, accessible design
        'tailwind_ui': 2.0,  # Professional designs
        'hyperui': 1.8,      # Good variety
        'daisyui': 1.2,      # Simple but effective
    }
    score += provider_scores.get(provider_name.lower(), 1.0)
    
    # Name-based scoring (cooler names often mean cooler components)
    name_lower = component.name.lower()
    if any(word in name_lower for word in ['magic', 'rainbow', 'neon', 'glow', 'animated', 'shimmer']):
        score += 2.0
    if any(word in name_lower for word in ['3d', 'gradient', 'glassmorphism', 'neumorphism']):
        score += 1.5
    if any(word in name_lower for word in ['hover', 'effect', 'transition']):
        score += 1.0
        
    # Description-based scoring
    desc_lower = component.description.lower()
    if any(word in desc_lower for word in ['animation', 'animated', 'effect', 'magic', 'beautiful']):
        score += 1.5
    if any(word in desc_lower for word in ['gradient', 'glow', 'shimmer', 'particle']):
        score += 1.0
    if any(word in desc_lower for word in ['hover', 'interactive', 'transition']):
        score += 0.5
        
    # Tags-based scoring
    if hasattr(component, 'tags') and component.tags:
        tag_text = ' '.join(component.tags).lower()
        if any(word in tag_text for word in ['magic', 'rainbow', 'animated', 'effect']):
            score += 1.0
            
    return min(score, 10.0)  # Cap at 10

async def get_component_code_preview(component, provider_name):
    """Get a preview of the component code."""
    try:
        # This is a simplified preview - in practice you'd call the provider's get_component method
        return f"// {component.name} component code preview"
    except:
        return None

if __name__ == "__main__":
    asyncio.run(get_beautiful_buttons())