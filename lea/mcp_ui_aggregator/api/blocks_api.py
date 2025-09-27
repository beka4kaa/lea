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
    },
    "footer": {
        "name": "Site Footer",
        "description": "Footer with links, social media, and company info",
        "dependencies": ["lucide-react"],
        "code": '''import React from 'react';
import { Github, Twitter, Linkedin, Mail } from 'lucide-react';

export default function Footer() {
  const navigation = {
    main: [
      { name: 'About', href: '#' },
      { name: 'Components', href: '#' },
      { name: 'Documentation', href: '#' },
      { name: 'Privacy', href: '#' },
      { name: 'Terms', href: '#' },
    ],
    social: [
      { name: 'Twitter', href: '#', icon: Twitter },
      { name: 'GitHub', href: '#', icon: Github },
      { name: 'LinkedIn', href: '#', icon: Linkedin },
      { name: 'Email', href: '#', icon: Mail },
    ],
  };

  return (
    <footer className="bg-gray-900">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-2xl font-bold text-white mb-4">Lea UI</h3>
            <p className="text-gray-400 max-w-md">
              Beautiful, accessible UI components for modern web applications. 
              Built with React, TypeScript, and Tailwind CSS.
            </p>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2">
              {navigation.main.map((item) => (
                <li key={item.name}>
                  <a href={item.href} className="text-gray-400 hover:text-white transition-colors">
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Connect</h4>
            <div className="flex space-x-4">
              {navigation.social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <item.icon className="h-6 w-6" />
                </a>
              ))}
            </div>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-gray-800">
          <p className="text-center text-gray-400">
            © 2024 Lea UI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}'''
    },
    "features": {
        "name": "Features Section",
        "description": "Product features showcase with icons",
        "dependencies": ["lucide-react"],
        "code": '''import React from 'react';
import { Zap, Shield, Users, Globe, Code, Smartphone } from 'lucide-react';

const features = [
  {
    name: 'Lightning Fast',
    description: 'Built for speed with modern technologies and optimized performance.',
    icon: Zap,
  },
  {
    name: 'Secure by Default',
    description: 'Enterprise-grade security with end-to-end encryption and compliance.',
    icon: Shield,
  },
  {
    name: 'Team Collaboration',
    description: 'Work together seamlessly with real-time collaboration tools.',
    icon: Users,
  },
  {
    name: 'Global Scale',
    description: 'Deploy worldwide with our global CDN and edge computing.',
    icon: Globe,
  },
  {
    name: 'Developer First',
    description: 'Built by developers, for developers with best practices in mind.',
    icon: Code,
  },
  {
    name: 'Mobile Ready',
    description: 'Responsive design that works perfectly on all devices.',
    icon: Smartphone,
  },
];

export default function Features() {
  return (
    <div className="py-12 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Features</h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to succeed
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Our platform provides all the tools and features you need to build amazing products.
          </p>
        </div>

        <div className="mt-10">
          <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-x-8 md:gap-y-10">
            {features.map((feature) => (
              <div key={feature.name} className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                  <feature.icon className="h-6 w-6" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">{feature.name}</p>
                <p className="mt-2 ml-16 text-base text-gray-500">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}'''
    },
    "testimonials": {
        "name": "Customer Testimonials",
        "description": "Customer reviews and testimonials",
        "dependencies": ["lucide-react"],
        "code": '''import React from 'react';
import { Star, Quote } from 'lucide-react';

const testimonials = [
  {
    content: "This platform has transformed our development workflow. The components are beautiful and the developer experience is outstanding.",
    author: {
      name: "Sarah Chen",
      role: "Lead Developer",
      company: "TechCorp Inc.",
      image: "https://images.unsplash.com/photo-1494790108755-2616b332c33c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
    },
    rating: 5
  },
  {
    content: "The best UI component library I've ever used. Clean, modern, and incredibly easy to customize.",
    author: {
      name: "Michael Rodriguez",
      role: "Product Manager",
      company: "StartupXYZ",
      image: "https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
    },
    rating: 5
  },
  {
    content: "Amazing components that helped us ship our product 3x faster. The documentation is excellent too.",
    author: {
      name: "Emily Johnson",
      role: "Frontend Architect",
      company: "DesignCo",
      image: "https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
    },
    rating: 5
  }
];

export default function Testimonials() {
  return (
    <div className="bg-gray-50 py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            What our customers say
          </h2>
          <p className="mt-4 text-xl text-gray-600">
            Don't just take our word for it - hear from some of our amazing customers
          </p>
        </div>
        
        <div className="mt-12 grid gap-8 lg:grid-cols-3 lg:gap-x-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex items-center mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              
              <div className="relative">
                <Quote className="absolute top-0 left-0 h-8 w-8 text-gray-300 transform -translate-x-2 -translate-y-2" />
                <p className="text-gray-700 text-lg leading-relaxed pl-6">
                  {testimonial.content}
                </p>
              </div>
              
              <div className="mt-6 flex items-center">
                <img
                  className="h-12 w-12 rounded-full"
                  src={testimonial.author.image}
                  alt={testimonial.author.name}
                />
                <div className="ml-4">
                  <div className="text-base font-medium text-gray-900">{testimonial.author.name}</div>
                  <div className="text-sm text-gray-600">
                    {testimonial.author.role} at {testimonial.author.company}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}'''
    },
    "cta": {
        "name": "Call to Action",
        "description": "Call-to-action section with buttons",
        "dependencies": ["lucide-react"],
        "code": '''import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';

export default function CallToAction() {
  return (
    <div className="bg-blue-700">
      <div className="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
        <div className="flex justify-center mb-6">
          <Sparkles className="h-12 w-12 text-blue-200" />
        </div>
        
        <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
          <span className="block">Ready to get started?</span>
          <span className="block text-blue-200">Start building today.</span>
        </h2>
        
        <p className="mt-4 text-lg leading-6 text-blue-200">
          Join thousands of developers who are already building amazing products with our platform.
          Get started in minutes with our comprehensive documentation and examples.
        </p>
        
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <button className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50 transition-colors">
            Start Free Trial
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
          
          <button className="inline-flex items-center justify-center px-8 py-3 border-2 border-white text-base font-medium rounded-md text-white hover:bg-white hover:text-blue-700 transition-colors">
            View Documentation
          </button>
        </div>
        
        <p className="mt-6 text-sm text-blue-200">
          No credit card required • Free 14-day trial • Cancel anytime
        </p>
      </div>
    </div>
  );
}'''
    },
    "dashboard": {
        "name": "Dashboard Layout",
        "description": "Admin dashboard with sidebar and stats",
        "dependencies": ["lucide-react"],
        "code": '''import React, { useState } from 'react';
import { Menu, X, Home, Users, BarChart3, Settings, Bell } from 'lucide-react';

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '#', icon: Home, current: true },
    { name: 'Users', href: '#', icon: Users, current: false },
    { name: 'Analytics', href: '#', icon: BarChart3, current: false },
    { name: 'Settings', href: '#', icon: Settings, current: false },
  ];

  const stats = [
    { name: 'Total Users', value: '12,345', change: '+12.5%', changeType: 'positive' },
    { name: 'Revenue', value: '$89,400', change: '+8.2%', changeType: 'positive' },
    { name: 'Orders', value: '1,234', change: '-2.1%', changeType: 'negative' },
    { name: 'Conversion', value: '3.24%', change: '+1.4%', changeType: 'positive' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}>
        <div className="flex items-center justify-center h-16 bg-gray-900">
          <h1 className="text-white text-xl font-bold">Admin Panel</h1>
        </div>
        
        <nav className="mt-8">
          <div className="px-4 space-y-2">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                  item.current
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </a>
            ))}
          </div>
        </nav>
      </div>

      {/* Main Content */}
      <div className="lg:pl-64">
        {/* Top Navigation */}
        <div className="sticky top-0 z-40 bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between px-4 h-16">
            <button
              type="button"
              className="lg:hidden"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              {sidebarOpen ? (
                <X className="h-6 w-6 text-gray-600" />
              ) : (
                <Menu className="h-6 w-6 text-gray-600" />
              )}
            </button>
            
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-600 hover:text-gray-900">
                <Bell className="h-6 w-6" />
              </button>
              <div className="h-8 w-8 bg-gray-300 rounded-full"></div>
            </div>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Welcome back! Here's what's happening.</p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat) => (
              <div key={stat.name} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-500">{stat.name}</p>
                    <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                  </div>
                  <div className={`text-sm font-medium ${
                    stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {stat.change}
                  </div>
                </div>
              </div>
            ))}
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
  );
}'''
    },
    "landing": {
        "name": "Complete Landing Page",
        "description": "Full landing page with hero, features, and CTA",
        "dependencies": ["lucide-react"],
        "code": '''import React from 'react';
import { ArrowRight, Check, Star, Zap, Shield, Users } from 'lucide-react';

export default function LandingPage() {
  const features = [
    { name: 'Lightning Fast', description: 'Built for speed and performance', icon: Zap },
    { name: 'Secure', description: 'Enterprise-grade security', icon: Shield },
    { name: 'Collaborative', description: 'Work together seamlessly', icon: Users },
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Build Amazing Products
              <span className="block text-blue-200">Faster Than Ever</span>
            </h1>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              The ultimate platform for developers to create beautiful, scalable applications
              with our comprehensive suite of tools and components.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="inline-flex items-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors">
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </button>
              <button className="inline-flex items-center px-8 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-blue-600 transition-colors">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why developers love our platform
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to build modern applications
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                  <feature.icon className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.name}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-blue-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
          <p className="text-xl mb-8">Join thousands of developers building amazing products</p>
          <button className="inline-flex items-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors">
            Start Building Today
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
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