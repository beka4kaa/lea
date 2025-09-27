"""Base provider interface and abstract classes."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.component_manifest import (
    ComponentManifest,
    ComponentSearchFilter,
    ComponentSearchResult,
    Provider
)


class ProviderError(Exception):
    """Base exception for provider errors."""
    pass


class ProviderNotFoundError(ProviderError):
    """Raised when a provider is not found."""
    pass


class ComponentNotFoundError(ProviderError):
    """Raised when a component is not found."""
    pass


class ProviderRateLimitError(ProviderError):
    """Raised when provider rate limit is exceeded."""
    pass


class BaseProvider(ABC):
    """Abstract base class for all component providers."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize provider with configuration."""
        self.config = config or {}
        self._cache: Dict[str, Any] = {}
        self._last_sync: Optional[datetime] = None
    
    @property
    @abstractmethod
    def provider_name(self) -> Provider:
        """Get provider name."""
        pass
    
    @property
    @abstractmethod
    def base_url(self) -> str:
        """Get base URL for the provider."""
        pass
    
    @property
    def supports_cli(self) -> bool:
        """Whether provider supports CLI installation."""
        return False
    
    @property
    def supports_search(self) -> bool:
        """Whether provider supports search functionality."""
        return True
    
    @property
    def requires_auth(self) -> bool:
        """Whether provider requires authentication."""
        return False
    
    @abstractmethod
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List all available components."""
        pass
    
    @abstractmethod
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get a specific component by ID."""
        pass
    
    async def search_components(
        self,
        filters: ComponentSearchFilter
    ) -> ComponentSearchResult:
        """Search components with filters."""
        # Default implementation - can be overridden by providers
        all_components = await self.list_components(
            limit=filters.limit,
            offset=filters.offset
        )
        
        # Apply filters
        filtered = []
        for component in all_components:
            if self._matches_filter(component, filters):
                filtered.append(component)
        
        return ComponentSearchResult(
            components=filtered[:filters.limit],
            total=len(filtered),
            limit=filters.limit,
            offset=filters.offset,
            filters=filters
        )
    
    def _matches_filter(
        self,
        component: ComponentManifest,
        filters: ComponentSearchFilter
    ) -> bool:
        """Check if component matches the search filters."""
        # Provider filter
        if filters.provider and component.provider != filters.provider:
            return False
        
        # Category filter
        if filters.category and component.category != filters.category:
            return False
        
        # Tags filter
        if filters.tags:
            component_tags = set(component.tags)
            filter_tags = set(filters.tags)
            if not filter_tags.intersection(component_tags):
                return False
        
        # Framework filter
        if filters.framework:
            framework_dict = component.framework.dict()
            if not framework_dict.get(filters.framework, False):
                return False
        
        # Tailwind version filter
        if filters.tailwind_version and component.tailwind:
            if component.tailwind.version != filters.tailwind_version:
                return False
        
        # Free only filter
        if filters.free_only and component.requires_pro_access():
            return False
        
        # Query filter (enhanced text search with synonyms)
        if filters.query:
            query_lower = filters.query.lower()
            
            # Define search aliases and synonyms
            search_aliases = {
                'cta': ['call to action', 'call-to-action', 'get started', 'sign up', 'register', 'start trial'],
                'call to action': ['cta', 'get started', 'sign up', 'register'],
                'features': ['features section', 'product features', 'why choose us', 'feature grid'],
                'features section': ['features', 'product features', 'feature grid'],  
                'testimonials': ['reviews', 'customer feedback', 'social proof', 'customer testimonials'],
                'reviews': ['testimonials', 'customer feedback', 'social proof'],
                'footer': ['site footer', 'page footer', 'bottom navigation'],
                'navigation': ['navbar', 'nav', 'menu', 'header'],
                'navbar': ['navigation', 'nav', 'menu', 'header'],
                'get started': ['cta', 'call to action', 'sign up', 'register', 'start trial'],
                'pricing': ['price', 'plans', 'subscription', 'cost'],
                'auth': ['authentication', 'login', 'signin', 'signup', 'register'],
                'hero': ['hero section', 'landing', 'banner', 'main section'],
                'dashboard': ['admin', 'panel', 'control panel', 'admin panel']
            }
            
            # Expand query with synonyms
            expanded_queries = [query_lower]
            if query_lower in search_aliases:
                expanded_queries.extend(search_aliases[query_lower])
            
            # Build searchable text
            searchable_text = " ".join([
                component.name,
                component.description or "",
                " ".join(component.tags),
                " ".join(component.keywords),
                component.slug,
                component.category
            ]).lower()
            
            # Check if any expanded query matches
            found_match = False
            for expanded_query in expanded_queries:
                if expanded_query in searchable_text:
                    found_match = True
                    break
            
            if not found_match:
                return False
        
        return True
    
    async def sync_components(self, force: bool = False) -> int:
        """Sync components from provider source."""
        # Check if sync is needed
        if not force and self._last_sync:
            time_since_sync = datetime.utcnow() - self._last_sync
            if time_since_sync.total_seconds() < 3600:  # 1 hour
                return 0
        
        # Perform sync
        components = await self.list_components(limit=10000)  # Get all
        self._last_sync = datetime.utcnow()
        
        return len(components)
    
    def get_cache_key(self, *args) -> str:
        """Generate cache key from arguments."""
        return ":".join(str(arg) for arg in args)
    
    def clear_cache(self):
        """Clear provider cache."""
        self._cache.clear()


class HTTPProvider(BaseProvider):
    """Base class for HTTP-based providers."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._session = None
    
    async def _get_session(self):
        """Get or create HTTP session."""
        if self._session is None:
            import aiohttp
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def _request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request."""
        session = await self._get_session()
        
        try:
            async with session.request(method, url, **kwargs) as response:
                if response.status == 429:
                    raise ProviderRateLimitError(f"Rate limit exceeded for {self.provider_name}")
                
                response.raise_for_status()
                return await response.json()
                
        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            raise ProviderError(f"HTTP request failed: {e}")
    
    async def cleanup(self):
        """Cleanup HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None


class GitHubProvider(HTTPProvider):
    """Base class for GitHub-based providers."""
    
    @property
    def github_repo(self) -> str:
        """Get GitHub repository (owner/repo)."""
        raise NotImplementedError
    
    @property
    def github_api_url(self) -> str:
        """Get GitHub API URL."""
        return f"https://api.github.com/repos/{self.github_repo}"
    
    async def get_file_content(
        self,
        file_path: str,
        ref: str = "main"
    ) -> str:
        """Get file content from GitHub."""
        url = f"{self.github_api_url}/contents/{file_path}"
        params = {"ref": ref}
        
        data = await self._request("GET", url, params=params)
        
        if data.get("encoding") == "base64":
            import base64
            return base64.b64decode(data["content"]).decode("utf-8")
        
        return data.get("content", "")
    
    async def get_directory_listing(
        self,
        directory_path: str = "",
        ref: str = "main"
    ) -> List[Dict[str, Any]]:
        """Get directory listing from GitHub."""
        url = f"{self.github_api_url}/contents/{directory_path}"
        params = {"ref": ref}
        
        return await self._request("GET", url, params=params)