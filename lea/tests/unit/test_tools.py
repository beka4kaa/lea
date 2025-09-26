"""Unit tests for component tools."""

import json
import pytest
from unittest.mock import patch, AsyncMock

from mcp_ui_aggregator.models.database import Component, ComponentType, Namespace
from mcp_ui_aggregator.tools.component_tools import (
    list_components, search_component, get_component_code,
    get_component_docs, install_component
)


@pytest.mark.asyncio
async def test_list_components_empty(test_session):
    """Test listing components when database is empty."""
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value = test_session
        
        result = await list_components()
        
        assert result["components"] == []
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["limit"] == 50
        assert result["pagination"]["offset"] == 0
        assert result["pagination"]["has_more"] is False


@pytest.mark.asyncio
async def test_list_components_with_data(test_session):
    """Test listing components with data."""
    # Create test components
    components = [
        Component(
            name="Button",
            namespace="material",
            component_type=ComponentType.BUTTON.value,
            title="Material UI Button",
            description="A button component",
            tags='["button", "material-ui"]',
            documentation_url="https://mui.com/button/",
        ),
        Component(
            name="Card",
            namespace="shadcn",
            component_type=ComponentType.CARD.value,
            title="shadcn/ui Card",
            description="A card component",
            tags='["card", "shadcn-ui"]',
        ),
    ]
    
    for comp in components:
        test_session.add(comp)
    await test_session.commit()
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value = test_session
        
        result = await list_components()
        
        assert len(result["components"]) == 2
        assert result["pagination"]["total"] == 2
        
        # Check component data
        button_comp = next(c for c in result["components"] if c["name"] == "Button")
        assert button_comp["namespace"] == "material"
        assert button_comp["component_type"] == "button"
        assert button_comp["tags"] == ["button", "material-ui"]


@pytest.mark.asyncio
async def test_list_components_with_filters(test_session):
    """Test listing components with namespace filter."""
    # Create test components in different namespaces
    components = [
        Component(
            name="Button",
            namespace="material",
            component_type=ComponentType.BUTTON.value,
            title="Material UI Button",
        ),
        Component(
            name="Button",
            namespace="shadcn",
            component_type=ComponentType.BUTTON.value,
            title="shadcn/ui Button",
        ),
    ]
    
    for comp in components:
        test_session.add(comp)
    await test_session.commit()
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value = test_session
        
        # Test namespace filter
        result = await list_components(namespace="material")
        
        assert len(result["components"]) == 1
        assert result["components"][0]["namespace"] == "material"
        assert result["components"][0]["title"] == "Material UI Button"


@pytest.mark.asyncio
async def test_search_component(test_session):
    """Test searching for components."""
    # Create test components
    components = [
        Component(
            name="Button",
            namespace="material",
            component_type=ComponentType.BUTTON.value,
            title="Material UI Button",
            description="A button component for user interactions",
            tags='["button", "material-ui", "interactive"]',
        ),
        Component(
            name="Card",
            namespace="shadcn",
            component_type=ComponentType.CARD.value,
            title="shadcn/ui Card",
            description="A card component for displaying content",
            tags='["card", "shadcn-ui", "container"]',
        ),
        Component(
            name="IconButton",
            namespace="material",
            component_type=ComponentType.BUTTON.value,
            title="Material UI Icon Button",
            description="A button component with icon support",
            tags='["button", "icon", "material-ui"]',
        ),
    ]
    
    for comp in components:
        test_session.add(comp)
    await test_session.commit()
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value = test_session
        
        # Test search by name
        result = await search_component("button")
        
        assert len(result["results"]) == 2  # Button and IconButton
        assert result["query"] == "button"
        
        # Check relevance scoring
        results = result["results"]
        button_result = next(r for r in results if r["name"] == "Button")
        icon_button_result = next(r for r in results if r["name"] == "IconButton")
        
        # Button should have higher relevance (exact name match)
        assert button_result["relevance_score"] > icon_button_result["relevance_score"]


@pytest.mark.asyncio
async def test_get_component_code_by_id(test_session):
    """Test getting component code by ID."""
    # Create test component
    component = Component(
        name="Button",
        namespace="material",
        component_type=ComponentType.BUTTON.value,
        title="Material UI Button",
        import_statement="import Button from '@mui/material/Button';",
        basic_usage="<Button>Click me</Button>",
    )
    test_session.add(component)
    await test_session.flush()
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value = test_session
        
        result = await get_component_code(component_id=component.id)
        
        assert "error" not in result
        assert result["component"]["name"] == "Button"
        assert result["component"]["namespace"] == "material"
        assert result["component"]["import_statement"] == "import Button from '@mui/material/Button';"
        assert result["component"]["basic_usage"] == "<Button>Click me</Button>"


@pytest.mark.asyncio
async def test_get_component_code_by_name(test_session):
    """Test getting component code by name and namespace."""
    # Create test component
    component = Component(
        name="Button",
        namespace="material",
        component_type=ComponentType.BUTTON.value,
        title="Material UI Button",
        import_statement="import Button from '@mui/material/Button';",
    )
    test_session.add(component)
    await test_session.commit()
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value = test_session
        
        result = await get_component_code(component_name="Button", namespace="material")
        
        assert "error" not in result
        assert result["component"]["name"] == "Button"
        assert result["component"]["namespace"] == "material"


@pytest.mark.asyncio
async def test_get_component_code_not_found():
    """Test getting component code for non-existent component."""
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        
        result = await get_component_code(component_id=999)
        
        assert "error" in result
        assert result["error"] == "Component not found"


@pytest.mark.asyncio
async def test_install_component_material():
    """Test installation instructions for Material UI component."""
    # Mock component
    component = Component(
        name="Button",
        namespace="material",
        component_type=ComponentType.BUTTON.value,
        title="Material UI Button",
        import_statement="import Button from '@mui/material/Button';",
        basic_usage="<Button>Click me</Button>",
    )
    component.id = 1
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = component
        
        result = await install_component("Button", "material", package_manager="npm")
        
        assert "error" not in result
        assert result["component"]["name"] == "Button"
        assert result["component"]["namespace"] == "material"
        
        installation = result["installation"]
        assert installation["package_manager"] == "npm"
        assert "@mui/material" in installation["install_command"]
        assert "npm install" in installation["install_command"]
        assert "@emotion/react" in installation["install_command"]


@pytest.mark.asyncio
async def test_install_component_shadcn():
    """Test installation instructions for shadcn/ui component."""
    # Mock component
    component = Component(
        name="Button",
        namespace="shadcn",
        component_type=ComponentType.BUTTON.value,
        title="shadcn/ui Button",
        import_statement='import { Button } from "@/components/ui/button"',
        basic_usage="<Button>Click me</Button>",
    )
    component.id = 1
    
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = component
        
        result = await install_component("Button", "shadcn")
        
        assert "error" not in result
        installation = result["installation"]
        assert "npx shadcn-ui@latest add button" in installation["install_command"]


@pytest.mark.asyncio
async def test_install_component_not_found():
    """Test installation for non-existent component."""
    with patch('mcp_ui_aggregator.tools.component_tools.async_session_maker') as mock_session:
        mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        
        result = await install_component("NonExistent", "material")
        
        assert "error" in result
        assert "Component material/NonExistent not found" in result["error"]