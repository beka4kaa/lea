"""Test AI-enhanced functionality."""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_ui_aggregator.tools.component_tools import (
    ai_search_components,
    suggest_component_combinations,
    ai_suggest_templates,
    analyze_generated_code
)


async def test_ai_features():
    """Test the AI-enhanced features."""
    print("Testing AI-Enhanced Features")
    print("=" * 50)
    
    # Test 1: AI semantic search
    print("\n1. Testing AI semantic search...")
    search_result = await ai_search_components(
        query="form input components for user registration",
        limit=5,
        include_suggestions=True
    )
    
    if search_result["status"] == "success":
        print(f"✓ Found {len(search_result['search_results'])} search results")
        print(f"✓ Generated {len(search_result['ai_recommendations'])} AI recommendations")
        print(f"✓ Search suggestions: {len(search_result['search_suggestions'])}")
        
        if search_result['search_results']:
            top_result = search_result['search_results'][0]
            print(f"  Top result: {top_result['name']} (relevance: {top_result['relevance_score']:.2f})")
    else:
        print(f"✗ Error: {search_result['error']}")
    
    # Test 2: Component combinations
    print("\n2. Testing component combination suggestions...")
    combo_result = await suggest_component_combinations(
        selected_components=["button", "input"],
        project_type="landing",
        limit=5
    )
    
    if combo_result["status"] == "success":
        print(f"✓ Generated {len(combo_result['suggestions'])} combination suggestions")
        if combo_result['suggestions']:
            top_suggestion = combo_result['suggestions'][0]
            print(f"  Top suggestion: {top_suggestion['name']} (confidence: {top_suggestion['confidence']:.2f})")
            print(f"  Reason: {top_suggestion['reason']}")
    else:
        print(f"✗ Error: {combo_result['error']}")
    
    # Test 3: AI template suggestions
    print("\n3. Testing AI template suggestions...")
    template_result = await ai_suggest_templates(
        query="I need a modern landing page for a tech startup",
        framework="react",
        project_context={"industry": "tech", "timeline": "quick"},
        limit=3
    )
    
    if template_result["status"] == "success":
        print(f"✓ Generated {len(template_result['suggestions'])} template suggestions")
        if template_result['suggestions']:
            top_template = template_result['suggestions'][0]
            print(f"  Top suggestion: {top_template['template_name']} ({top_template['framework']})")
            print(f"  Confidence: {top_template['confidence']:.2f}")
            print(f"  Reason: {top_template['reason']}")
            print(f"  Estimated time: {top_template['estimated_time']}")
    else:
        print(f"✗ Error: {template_result['error']}")
    
    # Test 4: Code analysis
    print("\n4. Testing code analysis...")
    sample_code = """
import React from 'react';

function MyComponent() {
    const items = [1, 2, 3];
    
    return (
        <div>
            <h1>Hello World</h1>
            {items.map(item => <div>{item}</div>)}
        </div>
    );
}

export default MyComponent;
"""
    
    analysis_result = await analyze_generated_code(
        code=sample_code,
        framework="react",
        target_quality="good"
    )
    
    if analysis_result["status"] == "success":
        analysis = analysis_result["analysis"]
        print(f"✓ Code quality score: {analysis['quality_score']:.1f}/100")
        print(f"✓ Quality level: {analysis['quality_level']}")
        print(f"✓ Found {len(analysis_result['suggestions'])} suggestions")
        print(f"✓ Generated {len(analysis_result['improvements'])} improvements")
        
        if analysis_result['suggestions']:
            print(f"  Key suggestion: {analysis_result['suggestions'][0]['description']}")
    else:
        print(f"✗ Error: {analysis_result['error']}")
    
    print("\n" + "=" * 50)
    print("AI features test completed!")


if __name__ == "__main__":
    asyncio.run(test_ai_features())