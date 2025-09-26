"""Test template system functionality."""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_ui_aggregator.templates.tools import (
    list_templates,
    preview_template_structure,
    generate_template_code,
    get_template_variants
)


async def test_template_system():
    """Test the template system functionality."""
    print("Testing Template System")
    print("=" * 50)
    
    # Test 1: List all templates
    print("\n1. Testing template variants...")
    variants = get_template_variants()
    print(f"Found {len(variants)} template categories:")
    for category, templates in variants.items():
        print(f"  {category}: {len(templates)} templates")
        for template in templates[:2]:  # Show first 2
            print(f"    - {template['id']} ({template['framework']})")
    
    # Test 2: Get template structure
    print("\n2. Testing template structure preview...")
    structure = preview_template_structure("landing_react")
    if "error" not in structure:
        print(f"Template: {structure['name']}")
        print(f"Framework: {structure['framework']}")
        print(f"Sections: {len(structure['sections'])}")
        for section in structure['sections'][:2]:
            print(f"  - {section['name']}: {len(section['components'])} components")
    else:
        print(f"Error: {structure['error']}")
    
    # Test 3: Generate template code
    print("\n3. Testing code generation...")
    code_result = generate_template_code("landing_react")
    if "error" not in code_result:
        print(f"Generated code for: {code_result['template_name']}")
        print(f"Framework: {code_result['framework']}")
        print(f"File extension: {code_result['file_extension']}")
        print(f"Dependencies: {code_result.get('dependencies', [])}")
        print(f"Code length: {len(code_result['code'])} characters")
        print(f"Setup steps: {len(code_result['instructions'])}")
    else:
        print(f"Error: {code_result['error']}")
    
    # Test 4: Generate with customizations
    print("\n4. Testing customizations...")
    customizations = {
        "texts": {
            "Revolutionary": "Amazing",
            "Experience": "Journey"
        },
        "styles": {
            ".hero": "background: linear-gradient(45deg, #ff6b6b, #4ecdc4)"
        }
    }
    
    custom_result = generate_template_code("landing_react", customizations)
    if "error" not in custom_result:
        print("Customizations applied successfully")
        print(f"Customized code length: {len(custom_result['code'])} characters")
    else:
        print(f"Error: {custom_result['error']}")
    
    print("\n" + "=" * 50)
    print("Template system test completed!")


if __name__ == "__main__":
    asyncio.run(test_template_system())