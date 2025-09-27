"""
Architect Mode Integration for LEA MCP Server Backend Tools
"""

from typing import Optional, Dict, Any
from ..core.system_prompts import get_system_prompt, available_roles

class ArchitectMode:
    """Enhanced backend generation with architect-level guidance."""
    
    def __init__(self, role: str = "backend_architect"):
        """Initialize architect mode with specified role."""
        self.role = role
        self.system_prompt = get_system_prompt(role)
        self.context = {}
    
    def set_context(self, project_config: Dict[str, Any]):
        """Set project context for architect recommendations."""
        self.context = {
            "name": project_config.get("name", ""),
            "description": project_config.get("description", ""),
            "database": project_config.get("db", ""),
            "authentication": project_config.get("auth", ""),
            "queue": project_config.get("queue", ""),
            "monitoring": project_config.get("monitoring", ""),
            "performance_mode": project_config.get("performance", False)
        }
    
    def get_enhanced_recommendations(self) -> Dict[str, Any]:
        """Get architect-level recommendations for the project."""
        if self.role == "backend_architect":
            return {
                "performance_optimizations": [
                    "ASGI middleware implementation for sub-10ms latency",
                    "ORJson/UJson response optimization for 2-3x JSON performance",
                    "Database connection pooling with optimal pool sizes",
                    "Redis caching layer with TTL optimization",
                    "Nginx keepalive connections for 15% throughput improvement"
                ],
                "security_enhancements": [
                    "JWT token rotation and refresh strategies",
                    "Rate limiting with Redis-backed counters",
                    "CORS configuration with environment-specific origins",
                    "Security headers middleware (HSTS, CSP, X-Frame-Options)",
                    "Input validation with Pydantic models"
                ],
                "scalability_patterns": [
                    "Horizontal scaling with load balancer configuration",
                    "Database read replicas and connection routing",
                    "Background task processing with Celery/RQ",
                    "Event-driven architecture with message queues",
                    "Microservices decomposition strategy"
                ],
                "monitoring_setup": [
                    "Prometheus metrics collection with custom gauges",
                    "Structured logging with correlation IDs",
                    "Health checks with dependency validation",
                    "OpenTelemetry distributed tracing",
                    "Grafana dashboards for SLA monitoring"
                ]
            }
        
        elif self.role == "frontend_architect":
            return {
                "performance_optimizations": [
                    "Code splitting with dynamic imports",
                    "Image optimization with WebP/AVIF formats",
                    "Service worker caching strategies",
                    "Bundle size optimization with tree shaking",
                    "Core Web Vitals optimization"
                ],
                "user_experience": [
                    "Loading states and skeleton screens",
                    "Error boundaries with fallback UI",
                    "Responsive design with mobile-first approach",
                    "Accessibility compliance (WCAG 2.1 AA)",
                    "Progressive enhancement strategies"
                ],
                "development_workflow": [
                    "Component-driven development with Storybook",
                    "Design system implementation",
                    "TypeScript strict mode configuration",
                    "Testing strategy with unit and e2e tests",
                    "CI/CD pipeline with automated deployments"
                ]
            }
        
        return {}
    
    def generate_architect_notes(self) -> str:
        """Generate architect-level implementation notes."""
        recommendations = self.get_enhanced_recommendations()
        
        notes = f"""
# 🏗️ Architect Implementation Notes

## Project: {self.context.get('name', 'Unknown')}
**Role**: {self.role.replace('_', ' ').title()}
**Performance Mode**: {'Enabled' if self.context.get('performance_mode') else 'Standard'}

## 🎯 Key Recommendations

"""
        
        for category, items in recommendations.items():
            category_title = category.replace('_', ' ').title()
            notes += f"### {category_title}\n"
            for item in items:
                notes += f"- {item}\n"
            notes += "\n"
        
        notes += f"""
## 🔧 Implementation Priority

1. **Foundation**: Set up core architecture with performance optimizations
2. **Security**: Implement authentication, authorization, and security headers
3. **Monitoring**: Add comprehensive logging, metrics, and health checks
4. **Scaling**: Prepare for horizontal scaling with proper patterns
5. **Testing**: Implement comprehensive testing strategy

## 📊 Success Metrics

- **Latency**: P95 < 50ms for API endpoints
- **Throughput**: > 1000 req/s per worker
- **Availability**: 99.9% uptime SLA
- **Security**: Zero critical vulnerabilities
- **Maintainability**: < 2 days for feature implementation

## 🚀 Next Steps

1. Run performance benchmarks with `performance_profiler.py`
2. Set up monitoring dashboard with Grafana
3. Configure CI/CD pipeline for automated deployments
4. Implement comprehensive test suite
5. Document architecture decisions and patterns

---
*Generated by LEA MCP Server - Architect Mode*
"""
        
        return notes

def create_architect_mode(role: str = "backend_architect") -> Optional[ArchitectMode]:
    """Create architect mode instance with validation."""
    if role not in available_roles():
        return None
    return ArchitectMode(role)

def get_available_architect_roles() -> list:
    """Get list of available architect roles."""
    return available_roles()