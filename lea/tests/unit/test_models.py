"""Unit tests for database models."""

import json
import pytest
from datetime import datetime

from mcp_ui_aggregator.models.database import (
    Component, CodeExample, DocumentationSection, IngestionLog,
    ComponentType, Namespace
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload


@pytest.mark.asyncio
async def test_component_creation(test_session):
    """Test creating a component."""
    component = Component(
        name="Button",
        namespace="material",
        component_type=ComponentType.BUTTON.value,
        title="Material UI Button",
        description="A button component for user interactions",
        tags='["button", "material-ui", "react"]',
        documentation_url="https://mui.com/material-ui/react-button/",
        import_statement="import Button from '@mui/material/Button';",
        basic_usage="<Button>Click me</Button>",
    )
    
    test_session.add(component)
    await test_session.commit()
    
    assert component.id is not None
    assert component.name == "Button"
    assert component.namespace == "material"
    assert component.component_type == ComponentType.BUTTON.value
    assert component.is_active is True


@pytest.mark.asyncio
async def test_component_with_examples(test_session):
    """Test creating a component with code examples."""
    component = Component(
        name="Card",
        namespace="shadcn",
        component_type=ComponentType.CARD.value,
        title="shadcn/ui Card",
        description="A card component for displaying content",
        tags='["card", "shadcn-ui", "react"]',
    )
    
    test_session.add(component)
    await test_session.flush()
    
    # Add code example
    example = CodeExample(
        component_id=component.id,
        title="Basic Card",
        description="A simple card example",
        code="<Card>\n  <CardHeader>\n    <CardTitle>Title</CardTitle>\n  </CardHeader>\n</Card>",
        language="tsx",
        framework="react",
        is_basic=True,
    )
    
    test_session.add(example)
    await test_session.commit()
    
    # Reload with eager-loaded relationship to avoid async lazy load
    res = await test_session.execute(
        select(Component).options(selectinload(Component.code_examples)).where(Component.id == component.id)
    )
    comp_loaded = res.scalar_one()
    assert len(comp_loaded.code_examples) == 1
    assert comp_loaded.code_examples[0].title == "Basic Card"
    assert comp_loaded.code_examples[0].is_basic is True


@pytest.mark.asyncio
async def test_component_with_docs(test_session):
    """Test creating a component with documentation sections."""
    component = Component(
        name="Input",
        namespace="material",
        component_type=ComponentType.INPUT.value,
        title="Material UI TextField",
        description="A text input component",
    )
    
    test_session.add(component)
    await test_session.flush()
    
    # Add documentation section
    docs = DocumentationSection(
        component_id=component.id,
        title="API Reference",
        content="The TextField component accepts the following props...",
        section_type="api",
        order_index=0,
    )
    
    test_session.add(docs)
    await test_session.commit()
    
    res = await test_session.execute(
        select(Component).options(selectinload(Component.docs_sections)).where(Component.id == component.id)
    )
    comp_loaded = res.scalar_one()
    assert len(comp_loaded.docs_sections) == 1
    assert comp_loaded.docs_sections[0].title == "API Reference"
    assert comp_loaded.docs_sections[0].section_type == "api"


@pytest.mark.asyncio
async def test_ingestion_log(test_session):
    """Test creating an ingestion log."""
    log = IngestionLog(
        namespace="material",
        source_url="https://mui.com/material-ui/",
        status="completed",
        components_processed=50,
        components_created=45,
        components_updated=5,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )
    
    test_session.add(log)
    await test_session.commit()
    
    assert log.id is not None
    assert log.namespace == "material"
    assert log.status == "completed"
    assert log.components_processed == 50


@pytest.mark.asyncio
async def test_component_uniqueness_constraint(test_session):
    """Test that components are unique by name and namespace."""
    # Create first component
    component1 = Component(
        name="Button",
        namespace="material",
        component_type=ComponentType.BUTTON.value,
        title="Material UI Button",
    )
    test_session.add(component1)
    await test_session.commit()
    
    # Try to create duplicate
    component2 = Component(
        name="Button",
        namespace="material",  # Same namespace
        component_type=ComponentType.BUTTON.value,
        title="Another Button",
    )
    test_session.add(component2)
    
    # This should raise an integrity error
    with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
        await test_session.commit()


def test_component_type_enum():
    """Test component type enumeration."""
    assert ComponentType.BUTTON.value == "button"
    assert ComponentType.INPUT.value == "input"
    assert ComponentType.CARD.value == "card"
    
    # Test all enum values
    expected_types = {
        "button", "input", "card", "modal", "navigation", 
        "layout", "data_display", "feedback", "form", "other"
    }
    actual_types = {ct.value for ct in ComponentType}
    assert actual_types == expected_types


def test_namespace_enum():
    """Test namespace enumeration."""
    assert Namespace.MATERIAL.value == "material"
    assert Namespace.SHADCN.value == "shadcn"
    
    # Test all enum values
    expected_namespaces = {"material", "shadcn", "chakra", "antd", "mantine"}
    actual_namespaces = {ns.value for ns in Namespace}
    assert actual_namespaces == expected_namespaces