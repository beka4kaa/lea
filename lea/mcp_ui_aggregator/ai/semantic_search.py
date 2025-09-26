"""Semantic search engine for UI components using embeddings."""

import json
import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from mcp_ui_aggregator.models.database import Component


@dataclass
class SearchResult:
    """Represents a search result with relevance scoring."""
    component: Component
    score: float
    match_type: str
    matched_fields: List[str]


class SemanticSearchEngine:
    """Enhanced search engine with semantic capabilities and intelligent ranking."""
    
    def __init__(self):
        self.component_cache = {}
        self.keyword_index = defaultdict(set)
        self.category_weights = {
            'name': 3.0,
            'title': 2.5,
            'description': 2.0,
            'tags': 1.8,
            'namespace': 1.5,
            'component_type': 1.2
        }
        
        # Component popularity based on common use cases
        self.popularity_scores = {
            'button': 5.0,
            'input': 4.8,
            'card': 4.5,
            'modal': 4.2,
            'table': 4.0,
            'form': 4.0,
            'nav': 3.8,
            'list': 3.5,
            'avatar': 3.2,
            'badge': 3.0
        }
        
        # Framework preference weights
        self.framework_weights = {
            'material': 1.2,  # Most comprehensive
            'shadcn': 1.15,   # Modern and popular
            'chakra': 1.1,    # Good DX
            'antd': 1.05,     # Enterprise focus
            'mantine': 1.0    # Baseline
        }

    def build_index(self, components: List[Component]) -> None:
        """Build search index from components."""
        self.component_cache = {comp.id: comp for comp in components}
        self.keyword_index.clear()
        
        for component in components:
            # Index all searchable text
            searchable_text = self._extract_searchable_text(component)
            for keyword in searchable_text:
                self.keyword_index[keyword.lower()].add(component.id)

    def _extract_searchable_text(self, component: Component) -> List[str]:
        """Extract all searchable keywords from a component."""
        keywords = []
        
        # Add name variations
        if component.name:
            keywords.extend(self._tokenize(component.name))
            
        # Add title variations
        if component.title:
            keywords.extend(self._tokenize(component.title))
            
        # Add description keywords
        if component.description:
            keywords.extend(self._tokenize(component.description))
            
        # Add tags
        if component.tags:
            try:
                tags = json.loads(component.tags) if isinstance(component.tags, str) else component.tags
                for tag in tags:
                    keywords.extend(self._tokenize(str(tag)))
            except (json.JSONDecodeError, TypeError):
                pass
                
        # Add namespace and type
        if component.namespace:
            keywords.append(component.namespace)
        if component.component_type:
            keywords.append(component.component_type)
            
        return list(set(keywords))

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into searchable keywords."""
        if not text:
            return []
            
        # Split on common delimiters and convert to lowercase
        import re
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        # Add partial matches for compound words
        result = set(tokens)
        for token in tokens:
            if len(token) > 3:
                # Add prefixes for autocomplete-style matching
                for i in range(3, len(token)):
                    result.add(token[:i])
                    
        return list(result)

    def search(
        self,
        query: str,
        components: List[Component],
        limit: int = 20,
        namespace_filter: Optional[str] = None,
        component_type_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """Enhanced semantic search with intelligent ranking."""
        
        if not self.component_cache:
            self.build_index(components)
            
        query_lower = query.lower().strip()
        if not query_lower:
            return []
            
        # Get query tokens
        query_tokens = self._tokenize(query_lower)
        
        # Score all components
        scored_results = []
        for component in components:
            # Apply filters
            if namespace_filter and component.namespace != namespace_filter:
                continue
            if component_type_filter and component.component_type != component_type_filter:
                continue
                
            score, match_type, matched_fields = self._score_component(
                component, query_lower, query_tokens
            )
            
            if score > 0:
                scored_results.append(SearchResult(
                    component=component,
                    score=score,
                    match_type=match_type,
                    matched_fields=matched_fields
                ))
        
        # Sort by score descending
        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:limit]

    def _score_component(
        self, 
        component: Component, 
        query: str, 
        query_tokens: List[str]
    ) -> Tuple[float, str, List[str]]:
        """Score a component's relevance to the query."""
        
        total_score = 0.0
        match_type = "partial"
        matched_fields = []
        
        # Exact name match gets highest score
        if component.name and component.name.lower() == query:
            return 100.0, "exact", ["name"]
            
        # Check each field for matches
        field_scores = {}
        
        # Name matching
        name_score = self._field_match_score(component.name, query, query_tokens)
        if name_score > 0:
            field_scores['name'] = name_score * self.category_weights['name']
            matched_fields.append('name')
            
        # Title matching
        title_score = self._field_match_score(component.title, query, query_tokens)
        if title_score > 0:
            field_scores['title'] = title_score * self.category_weights['title']
            matched_fields.append('title')
            
        # Description matching
        desc_score = self._field_match_score(component.description, query, query_tokens)
        if desc_score > 0:
            field_scores['description'] = desc_score * self.category_weights['description']
            matched_fields.append('description')
            
        # Tags matching
        tags_score = self._tags_match_score(component.tags, query, query_tokens)
        if tags_score > 0:
            field_scores['tags'] = tags_score * self.category_weights['tags']
            matched_fields.append('tags')
            
        # Calculate base score
        total_score = sum(field_scores.values())
        
        if total_score == 0:
            return 0.0, "none", []
            
        # Apply popularity boost
        popularity_boost = self._get_popularity_boost(component.name)
        total_score *= popularity_boost
        
        # Apply framework preference
        framework_boost = self.framework_weights.get(component.namespace, 1.0)
        total_score *= framework_boost
        
        # Determine match type
        if any(score > 0.8 for score in field_scores.values()):
            match_type = "strong"
        elif any(score > 0.5 for score in field_scores.values()):
            match_type = "good"
            
        return total_score, match_type, matched_fields

    def _field_match_score(self, field_value: Optional[str], query: str, query_tokens: List[str]) -> float:
        """Score how well a field matches the query."""
        if not field_value:
            return 0.0
            
        field_lower = field_value.lower()
        
        # Exact match
        if field_lower == query:
            return 1.0
            
        # Starts with query
        if field_lower.startswith(query):
            return 0.9
            
        # Contains exact query
        if query in field_lower:
            return 0.7
            
        # Token-based matching
        field_tokens = self._tokenize(field_lower)
        matched_tokens = sum(1 for token in query_tokens if token in field_tokens)
        
        if matched_tokens > 0:
            token_score = matched_tokens / len(query_tokens)
            return min(0.6, token_score)
            
        return 0.0

    def _tags_match_score(self, tags_json: Optional[str], query: str, query_tokens: List[str]) -> float:
        """Score tag matches."""
        if not tags_json:
            return 0.0
            
        try:
            tags = json.loads(tags_json) if isinstance(tags_json, str) else tags_json
            if not tags:
                return 0.0
                
            tag_strings = [str(tag).lower() for tag in tags]
            
            # Check for exact tag match
            if query in tag_strings:
                return 1.0
                
            # Check for partial matches
            max_score = 0.0
            for tag in tag_strings:
                score = self._field_match_score(tag, query, query_tokens)
                max_score = max(max_score, score)
                
            return max_score
            
        except (json.JSONDecodeError, TypeError):
            return 0.0

    def _get_popularity_boost(self, component_name: Optional[str]) -> float:
        """Get popularity boost for common components."""
        if not component_name:
            return 1.0
            
        name_lower = component_name.lower()
        
        # Direct popularity lookup
        for keyword, boost in self.popularity_scores.items():
            if keyword in name_lower:
                return 1.0 + (boost - 1.0) * 0.1  # Scale boost to 10%
                
        return 1.0

    def suggest_similar(self, component: Component, all_components: List[Component], limit: int = 5) -> List[Component]:
        """Suggest components similar to the given one."""
        if not component.name:
            return []
            
        # Use component name and type as query
        query_parts = []
        if component.name:
            query_parts.append(component.name)
        if component.component_type:
            query_parts.append(component.component_type)
            
        query = " ".join(query_parts)
        
        results = self.search(
            query=query,
            components=[c for c in all_components if c.id != component.id],
            limit=limit
        )
        
        return [result.component for result in results]

    def get_search_suggestions(self, partial_query: str, components: List[Component]) -> List[str]:
        """Get search suggestions for autocomplete."""
        if len(partial_query) < 2:
            return []
            
        suggestions = set()
        partial_lower = partial_query.lower()
        
        # Get suggestions from component names and common terms
        for component in components:
            if component.name and component.name.lower().startswith(partial_lower):
                suggestions.add(component.name)
                
            # Add suggestions from tags
            if component.tags:
                try:
                    tags = json.loads(component.tags) if isinstance(component.tags, str) else component.tags
                    for tag in tags:
                        tag_str = str(tag).lower()
                        if tag_str.startswith(partial_lower):
                            suggestions.add(tag_str)
                except (json.JSONDecodeError, TypeError):
                    pass
                    
        # Add popular search terms
        popular_terms = ['button', 'input', 'card', 'modal', 'table', 'form', 'navigation', 'list']
        for term in popular_terms:
            if term.startswith(partial_lower):
                suggestions.add(term)
                
        return sorted(list(suggestions))[:10]


# Global instance for easy access
semantic_search_engine = SemanticSearchEngine()