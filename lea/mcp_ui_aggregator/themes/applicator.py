"""Theme application system for components and templates."""

import re
from typing import Dict, List, Any, Optional
from mcp_ui_aggregator.themes import Theme, theme_registry
from mcp_ui_aggregator.templates import PageTemplate, Framework


class ThemeApplicator:
    """Applies themes to components and templates."""
    
    def __init__(self):
        self.framework_mappings = {
            Framework.REACT: {
                'style_property': 'style',
                'class_property': 'className',
                'css_in_js': True
            },
            Framework.VUE: {
                'style_property': 'style',
                'class_property': 'class',
                'css_in_js': False
            },
            Framework.HTML: {
                'style_property': 'style',
                'class_property': 'class',
                'css_in_js': False
            }
        }
    
    def apply_theme_to_template(
        self, 
        template: PageTemplate, 
        theme: Theme,
        include_css_variables: bool = True
    ) -> PageTemplate:
        """Apply theme to a page template."""
        
        # Create a copy of the template
        import copy
        themed_template = copy.deepcopy(template)
        
        # Generate theme CSS
        theme_css = self._generate_theme_css(theme, template.framework)
        
        # Apply theme to global styles
        if themed_template.global_styles is None:
            themed_template.global_styles = {}
        
        themed_template.global_styles.update(theme_css)
        
        # Apply theme to sections and components
        for section in themed_template.sections:
            self._apply_theme_to_section(section, theme, template.framework)
        
        # Add theme metadata
        themed_template.dependencies = themed_template.dependencies or []
        if include_css_variables and template.framework != Framework.HTML:
            themed_template.dependencies.append(f"/* Theme: {theme.name} */")
        
        return themed_template
    
    def _generate_theme_css(self, theme: Theme, framework: Framework) -> Dict[str, str]:
        """Generate CSS for the theme."""
        
        css_rules = {}
        
        # CSS Custom Properties (CSS Variables)
        css_variables = self._generate_css_variables(theme)
        css_rules[':root'] = css_variables
        
        # Body styles
        body_styles = f"""
            font-family: {theme.typography.font_family_primary};
            font-size: {theme.typography.font_size_base};
            line-height: {theme.typography.line_height_base};
            color: {theme.colors.text_primary};
            background-color: {theme.colors.background};
            margin: 0;
            padding: 0;
        """.strip()
        css_rules['body'] = body_styles
        
        # Common utility classes
        utility_classes = self._generate_utility_classes(theme)
        css_rules.update(utility_classes)
        
        # Framework-specific adjustments
        if framework == Framework.REACT:
            # React-specific styles
            css_rules['#root'] = f"background-color: {theme.colors.background};"
            
        elif framework == Framework.VUE:
            # Vue-specific styles
            css_rules['#app'] = f"background-color: {theme.colors.background};"
            
        return css_rules
    
    def _generate_css_variables(self, theme: Theme) -> str:
        """Generate CSS custom properties for the theme."""
        
        variables = []
        
        # Colors
        variables.extend([
            f"--color-primary: {theme.colors.primary};",
            f"--color-secondary: {theme.colors.secondary};",
            f"--color-accent: {theme.colors.accent};",
            f"--color-background: {theme.colors.background};",
            f"--color-surface: {theme.colors.surface};",
            f"--color-text-primary: {theme.colors.text_primary};",
            f"--color-text-secondary: {theme.colors.text_secondary};",
            f"--color-success: {theme.colors.success};",
            f"--color-warning: {theme.colors.warning};",
            f"--color-error: {theme.colors.error};",
            f"--color-info: {theme.colors.info};"
        ])
        
        # Typography
        variables.extend([
            f"--font-family-primary: {theme.typography.font_family_primary};",
            f"--font-family-secondary: {theme.typography.font_family_secondary};",
            f"--font-size-base: {theme.typography.font_size_base};",
            f"--font-size-small: {theme.typography.font_size_small};",
            f"--font-size-large: {theme.typography.font_size_large};",
            f"--font-weight-normal: {theme.typography.font_weight_normal};",
            f"--font-weight-bold: {theme.typography.font_weight_bold};",
            f"--line-height-base: {theme.typography.line_height_base};"
        ])
        
        # Spacing
        variables.extend([
            f"--spacing-xs: {theme.spacing.xs};",
            f"--spacing-sm: {theme.spacing.sm};",
            f"--spacing-md: {theme.spacing.md};",
            f"--spacing-lg: {theme.spacing.lg};",
            f"--spacing-xl: {theme.spacing.xl};",
            f"--spacing-xxl: {theme.spacing.xxl};"
        ])
        
        # Border radius
        variables.extend([
            f"--border-radius-none: {theme.border_radius.none};",
            f"--border-radius-sm: {theme.border_radius.sm};",
            f"--border-radius-md: {theme.border_radius.md};",
            f"--border-radius-lg: {theme.border_radius.lg};",
            f"--border-radius-xl: {theme.border_radius.xl};",
            f"--border-radius-full: {theme.border_radius.full};"
        ])
        
        # Shadows
        for name, shadow in theme.shadows.items():
            variables.append(f"--shadow-{name}: {shadow};")
        
        # Breakpoints
        for name, breakpoint in theme.breakpoints.items():
            variables.append(f"--breakpoint-{name}: {breakpoint};")
        
        return "\n            ".join(variables)
    
    def _generate_utility_classes(self, theme: Theme) -> Dict[str, str]:
        """Generate utility CSS classes for the theme."""
        
        utilities = {}
        
        # Color utilities
        utilities['.text-primary'] = f"color: {theme.colors.text_primary};"
        utilities['.text-secondary'] = f"color: {theme.colors.text_secondary};"
        utilities['.text-accent'] = f"color: {theme.colors.accent};"
        utilities['.bg-primary'] = f"background-color: {theme.colors.primary};"
        utilities['.bg-secondary'] = f"background-color: {theme.colors.secondary};"
        utilities['.bg-surface'] = f"background-color: {theme.colors.surface};"
        utilities['.bg-accent'] = f"background-color: {theme.colors.accent};"
        
        # Status colors
        utilities['.text-success'] = f"color: {theme.colors.success};"
        utilities['.text-warning'] = f"color: {theme.colors.warning};"
        utilities['.text-error'] = f"color: {theme.colors.error};"
        utilities['.text-info'] = f"color: {theme.colors.info};"
        utilities['.bg-success'] = f"background-color: {theme.colors.success};"
        utilities['.bg-warning'] = f"background-color: {theme.colors.warning};"
        utilities['.bg-error'] = f"background-color: {theme.colors.error};"
        utilities['.bg-info'] = f"background-color: {theme.colors.info};"
        
        # Spacing utilities
        spacing_map = {
            'xs': theme.spacing.xs,
            'sm': theme.spacing.sm,
            'md': theme.spacing.md,
            'lg': theme.spacing.lg,
            'xl': theme.spacing.xl,
            'xxl': theme.spacing.xxl
        }
        
        for size, value in spacing_map.items():
            utilities[f'.p-{size}'] = f"padding: {value};"
            utilities[f'.m-{size}'] = f"margin: {value};"
            utilities[f'.px-{size}'] = f"padding-left: {value}; padding-right: {value};"
            utilities[f'.py-{size}'] = f"padding-top: {value}; padding-bottom: {value};"
            utilities[f'.mx-{size}'] = f"margin-left: {value}; margin-right: {value};"
            utilities[f'.my-{size}'] = f"margin-top: {value}; margin-bottom: {value};"
        
        # Border radius utilities
        radius_map = {
            'none': theme.border_radius.none,
            'sm': theme.border_radius.sm,
            'md': theme.border_radius.md,
            'lg': theme.border_radius.lg,
            'xl': theme.border_radius.xl,
            'full': theme.border_radius.full
        }
        
        for size, value in radius_map.items():
            utilities[f'.rounded-{size}'] = f"border-radius: {value};"
        
        # Shadow utilities
        for name, shadow in theme.shadows.items():
            utilities[f'.shadow-{name}'] = f"box-shadow: {shadow};"
        
        # Typography utilities
        utilities['.font-primary'] = f"font-family: {theme.typography.font_family_primary};"
        utilities['.font-secondary'] = f"font-family: {theme.typography.font_family_secondary};"
        utilities['.text-base'] = f"font-size: {theme.typography.font_size_base};"
        utilities['.text-sm'] = f"font-size: {theme.typography.font_size_small};"
        utilities['.text-lg'] = f"font-size: {theme.typography.font_size_large};"
        utilities['.font-normal'] = f"font-weight: {theme.typography.font_weight_normal};"
        utilities['.font-bold'] = f"font-weight: {theme.typography.font_weight_bold};"
        
        return utilities
    
    def _apply_theme_to_section(self, section, theme: Theme, framework: Framework):
        """Apply theme to a template section."""
        
        # Apply theme classes to section
        if not section.css_classes:
            section.css_classes = []
        
        # Add theme-appropriate classes
        section.css_classes.extend(['bg-surface', 'text-primary'])
        
        # Apply theme to components in section
        for component in section.components:
            self._apply_theme_to_component(component, theme, framework)
    
    def _apply_theme_to_component(self, component, theme: Theme, framework: Framework):
        """Apply theme to a component."""
        
        if not component.props:
            component.props = {}
        
        # Apply theme based on component type
        component_name = component.name.lower()
        
        if 'button' in component_name:
            self._apply_button_theme(component, theme, framework)
        elif 'card' in component_name:
            self._apply_card_theme(component, theme, framework)
        elif 'input' in component_name or 'textfield' in component_name:
            self._apply_input_theme(component, theme, framework)
        elif 'text' in component_name or 'typography' in component_name:
            self._apply_text_theme(component, theme, framework)
        
        # Apply theme to child components
        if component.children:
            for child in component.children:
                self._apply_theme_to_component(child, theme, framework)
    
    def _apply_button_theme(self, component, theme: Theme, framework: Framework):
        """Apply theme to button components."""
        
        if framework == Framework.REACT:
            component.props['sx'] = {
                'backgroundColor': theme.colors.primary,
                'color': 'white',
                'borderRadius': theme.border_radius.md,
                'padding': f"{theme.spacing.sm} {theme.spacing.lg}",
                'fontFamily': theme.typography.font_family_primary,
                'fontWeight': theme.typography.font_weight_bold,
                'boxShadow': theme.shadows.get('md', 'none'),
                '&:hover': {
                    'backgroundColor': theme.colors.accent,
                    'boxShadow': theme.shadows.get('lg', 'none')
                }
            }
        else:
            # For Vue and HTML, use classes
            component.props['class'] = 'bg-primary text-white rounded-md px-lg py-sm font-bold shadow-md hover:bg-accent hover:shadow-lg'
    
    def _apply_card_theme(self, component, theme: Theme, framework: Framework):
        """Apply theme to card components."""
        
        if framework == Framework.REACT:
            component.props['sx'] = {
                'backgroundColor': theme.colors.surface,
                'borderRadius': theme.border_radius.lg,
                'padding': theme.spacing.lg,
                'boxShadow': theme.shadows.get('md', 'none'),
                'border': f"1px solid {theme.colors.text_secondary}20"
            }
        else:
            component.props['class'] = 'bg-surface rounded-lg p-lg shadow-md border border-gray-200'
    
    def _apply_input_theme(self, component, theme: Theme, framework: Framework):
        """Apply theme to input components."""
        
        if framework == Framework.REACT:
            component.props['sx'] = {
                'backgroundColor': theme.colors.background,
                'borderRadius': theme.border_radius.md,
                'padding': f"{theme.spacing.sm} {theme.spacing.md}",
                'border': f"1px solid {theme.colors.text_secondary}40",
                'fontFamily': theme.typography.font_family_primary,
                '&:focus': {
                    'borderColor': theme.colors.primary,
                    'boxShadow': f"0 0 0 2px {theme.colors.primary}20"
                }
            }
        else:
            component.props['class'] = 'bg-background rounded-md p-sm border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary focus:ring-opacity-20'
    
    def _apply_text_theme(self, component, theme: Theme, framework: Framework):
        """Apply theme to text components."""
        
        if framework == Framework.REACT:
            component.props['sx'] = {
                'fontFamily': theme.typography.font_family_primary,
                'fontSize': theme.typography.font_size_base,
                'lineHeight': theme.typography.line_height_base,
                'color': theme.colors.text_primary
            }
        else:
            component.props['class'] = 'font-primary text-base text-primary'
    
    def get_theme_suggestions(self, project_type: str, industry: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get theme suggestions based on project context."""
        
        suggestions = []
        
        # Project type based suggestions
        if project_type == 'corporate' or project_type == 'business':
            suggestions.extend([
                {'theme_id': 'corporate', 'reason': 'Professional appearance for business'},
                {'theme_id': 'dark_professional', 'reason': 'Modern professional look'},
                {'theme_id': 'minimal', 'reason': 'Clean and trustworthy design'}
            ])
        elif project_type == 'creative' or project_type == 'portfolio':
            suggestions.extend([
                {'theme_id': 'vibrant_creative', 'reason': 'Bold colors for creative expression'},
                {'theme_id': 'modern_light', 'reason': 'Clean modern aesthetic'},
                {'theme_id': 'minimal', 'reason': 'Focus on content over decoration'}
            ])
        elif project_type == 'tech' or project_type == 'saas':
            suggestions.extend([
                {'theme_id': 'modern_light', 'reason': 'Modern tech aesthetic'},
                {'theme_id': 'dark_professional', 'reason': 'Developer-friendly dark mode'},
                {'theme_id': 'minimal', 'reason': 'Clean and functional design'}
            ])
        else:
            # Default suggestions
            suggestions.extend([
                {'theme_id': 'modern_light', 'reason': 'Versatile and widely appealing'},
                {'theme_id': 'minimal', 'reason': 'Clean and professional'},
                {'theme_id': 'corporate', 'reason': 'Traditional business appeal'}
            ])
        
        # Industry specific adjustments
        if industry:
            if industry.lower() in ['finance', 'legal', 'government']:
                # Move corporate and minimal to front
                suggestions = [s for s in suggestions if s['theme_id'] in ['corporate', 'minimal']] + \
                             [s for s in suggestions if s['theme_id'] not in ['corporate', 'minimal']]
            elif industry.lower() in ['design', 'art', 'media']:
                # Prioritize creative themes
                suggestions = [s for s in suggestions if 'creative' in s['theme_id'] or 'vibrant' in s['theme_id']] + \
                             [s for s in suggestions if 'creative' not in s['theme_id'] and 'vibrant' not in s['theme_id']]
        
        # Add theme details
        for suggestion in suggestions:
            theme = theme_registry.get_theme(suggestion['theme_id'])
            if theme:
                suggestion.update({
                    'name': theme.name,
                    'description': theme.description,
                    'category': theme.category.value,
                    'primary_color': theme.colors.primary,
                    'preview_colors': [
                        theme.colors.primary,
                        theme.colors.secondary,
                        theme.colors.accent
                    ]
                })
        
        return suggestions[:5]  # Return top 5 suggestions


# Global theme applicator
theme_applicator = ThemeApplicator()