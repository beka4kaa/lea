"""Simplified API endpoints for component providers."""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.component_manifest import (
    ComponentManifest,
    ComponentSearchFilter,
    ComponentSearchResult,
    Provider,
    ComponentCategory,
    TailwindVersion
)
from ..providers import registry, get_provider
from ..providers.base import ComponentNotFoundError, ProviderError


router = APIRouter(tags=["providers"])


@router.get("/providers", response_model=List[str])
async def list_providers():
    """List all available component providers."""
    return [provider.value for provider in registry.list_providers()]


@router.get("/components", response_model=ComponentSearchResult)
async def search_components(
    provider: Optional[Provider] = Query(None, description="Filter by provider"),
    category: Optional[ComponentCategory] = Query(None, description="Filter by category"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    framework: Optional[str] = Query(None, description="Filter by framework (react, vue, etc.)"),
    tailwind_version: Optional[TailwindVersion] = Query(None, description="Filter by Tailwind version"),
    free_only: bool = Query(False, description="Show only free components"),
    q: Optional[str] = Query(None, description="Search query"),
    limit: int = Query(50, ge=1, le=200, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """Search components across all providers."""
    try:
        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        # Create search filter
        search_filter = ComponentSearchFilter(
            provider=provider,
            category=category,
            tags=tag_list,
            framework=framework,
            tailwind_version=tailwind_version,
            free_only=free_only,
            query=q,
            limit=limit,
            offset=offset
        )
        
        # If provider is specified, search only that provider
        if provider:
            provider_instance = get_provider(provider)
            return await provider_instance.search_components(search_filter)
        
        # Search across all providers
        all_components = []
        
        for provider_name in registry.list_providers():
            try:
                provider_instance = get_provider(provider_name)
                # Create a filter for this provider
                provider_filter = ComponentSearchFilter(
                    provider=provider_name,
                    category=search_filter.category,
                    tags=search_filter.tags,
                    framework=search_filter.framework,
                    tailwind_version=search_filter.tailwind_version,
                    free_only=search_filter.free_only,
                    query=search_filter.query,
                    limit=1000,  # Get all from provider
                    offset=0
                )
                
                result = await provider_instance.search_components(provider_filter)
                all_components.extend(result.components)
                
            except Exception as e:
                # Log error but continue with other providers
                print(f"Error searching provider {provider_name}: {e}")
                continue
        
        # Apply global sorting and pagination
                # Sort by popularity and name
        all_components.sort(key=lambda x: (-getattr(x, 'popularity_score', 0.0), x.name))
        
        # Apply pagination
        start = offset
        end = offset + limit
        paginated_components = all_components[start:end]
        
        return ComponentSearchResult(
            components=paginated_components,
            total=len(all_components),
            limit=limit,
            offset=offset,
            filters=search_filter
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/components/{component_id}", response_model=ComponentManifest)
async def get_component(component_id: str):
    """Get a specific component by ID (provider/slug format)."""
    try:
        # Parse component ID
        if "/" not in component_id:
            raise HTTPException(status_code=400, detail="Component ID must be in format 'provider/slug'")
        
        provider_name, slug = component_id.split("/", 1)
        
        try:
            provider_enum = Provider(provider_name)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' not found")
        
        # Get provider and component
        provider_instance = get_provider(provider_enum)
        component = await provider_instance.get_component(slug)
        
        return component
        
    except ComponentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Component '{component_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get component: {str(e)}")


@router.get("/components/{provider}/{component}/code")
async def get_component_code(
    provider: str, 
    component: str, 
    format: Optional[str] = Query("tsx", description="Code format (tsx, jsx, vue, etc.)")
):
    """Get component source code."""
    try:
        # Parse provider
        try:
            provider_enum = Provider(provider)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Provider '{provider}' not found")
        
        # Get provider and component
        provider_instance = get_provider(provider_enum)
        component_manifest = await provider_instance.get_component(component)
        
        # Extract code in requested format
        code_data = component_manifest.code
        if not code_data:
            raise HTTPException(status_code=404, detail=f"No code available for component '{provider}/{component}'")
        
        # Get code in requested format with intelligent fallback
        code = None
        actual_format = format
        
        # Try requested format first
        if format.lower() == "tsx" and code_data.tsx:
            code = code_data.tsx
        elif format.lower() == "jsx" and code_data.jsx:
            code = code_data.jsx
        elif format.lower() == "vue" and code_data.vue:
            code = code_data.vue
        elif format.lower() == "svelte" and code_data.svelte:
            code = code_data.svelte
        elif format.lower() == "html" and code_data.html:
            code = code_data.html
        elif format.lower() == "css" and code_data.css:
            code = code_data.css
        
        # If requested format not available, try fallback formats
        if not code:
            if code_data.tsx:
                code = code_data.tsx
                actual_format = "tsx"
            elif code_data.jsx:
                code = code_data.jsx
                actual_format = "jsx"
            elif code_data.vue:
                code = code_data.vue
                actual_format = "vue"
            elif code_data.svelte:
                code = code_data.svelte
                actual_format = "svelte"
            elif code_data.html:
                code = code_data.html
                actual_format = "html"
            elif code_data.css:
                code = code_data.css
                actual_format = "css"
        
        if not code:
            # Get available formats for better error message
            available_formats = []
            if code_data.tsx: available_formats.append("tsx")
            if code_data.jsx: available_formats.append("jsx")
            if code_data.vue: available_formats.append("vue")
            if code_data.svelte: available_formats.append("svelte")
            if code_data.html: available_formats.append("html")
            if code_data.css: available_formats.append("css")
            
            if available_formats:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Code not available in format '{format}' for component '{provider}/{component}'. Available formats: {', '.join(available_formats)}"
                )
            else:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No code available for component '{provider}/{component}'"
                )
        
        return {
            "component_id": f"{provider}/{component}",
            "format": actual_format,
            "requested_format": format,
            "code": code,
            "name": component_manifest.name,
            "description": component_manifest.description,
            "dependencies": component_manifest.runtime_deps,
            "framework": {
                "react": component_manifest.framework.react,
                "vue": component_manifest.framework.vue,
                "svelte": component_manifest.framework.svelte,
                "next": component_manifest.framework.next
            }
        }
        
    except ComponentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Component '{provider}/{component}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get component code: {str(e)}")


@router.get("/components/{provider}/{component}/docs")
async def get_component_docs(provider: str, component: str):
    """Get component documentation."""
    try:
        # Parse provider
        try:
            provider_enum = Provider(provider)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Provider '{provider}' not found")
        
        # Get provider and component
        provider_instance = get_provider(provider_enum)
        component_manifest = await provider_instance.get_component(component)
        
        return {
            "component_id": f"{provider}/{component}",
            "name": component_manifest.name,
            "description": component_manifest.description,
            "documentation_url": component_manifest.documentation_url,
            "demo_url": component_manifest.demo_url,
            "playground_url": component_manifest.playground_url,
            "tags": component_manifest.tags,
            "category": component_manifest.category,
            "framework": {
                "react": component_manifest.framework.react,
                "vue": component_manifest.framework.vue,
                "svelte": component_manifest.framework.svelte,
                "next": component_manifest.framework.next
            },
            "installation": {
                "npm": component_manifest.install.npm,
                "steps": component_manifest.install.steps
            },
            "dependencies": {
                "runtime": component_manifest.runtime_deps,
                "peer": component_manifest.peer_deps,
                "dev": component_manifest.dev_deps
            },
            "license": component_manifest.license,
            "examples": {
                "basic": f"import {{ {component_manifest.name.replace(' ', '')} }} from '@/components/{component}';",
                "usage": component_manifest.description
            }
        }
        
    except ComponentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Component '{provider}/{component}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get component docs: {str(e)}")


@router.get("/providers/{provider_name}/components", response_model=List[ComponentManifest])
async def list_provider_components(
    provider_name: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """List components from a specific provider."""
    try:
        provider_enum = Provider(provider_name)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' not found")
    
    try:
        provider_instance = get_provider(provider_enum)
        components = await provider_instance.list_components(limit=limit, offset=offset)
        
        return components
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list components: {str(e)}")


@router.get("/stats")
async def get_stats():
    """Get statistics about components and providers."""
    try:
        stats = {
            "providers": len(registry.list_providers()),
            "total_components": 0,
            "components_by_provider": {},
            "components_by_category": {},
            "free_components": 0,
            "pro_components": 0
        }
        
        category_counts = {}
        
        for provider_name in registry.list_providers():
            try:
                provider_instance = get_provider(provider_name)
                components = await provider_instance.list_components(limit=1000)
                
                provider_count = len(components)
                stats["total_components"] += provider_count
                stats["components_by_provider"][provider_name.value] = provider_count
                
                for component in components:
                    # Count by category
                    category = component.category
                    category_counts[category] = category_counts.get(category, 0) + 1
                    
                    # Count free vs pro
                    if component.requires_pro_access():
                        stats["pro_components"] += 1
                    else:
                        stats["free_components"] += 1
                        
            except Exception as e:
                print(f"Error getting stats for provider {provider_name}: {e}")
                continue
        
        stats["components_by_category"] = category_counts
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/providers/{provider_name}/sync")
async def sync_provider(provider_name: str, force: bool = Query(False)):
    """Sync components from a specific provider."""
    try:
        provider_enum = Provider(provider_name)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' not found")
    
    try:
        provider_instance = get_provider(provider_enum)
        synced_count = await provider_instance.sync_components(force=force)
        
        return {
            "provider": provider_name,
            "synced_components": synced_count,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.post("/render")
async def render_component(
    component_id: str,
    props: Optional[Dict[str, Any]] = None
):
    """Render component preview (placeholder for future implementation)."""
    # This would be implemented with a sandboxed React renderer
    # For now, return a placeholder response
    return {
        "component_id": component_id,
        "rendered": False,
        "message": "Component rendering not yet implemented",
        "props": props or {}
    }