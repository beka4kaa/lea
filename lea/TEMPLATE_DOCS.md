# Template System Documentation

## Overview
The MCP UI Aggregator now includes a comprehensive template system for rapid page generation using various UI frameworks.

## Available Templates

### Template Categories
1. **Landing Pages** - Marketing and promotional pages
2. **Dashboards** - Admin and analytics interfaces  
3. **E-commerce** - Online shopping pages
4. **Blogs** - Content and article pages
5. **Portfolios** - Personal and professional showcases

### Supported Frameworks
- **React** - Modern component-based framework
- **Vue.js** - Progressive JavaScript framework
- **HTML/CSS** - Pure HTML with styling

## MCP Tools Available

### 1. list_templates_tool()
Lists all available templates grouped by category.

**Returns:**
- Template categories and counts
- Framework information for each template

### 2. get_template_info_tool(template_id)
Get detailed structure of a specific template.

**Parameters:**
- `template_id`: Template identifier (e.g., 'landing_react', 'dashboard_vue')

**Returns:**
- Template metadata
- Section breakdown
- Component hierarchy
- Dependencies

### 3. generate_template_code_tool(template_id, customizations)
Generate complete code from a template.

**Parameters:**
- `template_id`: Template to generate
- `customizations` (optional): Object with customization options

**Customization Options:**
```json
{
  "texts": {
    "oldText": "newText"
  },
  "styles": {
    ".selector": "css-properties"  
  },
  "components": {
    "componentName": {
      "prop": "value"
    }
  }
}
```

**Returns:**
- Generated code
- File extension
- Dependencies list
- Setup instructions

### 4. customize_template_tool(template_id, customizations)
Apply customizations to a template without generating code.

**Parameters:**
- `template_id`: Template to customize
- `customizations`: Customization object

## Example Usage

### Generate a React Landing Page
```javascript
// List available templates
list_templates_tool()

// Get template info
get_template_info_tool("landing_react")

// Generate with customizations
generate_template_code_tool("landing_react", {
  "texts": {
    "Revolutionary": "Amazing",
    "Experience": "Journey"
  },
  "styles": {
    ".hero": "background: linear-gradient(45deg, #ff6b6b, #4ecdc4)"
  }
})
```

### Generate a Vue Dashboard
```javascript
// Generate Vue dashboard
generate_template_code_tool("dashboard_vue", {
  "texts": {
    "Dashboard": "Control Panel",
    "Analytics": "Metrics"
  }
})
```

## Template IDs Reference

### Landing Pages
- `landing_react` - React landing page with Material-UI
- `landing_vue` - Vue landing page with Vuetify
- `landing_html` - HTML landing page with Bootstrap

### Dashboards  
- `dashboard_react` - React admin dashboard
- `dashboard_vue` - Vue admin dashboard
- `dashboard_html` - HTML admin dashboard

### E-commerce
- `ecommerce_react` - React online store
- `ecommerce_vue` - Vue online store
- `ecommerce_html` - HTML online store

### Blogs
- `blog_react` - React blog layout
- `blog_vue` - Vue blog layout  
- `blog_html` - HTML blog layout

### Portfolios
- `portfolio_react` - React portfolio site
- `portfolio_vue` - Vue portfolio site
- `portfolio_html` - HTML portfolio site

## Generated Code Structure

Each generated template includes:
- Complete component/page code
- Required dependencies
- CSS styling (inline or separate)
- Setup instructions
- Import statements

## Integration Notes

- All templates use responsive design
- Components are production-ready
- Code follows framework best practices
- Templates can be customized extensively
- Generated code is immediately usable

## Next Steps

After generating a template:
1. Install required dependencies
2. Create component file with generated code
3. Integrate into your application
4. Customize further as needed