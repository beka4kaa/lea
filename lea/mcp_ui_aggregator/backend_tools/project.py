"""Project initialization and scaffolding tools."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
import uuid


@dataclass
class ProjectConfig:
    """Configuration for project initialization."""
    name: str
    stack: str = "fastapi+uvicorn"
    db: str = "postgres"
    orm: str = "sqlalchemy+alembic"
    queue: str = "rq"
    docker: bool = True
    ci: str = "github"
    telemetry: bool = True
    auth: bool = True
    preset: Optional[str] = None
    performance: bool = False
    architect_mode: str = "backend_architect"
    description: str = ""


class ProjectInitializer:
    """Handles FastAPI project initialization and scaffolding."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.templates_dir)))
        
    def init_project(self, config: ProjectConfig, target_dir: Path) -> Dict[str, Any]:
        """Initialize a new FastAPI project with given configuration."""
        
        # Initialize architect mode if enabled
        architect_recommendations = {}
        architect_notes = ""
        if config.architect_mode:
            from .architect_mode import create_architect_mode
            architect = create_architect_mode(config.architect_mode)
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
                architect_recommendations = architect.get_enhanced_recommendations()
                architect_notes = architect.generate_architect_notes()
        
        # Create project structure
        structure = self._create_project_structure(target_dir, config)
        
        # Generate core files  
        generated_files = self._generate_core_files(target_dir, config)
        
        # Generate performance optimizations if enabled
        if config.performance:
            generated_files.extend(self._generate_performance_files(target_dir, config))
        
        # Generate optional components
        if config.docker:
            generated_files.extend(self._generate_docker_files(target_dir, config))
            
        if config.ci:
            generated_files.extend(self._generate_ci_files(target_dir, config))
            
        if config.telemetry:
            generated_files.extend(self._generate_telemetry_files(target_dir, config))
        
        # Generate architect notes if available
        if architect_notes:
            self._write_file(target_dir / "ARCHITECT_NOTES.md", architect_notes)
            generated_files.append("ARCHITECT_NOTES.md")
        
        return {
            "project_name": config.name,
            "structure": structure,
            "generated_files": generated_files,
            "architect_recommendations": architect_recommendations,
            "next_steps": self._get_next_steps(config),
            "run_commands": self._get_run_commands(config)
        }
    
    def _create_project_structure(self, target_dir: Path, config: ProjectConfig) -> List[str]:
        """Create the basic project directory structure."""
        
        dirs = [
            "src",
            "src/core",
            "src/api",
            "src/db",
            "src/services",
            "tests",
            "tests/unit",
            "tests/e2e",
            "alembic",
            "alembic/versions",
            "docs",
        ]
        
        if config.queue != "none":
            dirs.extend(["src/jobs", "src/workers"])
            
        if config.docker:
            dirs.extend([".docker"])
            
        created_dirs = []
        for dir_path in dirs:
            full_path = target_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(dir_path))
            
        return created_dirs
    
    def _generate_core_files(self, target_dir: Path, config: ProjectConfig) -> List[str]:
        """Generate core application files."""
        
        files = []
        
        # Main app file
        app_content = self.env.get_template("app.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "app.py", app_content)
        files.append("src/app.py")
        
        # Core settings
        settings_content = self.env.get_template("core/settings.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "core" / "settings.py", settings_content)
        files.append("src/core/settings.py")
        
        # Database configuration
        db_content = self.env.get_template("db/database.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "db" / "database.py", db_content)
        files.append("src/db/database.py")
        
        # Base models
        models_content = self.env.get_template("db/models.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "db" / "models.py", models_content)
        files.append("src/db/models.py")
        
        # API router
        router_content = self.env.get_template("src/api/__init__.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "api" / "__init__.py", router_content)
        files.append("src/api/__init__.py")
        
        # Health check
        health_content = self.env.get_template("api/health.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "api" / "health.py", health_content)
        files.append("src/api/health.py")
        
        # Requirements
        pyproject_content = self.env.get_template("pyproject.toml.j2").render(config=config)
        self._write_file(target_dir / "pyproject.toml", pyproject_content)
        files.append("pyproject.toml")
        
        # Environment template
        env_content = self.env.get_template(".env.example.j2").render(config=config)
        self._write_file(target_dir / ".env.example", env_content)
        files.append(".env.example")
        
        # README
        readme_content = self.env.get_template("README.md.j2").render(config=config)
        self._write_file(target_dir / "README.md", readme_content)
        files.append("README.md")
        
        # Alembic configuration
        if config.orm == "sqlalchemy+alembic":
            alembic_content = self.env.get_template("alembic.ini.j2").render(config=config)
            self._write_file(target_dir / "alembic.ini", alembic_content)
            files.append("alembic.ini")
            
            alembic_env_content = self.env.get_template("alembic/env.py.j2").render(config=config)
            self._write_file(target_dir / "alembic" / "env.py", alembic_env_content)
            files.append("alembic/env.py")
        
        return files
    
    def _generate_docker_files(self, target_dir: Path, config: ProjectConfig) -> List[str]:
        """Generate Docker-related files."""
        
        files = []
        
        # Dockerfile
        dockerfile_content = self.env.get_template("Dockerfile.j2").render(config=config)
        self._write_file(target_dir / "Dockerfile", dockerfile_content)
        files.append("Dockerfile")
        
        # docker-compose.yml
        compose_content = self.env.get_template("docker-compose.yml.j2").render(config=config)
        self._write_file(target_dir / "docker-compose.yml", compose_content)
        files.append("docker-compose.yml")
        
        # .dockerignore
        dockerignore_content = self.env.get_template(".dockerignore.j2").render(config=config)
        self._write_file(target_dir / ".dockerignore", dockerignore_content)
        files.append(".dockerignore")
        
        return files
    
    def _generate_ci_files(self, target_dir: Path, config: ProjectConfig) -> List[str]:
        """Generate CI/CD files."""
        
        files = []
        
        if config.ci == "github":
            # Create .github/workflows directory
            workflows_dir = target_dir / ".github" / "workflows"
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # CI workflow
            ci_content = self.env.get_template("github/ci.yml.j2").render(config=config)
            self._write_file(workflows_dir / "ci.yml", ci_content)
            files.append(".github/workflows/ci.yml")
            
            # Deploy workflow (if Railway)
            if hasattr(config, 'deploy_target') and config.deploy_target == "railway":
                deploy_content = self.env.get_template("github/deploy-railway.yml.j2").render(config=config)
                self._write_file(workflows_dir / "deploy.yml", deploy_content)
                files.append(".github/workflows/deploy.yml")
        
        return files
    
    def _generate_performance_files(self, target_dir: Path, config: ProjectConfig) -> List[str]:
        """Generate performance optimization files."""
        
        files = []
        
        # Copy ASGI middleware
        from pathlib import Path as PPath
        import shutil
        
        # Copy optimized middleware files
        source_dir = PPath(__file__).parent.parent / "core"
        
        # ASGI middleware
        if (source_dir / "asgi_middleware.py").exists():
            shutil.copy2(source_dir / "asgi_middleware.py", target_dir / "src" / "core")
            files.append("src/core/asgi_middleware.py")
        
        # Optimized responses
        if (source_dir / "optimized_responses.py").exists():
            shutil.copy2(source_dir / "optimized_responses.py", target_dir / "src" / "core")
            files.append("src/core/optimized_responses.py")
        
        # Performance profiler
        root_dir = PPath(__file__).parent.parent.parent
        if (root_dir / "performance_profiler.py").exists():
            shutil.copy2(root_dir / "performance_profiler.py", target_dir)
            files.append("performance_profiler.py")
        
        # Nginx configuration
        if (root_dir / "nginx.conf").exists():
            shutil.copy2(root_dir / "nginx.conf", target_dir)
            files.append("nginx.conf")
        
        # Performance README
        if (root_dir / "PERFORMANCE_README.md").exists():
            shutil.copy2(root_dir / "PERFORMANCE_README.md", target_dir)
            files.append("PERFORMANCE_README.md")
        
        return files
    
    def _generate_telemetry_files(self, target_dir: Path, config: ProjectConfig) -> List[str]:
        """Generate telemetry and monitoring files."""
        
        files = []
        
        # OpenTelemetry configuration
        otel_content = self.env.get_template("core/telemetry.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "core" / "telemetry.py", otel_content)
        files.append("src/core/telemetry.py")
        
        # Prometheus metrics
        metrics_content = self.env.get_template("core/metrics.py.j2").render(config=config)
        self._write_file(target_dir / "src" / "core" / "metrics.py", metrics_content)
        files.append("src/core/metrics.py")
        
        return files
    
    def _write_file(self, filepath: Path, content: str):
        """Write content to file, creating directories if needed."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
    
    def _get_next_steps(self, config: ProjectConfig) -> List[str]:
        """Get next steps for project setup."""
        
        steps = [
            "Copy .env.example to .env and fill in your values",
            "Install dependencies: pip install -e .",
            "Run database migrations: alembic upgrade head",
        ]
        
        if config.docker:
            steps.extend([
                "Start services: docker-compose up -d postgres redis",
                "Run app: uvicorn src.app:app --reload"
            ])
        else:
            steps.append("Start the application: uvicorn src.app:app --reload")
            
        steps.extend([
            "Visit http://localhost:8000/docs for API documentation",
            "Check health: curl http://localhost:8000/health"
        ])
        
        return steps
    
    def _get_run_commands(self, config: ProjectConfig) -> Dict[str, str]:
        """Get common run commands."""
        
        return {
            "dev": "uvicorn src.app:app --reload --host 0.0.0.0 --port 8000",
            "prod": "uvicorn src.app:app --host 0.0.0.0 --port $PORT",
            "worker": "python -m src.workers.worker" if config.queue != "none" else None,
            "migrate": "alembic upgrade head",
            "test": "pytest tests/ -v --cov=src",
            "format": "black src tests && isort src tests",
            "lint": "ruff check src tests",
            "docker_build": "docker build -t {}/{}:latest .".format("registry", config.name),
            "docker_run": "docker run -p 8000:8000 {}/{}:latest".format("registry", config.name)
        }