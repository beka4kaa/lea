"""Bulma CSS framework component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class BulmaIngestionModule(BaseIngestionModule):
    """Bulma CSS framework component ingestion."""
    
    def get_namespace(self) -> str:
        return "bulma"
    
    def get_framework(self) -> str:
        return "html"
    
    def get_base_url(self) -> str:
        return "https://bulma.io/documentation"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Bulma CSS framework components."""
        return [
            {
                "name": "Button",
                "title": "Bulma Button",
                "description": "The classic button, in different colors, sizes, and states.",
                "component_type": "button",
                "category": "elements",
                "framework": "html",
                "tags": ["button", "bulma", "element", "interactive"],
                "documentation_url": f"{self.get_base_url()}/elements/button/",
                "import_statement": '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">',
                "basic_usage": '<button class="button">Button</button>',
                "variants": {
                    "primary": '<button class="button is-primary">Primary</button>',
                    "info": '<button class="button is-info">Info</button>',
                    "success": '<button class="button is-success">Success</button>',
                    "warning": '<button class="button is-warning">Warning</button>',
                    "danger": '<button class="button is-danger">Danger</button>',
                    "light": '<button class="button is-light">Light</button>',
                    "dark": '<button class="button is-dark">Dark</button>',
                    "outlined": '<button class="button is-primary is-outlined">Outlined</button>',
                    "inverted": '<button class="button is-primary is-inverted">Inverted</button>',
                    "loading": '<button class="button is-primary is-loading">Loading</button>',
                    "large": '<button class="button is-large">Large</button>',
                    "medium": '<button class="button is-medium">Medium</button>',
                    "small": '<button class="button is-small">Small</button>'
                },
                "examples": [
                    {
                        "title": "Button Groups",
                        "description": "Group buttons together with the field helper",
                        "code": '''<div class="field is-grouped">
  <p class="control">
    <button class="button is-primary">Save changes</button>
  </p>
  <p class="control">
    <button class="button">Cancel</button>
  </p>
</div>'''
                    },
                    {
                        "title": "Button Addons",
                        "description": "Attach buttons together",
                        "code": '''<div class="field has-addons">
  <p class="control">
    <button class="button">
      <span class="icon is-small"><i class="fas fa-bold"></i></span>
    </button>
  </p>
  <p class="control">
    <button class="button">
      <span class="icon is-small"><i class="fas fa-italic"></i></span>
    </button>
  </p>
  <p class="control">
    <button class="button">
      <span class="icon is-small"><i class="fas fa-underline"></i></span>
    </button>
  </p>
</div>'''
                    }
                ]
            },
            {
                "name": "Card",
                "title": "Bulma Card",
                "description": "An all-around flexible and composable component.",
                "component_type": "display",
                "category": "components",
                "framework": "html",
                "tags": ["card", "bulma", "container", "flexible"],
                "documentation_url": f"{self.get_base_url()}/components/card/",
                "import_statement": '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">',
                "basic_usage": '''<div class="card">
  <div class="card-content">
    <div class="content">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      <br>
      <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
    </div>
  </div>
</div>''',
                "examples": [
                    {
                        "title": "Card with Header and Footer",
                        "description": "Complete card with all sections",
                        "code": '''<div class="card">
  <header class="card-header">
    <p class="card-header-title">
      Component
    </p>
    <button class="card-header-icon">
      <span class="icon">
        <i class="fas fa-angle-down"></i>
      </span>
    </button>
  </header>
  <div class="card-content">
    <div class="content">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </div>
  </div>
  <footer class="card-footer">
    <a href="#" class="card-footer-item">Save</a>
    <a href="#" class="card-footer-item">Edit</a>
    <a href="#" class="card-footer-item">Delete</a>
  </footer>
</div>'''
                    }
                ]
            },
            {
                "name": "Modal",
                "title": "Bulma Modal",
                "description": "A classic modal overlay, in which you can include any content you want.",
                "component_type": "overlay",
                "category": "components",
                "framework": "html",
                "tags": ["modal", "overlay", "bulma", "dialog"],
                "documentation_url": f"{self.get_base_url()}/components/modal/",
                "import_statement": '''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
<script>
document.addEventListener('DOMContentLoaded', () => {
  function openModal($el) {
    $el.classList.add('is-active');
  }
  function closeModal($el) {
    $el.classList.remove('is-active');
  }
  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);
    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');
    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });
  document.addEventListener('keydown', (event) => {
    if(event.key === "Escape") {
      closeAllModals();
    }
  });
});
</script>''',
                "basic_usage": '''<button class="button is-primary js-modal-trigger" data-target="modal-js-example">
  Open JS example modal
</button>

<div id="modal-js-example" class="modal">
  <div class="modal-background"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Modal title</p>
      <button class="delete" aria-label="close"></button>
    </header>
    <section class="modal-card-body">
      Modal body content
    </section>
    <footer class="modal-card-foot">
      <button class="button is-success">Save changes</button>
      <button class="button">Cancel</button>
    </footer>
  </div>
</div>'''
            },
            {
                "name": "Navbar",
                "title": "Bulma Navbar",
                "description": "A responsive horizontal navbar that can support images, links, buttons, and dropdowns.",
                "component_type": "navigation",
                "category": "components",
                "framework": "html",
                "tags": ["navbar", "navigation", "bulma", "responsive"],
                "documentation_url": f"{self.get_base_url()}/components/navbar/",
                "import_statement": '''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
<script>
document.addEventListener('DOMContentLoaded', () => {
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  $navbarBurgers.forEach( el => {
    el.addEventListener('click', () => {
      const target = el.dataset.target;
      const $target = document.getElementById(target);
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');
    });
  });
});
</script>''',
                "basic_usage": '''<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="https://bulma.io">
      <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28">
    </a>
    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>
  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
      <a class="navbar-item">Home</a>
      <a class="navbar-item">Documentation</a>
    </div>
    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-primary"><strong>Sign up</strong></a>
          <a class="button is-light">Log in</a>
        </div>
      </div>
    </div>
  </div>
</nav>'''
            },
            {
                "name": "Form",
                "title": "Bulma Form Controls",
                "description": "All generic form controls, designed for consistency.",
                "component_type": "form",
                "category": "form",
                "framework": "html",
                "tags": ["form", "input", "bulma", "control"],
                "documentation_url": f"{self.get_base_url()}/form/general/",
                "import_statement": '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">',
                "basic_usage": '''<div class="field">
  <label class="label">Name</label>
  <div class="control">
    <input class="input" type="text" placeholder="Text input">
  </div>
</div>

<div class="field">
  <label class="label">Username</label>
  <div class="control has-icons-left has-icons-right">
    <input class="input is-success" type="text" placeholder="Text input" value="bulma">
    <span class="icon is-small is-left">
      <i class="fas fa-user"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-check"></i>
    </span>
  </div>
  <p class="help is-success">This username is available</p>
</div>

<div class="field">
  <label class="label">Email</label>
  <div class="control has-icons-left has-icons-right">
    <input class="input is-danger" type="email" placeholder="Email input" value="hello@">
    <span class="icon is-small is-left">
      <i class="fas fa-envelope"></i>
    </span>
    <span class="icon is-small is-right">
      <i class="fas fa-exclamation-triangle"></i>
    </span>
  </div>
  <p class="help is-danger">This email is invalid</p>
</div>

<div class="field">
  <div class="control">
    <button class="button is-link">Submit</button>
  </div>
</div>'''
            },
            {
                "name": "Notification",
                "title": "Bulma Notification",
                "description": "Bold notification blocks, to alert your users of something.",
                "component_type": "feedback",
                "category": "elements",
                "framework": "html",
                "tags": ["notification", "alert", "bulma", "feedback"],
                "documentation_url": f"{self.get_base_url()}/elements/notification/",
                "import_statement": '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">',
                "basic_usage": '''<div class="notification">
  Lorem ipsum dolor sit amet, consectetur adipiscing elit lorem ipsum dolor.
</div>''',
                "variants": {
                    "primary": '<div class="notification is-primary">Primary notification</div>',
                    "info": '<div class="notification is-info">Info notification</div>',
                    "success": '<div class="notification is-success">Success notification</div>',
                    "warning": '<div class="notification is-warning">Warning notification</div>',
                    "danger": '<div class="notification is-danger">Danger notification</div>',
                    "light": '<div class="notification is-light">Light notification</div>',
                    "dark": '<div class="notification is-dark">Dark notification</div>',
                    "dismissible": '''<div class="notification is-primary">
  <button class="delete"></button>
  Primary lorem ipsum dolor sit amet, consectetur adipiscing elit lorem ipsum dolor.
</div>'''
                }
            }
        ]