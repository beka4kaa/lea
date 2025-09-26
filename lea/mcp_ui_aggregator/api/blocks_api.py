"""API endpoints for UI blocks and installation plans."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from ..providers.registry import get_all_providers
from ..models.component_manifest import ComponentManifest

router = APIRouter()

# Request/Response models
class BlockRequest(BaseModel):
    block_type: str
    target: str = "nextjs"
    style: str = "tailwind"

class InstallPlanRequest(BaseModel):
    component_ids: List[str]
    target: str = "nextjs"
    package_manager: str = "npm"

class VerifyRequest(BaseModel):
    code: str
    framework: str
    check_imports: bool = True
    check_syntax: bool = True

class BlockResponse(BaseModel):
    name: str
    description: str
    files: List[Dict[str, str]]
    dependencies: List[str]
    commands: List[str]

class InstallPlanResponse(BaseModel):
    component_ids: List[str]
    target: str
    package_manager: str
    runtime_dependencies: List[str]
    peer_dependencies: List[str]
    commands: List[Dict[str, str]]

class VerifyResponse(BaseModel):
    code_length: int
    framework: str
    issues: List[Dict[str, str]]
    is_valid: bool
    suggestions: List[str]


# UI Block generators
UI_BLOCKS = {
    "auth": {
        "name": "Authentication Form",
        "description": "Login/signup form with validation",
        "dependencies": ["react-hook-form", "zod", "@hookform/resolvers"],
        "code": '''import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginFormData) => {
    console.log('Login data:', data);
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-center mb-6">Sign In</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            {...register('email')}
            type="email"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your email"
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
          )}
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            {...register('password')}
            type="password"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password"
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>
        
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
        >
          Sign In
        </button>
        
        <div className="text-center">
          <a href="#" className="text-sm text-blue-600 hover:text-blue-500">
            Forgot your password?
          </a>
        </div>
      </form>
    </div>
  );
}'''
    },
    "navbar": {
        "name": "Navigation Bar",
        "description": "Responsive navigation with mobile menu",
        "dependencies": ["@headlessui/react"],
        "code": '''import React, { useState } from 'react';
import { Menu, X } from 'lucide-react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const navigation = [
    { name: 'Home', href: '#' },
    { name: 'Components', href: '#' },
    { name: 'Documentation', href: '#' },
    { name: 'About', href: '#' },
  ];

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-gray-800">Lea</h1>
            </div>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  {item.name}
                </a>
              ))}
            </div>
          </div>
          
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-blue-600 focus:outline-none focus:text-blue-600"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>
      
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className="text-gray-700 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium"
              >
                {item.name}
              </a>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}'''
    },
    "hero": {
        "name": "Hero Section",
        "description": "Landing page hero with CTA",
        "dependencies": [],
        "code": '''import React from 'react';
import { ArrowRight, Star } from 'lucide-react';

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-10"></div>
      <div className="max-w-7xl mx-auto">
        <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div className="sm:text-center lg:text-left">
              <div className="flex items-center mb-6 sm:justify-center lg:justify-start">
                <div className="flex items-center bg-yellow-100 rounded-full px-3 py-1">
                  <Star className="h-4 w-4 text-yellow-500 mr-1" />
                  <span className="text-sm text-yellow-800 font-medium">New: 11 UI Libraries</span>
                </div>
              </div>
              
              <h1 className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
                <span className="block xl:inline">UI Components</span>{' '}
                <span className="block text-yellow-400 xl:inline">Made Simple</span>
              </h1>
              
              <p className="mt-3 text-base text-gray-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                Access thousands of beautiful, ready-to-use UI components from the best design systems.
                Copy, paste, and customize in seconds with AI-powered recommendations.
              </p>
              
              <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div className="rounded-md shadow">
                  <a
                    href="#"
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10 transition-colors"
                  >
                    Get Started
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </a>
                </div>
                <div className="mt-3 sm:mt-0 sm:ml-3">
                  <a
                    href="#"
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 md:py-4 md:text-lg md:px-10 transition-colors"
                  >
                    Browse Components
                  </a>
                </div>
              </div>
              
              <div className="mt-8 flex items-center sm:justify-center lg:justify-start space-x-6">
                <div className="flex items-center text-gray-200">
                  <span className="text-2xl font-bold text-white">326</span>
                  <span className="ml-2 text-sm">Components</span>
                </div>
                <div className="flex items-center text-gray-200">
                  <span className="text-2xl font-bold text-white">11</span>
                  <span className="ml-2 text-sm">Providers</span>
                </div>
                <div className="flex items-center text-gray-200">
                  <span className="text-2xl font-bold text-white">100%</span>
                  <span className="ml-2 text-sm">Free</span>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}'''
    },
    "pricing": {
        "name": "Pricing Table",
        "description": "Pricing plans with feature comparison",
        "dependencies": [],
        "code": '''import React from 'react';
import { Check, X } from 'lucide-react';

const plans = [
  {
    name: 'Free',
    price: '$0',
    description: 'Perfect for getting started',
    features: [
      { name: 'Access to basic components', included: true },
      { name: 'Copy & paste code', included: true },
      { name: 'Community support', included: true },
      { name: 'MIT licensed components', included: true },
      { name: 'Premium components', included: false },
      { name: 'Priority support', included: false },
    ],
    cta: 'Get Started',
    popular: false
  },
  {
    name: 'Pro',
    price: '$29',
    description: 'For professional developers',
    features: [
      { name: 'Access to all components', included: true },
      { name: 'Premium blocks & templates', included: true },
      { name: 'Priority support', included: true },
      { name: 'Commercial license', included: true },
      { name: 'Advanced customization', included: true },
      { name: 'Private component library', included: false },
    ],
    cta: 'Start Free Trial',
    popular: true
  },
  {
    name: 'Team',
    price: '$99',
    description: 'For growing teams',
    features: [
      { name: 'Everything in Pro', included: true },
      { name: 'Team collaboration', included: true },
      { name: 'Private component library', included: true },
      { name: 'Design system tools', included: true },
      { name: 'SSO integration', included: true },
      { name: 'Custom integrations', included: true },
    ],
    cta: 'Contact Sales',
    popular: false
  }
];

export default function PricingTable() {
  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mt-4 text-xl text-gray-600">
            Choose the plan that works for you
          </p>
        </div>
        
        <div className="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-3 sm:gap-6 lg:max-w-4xl lg:mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative p-8 bg-white border rounded-lg shadow-sm ${
                plan.popular ? 'border-blue-500 ring-2 ring-blue-500' : 'border-gray-200'
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 right-6 transform -translate-y-1/2">
                  <span className="inline-flex px-4 py-1 text-sm font-semibold text-white bg-blue-500 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="text-center">
                <h3 className="text-2xl font-semibold text-gray-900">{plan.name}</h3>
                <p className="mt-2 text-gray-500">{plan.description}</p>
                <div className="mt-4">
                  <span className="text-4xl font-extrabold text-gray-900">{plan.price}</span>
                  <span className="text-base font-medium text-gray-500">/month</span>
                </div>
              </div>
              
              <ul className="mt-8 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature.name} className="flex items-start">
                    <div className="flex-shrink-0">
                      {feature.included ? (
                        <Check className="h-6 w-6 text-green-500" />
                      ) : (
                        <X className="h-6 w-6 text-gray-300" />
                      )}
                    </div>
                    <p className={`ml-3 text-base ${feature.included ? 'text-gray-700' : 'text-gray-400'}`}>
                      {feature.name}
                    </p>
                  </li>
                ))}
              </ul>
              
              <div className="mt-8">
                <button
                  className={`w-full py-3 px-6 border border-transparent rounded-md text-center font-medium transition-colors ${
                    plan.popular
                      ? 'text-white bg-blue-600 hover:bg-blue-700'
                      : 'text-blue-600 bg-blue-50 hover:bg-blue-100'
                  }`}
                >
                  {plan.cta}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}'''
    }
}


@router.post("/blocks", response_model=BlockResponse)
async def create_block(request: BlockRequest):
    """Generate UI block with multiple components."""
    block_type = request.block_type.lower()
    
    if block_type not in UI_BLOCKS:
        raise HTTPException(
            status_code=404,
            detail=f"Block type '{block_type}' not found. Available: {list(UI_BLOCKS.keys())}"
        )
    
    block = UI_BLOCKS[block_type]
    
    # Generate file structure based on target framework
    file_extension = "tsx" if request.target in ["nextjs", "react"] else "vue" if request.target == "vue" else "svelte"
    file_path = f"components/{block_type}/{block['name'].replace(' ', '')}.{file_extension}"
    
    return BlockResponse(
        name=block["name"],
        description=block["description"],
        files=[
            {
                "path": file_path,
                "content": block["code"]
            }
        ],
        dependencies=block["dependencies"],
        commands=[f"npm install {' '.join(block['dependencies'])}" if block['dependencies'] else "# No additional dependencies needed"]
    )


@router.post("/install-plan", response_model=InstallPlanResponse)
async def create_install_plan(request: InstallPlanRequest):
    """Generate installation plan for components."""
    providers = get_all_providers()
    provider_map = {p.provider_name.value: p for p in providers}
    
    all_runtime_deps = set()
    all_peer_deps = set()
    commands = []
    
    for component_id in request.component_ids:
        if "/" not in component_id:
            continue
        
        provider_name, comp_slug = component_id.split("/", 1)
        
        if provider_name not in provider_map:
            continue
        
        provider = provider_map[provider_name]
        
        try:
            component = await provider.get_component(comp_slug)
            all_runtime_deps.update(component.runtime_deps)
            all_peer_deps.update(component.peer_deps)
            
            # Add CLI command if available
            if component.access.cli:
                commands.append({
                    "type": "cli",
                    "command": component.access.cli,
                    "description": f"Install {component.name}"
                })
        except Exception:
            continue
    
    # Generate install commands
    if all_runtime_deps or all_peer_deps:
        deps_to_install = list(all_runtime_deps | all_peer_deps)
        
        if request.package_manager == "npm":
            cmd = f"npm install {' '.join(deps_to_install)}"
        elif request.package_manager == "yarn":
            cmd = f"yarn add {' '.join(deps_to_install)}"
        elif request.package_manager == "pnpm":
            cmd = f"pnpm add {' '.join(deps_to_install)}"
        elif request.package_manager == "bun":
            cmd = f"bun add {' '.join(deps_to_install)}"
        else:
            cmd = f"npm install {' '.join(deps_to_install)}"
        
        commands.insert(0, {
            "type": "install",
            "command": cmd,
            "description": "Install dependencies"
        })
    
    return InstallPlanResponse(
        component_ids=request.component_ids,
        target=request.target,
        package_manager=request.package_manager,
        runtime_dependencies=list(all_runtime_deps),
        peer_dependencies=list(all_peer_deps),
        commands=commands
    )


@router.post("/verify", response_model=VerifyResponse)
async def verify_code(request: VerifyRequest):
    """Verify component code and dependencies."""
    issues = []
    
    if request.check_syntax:
        # Basic syntax checks
        if request.framework in ["react", "nextjs"]:
            if "import" in request.code and not request.code.strip().startswith("import"):
                issues.append({
                    "type": "syntax",
                    "severity": "warning", 
                    "message": "Imports should be at the top of the file"
                })
            
            if "export default" not in request.code and "export {" not in request.code:
                issues.append({
                    "type": "syntax",
                    "severity": "error",
                    "message": "Component must have a default export"
                })
            
            # Check for React import
            if "React" in request.code and "import React" not in request.code:
                issues.append({
                    "type": "import",
                    "severity": "error",
                    "message": "Missing React import"
                })
    
    if request.check_imports:
        # Check for common import issues
        import_lines = [line.strip() for line in request.code.split("\n") if line.strip().startswith("import")]
        
        for line in import_lines:
            if "from ''" in line or 'from ""' in line:
                issues.append({
                    "type": "import",
                    "severity": "error",
                    "message": f"Empty import path: {line}"
                })
            
            # Check for relative imports that might be broken
            if "from './" in line or 'from "./' in line:
                issues.append({
                    "type": "import",
                    "severity": "warning",
                    "message": f"Relative import detected, ensure path exists: {line}"
                })
    
    # Generate suggestions
    suggestions = []
    if not issues:
        suggestions.extend([
            "Consider adding TypeScript types for better development experience",
            "Add proper error boundaries for production use",
            "Consider accessibility attributes (aria-labels, roles, etc.)"
        ])
    
    return VerifyResponse(
        code_length=len(request.code),
        framework=request.framework,
        issues=issues,
        is_valid=len([i for i in issues if i["severity"] == "error"]) == 0,
        suggestions=suggestions
    )