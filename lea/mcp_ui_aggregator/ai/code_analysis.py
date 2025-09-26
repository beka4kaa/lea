"""Code analysis engine for intelligent code generation improvements."""

import re
import json
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
from enum import Enum


class CodeQuality(Enum):
    """Code quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    NEEDS_IMPROVEMENT = "needs_improvement"


@dataclass
class CodeSuggestion:
    """Represents a code improvement suggestion."""
    type: str
    severity: str
    description: str
    example: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class CodeAnalysis:
    """Represents analysis results for code."""
    quality_score: float
    quality_level: CodeQuality
    suggestions: List[CodeSuggestion]
    metrics: Dict[str, Any]
    best_practices: List[str]
    potential_issues: List[str]


class CodeAnalysisEngine:
    """Engine for analyzing and improving generated code quality."""
    
    def __init__(self):
        # Best practices for different frameworks
        self.best_practices = {
            'react': [
                'Use functional components with hooks',
                'Implement proper prop types or TypeScript',
                'Follow naming conventions (PascalCase for components)',
                'Use proper key props in lists',
                'Implement error boundaries',
                'Optimize with React.memo when needed',
                'Use proper event handlers',
                'Follow component composition patterns'
            ],
            'vue': [
                'Use composition API for better logic reuse',
                'Implement proper prop validation',
                'Follow Vue naming conventions',
                'Use proper event emission patterns',
                'Implement computed properties correctly',
                'Use proper lifecycle hooks',
                'Follow single file component structure',
                'Implement proper slot usage'
            ],
            'html': [
                'Use semantic HTML elements',
                'Implement proper accessibility attributes',
                'Follow proper document structure',
                'Use valid CSS and HTML',
                'Implement responsive design patterns',
                'Follow proper form validation',
                'Use proper meta tags',
                'Implement proper SEO practices'
            ]
        }
        
        # Common anti-patterns to detect
        self.antipatterns = {
            'react': [
                r'class\s+\w+\s+extends\s+React\.Component',  # Class components
                r'dangerouslySetInnerHTML',  # Direct HTML injection
                r'document\.getElementById',  # Direct DOM manipulation
                r'window\.',  # Direct window access
                r'var\s+',  # var usage instead of const/let
            ],
            'vue': [
                r'\$refs\.\w+\.innerHTML',  # Direct HTML manipulation
                r'v-html="[^"]+"',  # Potential XSS via v-html
                r'eval\(',  # eval usage
                r'var\s+',  # var usage
            ],
            'html': [
                r'<div[^>]*onclick="[^"]*"',  # Inline event handlers
                r'style="[^"]*"',  # Inline styles
                r'<[^>]*>[^<]*javascript:[^<]*</[^>]*>',  # JavaScript URLs
                r'<script[^>]*>[^<]*</script>',  # Inline scripts
            ]
        }
        
        # Code complexity metrics
        self.complexity_patterns = {
            'nested_depth': r'(\s{2,}){4,}',  # Deep nesting
            'long_lines': r'.{120,}',  # Very long lines
            'large_functions': r'function\s+\w+[^{]*{[^}]{500,}}',  # Large functions
            'many_parameters': r'\([^)]*,\s*[^)]*,\s*[^)]*,\s*[^)]*,\s*[^)]*\)',  # 5+ parameters
        }

    def analyze_generated_code(
        self, 
        code: str, 
        framework: str,
        template_type: Optional[str] = None
    ) -> CodeAnalysis:
        """Analyze generated code and provide improvement suggestions."""
        
        metrics = self._calculate_metrics(code, framework)
        suggestions = self._generate_suggestions(code, framework, metrics)
        quality_score = self._calculate_quality_score(metrics, suggestions)
        quality_level = self._determine_quality_level(quality_score)
        best_practices = self._check_best_practices(code, framework)
        potential_issues = self._detect_potential_issues(code, framework)
        
        return CodeAnalysis(
            quality_score=quality_score,
            quality_level=quality_level,
            suggestions=suggestions,
            metrics=metrics,
            best_practices=best_practices,
            potential_issues=potential_issues
        )

    def suggest_improvements(
        self, 
        code: str, 
        framework: str,
        target_quality: CodeQuality = CodeQuality.GOOD
    ) -> List[str]:
        """Suggest specific improvements to reach target quality."""
        
        analysis = self.analyze_generated_code(code, framework)
        improvements = []
        
        # Quality-based improvements
        if analysis.quality_level.value != target_quality.value:
            if target_quality == CodeQuality.EXCELLENT:
                improvements.extend([
                    "Add TypeScript support for better type safety",
                    "Implement comprehensive error handling",
                    "Add unit tests for components",
                    "Optimize for accessibility (WCAG compliance)",
                    "Add performance monitoring",
                    "Implement proper SEO optimization"
                ])
            elif target_quality == CodeQuality.GOOD:
                improvements.extend([
                    "Add prop validation",
                    "Implement basic error boundaries",
                    "Add loading and error states",
                    "Optimize component re-renders",
                    "Add basic accessibility attributes"
                ])
        
        # Framework-specific improvements
        if framework == 'react':
            if 'useState' not in code and 'state' in code.lower():
                improvements.append("Consider using React hooks for state management")
            if 'useEffect' not in code and 'componentDidMount' in code:
                improvements.append("Migrate to useEffect for lifecycle management")
                
        elif framework == 'vue':
            if 'ref(' not in code and 'reactive(' not in code:
                improvements.append("Consider using Composition API for better reactivity")
            if 'computed(' not in code and 'get ' in code:
                improvements.append("Use computed properties for derived state")
                
        elif framework == 'html':
            if 'aria-' not in code:
                improvements.append("Add ARIA attributes for better accessibility")
            if '@media' not in code:
                improvements.append("Add responsive design breakpoints")
        
        return improvements

    def optimize_for_performance(self, code: str, framework: str) -> Dict[str, Any]:
        """Suggest performance optimizations for the code."""
        
        optimizations = {
            'suggestions': [],
            'estimated_impact': 'medium',
            'implementation_effort': 'low'
        }
        
        if framework == 'react':
            # React-specific optimizations
            if 'map(' in code and 'key=' not in code:
                optimizations['suggestions'].append({
                    'type': 'performance',
                    'description': 'Add proper key props to list items',
                    'impact': 'high',
                    'example': '<Item key={item.id} {...item} />'
                })
            
            if re.search(r'function\s+\w+\([^)]*\)\s*{[^}]*}', code):
                optimizations['suggestions'].append({
                    'type': 'performance',
                    'description': 'Consider using React.memo for pure components',
                    'impact': 'medium',
                    'example': 'export default React.memo(MyComponent);'
                })
                
        elif framework == 'vue':
            # Vue-specific optimizations
            if 'v-for=' in code and ':key=' not in code:
                optimizations['suggestions'].append({
                    'type': 'performance',
                    'description': 'Add :key attribute to v-for loops',
                    'impact': 'high',
                    'example': 'v-for="item in items" :key="item.id"'
                })
                
        elif framework == 'html':
            # HTML-specific optimizations
            if '<img' in code and 'loading=' not in code:
                optimizations['suggestions'].append({
                    'type': 'performance',
                    'description': 'Add lazy loading to images',
                    'impact': 'medium',
                    'example': '<img loading="lazy" src="..." alt="..." />'
                })
        
        # Calculate overall impact
        high_impact_count = sum(1 for s in optimizations['suggestions'] if s.get('impact') == 'high')
        if high_impact_count > 2:
            optimizations['estimated_impact'] = 'high'
        elif high_impact_count > 0:
            optimizations['estimated_impact'] = 'medium'
        else:
            optimizations['estimated_impact'] = 'low'
            
        return optimizations

    def _calculate_metrics(self, code: str, framework: str) -> Dict[str, Any]:
        """Calculate various code quality metrics."""
        
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        metrics = {
            'total_lines': len(lines),
            'code_lines': len(non_empty_lines),
            'blank_lines': len(lines) - len(non_empty_lines),
            'avg_line_length': sum(len(line) for line in non_empty_lines) / max(len(non_empty_lines), 1),
            'max_line_length': max(len(line) for line in lines) if lines else 0,
            'indentation_consistency': self._check_indentation_consistency(lines),
            'complexity_score': self._calculate_complexity(code),
            'readability_score': self._calculate_readability(code, framework)
        }
        
        # Framework-specific metrics
        if framework == 'react':
            metrics.update({
                'component_count': len(re.findall(r'function\s+[A-Z]\w+|const\s+[A-Z]\w+\s*=', code)),
                'hook_usage': len(re.findall(r'use[A-Z]\w+', code)),
                'jsx_elements': len(re.findall(r'<[A-Z]\w+', code))
            })
        elif framework == 'vue':
            metrics.update({
                'component_count': len(re.findall(r'<template>|<script>|export\s+default', code)),
                'directive_usage': len(re.findall(r'v-\w+', code)),
                'computed_properties': len(re.findall(r'computed\s*:', code))
            })
        elif framework == 'html':
            metrics.update({
                'element_count': len(re.findall(r'<\w+', code)),
                'semantic_elements': len(re.findall(r'<(header|nav|main|section|article|aside|footer)', code)),
                'accessibility_attributes': len(re.findall(r'aria-\w+|role=', code))
            })
            
        return metrics

    def _generate_suggestions(
        self, 
        code: str, 
        framework: str, 
        metrics: Dict[str, Any]
    ) -> List[CodeSuggestion]:
        """Generate improvement suggestions based on code analysis."""
        
        suggestions = []
        
        # Line length suggestions
        if metrics['max_line_length'] > 120:
            suggestions.append(CodeSuggestion(
                type='formatting',
                severity='warning',
                description=f"Line too long ({metrics['max_line_length']} chars). Consider breaking into multiple lines.",
                auto_fixable=True
            ))
        
        # Complexity suggestions
        if metrics['complexity_score'] > 7:
            suggestions.append(CodeSuggestion(
                type='complexity',
                severity='warning',
                description="High complexity detected. Consider breaking down into smaller functions.",
                auto_fixable=False
            ))
        
        # Indentation suggestions
        if not metrics['indentation_consistency']:
            suggestions.append(CodeSuggestion(
                type='formatting',
                severity='error',
                description="Inconsistent indentation detected. Use consistent spaces or tabs.",
                auto_fixable=True
            ))
        
        # Framework-specific suggestions
        suggestions.extend(self._get_framework_suggestions(code, framework))
        
        # Anti-pattern detection
        antipatterns = self.antipatterns.get(framework, [])
        for pattern in antipatterns:
            if re.search(pattern, code):
                suggestions.append(CodeSuggestion(
                    type='antipattern',
                    severity='warning',
                    description=f"Potential anti-pattern detected: {pattern}",
                    auto_fixable=False
                ))
        
        return suggestions

    def _get_framework_suggestions(self, code: str, framework: str) -> List[CodeSuggestion]:
        """Get framework-specific suggestions."""
        
        suggestions = []
        
        if framework == 'react':
            # Check for missing keys in lists
            if '.map(' in code and 'key=' not in code:
                suggestions.append(CodeSuggestion(
                    type='react',
                    severity='warning',
                    description="Missing 'key' prop in list rendering",
                    example="items.map(item => <Item key={item.id} {...item} />)",
                    auto_fixable=True
                ))
            
            # Check for inline functions in JSX
            if re.search(r'onClick=\{[^}]*=>', code):
                suggestions.append(CodeSuggestion(
                    type='react',
                    severity='info',
                    description="Consider extracting inline functions to avoid re-renders",
                    auto_fixable=False
                ))
                
        elif framework == 'vue':
            # Check for missing keys in v-for
            if 'v-for=' in code and ':key=' not in code:
                suggestions.append(CodeSuggestion(
                    type='vue',
                    severity='warning',
                    description="Missing ':key' attribute in v-for directive",
                    example='v-for="item in items" :key="item.id"',
                    auto_fixable=True
                ))
                
        elif framework == 'html':
            # Check for missing alt attributes
            if '<img' in code and 'alt=' not in code:
                suggestions.append(CodeSuggestion(
                    type='accessibility',
                    severity='warning',
                    description="Missing 'alt' attribute in img elements",
                    example='<img src="..." alt="Description" />',
                    auto_fixable=False
                ))
        
        return suggestions

    def _calculate_quality_score(
        self, 
        metrics: Dict[str, Any], 
        suggestions: List[CodeSuggestion]
    ) -> float:
        """Calculate overall quality score (0-100)."""
        
        base_score = 100.0
        
        # Deduct points for suggestions
        for suggestion in suggestions:
            if suggestion.severity == 'error':
                base_score -= 15
            elif suggestion.severity == 'warning':
                base_score -= 10
            elif suggestion.severity == 'info':
                base_score -= 5
        
        # Deduct points for metrics
        if metrics['complexity_score'] > 7:
            base_score -= (metrics['complexity_score'] - 7) * 5
            
        if metrics['max_line_length'] > 120:
            base_score -= min(20, (metrics['max_line_length'] - 120) / 10)
        
        # Bonus points for good practices
        if metrics['readability_score'] > 0.8:
            base_score += 5
            
        return max(0.0, min(100.0, base_score))

    def _determine_quality_level(self, score: float) -> CodeQuality:
        """Determine quality level based on score."""
        
        if score >= 90:
            return CodeQuality.EXCELLENT
        elif score >= 75:
            return CodeQuality.GOOD
        elif score >= 60:
            return CodeQuality.AVERAGE
        else:
            return CodeQuality.NEEDS_IMPROVEMENT

    def _check_best_practices(self, code: str, framework: str) -> List[str]:
        """Check which best practices are followed."""
        
        followed_practices = []
        practices = self.best_practices.get(framework, [])
        
        for practice in practices:
            if self._practice_is_followed(code, practice, framework):
                followed_practices.append(practice)
                
        return followed_practices

    def _practice_is_followed(self, code: str, practice: str, framework: str) -> bool:
        """Check if a specific best practice is followed."""
        
        practice_lower = practice.lower()
        
        # Simple heuristics for practice detection
        if 'functional components' in practice_lower:
            return 'function ' in code and 'class ' not in code
        elif 'prop types' in practice_lower:
            return 'PropTypes' in code or 'interface' in code
        elif 'naming conventions' in practice_lower:
            return bool(re.search(r'function\s+[A-Z]\w+|const\s+[A-Z]\w+', code))
        elif 'key props' in practice_lower:
            return 'key=' in code
        elif 'semantic html' in practice_lower:
            return bool(re.search(r'<(header|nav|main|section|article|aside|footer)', code))
        elif 'accessibility' in practice_lower:
            return 'aria-' in code or 'alt=' in code
            
        return False

    def _detect_potential_issues(self, code: str, framework: str) -> List[str]:
        """Detect potential issues in the code."""
        
        issues = []
        
        # Security issues
        if 'dangerouslySetInnerHTML' in code:
            issues.append("Potential XSS vulnerability with dangerouslySetInnerHTML")
            
        if 'eval(' in code:
            issues.append("eval() usage detected - potential security risk")
            
        # Performance issues
        if framework == 'react' and re.search(r'onClick=\{[^}]*=>', code):
            issues.append("Inline functions in JSX may cause unnecessary re-renders")
            
        # Accessibility issues
        if framework == 'html' and '<img' in code and 'alt=' not in code:
            issues.append("Images missing alt attributes - accessibility concern")
            
        return issues

    def _check_indentation_consistency(self, lines: List[str]) -> bool:
        """Check if indentation is consistent throughout the file."""
        
        indentation_patterns = set()
        
        for line in lines:
            if line.strip():  # Skip empty lines
                leading_whitespace = len(line) - len(line.lstrip())
                if leading_whitespace > 0:
                    # Detect if using tabs or spaces
                    if line.startswith('\t'):
                        indentation_patterns.add('tab')
                    elif line.startswith(' '):
                        # Count spaces at beginning
                        spaces = 0
                        for char in line:
                            if char == ' ':
                                spaces += 1
                            else:
                                break
                        indentation_patterns.add(f'space_{spaces}')
        
        # Consistent if only one pattern or no indentation
        return len(indentation_patterns) <= 1

    def _calculate_complexity(self, code: str) -> float:
        """Calculate code complexity score."""
        
        complexity = 0
        
        # Count control structures
        complexity += len(re.findall(r'\b(if|else|elif|for|while|switch|case)\b', code))
        
        # Count nested structures
        nesting_levels = 0
        max_nesting = 0
        for char in code:
            if char in '{[(':
                nesting_levels += 1
                max_nesting = max(max_nesting, nesting_levels)
            elif char in '}])':
                nesting_levels = max(0, nesting_levels - 1)
        
        complexity += max_nesting * 0.5
        
        # Count function definitions
        complexity += len(re.findall(r'\bfunction\b|=>\s*{|\bdef\b', code)) * 0.3
        
        return complexity

    def _calculate_readability(self, code: str, framework: str) -> float:
        """Calculate readability score (0-1)."""
        
        readability = 1.0
        
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        if not non_empty_lines:
            return 0.0
        
        # Check average line length
        avg_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        if avg_length > 100:
            readability -= 0.2
        elif avg_length > 80:
            readability -= 0.1
        
        # Check for comments
        comment_lines = len([line for line in lines if line.strip().startswith(('//','#','/*','*'))])
        comment_ratio = comment_lines / len(lines)
        if comment_ratio < 0.1:
            readability -= 0.2
        
        # Check naming (simple heuristic)
        if framework in ['react', 'vue']:
            # Check for descriptive variable names
            short_names = len(re.findall(r'\b[a-z]{1,2}\b', code))
            total_names = len(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code))
            if total_names > 0 and short_names / total_names > 0.3:
                readability -= 0.15
        
        return max(0.0, readability)


# Global instance for easy access
code_analysis_engine = CodeAnalysisEngine()