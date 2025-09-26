"""API endpoints for component providers."""

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


router = APIRouter(prefix="/api/v1", tags=["providers"])


class InstallPlanRequest(BaseModel):
    """Request model for install plan generation."""
    component_id: str
    target_framework: Optional[str] = "react"
    tailwind_version: Optional[TailwindVersion] = TailwindVersion.V3
    package_manager: Optional[str] = "npm"


class InstallPlanResponse(BaseModel):
    """Response model for install plan."""
    component_id: str
    steps: List[Dict[str, Any]]
    dependencies: List[str]
    peer_dependencies: List[str]
    config_patches: List[Dict[str, Any]]
    cli_commands: List[str]
    estimated_time: str


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
        total_count = 0
        
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
        # Sort by popularity score and name
        all_components.sort(key=lambda x: (-x.popularity_score, x.name))
        
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


@router.post("/install-plan", response_model=InstallPlanResponse)
async def generate_install_plan(request: InstallPlanRequest):
    """Generate installation plan for a component."""
    try:
        # Get component
        if "/" not in request.component_id:
            raise HTTPException(status_code=400, detail="Component ID must be in format 'provider/slug'")
        
        provider_name, slug = request.component_id.split("/", 1)
        
        try:
            provider_enum = Provider(provider_name)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' not found")
        
        provider_instance = get_provider(provider_enum)
        component = await provider_instance.get_component(slug)
        
        # Generate install plan
        steps = []
        config_patches = []
        cli_commands = []
        
        # Add npm installation steps
        if component.runtime_deps:
            package_manager = request.package_manager or "npm"
            install_cmd = f"{package_manager} install {' '.join(component.runtime_deps)}"
            steps.append({
                "type": "install_dependencies",
                "command": install_cmd,
                "description": f"Install runtime dependencies",
                "dependencies": component.runtime_deps
            })
            cli_commands.append(install_cmd)
        
        # Add peer dependencies
        if component.peer_deps:
            package_manager = request.package_manager or "npm"
            peer_cmd = f"{package_manager} install {' '.join(component.peer_deps)}"
            steps.append({
                "type": "install_peer_dependencies", 
                "command": peer_cmd,
                "description": "Install peer dependencies",
                "dependencies": component.peer_deps
            })
            cli_commands.append(peer_cmd)
        
        # Add Tailwind configuration
        if component.tailwind:
            if component.tailwind.plugin_deps:
                plugin_cmd = f"{request.package_manager or 'npm'} install -D {' '.join(component.tailwind.plugin_deps)}"
                steps.append({
                    "type": "install_tailwind_plugins",
                    "command": plugin_cmd,
                    "description": "Install Tailwind plugins",
                    "dependencies": component.tailwind.plugin_deps
                })
                cli_commands.append(plugin_cmd)
                
                # Add config patch for plugins
                # Create plugin requires string
                plugin_requires = ', '.join([f'require("{plugin}")' for plugin in component.tailwind.plugin_deps])
                config_patches.append({
                    "file": "tailwind.config.js",
                    "type": "add_plugins",
                    "plugins": component.tailwind.plugin_deps,
                    "patch": f'plugins: [{plugin_requires}]'
                })
            
            # Version compatibility check
            if component.tailwind.version != request.tailwind_version:
                steps.append({
                    "type": "warning",
                    "description": f"Component is designed for Tailwind {component.tailwind.version.value}, but you're using {request.tailwind_version.value}. Some styles may not work correctly."
                })
        
        # Add CLI command if available
        if component.access.cli:
            steps.append({
                "type": "cli_install",
                "command": component.access.cli,
                "description": f"Install {component.name} via CLI",
                "preferred": True
            })
            cli_commands.append(component.access.cli)
        
        # Add code file creation
        if component.code.tsx or component.code.jsx:
            code_content = component.code.tsx or component.code.jsx
            filename = f"components/{component.slug}.tsx" if component.code.tsx else f"components/{component.slug}.jsx"
            
            steps.append({
                "type": "create_file",
                "file_path": filename,
                "content": code_content,
                "description": f"Create {component.name} component file"
            })
        
        # Estimate installation time
        estimated_minutes = len(component.runtime_deps) + len(component.peer_deps) + (2 if component.access.cli else 1)
        estimated_time = f"{estimated_minutes}-{estimated_minutes + 2} minutes"
        
        return InstallPlanResponse(
            component_id=request.component_id,
            steps=steps,
            dependencies=component.runtime_deps,
            peer_dependencies=component.peer_deps,
            config_patches=config_patches,
            cli_commands=cli_commands,
            estimated_time=estimated_time
        )
        
    except ComponentNotFoundError:
        raise HTTPException(status_code=404, detail=f"Component '{request.component_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate install plan: {str(e)}")


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
                    category = component.category.value
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