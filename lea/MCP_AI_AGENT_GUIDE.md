# 🤖 AI Agent Integration Guide for LEA UI Components MCP Server

> **Complete integration guide for AI agents to automatically understand and use the LEA UI Components MCP Server**

## 🚀 Quick Start for AI Agents

### Server Discovery
```bash
# Check if server is available
curl http://localhost:8000/mcp-discovery

# Get complete tools specification
curl http://localhost:8000/mcp-discovery | jq '.tools'
```

### MCP Connection
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "clientInfo": {
      "name": "Your AI Agent",
      "version": "1.0.0"
    }
  }
}
```

## 📋 Available Tools

### 1. **search_component** - Find UI Components
Use natural language to find components across 66 available components from 11 providers.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_component",
    "arguments": {
      "query": "animated button with hover effects",
      "limit": 5
    }
  }
}
```

**Common queries:**
- `"beautiful animated button"` → Magic Button, Rainbow Button
- `"contact form with validation"` → Contact Form component
- `"image gallery with lightbox"` → Image Gallery component
- `"loading spinner animated"` → Loading Spinner variants
- `"modal dialog popup"` → Modal Dialog component
- `"calculator interactive"` → Calculator component
- `"tooltip hover info"` → Tooltip component

### 2. **get_component_code** - Get Production Code
Retrieve complete, production-ready TSX/JSX code for any component.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_component_code",
    "arguments": {
      "component_id": "magicui/contact-form",
      "format": "tsx"
    }
  }
}
```

**Available component IDs:**
- **MagicUI Interactive:** `magicui/contact-form`, `magicui/modal-dialog`, `magicui/image-gallery`, `magicui/loading-spinner`, `magicui/tooltip`, `magicui/calculator`
- **MagicUI Animated:** `magicui/magic-button`, `magicui/rainbow-button`, `magicui/sparkles`, `magicui/marquee`
- **Shadcn Core:** `shadcn/button`, `shadcn/input`, `shadcn/card`, `shadcn/badge`, `shadcn/avatar`

### 3. **list_components** - Browse All Components
List and filter through all 66 components with pagination.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "list_components",
    "arguments": {
      "provider": "magicui",
      "category": "forms",
      "limit": 10
    }
  }
}
```

### 4. **get_component_docs** - Get Documentation
Get installation instructions, dependencies, and usage examples.

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "get_component_docs",
    "arguments": {
      "component_id": "magicui/contact-form"
    }
  }
}
```

### 5. **install_plan** - Get Installation Plan
Generate complete setup instructions with all dependencies.

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "install_plan",
    "arguments": {
      "component_ids": ["magicui/contact-form", "shadcn/button"],
      "target": "nextjs",
      "package_manager": "npm"
    }
  }
}
```

### 6. **get_block** - Get Complete UI Blocks
Get multi-component layouts for common use cases.

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "get_block",
    "arguments": {
      "block_type": "pricing",
      "target": "nextjs",
      "style": "tailwind"
    }
  }
}
```

### 7. **verify** - Verify Component Code
Check code for syntax errors and compatibility.

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "verify",
    "arguments": {
      "code": "import React from 'react'...",
      "framework": "react"
    }
  }
}
```

## 🎯 Common Workflows for AI Agents

### Workflow 1: Find and Implement a Button
```json
// Step 1: Search for buttons
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_component",
    "arguments": {"query": "animated button with hover", "limit": 3}
  }
}

// Step 2: Get code for selected button
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_component_code",
    "arguments": {"component_id": "magicui/magic-button"}
  }
}

// Step 3: Get installation plan
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "install_plan",
    "arguments": {"component_ids": ["magicui/magic-button"]}
  }
}
```

### Workflow 2: Create Complete Contact Form
```json
// Step 1: Find contact form
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_component",
    "arguments": {"query": "contact form validation"}
  }
}

// Step 2: Get form code (4000+ characters of production-ready code)
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_component_code",
    "arguments": {"component_id": "magicui/contact-form"}
  }
}

// Step 3: Get documentation and usage
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_component_docs",
    "arguments": {"component_id": "magicui/contact-form"}
  }
}
```

### Workflow 3: Build Interactive Gallery
```json
// Find image gallery component
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_component",
    "arguments": {"query": "image gallery lightbox interactive"}
  }
}

// Get complete gallery code (3500+ characters)
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_component_code",
    "arguments": {"component_id": "magicui/image-gallery"}
  }
}
```

## 🏗️ Server Capabilities

### Component Providers (11 total)
- **MagicUI** - 36 components with enhanced templates
- **Shadcn** - 30 components with enhanced templates  
- **DaisyUI** - UI components for Tailwind CSS
- **ReactBits** - Modern React components
- **Tremor** - Data visualization components
- **NextUI** - Beautiful React components
- **Chakra UI** - Simple, modular components
- **Mantine** - Full-featured React library
- **Ant Design** - Enterprise-class components
- **Arco Design** - Comprehensive component library
- **Semi Design** - Modern design system

### Enhanced Features
- **Production-Ready Code**: All components include complete TSX with TypeScript interfaces
- **Interactive Components**: Forms, modals, galleries, calculators with full functionality
- **Animation Support**: framer-motion integration for smooth animations
- **Responsive Design**: Tailwind CSS v4 compatibility
- **Accessibility**: ARIA compliant components
- **Modern Stack**: React 18+, Next.js 15, TypeScript 5+

### Categories Available
- `animated` - Animated elements and effects
- `forms` - Form components and inputs
- `navigation` - Navigation and menu components
- `buttons` - Button variants and interactions
- `inputs` - Input fields and controls
- `layouts` - Layout and grid systems
- `data_display` - Data visualization components
- `feedback` - Loading states and notifications
- `overlays` - Modals, tooltips, popovers
- `text` - Typography and text effects
- `backgrounds` - Background effects and patterns
- `cards` - Card layouts and designs
- `other` - Specialized components

## 🔧 Error Handling

The server provides detailed error responses:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Component 'invalid/component' not found",
    "data": {
      "suggestion": "Use search_component to find available components",
      "available_providers": ["magicui", "shadcn", "daisyui", "..."]
    }
  }
}
```

## 📊 Server Status

Check server health and statistics:

```bash
# Health check
curl http://localhost:8000/health

# MCP status
curl http://localhost:8000/mcp-status

# Complete discovery
curl http://localhost:8000/mcp-discovery
```

## 🎨 Example Component Responses

### Magic Button Code (1800+ chars)
```typescript
import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface MagicButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
}

export default function MagicButton({
  children,
  className,
  ...props
}: MagicButtonProps) {
  return (
    <motion.button
      className={cn(
        "relative inline-flex h-12 overflow-hidden rounded-full p-[1px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50",
        className
      )}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      {...props}
    >
      <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
      <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-full bg-slate-950 px-3 py-1 text-sm font-medium text-white backdrop-blur-3xl">
        {children}
      </span>
    </motion.button>
  );
}
```

### Contact Form Code (4000+ chars)
Complete form with validation, loading states, success feedback, TypeScript interfaces, and error handling.

### Image Gallery Code (3500+ chars)
Full gallery with lightbox, animations, keyboard navigation, and responsive grid layout.

## 🚀 Integration Tips for AI Agents

1. **Always start with search_component** to find relevant components
2. **Use natural language queries** - the semantic search is very powerful
3. **Get complete code with get_component_code** - includes all imports and styling
4. **Use install_plan** for dependency management
5. **Verify code** before deployment with the verify tool
6. **Check documentation** for usage examples and props

## 📞 Server Endpoints

- **MCP Endpoint**: `POST /mcp` (JSON-RPC 2.0)
- **Discovery**: `GET /mcp-discovery`
- **Health**: `GET /health`
- **Status**: `GET /mcp-status`
- **OpenAPI**: `GET /openapi-mcp.json`

---

**Ready to use!** 🎉 Your AI agent now has complete access to 66 production-ready UI components with full documentation and examples.