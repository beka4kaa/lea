"""Tailwind CSS component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class TailwindIngestionModule(BaseIngestionModule):
    """Tailwind CSS component ingestion."""
    
    def get_namespace(self) -> str:
        return "tailwind"
    
    def get_framework(self) -> str:
        return "html"
    
    def get_base_url(self) -> str:
        return "https://tailwindcss.com/docs"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Tailwind CSS utility-first components."""
        return [
            {
                "name": "Button",
                "title": "Tailwind Button",
                "description": "Beautiful buttons using Tailwind CSS utility classes.",
                "component_type": "button",
                "category": "forms",
                "framework": "html",
                "tags": ["button", "tailwind", "utility", "responsive"],
                "documentation_url": f"{self.get_base_url()}/",
                "import_statement": '<script src="https://cdn.tailwindcss.com"></script>',
                "basic_usage": '<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Button</button>',
                "variants": {
                    "primary": '<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Primary</button>',
                    "secondary": '<button class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">Secondary</button>',
                    "success": '<button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Success</button>',
                    "danger": '<button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">Danger</button>',
                    "outline": '<button class="bg-transparent hover:bg-blue-500 text-blue-700 hover:text-white border border-blue-500 hover:border-transparent py-2 px-4 rounded">Outline</button>',
                    "ghost": '<button class="text-blue-500 hover:text-blue-700 font-semibold py-2 px-4">Ghost</button>',
                    "loading": '<button class="bg-blue-500 text-white font-bold py-2 px-4 rounded opacity-50 cursor-not-allowed" disabled><span class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>Loading</button>'
                },
                "examples": [
                    {
                        "title": "Button Group",
                        "description": "Group buttons together",
                        "code": '''<div class="inline-flex rounded-md shadow-sm" role="group">
  <button class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-l-lg hover:bg-gray-100">Left</button>
  <button class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border-t border-b border-gray-200 hover:bg-gray-100">Middle</button>
  <button class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-r-md hover:bg-gray-100">Right</button>
</div>'''
                    }
                ]
            },
            {
                "name": "Card",
                "title": "Tailwind Card",
                "description": "Flexible card component built with Tailwind CSS.",
                "component_type": "display",
                "category": "layout",
                "framework": "html",
                "tags": ["card", "tailwind", "container", "shadow"],
                "documentation_url": f"{self.get_base_url()}/",
                "import_statement": '<script src="https://cdn.tailwindcss.com"></script>',
                "basic_usage": '''<div class="max-w-sm rounded overflow-hidden shadow-lg">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">Card Title</div>
    <p class="text-gray-700 text-base">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit.
    </p>
  </div>
</div>''',
                "examples": [
                    {
                        "title": "Card with Image",
                        "description": "Card with image header",
                        "code": '''<div class="max-w-sm rounded overflow-hidden shadow-lg">
  <img class="w-full" src="/img/card-top.jpg" alt="Sunset in the mountains">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">The Coldest Sunset</div>
    <p class="text-gray-700 text-base">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit.
    </p>
  </div>
  <div class="px-6 pt-4 pb-2">
    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">#photography</span>
    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">#travel</span>
  </div>
</div>'''
                    }
                ]
            },
            {
                "name": "Modal",
                "title": "Tailwind Modal",
                "description": "Modal dialog component with Tailwind CSS and Alpine.js.",
                "component_type": "overlay",
                "category": "feedback",
                "framework": "html",
                "tags": ["modal", "dialog", "tailwind", "alpine"],
                "documentation_url": f"{self.get_base_url()}/",
                "import_statement": '''<script src="https://cdn.tailwindcss.com"></script>
<script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>''',
                "basic_usage": '''<div x-data="{ open: false }">
  <button @click="open = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
    Open Modal
  </button>
  
  <div x-show="open" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" x-transition>
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <div class="mt-3 text-center">
        <h3 class="text-lg font-medium text-gray-900">Modal Title</h3>
        <div class="mt-2 px-7 py-3">
          <p class="text-sm text-gray-500">Modal content goes here.</p>
        </div>
        <div class="items-center px-4 py-3">
          <button @click="open = false" class="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md shadow-sm hover:bg-gray-700">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</div>'''
            },
            {
                "name": "Navbar",
                "title": "Tailwind Navbar",
                "description": "Responsive navigation bar with Tailwind CSS.",
                "component_type": "navigation",
                "category": "navigation",
                "framework": "html",
                "tags": ["navbar", "navigation", "tailwind", "responsive"],
                "documentation_url": f"{self.get_base_url()}/",
                "import_statement": '''<script src="https://cdn.tailwindcss.com"></script>
<script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>''',
                "basic_usage": '''<nav class="bg-gray-800" x-data="{ open: false }">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <img class="h-8 w-8" src="/logo.svg" alt="Logo">
        </div>
        <div class="hidden md:block">
          <div class="ml-10 flex items-baseline space-x-4">
            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
            <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
          </div>
        </div>
      </div>
      <div class="md:hidden">
        <button @click="open = !open" class="text-gray-400 hover:text-white focus:outline-none">
          <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
            <path :class="{'hidden': open, 'inline-flex': !open }" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path :class="{'hidden': !open, 'inline-flex': open }" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
  <div :class="{'block': open, 'hidden': !open}" class="md:hidden">
    <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
      <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Home</a>
      <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium">About</a>
    </div>
  </div>
</nav>'''
            },
            {
                "name": "Form",
                "title": "Tailwind Form",
                "description": "Beautiful forms with Tailwind CSS styling.",
                "component_type": "form",
                "category": "forms",
                "framework": "html",
                "tags": ["form", "input", "tailwind", "validation"],
                "documentation_url": f"{self.get_base_url()}/",
                "import_statement": '<script src="https://cdn.tailwindcss.com"></script>',
                "basic_usage": '''<form class="w-full max-w-lg">
  <div class="flex flex-wrap -mx-3 mb-6">
    <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
        First Name
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="grid-first-name" type="text" placeholder="Jane">
    </div>
    <div class="w-full md:w-1/2 px-3">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-last-name">
        Last Name
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-last-name" type="text" placeholder="Doe">
    </div>
  </div>
  <div class="flex flex-wrap -mx-3 mb-2">
    <div class="w-full px-3">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
        Send
      </button>
    </div>
  </div>
</form>'''
            }
        ]