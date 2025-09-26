"""Test ingestion functionality."""

import asyncio
import json
from datetime import datetime

from mcp_ui_aggregator.core.database import async_session_maker, create_tables, drop_tables
from mcp_ui_aggregator.models.database import Component, CodeExample, DocumentationSection, ComponentType, Namespace


import pytest


@pytest.mark.asyncio
async def test_ingestion():
    """Test ingestion with sample data."""
    # Ensure a clean database state for this test run
    await drop_tables()
    await create_tables()
    
    # Sample components to test with
    sample_components = [
        {
            "name": "Button",
            "namespace": "material",
            "component_type": ComponentType.BUTTON.value,
            "title": "Material UI Button",
            "description": "A button component for user interactions",
            "tags": '["button", "material-ui", "react", "interactive"]',
            "documentation_url": "https://mui.com/material-ui/react-button/",
            "api_reference_url": "https://mui.com/material-ui/react-button/#api",
            "import_statement": "import Button from '@mui/material/Button';",
            "basic_usage": "<Button variant=\"contained\">Hello World</Button>",
        },
        {
            "name": "Card",
            "namespace": "shadcn",
            "component_type": ComponentType.CARD.value,
            "title": "shadcn/ui Card",
            "description": "A card component for displaying content in a container",
            "tags": '["card", "shadcn-ui", "react", "container"]',
            "documentation_url": "https://ui.shadcn.com/docs/components/card",
            "api_reference_url": "https://ui.shadcn.com/docs/components/card",
            "import_statement": "import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'",
            "basic_usage": "<Card>\n  <CardHeader>\n    <CardTitle>Card Title</CardTitle>\n  </CardHeader>\n  <CardContent>\n    <p>Card content goes here.</p>\n  </CardContent>\n</Card>",
        },
        {
            "name": "TextField",
            "namespace": "material",
            "component_type": ComponentType.INPUT.value,
            "title": "Material UI TextField",
            "description": "A text input component with various styles and validation",
            "tags": '["input", "textfield", "material-ui", "react", "form"]',
            "documentation_url": "https://mui.com/material-ui/react-text-field/",
            "api_reference_url": "https://mui.com/material-ui/react-text-field/#api",
            "import_statement": "import TextField from '@mui/material/TextField';",
            "basic_usage": "<TextField label=\"Enter text\" variant=\"outlined\" />",
        },
    ]
    
    async with async_session_maker() as session:
        components_created = 0
        
        for comp_data in sample_components:
            # Create component
            component = Component(**comp_data)
            session.add(component)
            await session.flush()
            
            # Add some code examples
            if comp_data["name"] == "Button":
                examples = [
                    CodeExample(
                        component_id=component.id,
                        title="Basic Button",
                        description="A simple button example",
                        code="<Button variant=\"contained\">Click me</Button>",
                        language="tsx",
                        framework="react",
                        is_basic=True,
                    ),
                    CodeExample(
                        component_id=component.id,
                        title="Button with Icon",
                        description="Button with an icon",
                        code="<Button variant=\"contained\" startIcon={<DeleteIcon />}>\n  Delete\n</Button>",
                        language="tsx",
                        framework="react",
                        is_basic=False,
                    ),
                ]
                for example in examples:
                    session.add(example)
            
            # Add some documentation
            docs = [
                DocumentationSection(
                    component_id=component.id,
                    title="API Reference",
                    content=f"The {comp_data['name']} component accepts the following props...",
                    section_type="api",
                    order_index=0,
                ),
                DocumentationSection(
                    component_id=component.id,
                    title="Usage Examples",
                    content=f"Here are some examples of how to use the {comp_data['name']} component...",
                    section_type="examples",
                    order_index=1,
                ),
            ]
            for doc in docs:
                session.add(doc)
            
            components_created += 1
            print(f"Created component: {comp_data['namespace']}/{comp_data['name']}")
        
        await session.commit()
        print(f"\nTest ingestion completed: {components_created} components created")


if __name__ == "__main__":
    asyncio.run(test_ingestion())