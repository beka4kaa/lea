"""Component recommendation engine for intelligent suggestions."""

import json
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter

from mcp_ui_aggregator.models.database import Component


@dataclass
class ComponentRecommendation:
    """Represents a component recommendation with reasoning."""
    component: Component
    confidence: float
    reason: str
    category: str
    complementary_components: List[str]


class ComponentRecommendationEngine:
    """AI-powered component recommendation system."""
    
    def __init__(self):
        # Component relationship mapping
        self.component_relationships = {
            # Form components work together
            'form': ['input', 'button', 'select', 'checkbox', 'radio', 'textarea'],
            'input': ['button', 'form', 'label'],
            'button': ['form', 'modal', 'dialog'],
            'select': ['form', 'input'],
            'checkbox': ['form', 'list'],
            'radio': ['form'],
            'textarea': ['form'],
            
            # Navigation components
            'navbar': ['menu', 'breadcrumb', 'avatar', 'button'],
            'menu': ['navbar', 'dropdown', 'list'],
            'breadcrumb': ['navbar', 'link'],
            'sidebar': ['menu', 'list', 'avatar'],
            
            # Data display
            'table': ['pagination', 'search', 'filter', 'button'],
            'list': ['avatar', 'badge', 'button', 'checkbox'],
            'card': ['image', 'button', 'badge', 'avatar'],
            'grid': ['card', 'image'],
            
            # Feedback
            'modal': ['button', 'form', 'card'],
            'dialog': ['button', 'form'],
            'alert': ['button', 'icon'],
            'notification': ['button', 'icon'],
            'snackbar': ['button', 'icon'],
            
            # Layout
            'container': ['grid', 'card', 'list'],
            'grid': ['card', 'image', 'button'],
            'stack': ['card', 'button', 'text'],
            'spacer': ['container', 'grid'],
            
            # Media
            'image': ['card', 'avatar', 'grid'],
            'avatar': ['menu', 'navbar', 'list', 'card'],
            'icon': ['button', 'alert', 'notification'],
            
            # Typography
            'heading': ['text', 'card'],
            'text': ['card', 'list'],
            'link': ['breadcrumb', 'menu', 'text']
        }
        
        # Component categories for better organization
        self.component_categories = {
            'input': ['input', 'textarea', 'select', 'checkbox', 'radio', 'switch', 'slider'],
            'button': ['button', 'fab', 'icon-button', 'toggle'],
            'navigation': ['navbar', 'menu', 'breadcrumb', 'tabs', 'stepper', 'pagination'],
            'feedback': ['alert', 'snackbar', 'dialog', 'modal', 'progress', 'skeleton'],
            'data-display': ['table', 'list', 'card', 'chip', 'badge', 'avatar', 'tooltip'],
            'layout': ['container', 'grid', 'stack', 'divider', 'spacer'],
            'surface': ['paper', 'card', 'accordion'],
            'typography': ['heading', 'text', 'link'],
            'media': ['image', 'video', 'icon']
        }
        
        # Usage patterns for different page types
        self.page_patterns = {
            'landing': {
                'hero': ['heading', 'text', 'button', 'image'],
                'features': ['card', 'grid', 'icon', 'heading', 'text'],
                'cta': ['button', 'form', 'input'],
                'footer': ['link', 'text', 'grid']
            },
            'dashboard': {
                'sidebar': ['menu', 'list', 'avatar', 'divider'],
                'header': ['navbar', 'avatar', 'notification', 'search'],
                'content': ['card', 'table', 'chart', 'grid'],
                'widgets': ['card', 'progress', 'badge', 'button']
            },
            'ecommerce': {
                'product-grid': ['card', 'image', 'button', 'badge', 'rating'],
                'product-detail': ['image', 'button', 'select', 'radio', 'tab'],
                'cart': ['list', 'button', 'input', 'badge'],
                'checkout': ['form', 'input', 'button', 'stepper']
            },
            'blog': {
                'header': ['navbar', 'menu', 'search'],
                'content': ['heading', 'text', 'image', 'link'],
                'sidebar': ['list', 'card', 'badge'],
                'comments': ['form', 'input', 'button', 'avatar']
            }
        }

    def recommend_for_query(
        self, 
        query: str, 
        components: List[Component], 
        limit: int = 10
    ) -> List[ComponentRecommendation]:
        """Recommend components based on search query intent."""
        
        recommendations = []
        query_lower = query.lower()
        
        # Analyze query intent
        intent = self._analyze_query_intent(query_lower)
        
        # Get direct matches
        direct_matches = self._find_direct_matches(query_lower, components)
        for component in direct_matches[:3]:  # Top 3 direct matches
            recommendations.append(ComponentRecommendation(
                component=component,
                confidence=0.9,
                reason=f"Direct match for '{query}'",
                category="exact",
                complementary_components=self._get_complementary_components(component.name)
            ))
        
        # Get intent-based recommendations
        if intent['page_type']:
            intent_recs = self._recommend_for_page_type(intent['page_type'], components)
            recommendations.extend(intent_recs[:4])
            
        # Get component-type based recommendations
        if intent['component_types']:
            for comp_type in intent['component_types'][:2]:
                type_recs = self._recommend_for_component_type(comp_type, components)
                recommendations.extend(type_recs[:3])
        
        # Remove duplicates and limit
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec.component.id not in seen:
                seen.add(rec.component.id)
                unique_recs.append(rec)
                
        return unique_recs[:limit]

    def recommend_complementary(
        self, 
        selected_components: List[Component], 
        all_components: List[Component],
        limit: int = 8
    ) -> List[ComponentRecommendation]:
        """Recommend components that work well with already selected ones."""
        
        if not selected_components:
            return []
            
        recommendations = []
        selected_names = [comp.name.lower() for comp in selected_components if comp.name]
        
        # Get complementary components for each selected component
        complementary_names = set()
        for component in selected_components:
            if component.name:
                comp_name = component.name.lower()
                complements = self._get_complementary_components(comp_name)
                complementary_names.update(complements)
        
        # Remove already selected components
        complementary_names -= set(selected_names)
        
        # Find matching components
        for comp_name in complementary_names:
            matching_components = [
                comp for comp in all_components 
                if comp.name and comp_name in comp.name.lower()
            ]
            
            for component in matching_components[:2]:  # Top 2 per complement
                confidence = self._calculate_complement_confidence(
                    component, selected_components
                )
                
                recommendations.append(ComponentRecommendation(
                    component=component,
                    confidence=confidence,
                    reason=f"Complements {', '.join(selected_names)}",
                    category="complementary",
                    complementary_components=self._get_complementary_components(component.name)
                ))
        
        # Sort by confidence and limit
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return recommendations[:limit]

    def recommend_for_framework(
        self, 
        framework: str, 
        components: List[Component],
        use_case: Optional[str] = None,
        limit: int = 12
    ) -> List[ComponentRecommendation]:
        """Recommend best components for a specific framework."""
        
        framework_components = [
            comp for comp in components 
            if comp.namespace == framework
        ]
        
        if not framework_components:
            return []
        
        # Framework-specific priorities
        framework_priorities = {
            'material': ['button', 'card', 'input', 'table', 'menu'],
            'shadcn': ['button', 'card', 'input', 'dialog', 'select'],
            'chakra': ['button', 'box', 'input', 'modal', 'menu'],
            'antd': ['button', 'card', 'input', 'table', 'form'],
            'mantine': ['button', 'card', 'input', 'modal', 'group']
        }
        
        priorities = framework_priorities.get(framework, ['button', 'input', 'card'])
        
        recommendations = []
        
        # Add high-priority components first
        for priority in priorities:
            matching = [
                comp for comp in framework_components
                if comp.name and priority in comp.name.lower()
            ]
            
            for component in matching[:2]:
                recommendations.append(ComponentRecommendation(
                    component=component,
                    confidence=0.8,
                    reason=f"Essential {framework} component",
                    category="framework-essential",
                    complementary_components=self._get_complementary_components(component.name)
                ))
        
        # Add use-case specific components
        if use_case:
            use_case_recs = self._recommend_for_use_case(use_case, framework_components)
            recommendations.extend(use_case_recs)
        
        # Remove duplicates and limit
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec.component.id not in seen:
                seen.add(rec.component.id)
                unique_recs.append(rec)
                
        return unique_recs[:limit]

    def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze query to understand user intent."""
        
        intent = {
            'page_type': None,
            'component_types': [],
            'use_case': None,
            'framework_preference': None
        }
        
        # Detect page type intent
        page_keywords = {
            'landing': ['landing', 'homepage', 'hero', 'marketing'],
            'dashboard': ['dashboard', 'admin', 'analytics', 'control'],
            'ecommerce': ['shop', 'store', 'product', 'cart', 'checkout'],
            'blog': ['blog', 'article', 'post', 'content']
        }
        
        for page_type, keywords in page_keywords.items():
            if any(keyword in query for keyword in keywords):
                intent['page_type'] = page_type
                break
        
        # Detect component types
        for category, components in self.component_categories.items():
            if any(comp in query for comp in components):
                intent['component_types'].append(category)
        
        # Detect framework preference
        frameworks = ['material', 'shadcn', 'chakra', 'antd', 'mantine']
        for framework in frameworks:
            if framework in query:
                intent['framework_preference'] = framework
                break
                
        return intent

    def _find_direct_matches(self, query: str, components: List[Component]) -> List[Component]:
        """Find components that directly match the query."""
        
        matches = []
        
        for component in components:
            score = 0
            
            # Name match
            if component.name and query in component.name.lower():
                score += 3
                
            # Title match
            if component.title and query in component.title.lower():
                score += 2
                
            # Tag match
            if component.tags:
                try:
                    tags = json.loads(component.tags) if isinstance(component.tags, str) else component.tags
                    for tag in tags:
                        if query in str(tag).lower():
                            score += 1
                except (json.JSONDecodeError, TypeError):
                    pass
            
            if score > 0:
                matches.append((component, score))
        
        # Sort by score and return components
        matches.sort(key=lambda x: x[1], reverse=True)
        return [comp for comp, _ in matches]

    def _recommend_for_page_type(
        self, 
        page_type: str, 
        components: List[Component]
    ) -> List[ComponentRecommendation]:
        """Recommend components for a specific page type."""
        
        if page_type not in self.page_patterns:
            return []
            
        recommendations = []
        patterns = self.page_patterns[page_type]
        
        for section, component_names in patterns.items():
            for comp_name in component_names[:2]:  # Top 2 per section
                matching = [
                    comp for comp in components
                    if comp.name and comp_name in comp.name.lower()
                ]
                
                for component in matching[:1]:  # Top match per component name
                    recommendations.append(ComponentRecommendation(
                        component=component,
                        confidence=0.7,
                        reason=f"Recommended for {page_type} {section}",
                        category="page-pattern",
                        complementary_components=self._get_complementary_components(component.name)
                    ))
        
        return recommendations

    def _recommend_for_component_type(
        self, 
        component_type: str, 
        components: List[Component]
    ) -> List[ComponentRecommendation]:
        """Recommend components of a specific type."""
        
        if component_type not in self.component_categories:
            return []
            
        recommendations = []
        type_components = self.component_categories[component_type]
        
        for comp_name in type_components[:3]:  # Top 3 per type
            matching = [
                comp for comp in components
                if comp.name and comp_name in comp.name.lower()
            ]
            
            for component in matching[:2]:  # Top 2 matches
                recommendations.append(ComponentRecommendation(
                    component=component,
                    confidence=0.6,
                    reason=f"Popular {component_type} component",
                    category="type-based",
                    complementary_components=self._get_complementary_components(component.name)
                ))
        
        return recommendations

    def _recommend_for_use_case(
        self, 
        use_case: str, 
        components: List[Component]
    ) -> List[ComponentRecommendation]:
        """Recommend components for a specific use case."""
        
        use_case_patterns = {
            'form': ['input', 'button', 'select', 'checkbox'],
            'navigation': ['menu', 'navbar', 'breadcrumb', 'tabs'],
            'data': ['table', 'list', 'card', 'grid'],
            'feedback': ['alert', 'modal', 'snackbar', 'progress']
        }
        
        if use_case not in use_case_patterns:
            return []
            
        recommendations = []
        pattern_components = use_case_patterns[use_case]
        
        for comp_name in pattern_components:
            matching = [
                comp for comp in components
                if comp.name and comp_name in comp.name.lower()
            ]
            
            for component in matching[:1]:
                recommendations.append(ComponentRecommendation(
                    component=component,
                    confidence=0.7,
                    reason=f"Essential for {use_case} use case",
                    category="use-case",
                    complementary_components=self._get_complementary_components(component.name)
                ))
        
        return recommendations

    def _get_complementary_components(self, component_name: Optional[str]) -> List[str]:
        """Get list of components that complement the given component."""
        
        if not component_name:
            return []
            
        comp_name_lower = component_name.lower()
        
        # Find matching relationships
        for key, complements in self.component_relationships.items():
            if key in comp_name_lower:
                return complements[:5]  # Top 5 complements
                
        return []

    def _calculate_complement_confidence(
        self, 
        component: Component, 
        selected_components: List[Component]
    ) -> float:
        """Calculate confidence score for a complementary component."""
        
        if not component.name:
            return 0.0
            
        base_confidence = 0.6
        
        # Boost for multiple relationships
        relationship_count = 0
        for selected in selected_components:
            if selected.name:
                selected_name = selected.name.lower()
                complements = self._get_complementary_components(selected_name)
                if any(comp in component.name.lower() for comp in complements):
                    relationship_count += 1
        
        confidence_boost = min(0.3, relationship_count * 0.1)
        return base_confidence + confidence_boost


# Global instance for easy access
component_recommendation_engine = ComponentRecommendationEngine()