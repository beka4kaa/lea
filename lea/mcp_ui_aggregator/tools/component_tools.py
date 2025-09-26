"""MCP tools for UI component management."""

from typing import Any, Dict, List, Optional, Sequence
import asyncio
import json

from mcp.server.models import *
from mcp.types import *
from sqlalchemy import select, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from mcp_ui_aggregator.models.database import Component, CodeExample, DocumentationSection
from mcp_ui_aggregator.core.database import async_session_maker
from mcp_ui_aggregator.ai.semantic_search import semantic_search_engine
from mcp_ui_aggregator.ai.component_recommendations import component_recommendation_engine
from mcp_ui_aggregator.ai.template_suggestions import template_suggestion_engine
from mcp_ui_aggregator.ai.code_analysis import code_analysis_engine
from mcp_ui_aggregator.themes import theme_registry
from mcp_ui_aggregator.themes.applicator import theme_applicator


async def list_components(
    namespace: Optional[str] = None,
    component_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """List UI components with optional filtering.
    
    Args:
        namespace: Filter by namespace (material, shadcn)
        component_type: Filter by component type
        limit: Maximum number of components to return
        offset: Number of components to skip
        
    Returns:
        Dict with components list and metadata
    """
    async with async_session_maker() as session:
        # Build query
        query = select(Component).where(Component.is_active == True)
        
        if namespace:
            query = query.where(Component.namespace == namespace)
        
        if component_type:
            query = query.where(Component.component_type == component_type)
        
        # Get total count
        count_query = select(func.count(Component.id)).where(Component.is_active == True)
        if namespace:
            count_query = count_query.where(Component.namespace == namespace)
        if component_type:
            count_query = count_query.where(Component.component_type == component_type)
        
        total_result = await session.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        query = query.offset(offset).limit(limit).order_by(Component.name)
        
        result = await session.execute(query)
        components = result.scalars().all()
        
        return {
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "component_type": comp.component_type,
                    "title": comp.title,
                    "description": comp.description,
                    "tags": json.loads(comp.tags) if comp.tags else [],
                    "documentation_url": comp.documentation_url,
                    "created_at": comp.created_at.isoformat() if comp.created_at else None,
                }
                for comp in components
            ],
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": offset + len(components) < total
            }
        }


async def search_component(
    query: str,
    namespace: Optional[str] = None,
    component_type: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """Search for UI components by name, title, description, or tags.
    
    Args:
        query: Search query string
        namespace: Filter by namespace
        component_type: Filter by component type
        limit: Maximum number of results
        
    Returns:
        Dict with search results and metadata
    """
    async with async_session_maker() as session:
        # Build search query
        search_conditions = [
            Component.name.ilike(f"%{query}%"),
            Component.title.ilike(f"%{query}%"),
            Component.description.ilike(f"%{query}%"),
            Component.tags.ilike(f"%{query}%"),
        ]
        
        base_query = select(Component).where(
            and_(
                Component.is_active == True,
                or_(*search_conditions)
            )
        )
        
        if namespace:
            base_query = base_query.where(Component.namespace == namespace)
        
        if component_type:
            base_query = base_query.where(Component.component_type == component_type)
        
        # Apply limit and ordering (relevance-based)
        base_query = base_query.limit(limit).order_by(
            # Prioritize name matches, then title, then description
            func.length(Component.name).asc(),
            Component.name.asc()
        )
        
        result = await session.execute(base_query)
        components = result.scalars().all()

        # Simple relevance scoring to rank exact name matches higher
        ql = query.lower()
        def score(comp: Component) -> float:
            name = (comp.name or "").lower()
            title = (comp.title or "").lower()
            desc = (comp.description or "").lower()
            s = 0.0
            if name == ql:
                s += 100.0
            elif name.startswith(ql):
                s += 50.0
            elif ql in name:
                s += 20.0
            if ql in title:
                s += 10.0
            if ql in desc:
                s += 5.0
            # Favor shorter names a bit
            s += max(0, 30 - len(name))
            return s

        scored = [
            (
                comp,
                score(comp)
            ) for comp in components
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        return {
            "query": query,
            "results": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "component_type": comp.component_type,
                    "title": comp.title,
                    "description": comp.description,
                    "tags": json.loads(comp.tags) if comp.tags else [],
                    "documentation_url": comp.documentation_url,
                    "relevance_score": round(sc, 2),
                }
                for comp, sc in scored
            ],
            "total_results": len(components)
        }


async def get_component_code(
    component_id: Optional[int] = None,
    component_name: Optional[str] = None,
    namespace: Optional[str] = None,
    include_examples: bool = True
) -> Dict[str, Any]:
    """Get code examples for a UI component.
    
    Args:
        component_id: Component ID
        component_name: Component name (requires namespace if provided)
        namespace: Component namespace
        include_examples: Whether to include code examples
        
    Returns:
        Dict with component code and examples
    """
    async with async_session_maker() as session:
        # Build query
        if component_id:
            query = select(Component).where(Component.id == component_id)
        elif component_name and namespace:
            query = select(Component).where(
                and_(
                    Component.name == component_name,
                    Component.namespace == namespace,
                    Component.is_active == True
                )
            )
        else:
            raise ValueError("Either component_id or (component_name + namespace) must be provided")
        
        if include_examples:
            query = query.options(selectinload(Component.code_examples))
        
        result = await session.execute(query)
        component = result.scalar_one_or_none()
        # Support AsyncMock returning coroutine in tests
        if asyncio.iscoroutine(component):  # type: ignore[name-defined]
            component = await component  # type: ignore[assignment]
        
        if not component:
            return {"error": "Component not found"}
        
        response = {
            "component": {
                "id": component.id,
                "name": component.name,
                "namespace": component.namespace,
                "title": component.title,
                "import_statement": component.import_statement,
                "basic_usage": component.basic_usage,
            },
            "examples": []
        }
        
        if include_examples and component.code_examples:
            response["examples"] = [
                {
                    "id": example.id,
                    "title": example.title,
                    "description": example.description,
                    "code": example.code,
                    "language": example.language,
                    "framework": example.framework,
                    "is_basic": example.is_basic,
                    "is_advanced": example.is_advanced,
                }
                for example in component.code_examples
            ]
        
        return response


async def get_component_docs(
    component_id: Optional[int] = None,
    component_name: Optional[str] = None,
    namespace: Optional[str] = None,
    section_type: Optional[str] = None
) -> Dict[str, Any]:
    """Get documentation for a UI component.
    
    Args:
        component_id: Component ID
        component_name: Component name (requires namespace if provided)
        namespace: Component namespace
        section_type: Filter by documentation section type
        
    Returns:
        Dict with component documentation
    """
    async with async_session_maker() as session:
        # Build query
        if component_id:
            query = select(Component).where(Component.id == component_id)
        elif component_name and namespace:
            query = select(Component).where(
                and_(
                    Component.name == component_name,
                    Component.namespace == namespace,
                    Component.is_active == True
                )
            )
        else:
            raise ValueError("Either component_id or (component_name + namespace) must be provided")
        
        query = query.options(selectinload(Component.docs_sections))
        
        result = await session.execute(query)
        component = result.scalar_one_or_none()
        if asyncio.iscoroutine(component):  # type: ignore[name-defined]
            component = await component  # type: ignore[assignment]
        
        if not component:
            return {"error": "Component not found"}
        
        # Filter documentation sections
        docs_sections = component.docs_sections
        if section_type:
            docs_sections = [
                section for section in docs_sections 
                if section.section_type == section_type
            ]
        
        # Sort by order_index
        docs_sections.sort(key=lambda x: x.order_index)
        
        return {
            "component": {
                "id": component.id,
                "name": component.name,
                "namespace": component.namespace,
                "title": component.title,
                "description": component.description,
                "documentation_url": component.documentation_url,
                "api_reference_url": component.api_reference_url,
                "examples_url": component.examples_url,
            },
            "documentation": [
                {
                    "id": section.id,
                    "title": section.title,
                    "content": section.content,
                    "section_type": section.section_type,
                    "order_index": section.order_index,
                }
                for section in docs_sections
            ]
        }


async def install_component(
    component_name: str,
    namespace: str,
    target_framework: str = "react",
    package_manager: str = "npm"
) -> Dict[str, Any]:
    """Get installation instructions for a UI component.
    
    Args:
        component_name: Name of the component to install
        namespace: Component namespace (material, shadcn)
        target_framework: Target framework (react, vue, etc.)
        package_manager: Package manager (npm, yarn, pnpm)
        
    Returns:
        Dict with installation instructions
    """
    async with async_session_maker() as session:
        # Get component
        query = select(Component).where(
            and_(
                Component.name == component_name,
                Component.namespace == namespace,
                Component.is_active == True
            )
        )
        
        result = await session.execute(query)
        component = result.scalar_one_or_none()
        if asyncio.iscoroutine(component):  # type: ignore[name-defined]
            component = await component  # type: ignore[assignment]
        
        if not component:
            return {"error": f"Component {namespace}/{component_name} not found"}
        
        # Generate installation instructions based on namespace
        if namespace == "material":
            package_name = "@mui/material"
            additional_packages = ["@emotion/react", "@emotion/styled"]
            
            if package_manager == "npm":
                install_cmd = f"npm install {package_name} {' '.join(additional_packages)}"
            elif package_manager == "yarn":
                install_cmd = f"yarn add {package_name} {' '.join(additional_packages)}"
            elif package_manager == "pnpm":
                install_cmd = f"pnpm add {package_name} {' '.join(additional_packages)}"
            else:
                install_cmd = f"npm install {package_name} {' '.join(additional_packages)}"
                
        elif namespace == "shadcn":
            # shadcn/ui uses a different installation pattern
            install_cmd = f"npx shadcn-ui@latest add {component_name.lower()}"
            additional_packages = []
            package_name = "@/components/ui"
            
        else:
            return {"error": f"Installation not supported for namespace: {namespace}"}
        
        return {
            "component": {
                "name": component_name,
                "namespace": namespace,
                "title": component.title,
            },
            "installation": {
                "package_manager": package_manager,
                "target_framework": target_framework,
                "install_command": install_cmd,
                "package_name": package_name,
                "additional_packages": additional_packages,
                "import_statement": component.import_statement,
                "basic_usage": component.basic_usage,
            },
            "next_steps": [
                "Run the installation command in your project directory",
                "Import the component in your code",
                "Use the component according to the basic usage example",
                f"Check the documentation for more examples: {component.documentation_url}",
            ]
        }


# Template Tools

async def list_templates() -> Dict[str, Any]:
    """List all available page templates.
    
    Returns:
        Dict with templates grouped by type
    """
    from mcp_ui_aggregator.templates.tools import get_template_variants
    
    try:
        variants = get_template_variants()
        return {
            "status": "success",
            "templates": variants,
            "message": f"Found {sum(len(templates) for templates in variants.values())} templates across {len(variants)} categories"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to list templates"
        }


async def get_template_info(template_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific template.
    
    Args:
        template_id: ID of the template to retrieve
        
    Returns:
        Dict with template structure and details
    """
    from mcp_ui_aggregator.templates.tools import preview_template_structure
    
    try:
        template_info = preview_template_structure(template_id)
        
        if "error" in template_info:
            return {
                "status": "error",
                "error": template_info["error"],
                "message": f"Template '{template_id}' not found"
            }
        
        return {
            "status": "success",
            "template": template_info,
            "message": f"Retrieved template '{template_id}' information"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to get template info for '{template_id}'"
        }


async def generate_template_code(template_id: str, customizations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate code from a template with optional customizations.
    
    Args:
        template_id: ID of the template to generate
        customizations: Optional customizations to apply
        
    Returns:
        Dict with generated code and setup instructions
    """
    from mcp_ui_aggregator.templates.tools import generate_template_code as gen_code
    
    try:
        result = gen_code(template_id, customizations)
        
        if "error" in result:
            return {
                "status": "error",
                "error": result["error"],
                "message": f"Failed to generate template '{template_id}'"
            }
        
        return {
            "status": "success",
            "generated": result,
            "message": f"Successfully generated code for template '{template_id}'"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to generate template '{template_id}'"
        }


async def customize_template(template_id: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Apply customizations to a template.
    
    Args:
        template_id: ID of the template to customize
        customizations: Customizations to apply
        
    Returns:
        Dict with customization results
    """
    from mcp_ui_aggregator.templates.tools import customize_template as custom_template
    
    try:
        result = custom_template(template_id, customizations)
        
        if "error" in result:
            return {
                "status": "error",
                "error": result["error"],
                "message": f"Failed to customize template '{template_id}'"
            }
        
        return {
            "status": "success",
            "customized": result,
            "message": f"Successfully customized template '{template_id}'"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to customize template '{template_id}'"
        }


# AI-Enhanced Tools

async def ai_search_components(
    query: str,
    limit: int = 10,
    namespace: Optional[str] = None,
    include_suggestions: bool = True
) -> Dict[str, Any]:
    """AI-powered semantic search for components.
    
    Args:
        query: Natural language search query
        limit: Maximum number of results
        namespace: Filter by namespace
        include_suggestions: Whether to include AI suggestions
        
    Returns:
        Dict with enhanced search results and suggestions
    """
    from mcp_ui_aggregator.ai.semantic_search import SemanticSearchEngine
    from mcp_ui_aggregator.ai.component_recommendations import ComponentRecommendationEngine
    
    try:
        async with async_session_maker() as session:
            # Get all active components
            query_obj = select(Component).where(Component.is_active == True)
            if namespace:
                query_obj = query_obj.where(Component.namespace == namespace)
            
            result = await session.execute(query_obj)
            components = result.scalars().all()
            
            # Perform semantic search
            search_engine = SemanticSearchEngine()
            search_results = search_engine.search(
                query=query,
                components=components,
                limit=limit,
                namespace_filter=namespace
            )
            
            # Get AI recommendations
            recommendations = []
            if include_suggestions:
                rec_engine = ComponentRecommendationEngine()
                recommendations = rec_engine.recommend_for_query(
                    query=query,
                    components=components,
                    limit=min(5, limit)
                )
            
            # Format results
            search_data = []
            for result in search_results:
                comp = result.component
                search_data.append({
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "title": comp.title,
                    "description": comp.description,
                    "tags": json.loads(comp.tags) if comp.tags else [],
                    "relevance_score": result.score,
                    "match_type": result.match_type,
                    "matched_fields": result.matched_fields
                })
            
            recommendation_data = []
            for rec in recommendations:
                comp = rec.component
                recommendation_data.append({
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "title": comp.title,
                    "confidence": rec.confidence,
                    "reason": rec.reason,
                    "category": rec.category,
                    "complementary_components": rec.complementary_components
                })
            
            return {
                "status": "success",
                "query": query,
                "search_results": search_data,
                "ai_recommendations": recommendation_data,
                "search_suggestions": search_engine.get_search_suggestions(query, components),
                "message": f"Found {len(search_data)} results with {len(recommendation_data)} AI recommendations"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to perform AI search for '{query}'"
        }


async def suggest_component_combinations(
    selected_components: List[str],
    project_type: Optional[str] = None,
    limit: int = 8
) -> Dict[str, Any]:
    """Suggest complementary components for selected ones.
    
    Args:
        selected_components: List of component names or IDs
        project_type: Type of project (landing, dashboard, etc.)
        limit: Maximum number of suggestions
        
    Returns:
        Dict with component combination suggestions
    """
    from mcp_ui_aggregator.ai.component_recommendations import ComponentRecommendationEngine
    
    try:
        async with async_session_maker() as session:
            # Get selected components
            if not selected_components:
                return {
                    "status": "error",
                    "error": "No components selected",
                    "message": "Please provide at least one component"
                }
            
            # Parse component identifiers (could be names or IDs)
            selected_comps = []
            for comp_id in selected_components:
                if comp_id.isdigit():
                    # It's an ID
                    query_obj = select(Component).where(Component.id == int(comp_id))
                else:
                    # It's a name
                    query_obj = select(Component).where(
                        and_(
                            Component.name.ilike(f"%{comp_id}%"),
                            Component.is_active == True
                        )
                    ).limit(1)
                
                result = await session.execute(query_obj)
                component = result.scalar_one_or_none()
                if component:
                    selected_comps.append(component)
            
            if not selected_comps:
                return {
                    "status": "error",
                    "error": "No valid components found",
                    "message": "None of the provided component identifiers were found"
                }
            
            # Get all components for recommendations
            all_query = select(Component).where(Component.is_active == True)
            result = await session.execute(all_query)
            all_components = result.scalars().all()
            
            # Get recommendations
            rec_engine = ComponentRecommendationEngine()
            recommendations = rec_engine.recommend_complementary(
                selected_components=selected_comps,
                all_components=all_components,
                limit=limit
            )
            
            # Format results
            suggestions = []
            for rec in recommendations:
                comp = rec.component
                suggestions.append({
                    "id": comp.id,
                    "name": comp.name,
                    "namespace": comp.namespace,
                    "title": comp.title,
                    "description": comp.description,
                    "confidence": rec.confidence,
                    "reason": rec.reason,
                    "category": rec.category,
                    "complementary_components": rec.complementary_components
                })
            
            return {
                "status": "success",
                "selected_components": [comp.name for comp in selected_comps],
                "suggestions": suggestions,
                "project_type": project_type,
                "message": f"Generated {len(suggestions)} complementary component suggestions"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to generate component suggestions"
        }


async def ai_suggest_templates(
    query: str,
    framework: Optional[str] = None,
    project_context: Optional[Dict[str, Any]] = None,
    limit: int = 6
) -> Dict[str, Any]:
    """AI-powered template suggestions based on user intent.
    
    Args:
        query: Natural language description of needs
        framework: Preferred framework (react, vue, html)
        project_context: Additional context (industry, timeline, etc.)
        limit: Maximum number of suggestions
        
    Returns:
        Dict with intelligent template suggestions
    """
    from mcp_ui_aggregator.ai.template_suggestions import TemplateSuggestionEngine
    
    try:
        suggestion_engine = TemplateSuggestionEngine()
        
        suggestions = suggestion_engine.suggest_for_query(
            query=query,
            preferred_framework=framework,
            user_context=project_context,
            limit=limit
        )
        
        # Format suggestions
        suggestion_data = []
        for suggestion in suggestions:
            suggestion_data.append({
                "template_id": suggestion.template_id,
                "template_name": suggestion.template_name,
                "framework": suggestion.framework.value,
                "template_type": suggestion.template_type.value,
                "confidence": suggestion.confidence,
                "reason": suggestion.reason,
                "use_cases": suggestion.use_cases,
                "estimated_complexity": suggestion.estimated_complexity,
                "estimated_time": suggestion.estimated_time
            })
        
        return {
            "status": "success",
            "query": query,
            "suggestions": suggestion_data,
            "framework_preference": framework,
            "project_context": project_context,
            "message": f"Generated {len(suggestion_data)} AI-powered template suggestions"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to generate template suggestions for '{query}'"
        }


async def analyze_generated_code(
    code: str,
    framework: str,
    template_type: Optional[str] = None,
    target_quality: str = "good"
) -> Dict[str, Any]:
    """Analyze generated code quality and provide improvement suggestions.
    
    Args:
        code: Generated code to analyze
        framework: Framework used (react, vue, html)
        template_type: Type of template (landing, dashboard, etc.)
        target_quality: Target quality level (excellent, good, average)
        
    Returns:
        Dict with code analysis and improvement suggestions
    """
    from mcp_ui_aggregator.ai.code_analysis import CodeAnalysisEngine, CodeQuality
    
    try:
        analyzer = CodeAnalysisEngine()
        
        # Perform analysis
        analysis = analyzer.analyze_generated_code(
            code=code,
            framework=framework,
            template_type=template_type
        )
        
        # Get improvement suggestions
        quality_map = {
            "excellent": CodeQuality.EXCELLENT,
            "good": CodeQuality.GOOD,
            "average": CodeQuality.AVERAGE
        }
        target = quality_map.get(target_quality.lower(), CodeQuality.GOOD)
        
        improvements = analyzer.suggest_improvements(
            code=code,
            framework=framework,
            target_quality=target
        )
        
        # Get performance optimizations
        performance = analyzer.optimize_for_performance(code, framework)
        
        # Format results
        suggestions_data = []
        for suggestion in analysis.suggestions:
            suggestions_data.append({
                "type": suggestion.type,
                "severity": suggestion.severity,
                "description": suggestion.description,
                "example": suggestion.example,
                "auto_fixable": suggestion.auto_fixable
            })
        
        return {
            "status": "success",
            "analysis": {
                "quality_score": analysis.quality_score,
                "quality_level": analysis.quality_level.value,
                "metrics": analysis.metrics,
                "best_practices_followed": analysis.best_practices,
                "potential_issues": analysis.potential_issues
            },
            "suggestions": suggestions_data,
            "improvements": improvements,
            "performance_optimizations": performance,
            "message": f"Code analysis complete - Quality: {analysis.quality_level.value} ({analysis.quality_score:.1f}/100)"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to analyze code: {str(e)}",
            "analysis": None,
            "suggestions": [],
            "improvements": [],
            "performance_optimizations": []
        }


async def list_available_themes_tool(
    project_type: Optional[str] = None,
    industry: Optional[str] = None,
    include_preview: bool = True
) -> Dict[str, Any]:
    """List all available themes with suggestions."""
    
    try:
        # Get all themes
        all_themes = theme_registry.list_themes()
        
        # Get theme suggestions if context provided
        suggestions = []
        if project_type:
            suggestions = theme_applicator.get_theme_suggestions(project_type, industry)
        
        themes_data = []
        for theme in all_themes:
            theme_data = {
                "id": theme.id,
                "name": theme.name,
                "description": theme.description,
                "category": theme.category.value,
                "colors": {
                    "primary": theme.colors.primary,
                    "secondary": theme.colors.secondary,
                    "accent": theme.colors.accent,
                    "background": theme.colors.background,
                    "surface": theme.colors.surface,
                    "text_primary": theme.colors.text_primary
                }
            }
            
            if include_preview:
                theme_data["preview"] = {
                    "color_palette": [
                        theme.colors.primary,
                        theme.colors.secondary,
                        theme.colors.accent,
                        theme.colors.background,
                        theme.colors.surface
                    ],
                    "typography": {
                        "primary_font": theme.typography.font_family_primary,
                        "font_size": theme.typography.font_size_base
                    },
                    "spacing": {
                        "small": theme.spacing.sm,
                        "medium": theme.spacing.md,
                        "large": theme.spacing.lg
                    }
                }
            
            themes_data.append(theme_data)
        
        return {
            "themes": themes_data,
            "suggestions": suggestions,
            "total_count": len(all_themes),
            "message": f"Found {len(all_themes)} available themes"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to list themes: {str(e)}",
            "themes": [],
            "suggestions": []
        }


async def apply_theme_to_template_tool(
    template_id: str,
    theme_id: str,
    framework: str,
    customizations: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Apply a theme to a template."""
    
    try:
        from mcp_ui_aggregator.templates import template_registry
        from mcp_ui_aggregator.templates import Framework
        
        # Get template and theme
        template = template_registry.get_template(template_id)
        if not template:
            return {
                "error": f"Template '{template_id}' not found",
                "themed_template": None
            }
        
        theme = theme_registry.get_theme(theme_id)
        if not theme:
            return {
                "error": f"Theme '{theme_id}' not found",
                "themed_template": None
            }
        
        # Convert framework string to enum
        framework_map = {
            "react": Framework.REACT,
            "vue": Framework.VUE,
            "html": Framework.HTML
        }
        
        if framework not in framework_map:
            return {
                "error": f"Unsupported framework: {framework}",
                "themed_template": None
            }
        
        framework_enum = framework_map[framework]
        
        # Apply customizations to theme if provided
        if customizations:
            import copy
            theme = copy.deepcopy(theme)
            
            if "primary_color" in customizations:
                theme.colors.primary = customizations["primary_color"]
            if "secondary_color" in customizations:
                theme.colors.secondary = customizations["secondary_color"]
            if "font_family" in customizations:
                theme.typography.font_family_primary = customizations["font_family"]
        
        # Apply theme to template
        themed_template = theme_applicator.apply_theme_to_template(
            template, theme, include_css_variables=True
        )
        
        # Convert to serializable format
        template_data = {
            "id": themed_template.id,
            "name": themed_template.name,
            "description": themed_template.description,
            "framework": framework,
            "theme_applied": theme_id,
            "global_styles": themed_template.global_styles,
            "sections": []
        }
        
        for section in themed_template.sections:
            section_data = {
                "name": section.name,
                "css_classes": section.css_classes,
                "components": []
            }
            
            for component in section.components:
                component_data = {
                    "name": component.name,
                    "props": component.props,
                    "children": component.children
                }
                section_data["components"].append(component_data)
            
            template_data["sections"].append(section_data)
        
        return {
            "themed_template": template_data,
            "theme_info": {
                "id": theme.id,
                "name": theme.name,
                "colors": {
                    "primary": theme.colors.primary,
                    "secondary": theme.colors.secondary,
                    "accent": theme.colors.accent
                }
            },
            "customizations_applied": customizations or {},
            "message": f"Successfully applied theme '{theme.name}' to template '{template.name}'"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to apply theme: {str(e)}",
            "themed_template": None
        }


async def generate_custom_theme_tool(
    name: str,
    primary_color: str,
    style: str,
    secondary_color: Optional[str] = None,
    mood: Optional[str] = None,
    industry: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a custom theme based on preferences."""
    
    try:
        from mcp_ui_aggregator.themes import Theme, ColorPalette, Typography, Spacing, BorderRadius, ThemeCategory
        import colorsys
        import re
        
        # Parse primary color
        def parse_color(color_str: str) -> tuple:
            """Parse color string to RGB tuple."""
            # Remove # if present
            color_str = color_str.strip().lstrip('#')
            
            # Try hex format
            if len(color_str) == 6:
                try:
                    return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
                except ValueError:
                    pass
            
            # Default fallback
            return (33, 150, 243)  # Default blue
        
        def rgb_to_hex(r: int, g: int, b: int) -> str:
            """Convert RGB to hex."""
            return f"#{r:02x}{g:02x}{b:02x}"
        
        def adjust_brightness(r: int, g: int, b: int, factor: float) -> tuple:
            """Adjust color brightness."""
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            l = max(0, min(1, l * factor))
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return (int(r * 255), int(g * 255), int(b * 255))
        
        def generate_complementary(r: int, g: int, b: int) -> tuple:
            """Generate complementary color."""
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            h = (h + 0.5) % 1.0  # Opposite hue
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return (int(r * 255), int(g * 255), int(b * 255))
        
        # Parse primary color
        primary_rgb = parse_color(primary_color)
        primary_hex = rgb_to_hex(*primary_rgb)
        
        # Generate secondary color if not provided
        if secondary_color:
            secondary_rgb = parse_color(secondary_color)
        else:
            # Generate based on primary
            secondary_rgb = adjust_brightness(*primary_rgb, 0.7)
        secondary_hex = rgb_to_hex(*secondary_rgb)
        
        # Generate accent color
        accent_rgb = generate_complementary(*primary_rgb)
        accent_hex = rgb_to_hex(*accent_rgb)
        
        # Base colors based on mood
        mood_colors = {
            "professional": {"bg": "#ffffff", "surface": "#f8f9fa", "text": "#212529"},
            "friendly": {"bg": "#fefefe", "surface": "#f0f4f8", "text": "#2d3748"},
            "energetic": {"bg": "#fff9f0", "surface": "#fff2e6", "text": "#1a202c"},
            "calm": {"bg": "#f7fafc", "surface": "#edf2f7", "text": "#2d3748"},
            "sophisticated": {"bg": "#1a1a1a", "surface": "#2d2d2d", "text": "#ffffff"}
        }
        
        base_colors = mood_colors.get(mood, mood_colors["professional"])
        
        # Typography based on style
        style_fonts = {
            "modern": ("'Inter', 'Helvetica Neue', sans-serif", "'Roboto', sans-serif"),
            "classic": ("'Times New Roman', 'Georgia', serif", "'Arial', sans-serif"),
            "minimal": ("'Helvetica Neue', 'Arial', sans-serif", "'system-ui', sans-serif"),
            "bold": ("'Montserrat', 'Arial Black', sans-serif", "'Open Sans', sans-serif"),
            "elegant": ("'Playfair Display', 'Georgia', serif", "'Source Sans Pro', sans-serif")
        }
        
        fonts = style_fonts.get(style, style_fonts["modern"])
        
        # Spacing based on style
        style_spacing = {
            "modern": {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px", "xxl": "48px"},
            "classic": {"xs": "6px", "sm": "12px", "md": "18px", "lg": "30px", "xl": "42px", "xxl": "60px"},
            "minimal": {"xs": "2px", "sm": "6px", "md": "12px", "lg": "20px", "xl": "28px", "xxl": "40px"},
            "bold": {"xs": "8px", "sm": "16px", "md": "24px", "lg": "32px", "xl": "48px", "xxl": "64px"},
            "elegant": {"xs": "4px", "sm": "10px", "md": "20px", "lg": "30px", "xl": "40px", "xxl": "60px"}
        }
        
        spacing = style_spacing.get(style, style_spacing["modern"])
        
        # Border radius based on style
        style_radius = {
            "modern": {"none": "0", "sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"},
            "classic": {"none": "0", "sm": "2px", "md": "4px", "lg": "6px", "xl": "8px", "full": "9999px"},
            "minimal": {"none": "0", "sm": "1px", "md": "2px", "lg": "4px", "xl": "6px", "full": "9999px"},
            "bold": {"none": "0", "sm": "6px", "md": "12px", "lg": "18px", "xl": "24px", "full": "9999px"},
            "elegant": {"none": "0", "sm": "3px", "md": "6px", "lg": "10px", "xl": "14px", "full": "9999px"}
        }
        
        radius = style_radius.get(style, style_radius["modern"])
        
        # Create theme
        colors = ColorPalette(
            primary=primary_hex,
            secondary=secondary_hex,
            accent=accent_hex,
            background=base_colors["bg"],
            surface=base_colors["surface"],
            text_primary=base_colors["text"],
            text_secondary=adjust_brightness(*parse_color(base_colors["text"]), 0.7) if base_colors["text"] != "#ffffff" else rgb_to_hex(160, 160, 160),
            success="#10b981",
            warning="#f59e0b",
            error="#ef4444",
            info="#3b82f6"
        )
        
        typography = Typography(
            font_family_primary=fonts[0],
            font_family_secondary=fonts[1],
            font_size_base="16px",
            font_size_small="14px",
            font_size_large="18px",
            font_weight_normal="400",
            font_weight_bold="600",
            line_height_base="1.5"
        )
        
        spacing_obj = Spacing(
            xs=spacing["xs"],
            sm=spacing["sm"],
            md=spacing["md"],
            lg=spacing["lg"],
            xl=spacing["xl"],
            xxl=spacing["xxl"]
        )
        
        border_radius = BorderRadius(
            none=radius["none"],
            sm=radius["sm"],
            md=radius["md"],
            lg=radius["lg"],
            xl=radius["xl"],
            full=radius["full"]
        )
        
        # Determine category
        category = ThemeCategory.CUSTOM
        if industry:
            if industry.lower() in ['finance', 'legal', 'government']:
                category = ThemeCategory.BUSINESS
            elif industry.lower() in ['design', 'art', 'media']:
                category = ThemeCategory.CREATIVE
        
        custom_theme = Theme(
            id=f"custom_{name.lower().replace(' ', '_')}",
            name=name,
            description=f"Custom {style} theme with {mood or 'neutral'} mood",
            category=category,
            colors=colors,
            typography=typography,
            spacing=spacing_obj,
            border_radius=border_radius,
            shadows={
                "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
            },
            breakpoints={
                "xs": "480px",
                "sm": "640px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px"
            }
        )
        
        # Register the theme
        theme_registry.register_theme(custom_theme)
        
        return {
            "theme": {
                "id": custom_theme.id,
                "name": custom_theme.name,
                "description": custom_theme.description,
                "category": custom_theme.category.value,
                "colors": {
                    "primary": custom_theme.colors.primary,
                    "secondary": custom_theme.colors.secondary,
                    "accent": custom_theme.colors.accent,
                    "background": custom_theme.colors.background,
                    "surface": custom_theme.colors.surface,
                    "text_primary": custom_theme.colors.text_primary,
                    "text_secondary": custom_theme.colors.text_secondary
                },
                "typography": {
                    "primary_font": custom_theme.typography.font_family_primary,
                    "secondary_font": custom_theme.typography.font_family_secondary,
                    "base_size": custom_theme.typography.font_size_base
                },
                "preview_palette": [
                    custom_theme.colors.primary,
                    custom_theme.colors.secondary,
                    custom_theme.colors.accent,
                    custom_theme.colors.background,
                    custom_theme.colors.surface
                ]
            },
            "generation_info": {
                "style": style,
                "mood": mood,
                "industry": industry,
                "primary_color_input": primary_color,
                "secondary_color_input": secondary_color
            },
            "message": f"Successfully generated custom theme '{name}'"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to generate custom theme: {str(e)}",
            "theme": None
        }


async def preview_theme_combinations_tool(
    component_types: List[str],
    framework: str,
    theme_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Preview theme combinations with components."""
    
    try:
        from mcp_ui_aggregator.templates import Framework
        
        # Convert framework string to enum
        framework_map = {
            "react": Framework.REACT,
            "vue": Framework.VUE,
            "html": Framework.HTML
        }
        
        if framework not in framework_map:
            return {
                "error": f"Unsupported framework: {framework}",
                "previews": []
            }
        
        framework_enum = framework_map[framework]
        
        # Get themes to preview
        if theme_ids:
            themes = [theme_registry.get_theme(tid) for tid in theme_ids if theme_registry.get_theme(tid)]
        else:
            themes = theme_registry.list_themes()[:3]  # Default to first 3 themes
        
        if not themes:
            return {
                "error": "No valid themes found for preview",
                "previews": []
            }
        
        previews = []
        
        for theme in themes:
            theme_preview = {
                "theme_id": theme.id,
                "theme_name": theme.name,
                "components": []
            }
            
            for component_type in component_types:
                # Create mock component
                mock_component = type('MockComponent', (), {
                    'name': component_type,
                    'props': {},
                    'children': None
                })()
                
                # Apply theme
                theme_applicator._apply_theme_to_component(mock_component, theme, framework_enum)
                
                component_preview = {
                    "type": component_type,
                    "styled_props": mock_component.props,
                    "css_classes": getattr(mock_component.props, 'class', None) or getattr(mock_component.props, 'className', None),
                    "inline_styles": getattr(mock_component.props, 'style', None) or getattr(mock_component.props, 'sx', None)
                }
                
                theme_preview["components"].append(component_preview)
            
            previews.append(theme_preview)
        
        return {
            "previews": previews,
            "framework": framework,
            "component_types": component_types,
            "themes_compared": len(previews),
            "message": f"Generated previews for {len(component_types)} component types across {len(previews)} themes"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to generate theme preview: {str(e)}",
            "previews": []
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze generated code"
        }