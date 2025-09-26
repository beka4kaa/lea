#!/usr/bin/env python3
"""Script to add remaining UI libraries."""

import asyncio
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from mcp_ui_aggregator.core.database import async_session_maker, create_tables
from mcp_ui_aggregator.models.database import Component, ComponentType


# Remaining UI libraries components data
REMAINING_COMPONENTS_DATA = [
    # Semantic UI Components
    {
        "name": "Button",
        "namespace": "semantic-ui",
        "component_type": ComponentType.BUTTON.value,
        "title": "Semantic UI Button",
        "description": "A button indicates a possible user action.",
        "tags": json.dumps(["button", "semantic-ui", "css"]),
        "documentation_url": "https://semantic-ui.com/elements/button.html",
        "api_reference_url": "https://semantic-ui.com/elements/button.html",
        "import_statement": "<!-- Semantic UI CSS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css\">",
        "basic_usage": "<button class=\"ui button\">Button</button>",
    },
    {
        "name": "Card",
        "namespace": "semantic-ui",
        "component_type": ComponentType.CARD.value,
        "title": "Semantic UI Card",
        "description": "A card displays site content in a manner similar to a playing card.",
        "tags": json.dumps(["card", "semantic-ui", "css", "container"]),
        "documentation_url": "https://semantic-ui.com/views/card.html",
        "api_reference_url": "https://semantic-ui.com/views/card.html",
        "import_statement": "<!-- Semantic UI CSS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css\">",
        "basic_usage": "<div class=\"ui card\">\n  <div class=\"content\">\n    <div class=\"header\">Card Header</div>\n    <div class=\"description\">Card content</div>\n  </div>\n</div>",
    },
    {
        "name": "Modal",
        "namespace": "semantic-ui",
        "component_type": ComponentType.MODAL.value,
        "title": "Semantic UI Modal",
        "description": "A modal displays content that temporarily blocks interactions with the main view of a site.",
        "tags": json.dumps(["modal", "semantic-ui", "css", "javascript"]),
        "documentation_url": "https://semantic-ui.com/modules/modal.html",
        "api_reference_url": "https://semantic-ui.com/modules/modal.html",
        "import_statement": "<!-- Semantic UI CSS and JS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css\">\n<script src=\"https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js\"></script>",
        "basic_usage": "<div class=\"ui modal\">\n  <div class=\"header\">Modal Title</div>\n  <div class=\"content\">\n    <p>Modal content</p>\n  </div>\n  <div class=\"actions\">\n    <div class=\"ui button\">Cancel</div>\n    <div class=\"ui primary button\">OK</div>\n  </div>\n</div>",
    },
    
    # Foundation Components
    {
        "name": "Button",
        "namespace": "foundation",
        "component_type": ComponentType.BUTTON.value,
        "title": "Foundation Button",
        "description": "Buttons are convenient tools when you need more traditional actions.",
        "tags": json.dumps(["button", "foundation", "css"]),
        "documentation_url": "https://get.foundation/sites/docs/button.html",
        "api_reference_url": "https://get.foundation/sites/docs/button.html",
        "import_statement": "<!-- Foundation CSS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/foundation-sites@6.7.5/dist/css/foundation.min.css\">",
        "basic_usage": "<button class=\"button\">Primary Button</button>",
    },
    {
        "name": "Card",
        "namespace": "foundation",
        "component_type": ComponentType.CARD.value,
        "title": "Foundation Card",
        "description": "Cards are a popular and flexible UI component.",
        "tags": json.dumps(["card", "foundation", "css", "container"]),
        "documentation_url": "https://get.foundation/sites/docs/card.html",
        "api_reference_url": "https://get.foundation/sites/docs/card.html",
        "import_statement": "<!-- Foundation CSS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/foundation-sites@6.7.5/dist/css/foundation.min.css\">",
        "basic_usage": "<div class=\"card\">\n  <div class=\"card-divider\">\n    <h4>Card Title</h4>\n  </div>\n  <div class=\"card-section\">\n    <p>Card content goes here.</p>\n  </div>\n</div>",
    },
    {
        "name": "Reveal Modal",
        "namespace": "foundation",
        "component_type": ComponentType.MODAL.value,
        "title": "Foundation Reveal Modal",
        "description": "Modal dialogs, or pop-up windows, are handy for prototyping and production.",
        "tags": json.dumps(["modal", "foundation", "css", "javascript"]),
        "documentation_url": "https://get.foundation/sites/docs/reveal.html",
        "api_reference_url": "https://get.foundation/sites/docs/reveal.html",
        "import_statement": "<!-- Foundation CSS and JS -->\n<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/foundation-sites@6.7.5/dist/css/foundation.min.css\">\n<script src=\"https://cdn.jsdelivr.net/npm/foundation-sites@6.7.5/dist/js/foundation.min.js\"></script>",
        "basic_usage": "<div class=\"reveal\" id=\"exampleModal\" data-reveal>\n  <h1>Modal Title</h1>\n  <p>Modal content</p>\n  <button class=\"close-button\" data-close aria-label=\"Close modal\" type=\"button\">\n    <span aria-hidden=\"true\">&times;</span>\n  </button>\n</div>",
    },
    
    # Quasar Components
    {
        "name": "QBtn",
        "namespace": "quasar",
        "component_type": ComponentType.BUTTON.value,
        "title": "Quasar Button",
        "description": "The Quasar Button component is a clickable element for Vue.js applications.",
        "tags": json.dumps(["button", "quasar", "vue", "material"]),
        "documentation_url": "https://quasar.dev/vue-components/button",
        "api_reference_url": "https://quasar.dev/vue-components/button",
        "import_statement": "import { QBtn } from 'quasar'",
        "basic_usage": "<q-btn color=\"primary\" label=\"Primary\" />",
    },
    {
        "name": "QCard",
        "namespace": "quasar",
        "component_type": ComponentType.CARD.value,
        "title": "Quasar Card",
        "description": "The Quasar Card component is a great way to display important grouped information.",
        "tags": json.dumps(["card", "quasar", "vue", "material"]),
        "documentation_url": "https://quasar.dev/vue-components/card",
        "api_reference_url": "https://quasar.dev/vue-components/card",
        "import_statement": "import { QCard, QCardSection } from 'quasar'",
        "basic_usage": "<q-card class=\"my-card\">\n  <q-card-section>\n    <div class=\"text-h6\">Card Title</div>\n    <div class=\"text-subtitle2\">Card content</div>\n  </q-card-section>\n</q-card>",
    },
    {
        "name": "QDialog",
        "namespace": "quasar",
        "component_type": ComponentType.MODAL.value,
        "title": "Quasar Dialog",
        "description": "The Quasar Dialog component is a great way to offer the user the ability to confirm an action or add information.",
        "tags": json.dumps(["dialog", "quasar", "vue", "modal"]),
        "documentation_url": "https://quasar.dev/vue-components/dialog",
        "api_reference_url": "https://quasar.dev/vue-components/dialog",
        "import_statement": "import { QDialog } from 'quasar'",
        "basic_usage": "<q-dialog v-model=\"showDialog\">\n  <q-card>\n    <q-card-section>\n      <div class=\"text-h6\">Dialog Title</div>\n    </q-card-section>\n    <q-card-section>\n      Dialog content\n    </q-card-section>\n  </q-card>\n</q-dialog>",
    },
    
    # NextUI Components
    {
        "name": "Button",
        "namespace": "nextui",
        "component_type": ComponentType.BUTTON.value,
        "title": "NextUI Button",
        "description": "Buttons allow users to take actions, and make choices, with a single tap.",
        "tags": json.dumps(["button", "nextui", "react", "modern"]),
        "documentation_url": "https://nextui.org/docs/components/button",
        "api_reference_url": "https://nextui.org/docs/components/button",
        "import_statement": "import { Button } from '@nextui-org/react';",
        "basic_usage": "<Button color=\"primary\">Primary</Button>",
    },
    {
        "name": "Card",
        "namespace": "nextui",
        "component_type": ComponentType.CARD.value,
        "title": "NextUI Card",
        "description": "Cards contain content and actions about a single subject.",
        "tags": json.dumps(["card", "nextui", "react", "modern"]),
        "documentation_url": "https://nextui.org/docs/components/card",
        "api_reference_url": "https://nextui.org/docs/components/card",
        "import_statement": "import { Card, CardBody, CardHeader } from '@nextui-org/react';",
        "basic_usage": "<Card>\n  <CardHeader>\n    <h4>Card Title</h4>\n  </CardHeader>\n  <CardBody>\n    <p>Card content</p>\n  </CardBody>\n</Card>",
    },
    {
        "name": "Modal",
        "namespace": "nextui",
        "component_type": ComponentType.MODAL.value,
        "title": "NextUI Modal",
        "description": "Display popup content that requires attention or provides additional information.",
        "tags": json.dumps(["modal", "nextui", "react", "modern"]),
        "documentation_url": "https://nextui.org/docs/components/modal",
        "api_reference_url": "https://nextui.org/docs/components/modal",
        "import_statement": "import { Modal, ModalContent, ModalHeader, ModalBody, useDisclosure } from '@nextui-org/react';",
        "basic_usage": "<Modal isOpen={isOpen} onOpenChange={onOpenChange}>\n  <ModalContent>\n    <ModalHeader>Modal Title</ModalHeader>\n    <ModalBody>\n      Modal content\n    </ModalBody>\n  </ModalContent>\n</Modal>",
    },
]


async def load_remaining_components():
    """Load remaining UI library components into the database."""
    print("🚀 Loading remaining UI library components...")
    
    # Create tables if they don't exist
    await create_tables()
    
    total_components = 0
    frameworks = {}
    
    async with async_session_maker() as session:
        for component_data in REMAINING_COMPONENTS_DATA:
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
            
            # Track frameworks
            framework = component_data["namespace"]
            if framework not in frameworks:
                frameworks[framework] = 0
            frameworks[framework] += 1
            
            print(f"  ✅ Added '{component_data['name']}' ({framework})")
            total_components += 1
        
        # Commit all changes
        await session.commit()
    
    print(f"\n🎉 Successfully loaded {total_components} new components!")
    
    if frameworks:
        print("\n📦 New frameworks added:")
        for framework, count in frameworks.items():
            print(f"  • {framework}: {count} components")
    
    # Show updated summary
    print("\n📊 Updated Database Summary:")
    async with async_session_maker() as session:
        result = await session.execute(select(Component))
        all_components = result.scalars().all()
        
        framework_counts = {}
        for component in all_components:
            framework = component.namespace
            if framework not in framework_counts:
                framework_counts[framework] = 0
            framework_counts[framework] += 1
        
        for framework, count in sorted(framework_counts.items()):
            print(f"  • {framework}: {count} components")
        
        print(f"\n📈 Total components in database: {len(all_components)}")


if __name__ == "__main__":
    asyncio.run(load_remaining_components())