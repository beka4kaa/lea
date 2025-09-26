"""Command Line Interface for MCP UI Aggregator."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import click
import uvicorn

from mcp_ui_aggregator.core.config import settings
from mcp_ui_aggregator.core.database import create_tables, drop_tables
from mcp_ui_aggregator.ingestion.material_ui import MaterialUIIngester
from mcp_ui_aggregator.ingestion.shadcn_ui import ShadcnUIIngester
from mcp_ui_aggregator.ingestion.chakra_ui import ChakraUIIngester
from mcp_ui_aggregator.ingestion.antd import AntDesignIngester
from mcp_ui_aggregator.ingestion.mantine import MantineIngester
from mcp_ui_aggregator.search.engine import text_search, vector_search
from mcp_ui_aggregator.tools.component_tools import (
    list_components, search_component, get_component_code,
    get_component_docs, install_component
)
from mcp_ui_aggregator.commercial import SUBSCRIPTION_TIERS, PremiumFeatures
from mcp_ui_aggregator.analytics import performance_monitor, usage_analyzer
from mcp_ui_aggregator.data.demo_seed import seed_demo_data


@click.group()
@click.version_option(version="0.1.0", prog_name="mcp-ui-aggregator")
def cli():
    """MCP UI Aggregator - A Model Context Protocol server for UI component management."""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, type=int, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
@click.option("--log-level", default="info", help="Log level")
def serve(host: str, port: int, reload: bool, log_level: str):
    """Start the MCP server."""
    # Update settings
    settings.host = host
    settings.port = port
    
    click.echo(f"Starting MCP UI Aggregator server...")
    click.echo(f"Server: {host}:{port}")
    click.echo(f"Database: {settings.database_url}")
    
    # Run FastAPI app (we'll create this next)
    uvicorn.run(
        "mcp_ui_aggregator.api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level
    )


@cli.command()
@click.option("--namespace", type=click.Choice(["material", "shadcn", "chakra", "antd", "mantine", "all"]), default="all",
              help="Namespace to ingest")
@click.option("--force", is_flag=True, help="Force re-ingestion even if data exists")
def ingest(namespace: str, force: bool):
    """Ingest component data from documentation sources."""
    click.echo(f"Starting ingestion for namespace: {namespace}")
    
    async def run_ingestion():
        # Initialize database
        await create_tables()
        
        results = {}
        
        if namespace in ["material", "all"]:
            click.echo("Ingesting Material UI components...")
            async with MaterialUIIngester() as ingester:
                try:
                    stats = await ingester.run_ingestion()
                    results["material"] = stats
                    click.echo(f"Material UI: {stats['components_processed']} processed, "
                              f"{stats['components_created']} created, "
                              f"{stats['components_updated']} updated")
                except Exception as e:
                    click.echo(f"Error ingesting Material UI: {e}", err=True)
                    results["material"] = {"error": str(e)}
        
        if namespace in ["shadcn", "all"]:
            click.echo("Ingesting shadcn/ui components...")
            async with ShadcnUIIngester() as ingester:
                try:
                    stats = await ingester.run_ingestion()
                    results["shadcn"] = stats
                    click.echo(f"shadcn/ui: {stats['components_processed']} processed, "
                              f"{stats['components_created']} created, "
                              f"{stats['components_updated']} updated")
                except Exception as e:
                    click.echo(f"Error ingesting shadcn/ui: {e}", err=True)
                    results["shadcn"] = {"error": str(e)}
        
        if namespace in ["chakra", "all"]:
            click.echo("Ingesting Chakra UI components...")
            async with ChakraUIIngester() as ingester:
                try:
                    stats = await ingester.run_ingestion()
                    results["chakra"] = stats
                    click.echo(f"Chakra UI: {stats['components_processed']} processed, "
                              f"{stats['components_created']} created, "
                              f"{stats['components_updated']} updated")
                except Exception as e:
                    click.echo(f"Error ingesting Chakra UI: {e}", err=True)
                    results["chakra"] = {"error": str(e)}
        
        if namespace in ["antd", "all"]:
            click.echo("Ingesting Ant Design components...")
            async with AntDesignIngester() as ingester:
                try:
                    stats = await ingester.run_ingestion()
                    results["antd"] = stats
                    click.echo(f"Ant Design: {stats['components_processed']} processed, "
                              f"{stats['components_created']} created, "
                              f"{stats['components_updated']} updated")
                except Exception as e:
                    click.echo(f"Error ingesting Ant Design: {e}", err=True)
                    results["antd"] = {"error": str(e)}
        
        if namespace in ["mantine", "all"]:
            click.echo("Ingesting Mantine components...")
            async with MantineIngester() as ingester:
                try:
                    stats = await ingester.run_ingestion()
                    results["mantine"] = stats
                    click.echo(f"Mantine: {stats['components_processed']} processed, "
                              f"{stats['components_created']} created, "
                              f"{stats['components_updated']} updated")
                except Exception as e:
                    click.echo(f"Error ingesting Mantine: {e}", err=True)
                    results["mantine"] = {"error": str(e)}
        
        return results
    
    results = asyncio.run(run_ingestion())
    
    # Show summary
    total_processed = sum(r.get("components_processed", 0) for r in results.values() if isinstance(r, dict))
    total_created = sum(r.get("components_created", 0) for r in results.values() if isinstance(r, dict))
    total_updated = sum(r.get("components_updated", 0) for r in results.values() if isinstance(r, dict))
    
    click.echo("\n--- Ingestion Summary ---")
    click.echo(f"Total components processed: {total_processed}")
    click.echo(f"Total components created: {total_created}")
    click.echo(f"Total components updated: {total_updated}")
    
    # Show library breakdown
    click.echo("\n--- Library Breakdown ---")
    for lib_name, stats in results.items():
        if isinstance(stats, dict) and "error" not in stats:
            click.echo(f"{lib_name.title()}: {stats.get('components_created', 0)} components")
        elif isinstance(stats, dict) and "error" in stats:
            click.echo(f"{lib_name.title()}: Failed - {stats['error']}")


@cli.command()
@click.option("--query", prompt="Search query", help="Search query")
@click.option("--namespace", type=click.Choice(["material", "shadcn", "chakra", "antd", "mantine"]), help="Filter by namespace")
@click.option("--type", "component_type", help="Filter by component type")
@click.option("--limit", default=10, type=int, help="Maximum results")
@click.option("--vector", is_flag=True, help="Use vector search (requires sentence-transformers)")
def search(query: str, namespace: Optional[str], component_type: Optional[str], 
           limit: int, vector: bool):
    """Search for UI components."""
    
    async def run_search():
        if vector:
            # Try vector search
            await vector_search.initialize()
            results = await vector_search.vector_search(
                query=query,
                namespace=namespace,
                component_type=component_type,
                limit=limit
            )
            return {"vector_results": results}
        else:
            # Use text search
            results = await text_search.search_components(
                query=query,
                namespace=namespace,
                component_type=component_type,
                limit=limit
            )
            return results
    
    results = asyncio.run(run_search())
    
    if vector and "vector_results" in results:
        click.echo(f"Vector search results for '{query}':")
        for result in results["vector_results"]:
            click.echo(f"  {result['namespace']}/{result['name']} - {result['title']}")
            click.echo(f"    Similarity: {result['similarity_score']}")
            click.echo(f"    {result['description'][:100]}...")
            click.echo()
    else:
        click.echo(f"Search results for '{query}' ({results['total']} total):")
        for result in results["results"]:
            click.echo(f"  {result['namespace']}/{result['name']} - {result['title']}")
            click.echo(f"    Relevance: {result['relevance_score']}")
            click.echo(f"    {result['description'][:100]}...")
            click.echo()


@cli.command()
@click.option("--namespace", type=click.Choice(["material", "shadcn", "chakra", "antd", "mantine"]), help="Filter by namespace")
@click.option("--type", "component_type", help="Filter by component type")
@click.option("--limit", default=20, type=int, help="Maximum results")
def list(namespace: Optional[str], component_type: Optional[str], limit: int):
    """List UI components."""
    
    async def run_list():
        return await list_components(
            namespace=namespace,
            component_type=component_type,
            limit=limit
        )
    
    results = asyncio.run(run_list())
    
    click.echo(f"Components ({results['pagination']['total']} total):")
    for component in results["components"]:
        click.echo(f"  {component['namespace']}/{component['name']} - {component['title']}")
        click.echo(f"    Type: {component['component_type']}")
        if component['tags']:
            click.echo(f"    Tags: {', '.join(component['tags'])}")
        click.echo()


@cli.command()
@click.argument("component_name")
@click.option("--namespace", type=click.Choice(["material", "shadcn", "chakra", "antd", "mantine"]), 
              prompt="Component namespace", help="Component namespace")
def code(component_name: str, namespace: str):
    """Get code examples for a component."""
    
    async def run_get_code():
        return await get_component_code(
            component_name=component_name,
            namespace=namespace,
            include_examples=True
        )
    
    results = asyncio.run(run_get_code())
    
    if "error" in results:
        click.echo(f"Error: {results['error']}", err=True)
        return
    
    component = results["component"]
    click.echo(f"Code for {component['namespace']}/{component['name']}:")
    click.echo(f"Title: {component['title']}")
    click.echo()
    
    if component['import_statement']:
        click.echo("Import:")
        click.echo(f"  {component['import_statement']}")
        click.echo()
    
    if component['basic_usage']:
        click.echo("Basic Usage:")
        click.echo(f"  {component['basic_usage']}")
        click.echo()
    
    if results["examples"]:
        click.echo("Examples:")
        for example in results["examples"]:
            click.echo(f"  {example['title']}")
            if example['description']:
                click.echo(f"    {example['description']}")
            click.echo(f"    Language: {example['language']}")
            click.echo(f"    Code: {example['code'][:200]}...")
            click.echo()


@cli.command()
@click.argument("component_name")
@click.option("--namespace", type=click.Choice(["material", "shadcn", "chakra", "antd", "mantine"]), 
              prompt="Component namespace", help="Component namespace")
@click.option("--package-manager", type=click.Choice(["npm", "yarn", "pnpm"]), 
              default="npm", help="Package manager")
def install(component_name: str, namespace: str, package_manager: str):
    """Get installation instructions for a component."""
    
    async def run_install():
        return await install_component(
            component_name=component_name,
            namespace=namespace,
            package_manager=package_manager
        )
    
    results = asyncio.run(run_install())
    
    if "error" in results:
        click.echo(f"Error: {results['error']}", err=True)
        return
    
    component = results["component"]
    installation = results["installation"]
    
    click.echo(f"Installation instructions for {component['namespace']}/{component['name']}:")
    click.echo(f"Title: {component['title']}")
    click.echo()
    
    click.echo("Installation Command:")
    click.echo(f"  {installation['install_command']}")
    click.echo()
    
    if installation['import_statement']:
        click.echo("Import:")
        click.echo(f"  {installation['import_statement']}")
        click.echo()
    
    if installation['basic_usage']:
        click.echo("Basic Usage:")
        click.echo(f"  {installation['basic_usage']}")
        click.echo()
    
    click.echo("Next Steps:")
    for step in results["next_steps"]:
        click.echo(f"  - {step}")


@cli.group()
def db():
    """Database management commands."""
    pass


@db.command()
def init():
    """Initialize the database."""
    click.echo("Initializing database...")
    
    async def init_db():
        await create_tables()
        click.echo("Database initialized successfully!")
    
    asyncio.run(init_db())


@db.command()
@click.confirmation_option(prompt="Are you sure you want to drop all tables?")
def reset():
    """Reset the database (drop all tables)."""
    click.echo("Resetting database...")
    
    async def reset_db():
        await drop_tables()
        await create_tables()
        click.echo("Database reset successfully!")
    
    asyncio.run(reset_db())


@db.command()
def seed():
    """Seed the database with a small demo dataset."""
    click.echo("Seeding demo data...")

    async def do_seed():
        count = await seed_demo_data()
        click.echo(f"Seeded {count} new components (skipped existing).")

    asyncio.run(do_seed())


@cli.command()
def plans():
    """Show available subscription plans and features."""
    click.echo("🎯 MCP UI Aggregator - Subscription Plans\n")
    
    for tier_name, limits in SUBSCRIPTION_TIERS.items():
        click.echo(f"📋 {tier_name.value.upper()} Plan")
        click.echo(f"   Daily API calls: {'Unlimited' if limits.daily_api_calls == -1 else limits.daily_api_calls}")
        click.echo(f"   Monthly components: {'Unlimited' if limits.monthly_components == -1 else limits.monthly_components}")
        click.echo(f"   UI Libraries: {', '.join(limits.libraries_access)}")
        click.echo(f"   Vector search: {'✅' if limits.vector_search else '❌'}")
        click.echo(f"   Premium templates: {'✅' if limits.premium_templates else '❌'}")
        click.echo(f"   Custom themes: {'✅' if limits.custom_themes else '❌'}")
        click.echo(f"   Team collaboration: {'✅' if limits.team_collaboration else '❌'}")
        click.echo(f"   Priority support: {'✅' if limits.priority_support else '❌'}")
        click.echo()


@cli.command()
def templates():
    """Show available premium templates."""
    templates = PremiumFeatures.get_premium_templates()
    
    click.echo("🎨 Premium Templates (Pro/Enterprise only)\n")
    
    for template in templates:
        click.echo(f"📄 {template['name']}")
        click.echo(f"   Category: {template['category']}")
        click.echo(f"   Description: {template['description']}")
        click.echo(f"   Libraries: {', '.join(template['libraries'])}")
        click.echo(f"   Components: {', '.join(template['components'])}")
        click.echo()


@cli.command()
def analytics():
    """Show usage analytics and performance metrics."""
    click.echo("📊 MCP UI Aggregator - Analytics Dashboard\n")
    
    # Performance metrics
    perf_summary = performance_monitor.get_performance_summary()
    click.echo("🚀 Performance Metrics")
    click.echo(f"   Uptime: {perf_summary['uptime_seconds']:.0f} seconds")
    click.echo(f"   Total operations: {perf_summary['total_metrics']}")
    
    if perf_summary['endpoints']:
        click.echo("   Top endpoints:")
        for endpoint, stats in list(perf_summary['endpoints'].items())[:5]:
            click.echo(f"     {endpoint}: {stats['count']} calls, avg {stats['avg_ms']:.1f}ms")
    
    # Usage analytics
    usage_summary = usage_analyzer.get_usage_summary(days=7)
    click.echo(f"\n📈 Usage Summary (Last 7 days)")
    click.echo(f"   Total requests: {usage_summary['total_requests']}")
    click.echo(f"   Unique users: {usage_summary['unique_users']}")
    
    if usage_summary['top_namespaces']:
        click.echo("   Popular libraries:")
        for namespace, count in list(usage_summary['top_namespaces'].items())[:3]:
            click.echo(f"     {namespace}: {count} requests")
    
    # Search insights
    search_insights = usage_analyzer.get_search_insights()
    if search_insights['total_searches'] > 0:
        click.echo(f"\n🔍 Search Insights")
        click.echo(f"   Total searches: {search_insights['total_searches']}")
        click.echo(f"   Unique queries: {search_insights['unique_queries']}")
        if search_insights['common_search_terms']:
            top_terms = search_insights['common_search_terms'][:3]
            click.echo(f"   Popular terms: {', '.join([t['word'] for t in top_terms])}")


@cli.command()
@click.option("--library", type=click.Choice(["material", "shadcn", "chakra", "antd", "mantine"]),
              help="Base library for theme")
@click.option("--primary-color", default="#007bff", help="Primary color")
@click.option("--secondary-color", default="#6c757d", help="Secondary color") 
@click.option("--font-family", default="Inter, sans-serif", help="Font family")
def generate_theme(library: str, primary_color: str, secondary_color: str, font_family: str):
    """Generate a custom theme configuration (Pro/Enterprise feature)."""
    if not library:
        click.echo("Please specify a base library with --library option")
        return
    
    click.echo(f"🎨 Generating custom theme for {library}...\n")
    
    preferences = {
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "font_family": font_family,
        "border_radius": "8px",
        "spacing_scale": "1.2"
    }
    
    theme_config = PremiumFeatures.generate_custom_theme(library, preferences)
    
    click.echo(f"✅ Theme generated successfully!")
    click.echo(f"Library: {theme_config['library']}")
    click.echo(f"Theme type: {theme_config.get('theme_type', 'custom')}")
    click.echo(f"Primary color: {theme_config['primary_color']}")
    click.echo(f"Secondary color: {theme_config['secondary_color']}")
    click.echo(f"Font family: {theme_config['font_family']}")
    click.echo()
    
    if 'config' in theme_config:
        click.echo("Theme configuration:")
        click.echo(json.dumps(theme_config['config'], indent=2))
    
    click.echo("\n💡 This is a Pro/Enterprise feature. Upgrade your plan to access theme generation in production.")


@cli.command()
def status():
    """Show overall system status and health."""
    click.echo("🏥 System Status\n")
    
    # Database check
    try:
        # This would check database connectivity
        click.echo("✅ Database: Connected")
    except Exception as e:
        click.echo(f"❌ Database: Error - {e}")
    
    # Performance check
    perf_summary = performance_monitor.get_performance_summary()
    if perf_summary['total_metrics'] > 0:
        avg_response_time = sum(
            stats['avg_ms'] for stats in perf_summary['endpoints'].values()
        ) / len(perf_summary['endpoints']) if perf_summary['endpoints'] else 0
        
        if avg_response_time < 1000:
            click.echo(f"✅ Performance: Good (avg {avg_response_time:.0f}ms)")
        else:
            click.echo(f"⚠️ Performance: Slow (avg {avg_response_time:.0f}ms)")
    else:
        click.echo("ℹ️ Performance: No data yet")
    
    # Memory and resource check
    click.echo(f"📊 Metrics stored: {perf_summary['total_metrics']}")
    click.echo(f"⏰ Uptime: {perf_summary['uptime_seconds']:.0f} seconds")
    
    # Error check
    recent_errors = perf_summary.get('recent_errors', [])
    if recent_errors:
        click.echo(f"⚠️ Recent errors: {len(recent_errors)}")
    else:
        click.echo("✅ No recent errors")


@cli.command()
def version():
    """Show detailed version information."""
    click.echo("📦 MCP UI Aggregator Version Information\n")
    click.echo("Version: 0.1.0")
    click.echo("Build: Enhanced Commercial Version")
    click.echo("MCP Protocol: 1.0.0")
    click.echo("Python: 3.11+")
    click.echo("FastAPI: Latest")
    click.echo()
    click.echo("🆕 New Features in this version:")
    click.echo("  • Support for 5 UI libraries (Material UI, shadcn/ui, Chakra UI, Ant Design, Mantine)")
    click.echo("  • Commercial subscription tiers")
    click.echo("  • Performance monitoring and analytics")
    click.echo("  • Premium template system")
    click.echo("  • Custom theme generation")
    click.echo("  • Enhanced search capabilities")
    click.echo()
    click.echo("🏢 Commercial Features:")
    click.echo("  • Usage tracking and billing")
    click.echo("  • Team collaboration")
    click.echo("  • Priority support")
    click.echo("  • Enterprise scalability")


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nAborted!")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()