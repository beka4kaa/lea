"""Template suggestion engine for intelligent template recommendations."""

import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

from mcp_ui_aggregator.templates.predefined import TEMPLATE_REGISTRY
from mcp_ui_aggregator.templates import Framework, TemplateType


@dataclass
class TemplateSuggestion:
    """Represents a template suggestion with reasoning."""
    template_id: str
    template_name: str
    framework: Framework
    template_type: TemplateType
    confidence: float
    reason: str
    use_cases: List[str]
    estimated_complexity: str
    estimated_time: str


class TemplateSuggestionEngine:
    """AI-powered template suggestion system."""
    
    def __init__(self):
        # Template characteristics for better matching
        self.template_characteristics = {
            'landing': {
                'keywords': ['marketing', 'homepage', 'hero', 'cta', 'features', 'testimonials'],
                'use_cases': ['Product launch', 'Company website', 'Marketing campaign', 'Portfolio showcase'],
                'complexity': 'Medium',
                'time_estimate': '2-4 hours'
            },
            'dashboard': {
                'keywords': ['admin', 'analytics', 'metrics', 'charts', 'data', 'monitoring'],
                'use_cases': ['Admin panel', 'Analytics dashboard', 'Business intelligence', 'Monitoring system'],
                'complexity': 'High',
                'time_estimate': '4-8 hours'
            },
            'ecommerce': {
                'keywords': ['shop', 'store', 'product', 'cart', 'checkout', 'payment'],
                'use_cases': ['Online store', 'Product catalog', 'Shopping cart', 'Marketplace'],
                'complexity': 'High',
                'time_estimate': '6-12 hours'
            },
            'blog': {
                'keywords': ['content', 'article', 'post', 'news', 'publication', 'writing'],
                'use_cases': ['Personal blog', 'News site', 'Documentation', 'Content platform'],
                'complexity': 'Low',
                'time_estimate': '1-3 hours'
            },
            'portfolio': {
                'keywords': ['portfolio', 'showcase', 'work', 'projects', 'gallery', 'personal'],
                'use_cases': ['Personal portfolio', 'Agency showcase', 'Artist gallery', 'Professional profile'],
                'complexity': 'Medium',
                'time_estimate': '2-5 hours'
            }
        }
        
        # Framework preferences for different use cases
        self.framework_preferences = {
            'startup': {'react': 0.8, 'vue': 0.6, 'html': 0.4},
            'enterprise': {'react': 0.9, 'vue': 0.7, 'html': 0.3},
            'personal': {'html': 0.8, 'vue': 0.6, 'react': 0.5},
            'prototype': {'html': 0.9, 'vue': 0.7, 'react': 0.6},
            'production': {'react': 0.9, 'vue': 0.8, 'html': 0.4}
        }
        
        # Industry-specific recommendations
        self.industry_templates = {
            'tech': ['dashboard', 'landing'],
            'ecommerce': ['ecommerce', 'landing'],
            'media': ['blog', 'portfolio'],
            'finance': ['dashboard', 'landing'],
            'healthcare': ['landing', 'dashboard'],
            'education': ['blog', 'landing'],
            'creative': ['portfolio', 'blog'],
            'saas': ['landing', 'dashboard']
        }

    def suggest_for_query(
        self, 
        query: str, 
        preferred_framework: Optional[str] = None,
        user_context: Optional[Dict[str, Any]] = None,
        limit: int = 6
    ) -> List[TemplateSuggestion]:
        """Suggest templates based on user query and context."""
        
        suggestions = []
        query_lower = query.lower()
        
        # Analyze query intent
        intent = self._analyze_query_intent(query_lower)
        
        # Get direct template type matches
        for template_type, confidence in intent['template_types'].items():
            type_suggestions = self._suggest_for_template_type(
                template_type, preferred_framework, confidence
            )
            suggestions.extend(type_suggestions)
        
        # Get keyword-based suggestions
        keyword_suggestions = self._suggest_for_keywords(query_lower, preferred_framework)
        suggestions.extend(keyword_suggestions)
        
        # Apply user context if available
        if user_context:
            context_suggestions = self._suggest_for_context(user_context, preferred_framework)
            suggestions.extend(context_suggestions)
        
        # Remove duplicates and sort by confidence
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion.template_id not in seen:
                seen.add(suggestion.template_id)
                unique_suggestions.append(suggestion)
        
        unique_suggestions.sort(key=lambda x: x.confidence, reverse=True)
        return unique_suggestions[:limit]

    def suggest_for_project_type(
        self, 
        project_type: str,
        framework: Optional[str] = None,
        experience_level: str = 'intermediate',
        limit: int = 4
    ) -> List[TemplateSuggestion]:
        """Suggest templates for a specific project type."""
        
        suggestions = []
        
        # Map project types to template types
        project_mappings = {
            'website': ['landing', 'blog'],
            'webapp': ['dashboard', 'ecommerce'],
            'portfolio': ['portfolio', 'blog'],
            'admin': ['dashboard'],
            'blog': ['blog'],
            'store': ['ecommerce', 'landing'],
            'landing': ['landing'],
            'dashboard': ['dashboard']
        }
        
        template_types = project_mappings.get(project_type.lower(), ['landing'])
        
        for template_type in template_types:
            type_suggestions = self._suggest_for_template_type(
                template_type, framework, confidence=0.8
            )
            
            # Adjust confidence based on experience level
            for suggestion in type_suggestions:
                if experience_level == 'beginner':
                    if suggestion.estimated_complexity == 'Low':
                        suggestion.confidence *= 1.2
                    elif suggestion.estimated_complexity == 'High':
                        suggestion.confidence *= 0.8
                elif experience_level == 'advanced':
                    if suggestion.estimated_complexity == 'High':
                        suggestion.confidence *= 1.1
            
            suggestions.extend(type_suggestions)
        
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        return suggestions[:limit]

    def suggest_similar(
        self, 
        template_id: str, 
        preferred_framework: Optional[str] = None,
        limit: int = 3
    ) -> List[TemplateSuggestion]:
        """Suggest templates similar to the given one."""
        
        if template_id not in TEMPLATE_REGISTRY:
            return []
        
        current_template = TEMPLATE_REGISTRY[template_id]
        suggestions = []
        
        # Find templates of the same type but different frameworks
        for tid, template in TEMPLATE_REGISTRY.items():
            if tid == template_id:
                continue
                
            confidence = 0.0
            reason = ""
            
            # Same type, different framework
            if template.type == current_template.type and template.framework != current_template.framework:
                confidence = 0.8
                reason = f"Same {template.type.value} template in {template.framework.value}"
                
            # Different type, same framework
            elif template.framework == current_template.framework and template.type != current_template.type:
                confidence = 0.6
                reason = f"Different template in same {template.framework.value} framework"
            
            if confidence > 0:
                # Boost if matches preferred framework
                if preferred_framework and template.framework.value == preferred_framework:
                    confidence *= 1.2
                    
                characteristics = self.template_characteristics[template.type.value]
                
                suggestions.append(TemplateSuggestion(
                    template_id=tid,
                    template_name=template.name,
                    framework=template.framework,
                    template_type=template.type,
                    confidence=confidence,
                    reason=reason,
                    use_cases=characteristics['use_cases'],
                    estimated_complexity=characteristics['complexity'],
                    estimated_time=characteristics['time_estimate']
                ))
        
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        return suggestions[:limit]

    def suggest_for_industry(
        self, 
        industry: str, 
        framework: Optional[str] = None,
        limit: int = 4
    ) -> List[TemplateSuggestion]:
        """Suggest templates for a specific industry."""
        
        industry_lower = industry.lower()
        template_types = self.industry_templates.get(industry_lower, ['landing', 'blog'])
        
        suggestions = []
        for template_type in template_types:
            type_suggestions = self._suggest_for_template_type(
                template_type, framework, confidence=0.7
            )
            # Update reason for industry context
            for suggestion in type_suggestions:
                suggestion.reason = f"Recommended for {industry} industry"
                suggestion.confidence *= 1.1  # Industry boost
                
            suggestions.extend(type_suggestions)
        
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        return suggestions[:limit]

    def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze query to understand template intent."""
        
        intent = {
            'template_types': {},
            'framework_preference': None,
            'complexity_preference': None
        }
        
        # Check for template type keywords
        for template_type, characteristics in self.template_characteristics.items():
            score = 0
            for keyword in characteristics['keywords']:
                if keyword in query:
                    score += 1
            
            if score > 0:
                confidence = min(0.9, 0.5 + (score * 0.1))
                intent['template_types'][template_type] = confidence
        
        # Check for framework mentions
        frameworks = ['react', 'vue', 'html', 'javascript', 'typescript']
        for framework in frameworks:
            if framework in query:
                intent['framework_preference'] = framework
                break
        
        # Check for complexity indicators
        if any(word in query for word in ['simple', 'basic', 'quick', 'minimal']):
            intent['complexity_preference'] = 'low'
        elif any(word in query for word in ['complex', 'advanced', 'full', 'complete']):
            intent['complexity_preference'] = 'high'
            
        return intent

    def _suggest_for_template_type(
        self, 
        template_type: str, 
        preferred_framework: Optional[str] = None,
        confidence: float = 0.7
    ) -> List[TemplateSuggestion]:
        """Get suggestions for a specific template type."""
        
        suggestions = []
        characteristics = self.template_characteristics.get(template_type, {})
        
        # Find matching templates
        for template_id, template in TEMPLATE_REGISTRY.items():
            if template.type.value == template_type:
                
                # Adjust confidence based on framework preference
                adjusted_confidence = confidence
                if preferred_framework:
                    if template.framework.value == preferred_framework:
                        adjusted_confidence *= 1.3
                    else:
                        adjusted_confidence *= 0.8
                
                suggestions.append(TemplateSuggestion(
                    template_id=template_id,
                    template_name=template.name,
                    framework=template.framework,
                    template_type=template.type,
                    confidence=adjusted_confidence,
                    reason=f"Matches {template_type} template requirements",
                    use_cases=characteristics.get('use_cases', []),
                    estimated_complexity=characteristics.get('complexity', 'Medium'),
                    estimated_time=characteristics.get('time_estimate', '2-4 hours')
                ))
        
        return suggestions

    def _suggest_for_keywords(
        self, 
        query: str, 
        preferred_framework: Optional[str] = None
    ) -> List[TemplateSuggestion]:
        """Get suggestions based on keywords in query."""
        
        suggestions = []
        
        # Check each template type's keywords
        for template_type, characteristics in self.template_characteristics.items():
            keyword_matches = sum(1 for keyword in characteristics['keywords'] if keyword in query)
            
            if keyword_matches > 0:
                confidence = min(0.8, 0.4 + (keyword_matches * 0.1))
                type_suggestions = self._suggest_for_template_type(
                    template_type, preferred_framework, confidence
                )
                suggestions.extend(type_suggestions)
        
        return suggestions

    def _suggest_for_context(
        self, 
        user_context: Dict[str, Any], 
        preferred_framework: Optional[str] = None
    ) -> List[TemplateSuggestion]:
        """Get suggestions based on user context."""
        
        suggestions = []
        
        # Check for industry context
        if 'industry' in user_context:
            industry_suggestions = self.suggest_for_industry(
                user_context['industry'], preferred_framework
            )
            suggestions.extend(industry_suggestions)
        
        # Check for project type context
        if 'project_type' in user_context:
            project_suggestions = self.suggest_for_project_type(
                user_context['project_type'], 
                preferred_framework,
                user_context.get('experience_level', 'intermediate')
            )
            suggestions.extend(project_suggestions)
        
        # Check for timeline context
        if 'timeline' in user_context:
            timeline = user_context['timeline'].lower()
            if 'quick' in timeline or 'fast' in timeline:
                # Boost simple templates
                for suggestion in suggestions:
                    if suggestion.estimated_complexity == 'Low':
                        suggestion.confidence *= 1.2
        
        return suggestions

    def get_template_comparison(
        self, 
        template_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare multiple templates and provide recommendations."""
        
        if not template_ids:
            return {}
        
        comparisons = []
        
        for template_id in template_ids:
            if template_id in TEMPLATE_REGISTRY:
                template = TEMPLATE_REGISTRY[template_id]
                characteristics = self.template_characteristics[template.type.value]
                
                comparisons.append({
                    'template_id': template_id,
                    'name': template.name,
                    'framework': template.framework.value,
                    'type': template.type.value,
                    'complexity': characteristics['complexity'],
                    'estimated_time': characteristics['time_estimate'],
                    'use_cases': characteristics['use_cases'],
                    'section_count': len(template.sections),
                    'dependencies': len(template.dependencies or [])
                })
        
        # Provide recommendations
        recommendations = []
        
        # Find simplest option
        simplest = min(comparisons, key=lambda x: (
            0 if x['complexity'] == 'Low' else 1 if x['complexity'] == 'Medium' else 2
        ))
        recommendations.append(f"For quick implementation, choose {simplest['name']} ({simplest['complexity']} complexity)")
        
        # Find most feature-rich
        richest = max(comparisons, key=lambda x: x['section_count'])
        recommendations.append(f"For comprehensive features, choose {richest['name']} ({richest['section_count']} sections)")
        
        # Framework recommendations
        frameworks = list(set(comp['framework'] for comp in comparisons))
        if 'react' in frameworks:
            recommendations.append("React templates offer the best ecosystem and community support")
        if 'html' in frameworks:
            recommendations.append("HTML templates are easiest to customize and deploy")
        
        return {
            'comparisons': comparisons,
            'recommendations': recommendations,
            'summary': {
                'total_templates': len(comparisons),
                'frameworks': frameworks,
                'complexity_range': list(set(comp['complexity'] for comp in comparisons))
            }
        }

# Global instance for easy access  
template_suggestion_engine = TemplateSuggestionEngine()
