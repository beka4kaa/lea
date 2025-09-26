"""Provider registry and factory."""

from typing import Dict, Type, Optional, List
from .base import BaseProvider, ProviderNotFoundError
from ..models.component_manifest import Provider


class ProviderRegistry:
    """Registry for component providers."""
    
    def __init__(self):
        self._providers: Dict[Provider, Type[BaseProvider]] = {}
        self._instances: Dict[Provider, BaseProvider] = {}
    
    def register(self, provider_class: Type[BaseProvider]):
        """Register a provider class."""
        # Get provider name from class
        instance = provider_class()
        provider_name = instance.provider_name
        self._providers[provider_name] = provider_class
    
    def get_provider(self, provider_name: Provider) -> BaseProvider:
        """Get provider instance."""
        if provider_name not in self._instances:
            if provider_name not in self._providers:
                raise ProviderNotFoundError(f"Provider {provider_name} not found")
            
            provider_class = self._providers[provider_name]
            self._instances[provider_name] = provider_class()
        
        return self._instances[provider_name]
    
    def list_providers(self) -> List[Provider]:
        """List all registered providers."""
        return list(self._providers.keys())
    
    def is_registered(self, provider_name: Provider) -> bool:
        """Check if provider is registered."""
        return provider_name in self._providers


# Global registry instance
registry = ProviderRegistry()


def register_provider(provider_class: Type[BaseProvider]):
    """Decorator to register a provider."""
    registry.register(provider_class)
    return provider_class


def get_provider(provider_name: Provider) -> BaseProvider:
    """Get provider instance."""
    return registry.get_provider(provider_name)


def get_all_providers() -> List[BaseProvider]:
    """Get all registered provider instances."""
    providers = []
    for provider_name in registry.list_providers():
        providers.append(registry.get_provider(provider_name))
    return providers