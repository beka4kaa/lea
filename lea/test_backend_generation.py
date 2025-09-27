#!/usr/bin/env python3
"""Test script for the backend project generation system."""

import tempfile
import shutil
from pathlib import Path

from mcp_ui_aggregator.backend_tools.project import ProjectInitializer, ProjectConfig


def test_project_generation():
    """Test basic project generation functionality."""
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        project_path = temp_path / "test_project"
        
        # Configuration
        config = ProjectConfig(
            name="test_api",
            stack="fastapi+uvicorn",
            db="postgres",
            orm="sqlalchemy+alembic", 
            queue="rq",
            docker=True,
            ci="github",
            telemetry=True,
            auth=True
        )
        
        # Initialize project generator
        initializer = ProjectInitializer()
        
        # Generate project
        result = initializer.init_project(config, project_path)
        
        print("Project Generation Result:")
        print(f"Project Name: {result['project_name']}")
        print(f"Structure Created: {len(result['structure'])} directories")
        print(f"Files Generated: {len(result['generated_files'])} files")
        
        print("\nGenerated Files:")
        for file in result['generated_files']:
            print(f"  ✓ {file}")
            
        print("\nNext Steps:")
        for step in result['next_steps']:
            print(f"  • {step}")
            
        # Verify some key files exist
        key_files = [
            "src/app.py",
            "src/core/settings.py", 
            "src/db/database.py",
            "src/api/health.py",
            "pyproject.toml",
            ".env.example",
            "README.md"
        ]
        
        print("\nFile Verification:")
        for file in key_files:
            file_path = project_path / file
            if file_path.exists():
                print(f"  ✓ {file} ({file_path.stat().st_size} bytes)")
            else:
                print(f"  ✗ {file} (missing)")
                
        print(f"\nProject generated successfully in: {project_path}")
        
        # Show directory structure
        print("\nDirectory Structure:")
        for item in sorted(project_path.rglob("*")):
            if item.is_file():
                rel_path = item.relative_to(project_path)
                print(f"  {rel_path}")


if __name__ == "__main__":
    test_project_generation()