"""Search functionality for components."""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy import select, or_, and_, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from mcp_ui_aggregator.models.database import Component, ComponentType, Namespace
from mcp_ui_aggregator.core.database import async_session_maker


class ComponentSearchEngine:
    """Full-text search engine for components."""
    
    def __init__(self):
        self.stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
            'have', 'had', 'what', 'said', 'each', 'which', 'she', 'do', 'how',
            'their', 'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so',
            'some', 'her', 'would', 'make', 'like', 'into', 'him', 'time',
            'two', 'more', 'very', 'when', 'come', 'may', 'its', 'only',
            'other', 'new', 'years', 'could', 'there', 'my', 'than', 'first',
            'been', 'call', 'who', 'oil', 'sit', 'now', 'find', 'down', 'day',
            'did', 'get', 'come', 'made', 'may', 'part'
        }
    
    def preprocess_query(self, query: str) -> List[str]:
        """Preprocess search query into terms."""
        # Convert to lowercase and split
        terms = re.findall(r'\b\w+\b', query.lower())
        
        # Remove stopwords and short terms
        terms = [term for term in terms if term not in self.stopwords and len(term) > 2]
        
        return terms
    
    async def search_components(
        self,
        query: str,
        namespace: Optional[str] = None,
        component_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Search for components using full-text search."""
        async with async_session_maker() as session:
            # Preprocess query
            terms = self.preprocess_query(query)
            if not terms:
                return {"results": [], "total": 0, "query": query}
            
            # Build search conditions
            search_conditions = []
            
            for term in terms:
                term_pattern = f"%{term}%"
                term_conditions = [
                    Component.name.ilike(term_pattern),
                    Component.title.ilike(term_pattern),
                    Component.description.ilike(term_pattern),
                    Component.tags.ilike(term_pattern),
                ]
                search_conditions.append(or_(*term_conditions))
            
            # Base query
            base_query = select(Component).where(
                and_(
                    Component.is_active == True,
                    *search_conditions
                )
            )
            
            # Apply filters
            if namespace:
                base_query = base_query.where(Component.namespace == namespace)
            
            if component_type:
                base_query = base_query.where(Component.component_type == component_type)
            
            # Get total count
            count_query = select(func.count(Component.id)).select_from(base_query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()
            
            # Apply ordering and pagination
            # Order by relevance: exact name matches first, then title, then description
            ordered_query = base_query.order_by(
                # Exact name match gets highest priority
                func.lower(Component.name) == query.lower(),
                # Name starts with query
                Component.name.ilike(f"{query}%"),
                # Title contains query
                Component.title.ilike(f"%{query}%"),
                # Shorter names first (more specific)
                func.length(Component.name).asc(),
                Component.name.asc()
            ).offset(offset).limit(limit)
            
            result = await session.execute(ordered_query)
            components = result.scalars().all()
            
            # Calculate relevance scores
            results = []
            for comp in components:
                score = self._calculate_relevance_score(comp, query, terms)
                results.append({
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "component_type": comp.component_type,
                    "title": comp.title,
                    "description": comp.description,
                    "tags": json.loads(comp.tags) if comp.tags else [],
                    "documentation_url": comp.documentation_url,
                    "relevance_score": score,
                    "created_at": comp.created_at.isoformat() if comp.created_at else None,
                })
            
            # Sort by relevance score (descending)
            results.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return {
                "query": query,
                "terms": terms,
                "results": results,
                "total": total,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + len(results) < total
                }
            }
    
    def _calculate_relevance_score(self, component: Component, query: str, terms: List[str]) -> float:
        """Calculate relevance score for a component."""
        score = 0.0
        query_lower = query.lower()
        
        # Exact name match
        if component.name.lower() == query_lower:
            score += 100.0
        
        # Name starts with query
        elif component.name.lower().startswith(query_lower):
            score += 50.0
        
        # Name contains query
        elif query_lower in component.name.lower():
            score += 25.0
        
        # Title exact match
        if component.title and component.title.lower() == query_lower:
            score += 75.0
        
        # Title contains query
        elif component.title and query_lower in component.title.lower():
            score += 15.0
        
        # Description contains query
        if component.description and query_lower in component.description.lower():
            score += 10.0
        
        # Tags contain query terms
        if component.tags:
            try:
                tags = json.loads(component.tags)
                for tag in tags:
                    if query_lower in tag.lower():
                        score += 5.0
            except:
                pass
        
        # Term-based scoring
        for term in terms:
            # Name contains term
            if term in component.name.lower():
                score += 20.0
            
            # Title contains term
            if component.title and term in component.title.lower():
                score += 10.0
            
            # Description contains term
            if component.description and term in component.description.lower():
                score += 5.0
        
        # Length penalty (shorter names are more relevant)
        if component.name:
            score += max(0, 50 - len(component.name))
        
        return round(score, 2)
    
    async def get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """Get search suggestions based on partial query."""
        async with async_session_maker() as session:
            query_pattern = f"{query}%"
            
            # Get component names that start with query
            name_query = select(Component.name).where(
                and_(
                    Component.is_active == True,
                    Component.name.ilike(query_pattern)
                )
            ).limit(limit)
            
            result = await session.execute(name_query)
            suggestions = [row[0] for row in result.fetchall()]
            
            # Also get from titles if we don't have enough suggestions
            if len(suggestions) < limit:
                title_query = select(Component.title).where(
                    and_(
                        Component.is_active == True,
                        Component.title.ilike(f"%{query}%"),
                        Component.name.notilike(query_pattern)  # Exclude already found
                    )
                ).limit(limit - len(suggestions))
                
                result = await session.execute(title_query)
                title_suggestions = [row[0] for row in result.fetchall()]
                suggestions.extend(title_suggestions)
            
            return suggestions[:limit]
    
    async def get_popular_components(self, namespace: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get popular/recommended components."""
        async with async_session_maker() as session:
            # For now, we'll use creation date as proxy for popularity
            # In a real system, this would be based on usage analytics
            query = select(Component).where(Component.is_active == True)
            
            if namespace:
                query = query.where(Component.namespace == namespace)
            
            # Order by creation date (newer first) and name
            query = query.order_by(Component.created_at.desc(), Component.name.asc()).limit(limit)
            
            result = await session.execute(query)
            components = result.scalars().all()
            
            return [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "component_type": comp.component_type,
                    "title": comp.title,
                    "description": comp.description,
                    "documentation_url": comp.documentation_url,
                }
                for comp in components
            ]


class VectorSearchEngine:
    """Vector search engine for semantic component search."""
    
    def __init__(self):
        self.model = None
        self.embeddings_cache = {}
    
    async def initialize(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the vector search engine (optional feature)."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            return True
        except ImportError:
            print("sentence-transformers not installed. Vector search disabled.")
            return False
    
    def encode_text(self, text: str) -> Optional[List[float]]:
        """Encode text to vector embeddings."""
        if not self.model:
            return None
        
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        try:
            embedding = self.model.encode(text).tolist()
            self.embeddings_cache[text] = embedding
            return embedding
        except Exception as e:
            print(f"Error encoding text: {e}")
            return None
    
    async def vector_search(
        self,
        query: str,
        namespace: Optional[str] = None,
        component_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Perform vector-based semantic search."""
        if not self.model:
            return []
        
        # Encode query
        query_embedding = self.encode_text(query)
        if not query_embedding:
            return []
        
        async with async_session_maker() as session:
            # Get all components (this would be optimized with a vector database in production)
            base_query = select(Component).where(Component.is_active == True)
            
            if namespace:
                base_query = base_query.where(Component.namespace == namespace)
            
            if component_type:
                base_query = base_query.where(Component.component_type == component_type)
            
            result = await session.execute(base_query)
            components = result.scalars().all()
            
            # Calculate similarities
            similarities = []
            for comp in components:
                # Create searchable text
                search_text = f"{comp.name} {comp.title} {comp.description or ''}"
                comp_embedding = self.encode_text(search_text)
                
                if comp_embedding:
                    similarity = self._cosine_similarity(query_embedding, comp_embedding)
                    similarities.append((comp, similarity))
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for comp, similarity in similarities[:limit]:
                results.append({
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "component_type": comp.component_type,
                    "title": comp.title,
                    "description": comp.description,
                    "documentation_url": comp.documentation_url,
                    "similarity_score": round(similarity, 4),
                })
            
            return results
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


# Global search engine instances
text_search = ComponentSearchEngine()
vector_search = VectorSearchEngine()