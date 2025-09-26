"""Template generation tools for MCP server."""

from typing import Dict, List, Any, Optional
from .predefined import get_template, list_templates, TEMPLATE_REGISTRY
from . import get_template_generator, Framework


def generate_template_code(template_id: str, customizations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate code for a specific template."""
    template = get_template(template_id)
    if not template:
        return {"error": f"Template '{template_id}' not found"}
    
    # Apply customizations if provided
    if customizations:
        template = _apply_customizations(template, customizations)
    
    # Get appropriate generator
    generator = get_template_generator(template.framework)
    
    # Generate code
    code = generator.generate_code(template)
    dependencies = generator.get_dependencies(template)
    
    return {
        "template_id": template_id,
        "template_name": template.name,
        "framework": template.framework.value,
        "code": code,
        "dependencies": dependencies,
        "file_extension": _get_file_extension(template.framework),
        "instructions": _get_setup_instructions(template)
    }


def preview_template_structure(template_id: str) -> Dict[str, Any]:
    """Get template structure preview without generating full code."""
    template = get_template(template_id)
    if not template:
        return {"error": f"Template '{template_id}' not found"}
    
    sections = []
    for section in template.sections:
        components = []
        for component in section.components:
            components.append({
                "name": component.name,
                "namespace": component.namespace,
                "props": component.props,
                "has_children": bool(component.children),
                "has_content": bool(component.content)
            })
        
        sections.append({
            "name": section.name,
            "description": section.description,
            "components": components,
            "css_classes": section.css_classes
        })
    
    return {
        "template_id": template_id,
        "name": template.name,
        "type": template.type.value,
        "framework": template.framework.value,
        "description": template.description,
        "sections": sections,
        "dependencies": template.dependencies,
        "global_styles": template.global_styles
    }


def customize_template(template_id: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Apply customizations to a template and return the modified version."""
    template = get_template(template_id)
    if not template:
        return {"error": f"Template '{template_id}' not found"}
    
    customized_template = _apply_customizations(template, customizations)
    
    return {
        "template_id": template_id,
        "customizations_applied": customizations,
        "preview": preview_template_structure(template_id)
    }


def get_template_variants() -> Dict[str, List[str]]:
    """Get all available template variants grouped by type."""
    variants = {}
    
    for template_id, template in TEMPLATE_REGISTRY.items():
        template_type = template.type.value
        if template_type not in variants:
            variants[template_type] = []
        
        variants[template_type].append({
            "id": template_id,
            "framework": template.framework.value,
            "name": template.name
        })
    
    return variants


def _apply_customizations(template, customizations: Dict[str, Any]):
    """Apply customizations to a template."""
    # Create a deep copy of the template
    import copy
    customized_template = copy.deepcopy(template)
    
    # Apply text customizations
    if "texts" in customizations:
        _apply_text_customizations(customized_template, customizations["texts"])
    
    # Apply style customizations
    if "styles" in customizations:
        _apply_style_customizations(customized_template, customizations["styles"])
    
    # Apply component customizations
    if "components" in customizations:
        _apply_component_customizations(customized_template, customizations["components"])
    
    return customized_template


def _apply_text_customizations(template, text_customizations: Dict[str, str]):
    """Apply text content customizations."""
    for section in template.sections:
        for component in section.components:
            _update_component_text(component, text_customizations)


def _update_component_text(component, text_customizations: Dict[str, str]):
    """Recursively update component text content."""
    # Update content if it matches a customization key
    if component.content:
        for key, new_text in text_customizations.items():
            if key.lower() in component.content.lower():
                component.content = new_text
                break
    
    # Update children recursively
    if component.children:
        for child in component.children:
            _update_component_text(child, text_customizations)


def _apply_style_customizations(template, style_customizations: Dict[str, str]):
    """Apply style customizations."""
    if not template.global_styles:
        template.global_styles = {}
    
    for selector, styles in style_customizations.items():
        if selector in template.global_styles:
            template.global_styles[selector] += f"; {styles}"
        else:
            template.global_styles[selector] = styles


def _apply_component_customizations(template, component_customizations: Dict[str, Dict[str, Any]]):
    """Apply component-specific customizations."""
    for section in template.sections:
        for component in section.components:
            _update_component_props(component, component_customizations)


def _update_component_props(component, component_customizations: Dict[str, Dict[str, Any]]):
    """Recursively update component props."""
    # Check if this component has customizations
    component_key = f"{component.namespace}_{component.name}"
    if component_key in component_customizations:
        custom_props = component_customizations[component_key]
        if not component.props:
            component.props = {}
        component.props.update(custom_props)
    
    # Update children recursively
    if component.children:
        for child in component.children:
            _update_component_props(child, component_customizations)


def _get_file_extension(framework: Framework) -> str:
    """Get appropriate file extension for framework."""
    extensions = {
        Framework.REACT: ".jsx",
        Framework.VUE: ".vue",
        Framework.ANGULAR: ".component.ts",
        Framework.SVELTE: ".svelte",
        Framework.HTML: ".html"
    }
    return extensions.get(framework, ".txt")


def _get_setup_instructions(template) -> List[str]:
    """Get setup instructions for the template."""
    instructions = []
    
    if template.framework == Framework.REACT:
        instructions.extend([
            "1. Create a new React component file with the generated code",
            "2. Install required dependencies: npm install " + " ".join(template.dependencies or []),
            "3. Import and use the component in your app",
            "4. Add any additional styling as needed"
        ])
    elif template.framework == Framework.VUE:
        instructions.extend([
            "1. Create a new Vue component file with the generated code",
            "2. Install required dependencies: npm install " + " ".join(template.dependencies or []),
            "3. Register and use the component in your app",
            "4. Configure any required Vue plugins"
        ])
    elif template.framework == Framework.HTML:
        instructions.extend([
            "1. Save the generated code as an HTML file",
            "2. Ensure all CDN links are included in the head section",
            "3. Open the file in a web browser",
            "4. Customize content and styling as needed"
        ])
    
    return instructions