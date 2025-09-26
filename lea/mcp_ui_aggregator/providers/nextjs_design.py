"""Next.js Design provider implementation - Next.js Templates and Components."""

import json
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import HTTPProvider, ComponentNotFoundError
from .registry import register_provider
from ..models.component_manifest import (
    ComponentManifest,
    Provider,
    License,
    LicenseType,
    Source,
    Framework,
    TailwindConfig,
    TailwindVersion,
    ComponentCode,
    ComponentAccess,
    InstallPlan,
    ComponentCategory
)


@register_provider
class NextJSDesignProvider(HTTPProvider):
    """Next.js Design templates and components provider."""
    
    @property
    def provider_name(self) -> Provider:
        return Provider.NEXTJS_DESIGN
    
    @property
    def base_url(self) -> str:
        return "https://nextjs.design"
    
    async def list_components(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> List[ComponentManifest]:
        """List Next.js Design components."""
        try:
            components = await self._get_all_components()
            
            # Apply pagination
            start = offset
            end = offset + limit
            return components[start:end]
            
        except Exception as e:
            print(f"Error listing Next.js Design components: {e}")
            return []
    
    async def get_component(self, component_id: str) -> ComponentManifest:
        """Get specific Next.js Design component."""
        # Remove provider prefix if present
        if "/" in component_id:
            component_id = component_id.split("/", 1)[1]
        
        components = await self.list_components(limit=1000)
        for component in components:
            if component.slug == component_id:
                return component
        
        raise ComponentNotFoundError(f"Component {component_id} not found in Next.js Design")
    
    async def _get_all_components(self) -> List[ComponentManifest]:
        """Get all Next.js Design components."""
        # Next.js Design templates and components
        nextjs_components = [
            # Landing Page Templates
            {
                "name": "SaaS Landing Page",
                "slug": "saas-landing-page",
                "category": "templates",
                "description": "Complete SaaS landing page with hero, features, pricing, and CTA sections",
                "tags": ["saas", "landing", "hero", "pricing", "features"],
                "template_type": "landing",
                "pages": ["index.tsx"],
                "components": ["Hero", "Features", "Pricing", "CTA", "Footer"]
            },
            {
                "name": "Startup Landing",
                "slug": "startup-landing",
                "category": "templates",
                "description": "Modern startup landing page with gradient backgrounds and animations",
                "tags": ["startup", "modern", "gradient", "animated"],
                "template_type": "landing",
                "pages": ["index.tsx"],
                "components": ["AnimatedHero", "FeatureGrid", "TeamSection", "ContactForm"]
            },
            {
                "name": "Portfolio Template",
                "slug": "portfolio-template",
                "category": "templates",
                "description": "Creative portfolio template for designers and developers",
                "tags": ["portfolio", "creative", "showcase", "gallery"],
                "template_type": "portfolio",
                "pages": ["index.tsx", "projects/[slug].tsx", "about.tsx"],
                "components": ["ProjectGrid", "SkillsList", "ContactSection"]
            },
            {
                "name": "Agency Website",
                "slug": "agency-website",
                "category": "templates",
                "description": "Professional agency website with service pages and team showcase",
                "tags": ["agency", "professional", "services", "team"],
                "template_type": "business",
                "pages": ["index.tsx", "services.tsx", "team.tsx", "contact.tsx"],
                "components": ["ServiceCards", "TeamGrid", "TestimonialSlider"]
            },
            {
                "name": "E-commerce Store",
                "slug": "ecommerce-store",
                "category": "templates",
                "description": "Full e-commerce template with product catalog and shopping cart",
                "tags": ["ecommerce", "store", "products", "cart"],
                "template_type": "ecommerce",
                "pages": ["index.tsx", "products/[id].tsx", "cart.tsx", "checkout.tsx"],
                "components": ["ProductGrid", "ProductCard", "ShoppingCart", "CheckoutForm"]
            },
            
            # Dashboard Templates
            {
                "name": "Admin Dashboard",
                "slug": "admin-dashboard",
                "category": "templates",
                "description": "Complete admin dashboard with charts, tables, and management tools",
                "tags": ["dashboard", "admin", "charts", "tables"],
                "template_type": "dashboard",
                "pages": ["dashboard/index.tsx", "dashboard/users.tsx", "dashboard/analytics.tsx"],
                "components": ["Sidebar", "StatsCards", "DataTable", "ChartWidget"]
            },
            {
                "name": "Analytics Dashboard",
                "slug": "analytics-dashboard",
                "category": "templates",
                "description": "Analytics-focused dashboard with real-time data visualization",
                "tags": ["analytics", "charts", "realtime", "data"],
                "template_type": "dashboard",
                "pages": ["analytics/index.tsx", "analytics/reports.tsx"],
                "components": ["RealtimeChart", "MetricCards", "FilterPanel"]
            },
            
            # Blog Templates
            {
                "name": "Blog Template",
                "slug": "blog-template",
                "category": "templates",
                "description": "Clean blog template with MDX support and SEO optimization",
                "tags": ["blog", "mdx", "seo", "content"],
                "template_type": "blog",
                "pages": ["blog/index.tsx", "blog/[slug].tsx"],
                "components": ["PostCard", "PostContent", "AuthorBio", "RelatedPosts"]
            },
            {
                "name": "Documentation Site",
                "slug": "documentation-site",
                "category": "templates",
                "description": "Documentation template with search and navigation",
                "tags": ["docs", "documentation", "search", "navigation"],
                "template_type": "documentation",
                "pages": ["docs/[[...slug]].tsx"],
                "components": ["DocsSidebar", "SearchBar", "ContentNav", "CodeBlock"]
            },
            
            # Component Library
            {
                "name": "Next.js Navigation",
                "slug": "nextjs-navigation",
                "category": "navigation",
                "description": "Navigation components optimized for Next.js with Link integration",
                "tags": ["navigation", "nextjs", "link", "routing"],
                "template_type": "component",
                "components": ["NavBar", "SideNav", "BreadcrumbNav"]
            },
            {
                "name": "SEO Components",
                "slug": "seo-components",
                "category": "other",
                "description": "SEO-optimized components with Next.js Head integration",
                "tags": ["seo", "head", "meta", "optimization"],
                "template_type": "component",
                "components": ["SEOHead", "OpenGraphMeta", "StructuredData"]
            },
            {
                "name": "Image Components",
                "slug": "image-components",
                "category": "data_display",
                "description": "Optimized image components using Next.js Image",
                "tags": ["image", "optimization", "responsive", "lazy"],
                "template_type": "component",
                "components": ["OptimizedImage", "ImageGallery", "ImagePlaceholder"]
            },
            {
                "name": "Form Components",
                "slug": "form-components",
                "category": "forms",
                "description": "Form components with validation and Next.js API integration",
                "tags": ["forms", "validation", "api", "submission"],
                "template_type": "component",
                "components": ["ContactForm", "NewsletterForm", "FeedbackForm"]
            },
            {
                "name": "Loading States",
                "slug": "loading-states",
                "category": "feedback",
                "description": "Loading components optimized for Next.js routing",
                "tags": ["loading", "skeleton", "spinner", "routing"],
                "template_type": "component",
                "components": ["RouteLoader", "ContentSkeleton", "LazyLoader"]
            },
            {
                "name": "Error Boundaries",
                "slug": "error-boundaries",
                "category": "feedback",
                "description": "Error handling components for Next.js applications",
                "tags": ["error", "boundary", "fallback", "recovery"],
                "template_type": "component",
                "components": ["ErrorBoundary", "ErrorPage", "NotFound"]
            }
        ]
        
        components = []
        for comp_data in nextjs_components:
            manifest = self._create_manifest_from_data(comp_data)
            components.append(manifest)
        
        return components
    
    def _create_manifest_from_data(self, comp_data: Dict[str, Any]) -> ComponentManifest:
        """Create component manifest from component data."""
        name = comp_data["name"]
        slug = comp_data["slug"]
        category = comp_data["category"]
        
        # Generate sample code based on template type
        sample_code = self._generate_nextjs_code(comp_data)
        
        return ComponentManifest(
            id=f"nextjs-design/{slug}",
            provider=Provider.NEXTJS_DESIGN,
            name=name,
            slug=slug,
            category=ComponentCategory(category),
            tags=comp_data["tags"],
            license=License(
                type=LicenseType.MIT,
                url="https://nextjs.design/license",
                notes="Next.js Design templates and components under MIT license",
                redistribute=True,
                commercial=True
            ),
            source=Source(
                url=f"https://nextjs.design/templates/{slug}",
                branch=None
            ),
            framework=Framework(
                react=True,
                next=True,  # Next.js specific
                vue=False,
                svelte=False,
                angular=False
            ),
            tailwind=TailwindConfig(
                version=TailwindVersion.V3,
                plugin_deps=["@tailwindcss/typography", "@tailwindcss/forms"],
                required_classes=[]
            ),
            runtime_deps=["next", "react", "react-dom"] + self._get_template_deps(comp_data),
            install=InstallPlan(
                npm=["next", "react", "react-dom"] + self._get_template_deps(comp_data),
                steps=[
                    {
                        "type": "info",
                        "description": "Next.js Design template optimized for Next.js applications"
                    },
                    {
                        "type": "action", 
                        "description": "Run 'npx create-next-app@latest' to start with Next.js"
                    }
                ]
            ),
            code=ComponentCode(
                tsx=sample_code
            ),
            access=ComponentAccess(
                copy_paste=True,
                pro=False
            ),
            description=comp_data["description"],
            documentation_url=f"https://nextjs.design/docs/{slug}",
            demo_url=f"https://nextjs.design/templates/{slug}",
            keywords=comp_data["tags"] + ["nextjs", "react", "template"]
        )
    
    def _get_template_deps(self, comp_data: Dict[str, Any]) -> List[str]:
        """Get dependencies based on template type."""
        template_type = comp_data.get("template_type", "component")
        base_deps = []
        
        if template_type == "dashboard":
            base_deps.extend(["recharts", "@heroicons/react"])
        elif template_type == "ecommerce":
            base_deps.extend(["@heroicons/react", "stripe"])
        elif template_type == "blog":
            base_deps.extend(["@next/mdx", "gray-matter", "remark", "rehype"])
        elif template_type == "documentation":
            base_deps.extend(["@next/mdx", "flexsearch", "@heroicons/react"])
        elif "seo" in comp_data["slug"]:
            base_deps.extend(["next-seo"])
        elif "form" in comp_data["slug"]:
            base_deps.extend(["react-hook-form", "@hookform/resolvers", "zod"])
        
        return base_deps
    
    def _generate_nextjs_code(self, comp_data: Dict[str, Any]) -> str:
        """Generate Next.js specific code."""
        slug = comp_data["slug"]
        name = comp_data["name"]
        template_type = comp_data.get("template_type", "component")
        
        if template_type == "landing" and "saas" in slug:
            return '''import Head from 'next/head'
import Link from 'next/link'
import Image from 'next/image'

export default function SaaSLandingPage() {
  return (
    <>
      <Head>
        <title>SaaS Product - Streamline Your Workflow</title>
        <meta name="description" content="Revolutionary SaaS solution to boost your productivity" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      
      <div className="min-h-screen bg-white">
        {/* Navigation */}
        <nav className="border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <h1 className="text-2xl font-bold text-gray-900">SaaSApp</h1>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/login" className="text-gray-500 hover:text-gray-900">
                  Sign in
                </Link>
                <Link href="/signup" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                  Get Started
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="relative bg-white overflow-hidden">
          <div className="max-w-7xl mx-auto">
            <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
              <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
                <div className="sm:text-center lg:text-left">
                  <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                    <span className="block xl:inline">Streamline your</span>
                    <span className="block text-blue-600 xl:inline">workflow today</span>
                  </h1>
                  <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                    Boost productivity with our revolutionary SaaS platform. Automate tasks, 
                    collaborate seamlessly, and scale your business effortlessly.
                  </p>
                  <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                    <div className="rounded-md shadow">
                      <Link href="/signup" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10">
                        Start Free Trial
                      </Link>
                    </div>
                    <div className="mt-3 sm:mt-0 sm:ml-3">
                      <Link href="/demo" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 md:py-4 md:text-lg md:px-10">
                        Watch Demo
                      </Link>
                    </div>
                  </div>
                </div>
              </main>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-12 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="lg:text-center">
              <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Features</h2>
              <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                Everything you need to succeed
              </p>
            </div>

            <div className="mt-10">
              <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
                <div className="relative">
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Lightning Fast</p>
                  <p className="mt-2 ml-16 text-base text-gray-500">
                    Built for speed with modern technologies and optimized performance.
                  </p>
                </div>

                <div className="relative">
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Secure by Default</p>
                  <p className="mt-2 ml-16 text-base text-gray-500">
                    Enterprise-grade security with end-to-end encryption and compliance.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}'''
        
        elif template_type == "dashboard":
            return '''import Head from 'next/head'
import { useState } from 'react'
import Link from 'next/link'

export default function AdminDashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <>
      <Head>
        <title>Admin Dashboard</title>
        <meta name="description" content="Admin dashboard with analytics and management tools" />
      </Head>

      <div className="min-h-screen bg-gray-100">
        {/* Sidebar */}
        <div className="fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0">
          <div className="flex items-center justify-center h-16 bg-gray-900">
            <h1 className="text-white text-xl font-bold">Admin Panel</h1>
          </div>
          
          <nav className="mt-8">
            <div className="px-4 space-y-2">
              <Link href="/dashboard" className="flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md">
                <svg className="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                </svg>
                Dashboard
              </Link>
              
              <Link href="/users" className="flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md">
                <svg className="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
                Users
              </Link>
              
              <Link href="/analytics" className="flex items-center px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white rounded-md">
                <svg className="mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                Analytics
              </Link>
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <div className="lg:pl-64">
          <div className="px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8">
              <h1 className="text-2xl font-semibold text-gray-900">Dashboard Overview</h1>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Total Users</p>
                    <p className="text-2xl font-semibold text-gray-900">12,345</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"></path>
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Revenue</p>
                    <p className="text-2xl font-semibold text-gray-900">$54,321</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Orders</p>
                    <p className="text-2xl font-semibold text-gray-900">1,234</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clipRule="evenodd"></path>
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Active Users</p>
                    <p className="text-2xl font-semibold text-gray-900">8,901</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Chart Placeholder */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Analytics Overview</h2>
              <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                <p className="text-gray-500">Chart component would go here</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}'''
        
        elif "navigation" in slug:
            return '''import Link from 'next/link'
import { useRouter } from 'next/router'
import { useState } from 'react'

export function NextJSNavigation() {
  const router = useRouter()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'About', href: '/about' },
    { name: 'Services', href: '/services' },
    { name: 'Contact', href: '/contact' },
  ]

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0">
              <span className="text-2xl font-bold text-blue-600">Logo</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  router.pathname === item.href
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                    router.pathname === item.href
                      ? 'text-blue-600 bg-blue-50'
                      : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                  }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}'''
        
        else:
            # Generic Next.js component
            component_name = name.replace(" ", "").replace(".", "")
            return f'''import Head from 'next/head'
import {{ useState, useEffect }} from 'react'

export default function {component_name}() {{
  const [mounted, setMounted] = useState(false)

  useEffect(() => {{
    setMounted(true)
  }}, [])

  if (!mounted) {{
    return null
  }}

  return (
    <>
      <Head>
        <title>{name}</title>
        <meta name="description" content="{comp_data['description']}" />
      </Head>
      
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
              {name}
            </h1>
            <p className="mt-4 text-xl text-gray-600">
              {comp_data['description']}
            </p>
          </div>
          
          <div className="mt-12">
            {{/* Component content goes here */}}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <p className="text-gray-600">
                This is a Next.js component template. Customize the content 
                based on your specific needs.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}}'''