#!/usr/bin/env python3
"""Script to load new ingestion modules into the database."""

import asyncio
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from mcp_ui_aggregator.core.database import async_session_maker, create_tables
from mcp_ui_aggregator.models.database import Component, ComponentType


# New components data to add
NEW_COMPONENTS_DATA = [
    # Bootstrap Components
    {
        "name": "Button",
        "namespace": "bootstrap",
        "component_type": ComponentType.BUTTON.value,
        "title": "Bootstrap Button",
        "description": "Bootstrap's custom button styles for actions in forms, dialogs, and more with support for multiple sizes, states, and more.",
        "tags": json.dumps(["button", "bootstrap", "html", "css"]),
        "documentation_url": "https://getbootstrap.com/docs/5.3/components/buttons/",
        "api_reference_url": "https://getbootstrap.com/docs/5.3/components/buttons/",
        "import_statement": "<!-- Bootstrap CSS -->\n<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">",
        "basic_usage": "<button type=\"button\" class=\"btn btn-primary\">Primary</button>",
    },
    {
        "name": "Card",
        "namespace": "bootstrap",
        "component_type": ComponentType.CARD.value,
        "title": "Bootstrap Card",
        "description": "Bootstrap's cards provide a flexible and extensible content container with multiple variants and options.",
        "tags": json.dumps(["card", "bootstrap", "html", "container"]),
        "documentation_url": "https://getbootstrap.com/docs/5.3/components/card/",
        "api_reference_url": "https://getbootstrap.com/docs/5.3/components/card/",
        "import_statement": "<!-- Bootstrap CSS -->\n<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">",
        "basic_usage": "<div class=\"card\">\n  <div class=\"card-body\">\n    <h5 class=\"card-title\">Card title</h5>\n    <p class=\"card-text\">Some quick example text.</p>\n  </div>\n</div>",
    },
    {
        "name": "Modal",
        "namespace": "bootstrap",
        "component_type": ComponentType.MODAL.value,
        "title": "Bootstrap Modal",
        "description": "Use Bootstrap's JavaScript modal plugin to add dialogs to your site for lightboxes, user notifications, or completely custom content.",
        "tags": json.dumps(["modal", "bootstrap", "html", "javascript"]),
        "documentation_url": "https://getbootstrap.com/docs/5.3/components/modal/",
        "api_reference_url": "https://getbootstrap.com/docs/5.3/components/modal/",
        "import_statement": "<!-- Bootstrap CSS and JS -->\n<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>",
        "basic_usage": "<div class=\"modal fade\" id=\"exampleModal\" tabindex=\"-1\">\n  <div class=\"modal-dialog\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <h5 class=\"modal-title\">Modal title</h5>\n      </div>\n      <div class=\"modal-body\">...</div>\n    </div>\n  </div>\n</div>",
    },
    
    # Tailwind Components
    {
        "name": "Button",
        "namespace": "tailwind",
        "component_type": ComponentType.BUTTON.value,
        "title": "Tailwind Button",
        "description": "Utility-first CSS button component with Tailwind classes for maximum customization.",
        "tags": json.dumps(["button", "tailwind", "css", "utility"]),
        "documentation_url": "https://tailwindcss.com/docs",
        "api_reference_url": "https://tailwindcss.com/docs",
        "import_statement": "<!-- Tailwind CSS -->\n<script src=\"https://cdn.tailwindcss.com\"></script>",
        "basic_usage": "<button class=\"bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded\">Button</button>",
    },
    {
        "name": "Card",
        "namespace": "tailwind",
        "component_type": ComponentType.CARD.value,
        "title": "Tailwind Card",
        "description": "Flexible card component built with Tailwind CSS utility classes.",
        "tags": json.dumps(["card", "tailwind", "css", "container"]),
        "documentation_url": "https://tailwindcss.com/docs",
        "api_reference_url": "https://tailwindcss.com/docs",
        "import_statement": "<!-- Tailwind CSS -->\n<script src=\"https://cdn.tailwindcss.com\"></script>",
        "basic_usage": "<div class=\"max-w-sm rounded overflow-hidden shadow-lg\">\n  <div class=\"px-6 py-4\">\n    <div class=\"font-bold text-xl mb-2\">Card Title</div>\n    <p class=\"text-gray-700 text-base\">Card content</p>\n  </div>\n</div>",
    },
    
    # Bulma Components  
    {
        "name": "Button",
        "namespace": "bulma",
        "component_type": ComponentType.BUTTON.value,
        "title": "Bulma Button",
        "description": "The classic button, in different colors, sizes, and states.",
        "tags": json.dumps(["button", "bulma", "css"]),
        "documentation_url": "https://bulma.io/documentation/elements/button/",
        "api_reference_url": "https://bulma.io/documentation/elements/button/",
        "import_statement": "<!-- Bulma CSS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css\">",
        "basic_usage": "<button class=\"button is-primary\">Primary</button>",
    },
    {
        "name": "Card",
        "namespace": "bulma",
        "component_type": ComponentType.CARD.value,
        "title": "Bulma Card",
        "description": "An all-around flexible and composable component.",
        "tags": json.dumps(["card", "bulma", "css", "container"]),
        "documentation_url": "https://bulma.io/documentation/components/card/",
        "api_reference_url": "https://bulma.io/documentation/components/card/",
        "import_statement": "<!-- Bulma CSS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css\">",
        "basic_usage": "<div class=\"card\">\n  <div class=\"card-content\">\n    <div class=\"content\">\n      Card content\n    </div>\n  </div>\n</div>",
    },
    
    # Vuetify Components
    {
        "name": "VBtn",
        "namespace": "vuetify",
        "component_type": ComponentType.BUTTON.value,
        "title": "Vuetify Button",
        "description": "The v-btn component replaces the standard html button with a material design theme and a multitude of options.",
        "tags": json.dumps(["button", "vuetify", "vue", "material"]),
        "documentation_url": "https://vuetifyjs.com/en/components/buttons/",
        "api_reference_url": "https://vuetifyjs.com/en/components/buttons/",
        "import_statement": "import { createApp } from 'vue'\nimport { createVuetify } from 'vuetify'",
        "basic_usage": "<v-btn color=\"primary\">Primary</v-btn>",
    },
    {
        "name": "VCard",
        "namespace": "vuetify",
        "component_type": ComponentType.CARD.value,
        "title": "Vuetify Card",
        "description": "The v-card component is a versatile component that can be used for anything from a panel to a static image.",
        "tags": json.dumps(["card", "vuetify", "vue", "material"]),
        "documentation_url": "https://vuetifyjs.com/en/components/cards/",
        "api_reference_url": "https://vuetifyjs.com/en/components/cards/",
        "import_statement": "import { createApp } from 'vue'\nimport { createVuetify } from 'vuetify'",
        "basic_usage": "<v-card>\n  <v-card-title>Card Title</v-card-title>\n  <v-card-text>Card content</v-card-text>\n</v-card>",
    },
    
    # PrimeNG Components
    {
        "name": "Button",
        "namespace": "primeng",
        "component_type": ComponentType.BUTTON.value,
        "title": "PrimeNG Button",
        "description": "Button is an extension to standard button element with icons and theming.",
        "tags": json.dumps(["button", "primeng", "angular"]),
        "documentation_url": "https://primeng.org/button",
        "api_reference_url": "https://primeng.org/button",
        "import_statement": "import { ButtonModule } from 'primeng/button';",
        "basic_usage": "<p-button label=\"Click\" (onClick)=\"handleClick()\"></p-button>",
    },
    {
        "name": "Card",
        "namespace": "primeng",
        "component_type": ComponentType.CARD.value,
        "title": "PrimeNG Card",
        "description": "Card is a flexible container component.",
        "tags": json.dumps(["card", "primeng", "angular"]),
        "documentation_url": "https://primeng.org/card",
        "api_reference_url": "https://primeng.org/card",
        "import_statement": "import { CardModule } from 'primeng/card';",
        "basic_usage": "<p-card header=\"Card Title\">\n  <p>Lorem ipsum dolor sit amet.</p>\n</p-card>",
    },
    
    # Angular Material Components
    {
        "name": "MatButton",
        "namespace": "angular-material",
        "component_type": ComponentType.BUTTON.value,
        "title": "Angular Material Button",
        "description": "Material Design button with elevation and ink ripples.",
        "tags": json.dumps(["button", "material", "angular"]),
        "documentation_url": "https://material.angular.io/components/button",
        "api_reference_url": "https://material.angular.io/components/button",
        "import_statement": "import { MatButtonModule } from '@angular/material/button';",
        "basic_usage": "<button mat-button>Basic</button>",
    },
    {
        "name": "MatCard",
        "namespace": "angular-material",
        "component_type": ComponentType.CARD.value,
        "title": "Angular Material Card",
        "description": "Material Design card container for content.",
        "tags": json.dumps(["card", "material", "angular"]),
        "documentation_url": "https://material.angular.io/components/card",
        "api_reference_url": "https://material.angular.io/components/card",
        "import_statement": "import { MatCardModule } from '@angular/material/card';",
        "basic_usage": "<mat-card>\n  <mat-card-content>\n    Simple card\n  </mat-card-content>\n</mat-card>",
    },
    
    # Svelte Components
    {
        "name": "Button",
        "namespace": "svelte",
        "component_type": ComponentType.BUTTON.value,
        "title": "Svelte Button",
        "description": "Interactive button component with various styles and states.",
        "tags": json.dumps(["button", "svelte", "interactive"]),
        "documentation_url": "https://svelte.dev/docs",
        "api_reference_url": "https://svelte.dev/docs",
        "import_statement": "import Button from '$lib/components/Button.svelte';",
        "basic_usage": "<Button>Click me</Button>",
    },
    {
        "name": "Card",
        "namespace": "svelte",
        "component_type": ComponentType.CARD.value,
        "title": "Svelte Card",
        "description": "Flexible card container component for displaying content.",
        "tags": json.dumps(["card", "svelte", "container"]),
        "documentation_url": "https://svelte.dev/docs",
        "api_reference_url": "https://svelte.dev/docs",
        "import_statement": "import Card from '$lib/components/Card.svelte';",
        "basic_usage": "<Card>\n  <p>Card content</p>\n</Card>",
    },
]


async def load_new_modules():
    """Load all new components into the database."""
    print("🚀 Starting to load new UI library components...")
    
    # Create tables if they don't exist
    await create_tables()
    
    total_components = 0
    
    async with async_session_maker() as session:
        for component_data in NEW_COMPONENTS_DATA:
            # Check if component already exists
            exists_q = select(Component.id).where(
                Component.name == component_data["name"],
                Component.namespace == component_data["namespace"],
            )
            res = await session.execute(exists_q)
            if res.scalar_one_or_none() is not None:
                print(f"  ⚠️  Component '{component_data['name']}' ({component_data['namespace']}) already exists, skipping...")
                continue
            
            # Add component to database
            component = Component(**component_data)
            session.add(component)
            print(f"  ✅ Added '{component_data['name']}' ({component_data['namespace']})")
            total_components += 1
        
        # Commit all changes
        await session.commit()
    
    print(f"\n🎉 Successfully loaded {total_components} new components!")
    
    # Show summary
    print("\n📊 Database Summary:")
    async with async_session_maker() as session:
        result = await session.execute(select(Component))
        all_components = result.scalars().all()
        
        frameworks = {}
        for component in all_components:
            framework = component.namespace
            if framework not in frameworks:
                frameworks[framework] = 0
            frameworks[framework] += 1
        
        for framework, count in frameworks.items():
            print(f"  • {framework}: {count} components")
        
        print(f"\n📈 Total components in database: {len(all_components)}")


if __name__ == "__main__":
    asyncio.run(load_new_modules())