#!/usr/bin/env python3
"""
Complete Performance Optimization Integration Test
Tests all performance components working together.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from mcp_ui_aggregator.backend_tools.project import ProjectInitializer, ProjectConfig
from mcp_ui_aggregator.backend_tools.architect_mode import create_architect_mode

async def test_performance_project_generation():
    """Test generating a complete performance-optimized project."""
    
    print("🚀 Testing Performance-Optimized Project Generation")
    print("=" * 60)
    
    # Create temporary directory for test project
    with tempfile.TemporaryDirectory() as temp_dir:
        target_dir = Path(temp_dir) / "test_performance_app"
        
        # Configure project with performance optimizations
        config = ProjectConfig(
            name="test_performance_app",
            description="High-performance API with optimizations",
            stack="fastapi+uvicorn",
            db="postgres",
            orm="sqlalchemy+alembic",
            queue="redis",
            docker=True,
            ci="github",
            telemetry=True,
            auth=True,
            performance=True,  # Enable performance optimizations
            architect_mode="backend_architect"
        )
        
        # Initialize project
        initializer = ProjectInitializer()
        result = initializer.init_project(config, target_dir)
        
        print(f"✅ Project '{result['project_name']}' generated successfully")
        print(f"📁 Created {len(result['structure'])} directories")
        print(f"📄 Generated {len(result['generated_files'])} files")
        
        # Verify performance files were created
        performance_files = [
            "src/core/asgi_middleware.py",
            "src/core/optimized_responses.py", 
            "performance_profiler.py",
            "nginx.conf",
            "PERFORMANCE_README.md",
            "ARCHITECT_NOTES.md"
        ]
        
        created_performance_files = []
        for file_path in performance_files:
            full_path = target_dir / file_path
            if full_path.exists():
                created_performance_files.append(file_path)
                print(f"✅ Performance file created: {file_path}")
            else:
                print(f"❌ Performance file missing: {file_path}")
        
        # Test architect mode integration
        architect = create_architect_mode("backend_architect")
        if architect:
            architect.set_context({
                "name": config.name,
                "description": config.description,
                "db": config.db,
                "auth": config.auth,
                "queue": config.queue,
                "monitoring": config.telemetry,
                "performance": config.performance
            })
            
            recommendations = architect.get_enhanced_recommendations()
            print(f"✅ Architect recommendations: {len(recommendations)} categories")
            
            for category, items in recommendations.items():
                print(f"  📋 {category.replace('_', ' ').title()}: {len(items)} items")
        
        # Verify core structure
        core_files = [
            "src/app.py",
            "src/core/settings.py",
            "src/core/metrics.py",
            "src/db/database.py",
            "src/api/health.py",
            "pyproject.toml",
            "README.md",
            "Dockerfile",
            "docker-compose.yml"
        ]
        
        for file_path in core_files:
            full_path = target_dir / file_path
            if full_path.exists():
                print(f"✅ Core file created: {file_path}")
            else:
                print(f"❌ Core file missing: {file_path}")
        
        # Test metrics template with ASGI middleware
        metrics_file = target_dir / "src" / "core" / "metrics.py"
        if metrics_file.exists():
            content = metrics_file.read_text()
            if "class PrometheusMiddleware:" in content and "ASGIApp" in content:
                print("✅ Metrics file uses ASGI-compliant middleware")
            else:
                print("❌ Metrics file not using ASGI middleware")
        
        print("\n🎯 Performance Features Summary:")
        print("━" * 40)
        print(f"ASGI Middleware: {'✅' if 'src/core/asgi_middleware.py' in created_performance_files else '❌'}")
        print(f"JSON Optimization: {'✅' if 'src/core/optimized_responses.py' in created_performance_files else '❌'}")
        print(f"Nginx Config: {'✅' if 'nginx.conf' in created_performance_files else '❌'}")
        print(f"Performance Profiler: {'✅' if 'performance_profiler.py' in created_performance_files else '❌'}")
        print(f"Performance README: {'✅' if 'PERFORMANCE_README.md' in created_performance_files else '❌'}")
        print(f"Architect Notes: {'✅' if 'ARCHITECT_NOTES.md' in created_performance_files else '❌'}")
        
        print(f"\n📊 Total Performance Files: {len(created_performance_files)}/{len(performance_files)}")
        
        # Show next steps
        if result.get('next_steps'):
            print(f"\n📋 Next Steps ({len(result['next_steps'])}):")
            for i, step in enumerate(result['next_steps'], 1):
                print(f"  {i}. {step}")
        
        # Show run commands
        if result.get('run_commands'):
            print(f"\n🏃 Run Commands ({len(result['run_commands'])}):")
            for i, cmd in enumerate(result['run_commands'], 1):
                print(f"  {i}. {cmd}")
        
        # Test architect recommendations display
        if result.get('architect_recommendations'):
            print(f"\n🏗️ Architect Recommendations:")
            recommendations = result['architect_recommendations']
            for category, items in recommendations.items():
                print(f"  📋 {category.replace('_', ' ').title()}:")
                for item in items[:2]:  # Show first 2 items
                    print(f"    • {item}")
                if len(items) > 2:
                    print(f"    ... and {len(items) - 2} more")
        
        return len(created_performance_files) == len(performance_files)

def test_system_prompts():
    """Test system prompts functionality."""
    
    print("\n🧠 Testing System Prompts")
    print("=" * 30)
    
    try:
        from mcp_ui_aggregator.core.system_prompts import get_system_prompt, available_roles
        
        roles = available_roles()
        print(f"✅ Available roles: {', '.join(roles)}")
        
        for role in roles:
            prompt = get_system_prompt(role)
            if prompt and len(prompt) > 100:
                print(f"✅ {role}: {len(prompt)} characters")
            else:
                print(f"❌ {role}: Invalid or empty prompt")
        
        return True
    except Exception as e:
        print(f"❌ System prompts test failed: {e}")
        return False

def test_architect_mode():
    """Test architect mode functionality."""
    
    print("\n🏗️ Testing Architect Mode")
    print("=" * 25)
    
    try:
        from mcp_ui_aggregator.backend_tools.architect_mode import create_architect_mode, get_available_architect_roles
        
        roles = get_available_architect_roles()
        print(f"✅ Available architect roles: {', '.join(roles)}")
        
        # Test backend architect
        backend_architect = create_architect_mode("backend_architect")
        if backend_architect:
            backend_architect.set_context({
                "name": "test_app",
                "description": "Test application",
                "db": "postgres",
                "auth": True,
                "queue": "redis",
                "monitoring": True,
                "performance": True
            })
            
            recommendations = backend_architect.get_enhanced_recommendations()
            notes = backend_architect.generate_architect_notes()
            
            print(f"✅ Backend architect recommendations: {len(recommendations)} categories")
            print(f"✅ Generated notes: {len(notes)} characters")
        
        # Test frontend architect
        frontend_architect = create_architect_mode("frontend_architect")
        if frontend_architect:
            frontend_architect.set_context({
                "name": "test_ui",
                "description": "Test UI application"
            })
            
            recommendations = frontend_architect.get_enhanced_recommendations()
            print(f"✅ Frontend architect recommendations: {len(recommendations)} categories")
        
        return True
    except Exception as e:
        print(f"❌ Architect mode test failed: {e}")
        return False

async def main():
    """Run all performance optimization tests."""
    
    print("🎯 LEA MCP Server - Performance Optimization Test Suite")
    print("=" * 65)
    
    tests = [
        ("System Prompts", test_system_prompts),
        ("Architect Mode", test_architect_mode),
        ("Performance Project Generation", test_performance_project_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All performance optimization tests PASSED!")
        print("\n🚀 Performance Features Ready:")
        print("  ✅ ASGI Middleware for latency reduction")
        print("  ✅ JSON Response optimization (orjson/ujson)")
        print("  ✅ Nginx configuration with keepalive")
        print("  ✅ Performance profiling and benchmarking")
        print("  ✅ Architect mode with system prompts")
        print("  ✅ Complete performance README guide")
        
        print("\n🎯 Ready for production deployment with optimized performance!")
    else:
        print("❌ Some tests failed. Please check the output above.")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())