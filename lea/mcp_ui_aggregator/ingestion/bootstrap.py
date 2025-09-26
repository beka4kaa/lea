"""Bootstrap UI component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class BootstrapIngestionModule(BaseIngestionModule):
    """Bootstrap component ingestion."""
    
    def get_namespace(self) -> str:
        return "bootstrap"
    
    def get_framework(self) -> str:
        return "html"
    
    def get_base_url(self) -> str:
        return "https://getbootstrap.com/docs/5.3"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Bootstrap components for rapid prototyping."""
        return [
            {
                "name": "Button",
                "title": "Bootstrap Button",
                "description": "Bootstrap's custom button styles for forms, dialogs, and more with support for multiple sizes, states, and more.",
                "component_type": "button",
                "category": "forms",
                "framework": "html",
                "tags": ["button", "bootstrap", "form", "interactive"],
                "documentation_url": f"{self.get_base_url()}/components/buttons/",
                "import_statement": '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">',
                "basic_usage": '<button type="button" class="btn btn-primary">Primary</button>',
                "variants": {
                    "primary": '<button type="button" class="btn btn-primary">Primary</button>',
                    "secondary": '<button type="button" class="btn btn-secondary">Secondary</button>',
                    "success": '<button type="button" class="btn btn-success">Success</button>',
                    "danger": '<button type="button" class="btn btn-danger">Danger</button>',
                    "warning": '<button type="button" class="btn btn-warning">Warning</button>',
                    "info": '<button type="button" class="btn btn-info">Info</button>',
                    "light": '<button type="button" class="btn btn-light">Light</button>',
                    "dark": '<button type="button" class="btn btn-dark">Dark</button>',
                    "outline": '<button type="button" class="btn btn-outline-primary">Outline</button>',
                },
                "examples": [
                    {
                        "title": "Button Group",
                        "description": "Group a series of buttons together on a single line",
                        "code": '''<div class="btn-group" role="group">
  <button type="button" class="btn btn-primary">Left</button>
  <button type="button" class="btn btn-primary">Middle</button>
  <button type="button" class="btn btn-primary">Right</button>
</div>'''
                    },
                    {
                        "title": "Loading Button",
                        "description": "Show loading state",
                        "code": '''<button class="btn btn-primary" type="button" disabled>
  <span class="spinner-border spinner-border-sm" role="status"></span>
  Loading...
</button>'''
                    }
                ]
            },
            {
                "name": "Card",
                "title": "Bootstrap Card",
                "description": "Bootstrap's cards provide a flexible content container with multiple variants and options.",
                "component_type": "display",
                "category": "layout",
                "framework": "html",
                "tags": ["card", "bootstrap", "container", "layout"],
                "documentation_url": f"{self.get_base_url()}/components/card/",
                "import_statement": '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">',
                "basic_usage": '''<div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Card content goes here.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>''',
                "examples": [
                    {
                        "title": "Card with Image",
                        "description": "Card with image header",
                        "code": '''<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>'''
                    }
                ]
            },
            {
                "name": "Modal",
                "title": "Bootstrap Modal",
                "description": "Use Bootstrap's modal component to add dialogs for lightboxes, user notifications, or custom content.",
                "component_type": "overlay",
                "category": "feedback",
                "framework": "html",
                "tags": ["modal", "dialog", "bootstrap", "overlay"],
                "documentation_url": f"{self.get_base_url()}/components/modal/",
                "import_statement": '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>''',
                "basic_usage": '''<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5">Modal title</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        Modal body content goes here.
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>'''
            },
            {
                "name": "Navbar",
                "title": "Bootstrap Navbar",
                "description": "Bootstrap navbar for responsive navigation headers.",
                "component_type": "navigation",
                "category": "navigation",
                "framework": "html",
                "tags": ["navbar", "navigation", "bootstrap", "responsive"],
                "documentation_url": f"{self.get_base_url()}/components/navbar/",
                "import_statement": '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>''',
                "basic_usage": '''<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Features</a>
        </li>
      </ul>
    </div>
  </div>
</nav>'''
            },
            {
                "name": "Form",
                "title": "Bootstrap Form",
                "description": "Bootstrap form controls for collecting user input.",
                "component_type": "form",
                "category": "forms",
                "framework": "html",
                "tags": ["form", "input", "bootstrap", "validation"],
                "documentation_url": f"{self.get_base_url()}/forms/overview/",
                "import_statement": '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">',
                "basic_usage": '''<form>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1">
  </div>
  <div class="mb-3">
    <label for="exampleInputPassword1" class="form-label">Password</label>
    <input type="password" class="form-control" id="exampleInputPassword1">
  </div>
  <div class="mb-3 form-check">
    <input type="checkbox" class="form-check-input" id="exampleCheck1">
    <label class="form-check-label" for="exampleCheck1">Check me out</label>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>'''
            },
            {
                "name": "Alert",
                "title": "Bootstrap Alert",
                "description": "Provide contextual feedback messages for user actions with alerts.",
                "component_type": "feedback",
                "category": "feedback",
                "framework": "html",
                "tags": ["alert", "notification", "bootstrap", "feedback"],
                "documentation_url": f"{self.get_base_url()}/components/alerts/",
                "import_statement": '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">',
                "basic_usage": '<div class="alert alert-primary" role="alert">A simple primary alert—check it out!</div>',
                "variants": {
                    "primary": '<div class="alert alert-primary" role="alert">Primary alert</div>',
                    "secondary": '<div class="alert alert-secondary" role="alert">Secondary alert</div>',
                    "success": '<div class="alert alert-success" role="alert">Success alert</div>',
                    "danger": '<div class="alert alert-danger" role="alert">Danger alert</div>',
                    "warning": '<div class="alert alert-warning" role="alert">Warning alert</div>',
                    "info": '<div class="alert alert-info" role="alert">Info alert</div>',
                    "dismissible": '''<div class="alert alert-warning alert-dismissible fade show" role="alert">
  <strong>Holy guacamole!</strong> You should check in on some of those fields below.
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>'''
                }
            }
        ]