"""Template system for generating complete page layouts."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TemplateType(Enum):
    """Types of page templates."""
    LANDING = "landing"
    DASHBOARD = "dashboard"
    ECOMMERCE = "ecommerce"
    BLOG = "blog"
    PORTFOLIO = "portfolio"
    ADMIN = "admin"
    AUTH = "auth"


class Framework(Enum):
    """Supported frameworks for templates."""
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"
    HTML = "html"


@dataclass
class TemplateComponent:
    """A component used in a template."""
    name: str
    namespace: str
    props: Dict[str, Any]
    children: Optional[List['TemplateComponent']] = None
    content: Optional[str] = None


@dataclass
class PageSection:
    """A section of a page template."""
    name: str
    description: str
    components: List[TemplateComponent]
    layout_type: str = "default"  # flex, grid, stack, etc.
    css_classes: List[str] = None


@dataclass
class PageTemplate:
    """Complete page template definition."""
    name: str
    type: TemplateType
    framework: Framework
    description: str
    sections: List[PageSection]
    global_styles: Dict[str, str] = None
    dependencies: List[str] = None
    meta_tags: Dict[str, str] = None


class TemplateGenerator(ABC):
    """Base class for template generators."""
    
    @abstractmethod
    def generate_code(self, template: PageTemplate) -> str:
        """Generate complete code for the template."""
        pass
    
    @abstractmethod
    def get_dependencies(self, template: PageTemplate) -> List[str]:
        """Get list of required dependencies."""
        pass


class ReactTemplateGenerator(TemplateGenerator):
    """Generate React code from templates."""
    
    def generate_code(self, template: PageTemplate) -> str:
        """Generate React component code."""
        imports = self._generate_imports(template)
        component_code = self._generate_component(template)
        styles = self._generate_styles(template)
        
        return f"""{imports}

{styles}

{component_code}

export default {template.name};"""
    
    def get_dependencies(self, template: PageTemplate) -> List[str]:
        """Get required npm dependencies."""
        deps = ["react", "react-dom"]
        if template.dependencies:
            deps.extend(template.dependencies)
        return deps
    
    def _generate_imports(self, template: PageTemplate) -> str:
        """Generate import statements."""
        imports = ["import React from 'react';"]
        
        # Track unique namespaces
        namespaces = set()
        for section in template.sections:
            for component in section.components:
                namespaces.add(component.namespace)
        
        # Generate imports based on namespace
        for namespace in namespaces:
            if namespace == "material":
                imports.append("import { Button, Card, Typography } from '@mui/material';")
            elif namespace == "shadcn":
                imports.append("import { Button } from '@/components/ui/button';")
                imports.append("import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';")
            elif namespace == "chakra":
                imports.append("import { Button, Card, CardBody, CardHeader, Heading, Text } from '@chakra-ui/react';")
            # Add more namespace imports as needed
        
        return "\n".join(imports)
    
    def _generate_component(self, template: PageTemplate) -> str:
        """Generate React component."""
        sections_code = []
        
        for section in template.sections:
            section_code = self._generate_section(section)
            sections_code.append(section_code)
        
        return f"""const {template.name} = () => {{
  return (
    <div className="{template.name.lower()}-page">
{chr(10).join(['      ' + line for line in chr(10).join(sections_code).split(chr(10))])}
    </div>
  );
}};"""
    
    def _generate_section(self, section: PageSection) -> str:
        """Generate code for a page section."""
        components_code = []
        
        for component in section.components:
            component_code = self._generate_component_code(component)
            components_code.append(component_code)
        
        css_classes = " ".join(section.css_classes or [])
        
        return f"""<section className="{section.name.lower()}-section {css_classes}">
{chr(10).join(['  ' + line for line in chr(10).join(components_code).split(chr(10))])}
</section>"""
    
    def _generate_component_code(self, component: TemplateComponent) -> str:
        """Generate code for a single component."""
        props_str = ""
        if component.props:
            props_list = []
            for key, value in component.props.items():
                if isinstance(value, str):
                    props_list.append(f'{key}="{value}"')
                elif isinstance(value, bool):
                    props_list.append(f'{key}={str(value).lower()}')
                else:
                    props_list.append(f'{key}={{{value}}}')
            props_str = " " + " ".join(props_list)
        
        if component.content:
            return f"<{component.name}{props_str}>{component.content}</{component.name}>"
        elif component.children:
            children_code = []
            for child in component.children:
                children_code.append(self._generate_component_code(child))
            children_str = "\n".join(['  ' + line for line in "\n".join(children_code).split("\n")])
            return f"<{component.name}{props_str}>\n{children_str}\n</{component.name}>"
        else:
            return f"<{component.name}{props_str} />"
    
    def _generate_styles(self, template: PageTemplate) -> str:
        """Generate CSS styles."""
        if not template.global_styles:
            return ""
        
        styles = []
        for selector, rules in template.global_styles.items():
            styles.append(f"{selector} {{\n  {rules}\n}}")
        
        return f"""const styles = `
{chr(10).join(styles)}
`;

// Add styles to document
if (typeof document !== 'undefined') {{
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}}"""


class VueTemplateGenerator(TemplateGenerator):
    """Generate Vue.js code from templates."""
    
    def generate_code(self, template: PageTemplate) -> str:
        """Generate Vue component code."""
        template_code = self._generate_template(template)
        script_code = self._generate_script(template)
        style_code = self._generate_style(template)
        
        return f"""<template>
{template_code}
</template>

<script>
{script_code}
</script>

<style scoped>
{style_code}
</style>"""
    
    def get_dependencies(self, template: PageTemplate) -> List[str]:
        """Get required npm dependencies."""
        deps = ["vue"]
        if template.dependencies:
            deps.extend(template.dependencies)
        return deps
    
    def _generate_template(self, template: PageTemplate) -> str:
        """Generate Vue template."""
        sections_code = []
        
        for section in template.sections:
            section_code = self._generate_section(section)
            sections_code.append(section_code)
        
        return f"""  <div class="{template.name.lower()}-page">
{chr(10).join(['    ' + line for line in chr(10).join(sections_code).split(chr(10))])}
  </div>"""
    
    def _generate_section(self, section: PageSection) -> str:
        """Generate Vue section."""
        components_code = []
        
        for component in section.components:
            component_code = self._generate_component_code(component)
            components_code.append(component_code)
        
        css_classes = " ".join(section.css_classes or [])
        
        return f"""<section class="{section.name.lower()}-section {css_classes}">
{chr(10).join(['  ' + line for line in chr(10).join(components_code).split(chr(10))])}
</section>"""
    
    def _generate_component_code(self, component: TemplateComponent) -> str:
        """Generate Vue component code."""
        # Convert React-style props to Vue-style
        props_str = ""
        if component.props:
            props_list = []
            for key, value in component.props.items():
                if key == "onClick":
                    props_list.append(f'@click="{value}"')
                elif isinstance(value, str):
                    props_list.append(f'{key}="{value}"')
                elif isinstance(value, bool):
                    props_list.append(f':{key}="{str(value).lower()}"')
                else:
                    props_list.append(f':{key}="{value}"')
            props_str = " " + " ".join(props_list)
        
        # Map component names to Vue equivalents
        vue_name = self._map_component_name(component.name, component.namespace)
        
        if component.content:
            return f"<{vue_name}{props_str}>{component.content}</{vue_name}>"
        elif component.children:
            children_code = []
            for child in component.children:
                children_code.append(self._generate_component_code(child))
            children_str = "\n".join(['  ' + line for line in "\n".join(children_code).split("\n")])
            return f"<{vue_name}{props_str}>\n{children_str}\n</{vue_name}>"
        else:
            return f"<{vue_name}{props_str} />"
    
    def _map_component_name(self, name: str, namespace: str) -> str:
        """Map React component names to Vue equivalents."""
        if namespace == "vuetify":
            mapping = {
                "Button": "v-btn",
                "Card": "v-card",
                "Typography": "v-typography"
            }
            return mapping.get(name, name.lower())
        elif namespace == "quasar":
            mapping = {
                "Button": "q-btn",
                "Card": "q-card",
                "Typography": "q-typography"
            }
            return mapping.get(name, name.lower())
        return name.lower()
    
    def _generate_script(self, template: PageTemplate) -> str:
        """Generate Vue script section."""
        return f"""export default {{
  name: '{template.name}',
  data() {{
    return {{
      // Component data
    }};
  }},
  methods: {{
    // Component methods
  }}
}};"""
    
    def _generate_style(self, template: PageTemplate) -> str:
        """Generate Vue styles."""
        if not template.global_styles:
            return "/* Add your styles here */"
        
        styles = []
        for selector, rules in template.global_styles.items():
            styles.append(f"{selector} {{\n  {rules}\n}}")
        
        return "\n".join(styles)


class HTMLTemplateGenerator(TemplateGenerator):
    """Generate HTML code from templates."""
    
    def generate_code(self, template: PageTemplate) -> str:
        """Generate complete HTML page."""
        head = self._generate_head(template)
        body = self._generate_body(template)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
</head>
<body>
{body}
</body>
</html>"""
    
    def get_dependencies(self, template: PageTemplate) -> List[str]:
        """Get required CDN links."""
        deps = []
        if template.dependencies:
            deps.extend(template.dependencies)
        return deps
    
    def _generate_head(self, template: PageTemplate) -> str:
        """Generate HTML head section."""
        head_content = [
            '  <meta charset="UTF-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'  <title>{template.name}</title>'
        ]
        
        # Add meta tags
        if template.meta_tags:
            for name, content in template.meta_tags.items():
                head_content.append(f'  <meta name="{name}" content="{content}">')
        
        # Add framework-specific dependencies
        deps = self._get_framework_dependencies(template)
        head_content.extend(deps)
        
        # Add custom styles
        if template.global_styles:
            head_content.append('  <style>')
            for selector, rules in template.global_styles.items():
                head_content.append(f'    {selector} {{ {rules} }}')
            head_content.append('  </style>')
        
        return "\n".join(head_content)
    
    def _generate_body(self, template: PageTemplate) -> str:
        """Generate HTML body."""
        sections_code = []
        
        for section in template.sections:
            section_code = self._generate_section(section)
            sections_code.append(section_code)
        
        return f"""  <div class="{template.name.lower()}-page">
{chr(10).join(['    ' + line for line in chr(10).join(sections_code).split(chr(10))])}
  </div>"""
    
    def _generate_section(self, section: PageSection) -> str:
        """Generate HTML section."""
        components_code = []
        
        for component in section.components:
            component_code = self._generate_component_code(component)
            components_code.append(component_code)
        
        css_classes = " ".join(section.css_classes or [])
        
        return f"""<section class="{section.name.lower()}-section {css_classes}">
{chr(10).join(['  ' + line for line in chr(10).join(components_code).split(chr(10))])}
</section>"""
    
    def _generate_component_code(self, component: TemplateComponent) -> str:
        """Generate HTML component code."""
        # Map to HTML elements
        html_element = self._map_to_html(component.name, component.namespace)
        
        # Convert props to HTML attributes
        attrs = self._convert_props_to_attrs(component.props, component.namespace)
        attrs_str = " " + " ".join(attrs) if attrs else ""
        
        if component.content:
            return f"<{html_element}{attrs_str}>{component.content}</{html_element}>"
        elif component.children:
            children_code = []
            for child in component.children:
                children_code.append(self._generate_component_code(child))
            children_str = "\n".join(['  ' + line for line in "\n".join(children_code).split("\n")])
            return f"<{html_element}{attrs_str}>\n{children_str}\n</{html_element}>"
        else:
            return f"<{html_element}{attrs_str}></{html_element}>"
    
    def _map_to_html(self, component_name: str, namespace: str) -> str:
        """Map component names to HTML elements."""
        if namespace == "bootstrap":
            if component_name == "Button":
                return "button"
            elif component_name == "Card":
                return "div"
        elif namespace == "tailwind":
            if component_name == "Button":
                return "button"
            elif component_name == "Card":
                return "div"
        
        # Default mapping
        return {
            "Button": "button",
            "Card": "div",
            "Typography": "p",
            "Heading": "h1",
            "Text": "p"
        }.get(component_name, "div")
    
    def _convert_props_to_attrs(self, props: Dict[str, Any], namespace: str) -> List[str]:
        """Convert component props to HTML attributes."""
        if not props:
            return []
        
        attrs = []
        for key, value in props.items():
            if key == "variant" and namespace == "bootstrap":
                attrs.append(f'class="btn btn-{value}"')
            elif key == "className" or key == "class":
                attrs.append(f'class="{value}"')
            elif key == "onClick":
                attrs.append(f'onclick="{value}"')
            else:
                attrs.append(f'{key}="{value}"')
        
        return attrs
    
    def _get_framework_dependencies(self, template: PageTemplate) -> List[str]:
        """Get framework-specific CDN dependencies."""
        deps = []
        
        # Detect which frameworks are used
        namespaces = set()
        for section in template.sections:
            for component in section.components:
                namespaces.add(component.namespace)
        
        # Add appropriate CDN links
        if "bootstrap" in namespaces:
            deps.append('  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">')
            deps.append('  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>')
        
        if "tailwind" in namespaces:
            deps.append('  <script src="https://cdn.tailwindcss.com"></script>')
        
        if "bulma" in namespaces:
            deps.append('  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">')
        
        if "semantic-ui" in namespaces:
            deps.append('  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css">')
            deps.append('  <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js"></script>')
        
        return deps


def get_template_generator(framework: Framework) -> TemplateGenerator:
    """Get appropriate template generator for framework."""
    generators = {
        Framework.REACT: ReactTemplateGenerator(),
        Framework.VUE: VueTemplateGenerator(),
        Framework.HTML: HTMLTemplateGenerator(),
        # Framework.ANGULAR: AngularTemplateGenerator(),
        # Framework.SVELTE: SvelteTemplateGenerator(),
    }
    
    return generators.get(framework, HTMLTemplateGenerator())