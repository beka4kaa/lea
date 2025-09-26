"""Svelte component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class SvelteIngestionModule(BaseIngestionModule):
    """Svelte component ingestion."""
    
    def get_namespace(self) -> str:
        return "svelte"
    
    def get_framework(self) -> str:
        return "svelte"
    
    def get_base_url(self) -> str:
        return "https://svelte.dev"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Svelte components with modern UI patterns."""
        return [
            {
                "name": "Button",
                "title": "Svelte Button",
                "description": "Interactive button component with various styles and states.",
                "component_type": "button",
                "category": "form",
                "framework": "svelte",
                "tags": ["button", "svelte", "form", "interactive"],
                "documentation_url": f"{self.get_base_url()}/docs",
                "import_statement": '''<script>
  import Button from '$lib/components/Button.svelte';
</script>''',
                "basic_usage": '<Button>Click me</Button>',
                "variants": {
                    "primary": '<Button variant="primary">Primary</Button>',
                    "secondary": '<Button variant="secondary">Secondary</Button>',
                    "success": '<Button variant="success">Success</Button>',
                    "danger": '<Button variant="danger">Danger</Button>',
                    "warning": '<Button variant="warning">Warning</Button>',
                    "info": '<Button variant="info">Info</Button>',
                    "light": '<Button variant="light">Light</Button>',
                    "dark": '<Button variant="dark">Dark</Button>',
                    "outline": '<Button variant="outline">Outline</Button>',
                    "ghost": '<Button variant="ghost">Ghost</Button>',
                    "disabled": '<Button disabled>Disabled</Button>',
                    "loading": '<Button loading>Loading</Button>',
                    "small": '<Button size="sm">Small</Button>',
                    "large": '<Button size="lg">Large</Button>',
                    "with-icon": '<Button><Icon name="plus" /> Add Item</Button>'
                },
                "examples": [
                    {
                        "title": "Button Component Implementation",
                        "description": "Complete Svelte button component with props and styling",
                        "code": '''<!-- Button.svelte -->
<script>
  export let variant = 'primary';
  export let size = 'md';
  export let disabled = false;
  export let loading = false;
  export let type = 'button';
  
  let className = '';
  export { className as class };
  
  $: buttonClass = `btn btn-${variant} btn-${size} ${className}`;
</script>

<button 
  class={buttonClass}
  {type}
  {disabled}
  class:loading
  on:click
  on:mouseover
  on:mouseout
  on:focus
  on:blur
  {...$$restProps}
>
  {#if loading}
    <span class="spinner"></span>
  {/if}
  <slot />
</button>

<style>
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-all duration-200;
    @apply focus:outline-none focus:ring-2 focus:ring-offset-2;
    @apply disabled:opacity-50 disabled:cursor-not-allowed;
  }
  
  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700;
    @apply focus:ring-blue-500;
  }
  
  .btn-secondary {
    @apply bg-gray-600 text-white hover:bg-gray-700;
    @apply focus:ring-gray-500;
  }
  
  .btn-success {
    @apply bg-green-600 text-white hover:bg-green-700;
    @apply focus:ring-green-500;
  }
  
  .btn-danger {
    @apply bg-red-600 text-white hover:bg-red-700;
    @apply focus:ring-red-500;
  }
  
  .btn-outline {
    @apply border-2 border-gray-300 text-gray-700;
    @apply hover:bg-gray-50 focus:ring-gray-500;
  }
  
  .btn-ghost {
    @apply text-gray-600 hover:bg-gray-100;
    @apply focus:ring-gray-500;
  }
  
  .btn-sm {
    @apply px-3 py-1.5 text-sm;
  }
  
  .btn-lg {
    @apply px-6 py-3 text-lg;
  }
  
  .loading {
    @apply pointer-events-none;
  }
  
  .spinner {
    @apply inline-block w-4 h-4 border-2 border-white border-t-transparent;
    @apply rounded-full animate-spin mr-2;
  }
</style>'''
                    },
                    {
                        "title": "Usage Examples",
                        "description": "Different ways to use the button component",
                        "code": '''<!-- Page.svelte -->
<script>
  import Button from '$lib/components/Button.svelte';
  import Icon from '$lib/components/Icon.svelte';
  
  let loading = false;
  
  async function handleAsyncAction() {
    loading = true;
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('Action completed');
    } finally {
      loading = false;
    }
  }
</script>

<div class="space-y-4">
  <!-- Basic buttons -->
  <div class="flex gap-2">
    <Button>Default</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="success">Success</Button>
    <Button variant="danger">Danger</Button>
  </div>
  
  <!-- Sizes -->
  <div class="flex gap-2 items-center">
    <Button size="sm">Small</Button>
    <Button>Medium</Button>
    <Button size="lg">Large</Button>
  </div>
  
  <!-- States -->
  <div class="flex gap-2">
    <Button disabled>Disabled</Button>
    <Button {loading} on:click={handleAsyncAction}>
      {loading ? 'Loading...' : 'Async Action'}
    </Button>
  </div>
  
  <!-- With icons -->
  <div class="flex gap-2">
    <Button variant="primary">
      <Icon name="plus" />
      Add Item
    </Button>
    <Button variant="outline">
      <Icon name="download" />
      Download
    </Button>
  </div>
</div>'''
                    }
                ]
            },
            {
                "name": "Card",
                "title": "Svelte Card",
                "description": "Flexible card container component for displaying content.",
                "component_type": "display",
                "category": "layout",
                "framework": "svelte",
                "tags": ["card", "svelte", "container", "layout"],
                "documentation_url": f"{self.get_base_url()}/docs",
                "import_statement": '''<script>
  import Card from '$lib/components/Card.svelte';
</script>''',
                "basic_usage": '''<Card>
  <p>Card content</p>
</Card>''',
                "examples": [
                    {
                        "title": "Card Component Implementation",
                        "description": "Flexible Svelte card component with slots",
                        "code": '''<!-- Card.svelte -->
<script>
  export let variant = 'default';
  export let padding = 'md';
  export let shadow = 'md';
  export let rounded = 'lg';
  export let border = true;
  
  let className = '';
  export { className as class };
  
  $: cardClass = `card card-${variant} p-${padding} shadow-${shadow} rounded-${rounded} ${border ? 'border' : ''} ${className}`;
</script>

<div class={cardClass} {...$$restProps}>
  {#if $$slots.header}
    <div class="card-header">
      <slot name="header" />
    </div>
  {/if}
  
  <div class="card-content">
    <slot />
  </div>
  
  {#if $$slots.footer}
    <div class="card-footer">
      <slot name="footer" />
    </div>
  {/if}
</div>

<style>
  .card {
    @apply bg-white;
  }
  
  .card-default {
    @apply border-gray-200;
  }
  
  .card-elevated {
    @apply border-0;
  }
  
  .card-outlined {
    @apply border-2 shadow-none;
  }
  
  .card-header {
    @apply border-b border-gray-200 pb-4 mb-4;
  }
  
  .card-footer {
    @apply border-t border-gray-200 pt-4 mt-4;
  }
  
  .p-sm {
    @apply p-3;
  }
  
  .p-md {
    @apply p-6;
  }
  
  .p-lg {
    @apply p-8;
  }
  
  .shadow-sm {
    @apply shadow-sm;
  }
  
  .shadow-md {
    @apply shadow-md;
  }
  
  .shadow-lg {
    @apply shadow-lg;
  }
  
  .rounded-sm {
    @apply rounded;
  }
  
  .rounded-lg {
    @apply rounded-lg;
  }
  
  .rounded-xl {
    @apply rounded-xl;
  }
</style>'''
                    },
                    {
                        "title": "Card Usage Examples",
                        "description": "Different card layouts and styles",
                        "code": '''<!-- CardExamples.svelte -->
<script>
  import Card from '$lib/components/Card.svelte';
  import Button from '$lib/components/Button.svelte';
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Simple card -->
  <Card>
    <h3 class="text-lg font-semibold mb-2">Simple Card</h3>
    <p class="text-gray-600">This is a basic card with just content.</p>
  </Card>
  
  <!-- Card with header and footer -->
  <Card>
    <svelte:fragment slot="header">
      <h3 class="text-lg font-semibold">Card with Header</h3>
      <p class="text-sm text-gray-500">Subtitle text</p>
    </svelte:fragment>
    
    <p class="text-gray-600">
      This card has both header and footer sections.
    </p>
    
    <svelte:fragment slot="footer">
      <div class="flex gap-2">
        <Button size="sm">Action</Button>
        <Button variant="outline" size="sm">Cancel</Button>
      </div>
    </svelte:fragment>
  </Card>
  
  <!-- Elevated card -->
  <Card variant="elevated" shadow="lg">
    <h3 class="text-lg font-semibold mb-2">Elevated Card</h3>
    <p class="text-gray-600">This card has a larger shadow and no border.</p>
  </Card>
  
  <!-- Product card example -->
  <Card class="overflow-hidden">
    <img 
      src="https://via.placeholder.com/400x200" 
      alt="Product" 
      class="w-full h-48 object-cover -m-6 mb-4"
    />
    <h3 class="text-lg font-semibold mb-2">Product Name</h3>
    <p class="text-gray-600 mb-4">Product description goes here.</p>
    <div class="flex justify-between items-center">
      <span class="text-xl font-bold text-green-600">$99.99</span>
      <Button size="sm">Add to Cart</Button>
    </div>
  </Card>
</div>'''
                    }
                ]
            },
            {
                "name": "Modal",
                "title": "Svelte Modal",
                "description": "Modal dialog component with backdrop and animations.",
                "component_type": "overlay",
                "category": "overlay",
                "framework": "svelte",
                "tags": ["modal", "dialog", "svelte", "overlay"],
                "documentation_url": f"{self.get_base_url()}/docs",
                "import_statement": '''<script>
  import Modal from '$lib/components/Modal.svelte';
</script>''',
                "basic_usage": '''<Modal bind:open={showModal}>
  <h2>Modal Title</h2>
  <p>Modal content goes here.</p>
</Modal>''',
                "examples": [
                    {
                        "title": "Modal Component Implementation",
                        "description": "Full-featured modal with animations and accessibility",
                        "code": '''<!-- Modal.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import { fade, scale } from 'svelte/transition';
  import { clickOutside } from '$lib/actions/clickOutside.js';
  
  export let open = false;
  export let title = '';
  export let size = 'md';
  export let closable = true;
  export let backdrop = true;
  
  const dispatch = createEventDispatcher();
  
  function close() {
    if (closable) {
      open = false;
      dispatch('close');
    }
  }
  
  function handleKeydown(event) {
    if (event.key === 'Escape' && closable) {
      close();
    }
  }
  
  $: if (open) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div 
    class="modal-backdrop"
    transition:fade={{ duration: 200 }}
    on:click={backdrop ? close : undefined}
  >
    <div 
      class="modal modal-{size}"
      transition:scale={{ duration: 200, start: 0.9 }}
      use:clickOutside
      on:click_outside={backdrop ? close : undefined}
      on:click|stopPropagation
      role="dialog"
      aria-modal="true"
      aria-labelledby={title ? 'modal-title' : undefined}
    >
      {#if closable}
        <button class="modal-close" on:click={close} aria-label="Close modal">
          ×
        </button>
      {/if}
      
      {#if title || $$slots.header}
        <div class="modal-header">
          {#if title}
            <h2 id="modal-title" class="modal-title">{title}</h2>
          {/if}
          <slot name="header" />
        </div>
      {/if}
      
      <div class="modal-body">
        <slot />
      </div>
      
      {#if $$slots.footer}
        <div class="modal-footer">
          <slot name="footer" />
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4;
    @apply z-50;
  }
  
  .modal {
    @apply bg-white rounded-lg shadow-xl max-h-full overflow-auto;
    @apply relative;
  }
  
  .modal-sm {
    @apply w-full max-w-sm;
  }
  
  .modal-md {
    @apply w-full max-w-md;
  }
  
  .modal-lg {
    @apply w-full max-w-2xl;
  }
  
  .modal-xl {
    @apply w-full max-w-4xl;
  }
  
  .modal-close {
    @apply absolute top-4 right-4 text-gray-400 hover:text-gray-600;
    @apply text-2xl font-bold w-8 h-8 flex items-center justify-center;
    @apply rounded-full hover:bg-gray-100 transition-colors;
  }
  
  .modal-header {
    @apply p-6 border-b border-gray-200;
  }
  
  .modal-title {
    @apply text-xl font-semibold text-gray-900;
  }
  
  .modal-body {
    @apply p-6;
  }
  
  .modal-footer {
    @apply p-6 border-t border-gray-200 flex gap-3 justify-end;
  }
</style>'''
                    },
                    {
                        "title": "Modal Usage Examples",
                        "description": "Different modal types and use cases",
                        "code": '''<!-- ModalExamples.svelte -->
<script>
  import Modal from '$lib/components/Modal.svelte';
  import Button from '$lib/components/Button.svelte';
  
  let showBasicModal = false;
  let showConfirmModal = false;
  let showFormModal = false;
  
  let formData = { name: '', email: '' };
  
  function handleConfirm() {
    console.log('Confirmed!');
    showConfirmModal = false;
  }
  
  function handleSubmit() {
    console.log('Form submitted:', formData);
    showFormModal = false;
  }
</script>

<div class="space-x-4">
  <Button on:click={() => showBasicModal = true}>
    Show Basic Modal
  </Button>
  
  <Button on:click={() => showConfirmModal = true} variant="danger">
    Show Confirm Modal
  </Button>
  
  <Button on:click={() => showFormModal = true} variant="primary">
    Show Form Modal
  </Button>
</div>

<!-- Basic Modal -->
<Modal bind:open={showBasicModal} title="Basic Modal">
  <p>This is a basic modal with just content and a title.</p>
  <p>You can close it by clicking the X, pressing Escape, or clicking outside.</p>
</Modal>

<!-- Confirmation Modal -->
<Modal bind:open={showConfirmModal} title="Confirm Action" size="sm">
  <p>Are you sure you want to delete this item? This action cannot be undone.</p>
  
  <svelte:fragment slot="footer">
    <Button variant="outline" on:click={() => showConfirmModal = false}>
      Cancel
    </Button>
    <Button variant="danger" on:click={handleConfirm}>
      Delete
    </Button>
  </svelte:fragment>
</Modal>

<!-- Form Modal -->
<Modal bind:open={showFormModal} title="Add User" size="lg">
  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
      <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
        Name
      </label>
      <input
        id="name"
        type="text"
        bind:value={formData.name}
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>
    
    <div>
      <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
        Email
      </label>
      <input
        id="email"
        type="email"
        bind:value={formData.email}
        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>
  </form>
  
  <svelte:fragment slot="footer">
    <Button variant="outline" on:click={() => showFormModal = false}>
      Cancel
    </Button>
    <Button type="submit" on:click={handleSubmit}>
      Add User
    </Button>
  </svelte:fragment>
</Modal>'''
                    }
                ]
            },
            {
                "name": "Input",
                "title": "Svelte Input",
                "description": "Enhanced input component with validation and styling.",
                "component_type": "input",
                "category": "form",
                "framework": "svelte",
                "tags": ["input", "form", "svelte", "validation"],
                "documentation_url": f"{self.get_base_url()}/docs",
                "import_statement": '''<script>
  import Input from '$lib/components/Input.svelte';
</script>''',
                "basic_usage": '<Input label="Name" bind:value={name} />',
                "examples": [
                    {
                        "title": "Input Component Implementation",
                        "description": "Feature-rich input component with validation",
                        "code": '''<!-- Input.svelte -->
<script>
  export let type = 'text';
  export let value = '';
  export let label = '';
  export let placeholder = '';
  export let required = false;
  export let disabled = false;
  export let readonly = false;
  export let error = '';
  export let hint = '';
  export let size = 'md';
  export let variant = 'default';
  
  let className = '';
  export { className as class };
  
  export let id = `input-${Math.random().toString(36).substr(2, 9)}`;
  
  let inputElement;
  let focused = false;
  
  $: hasError = !!error;
  $: hasValue = !!value;
  
  $: inputClass = `
    input input-${size} input-${variant} ${className}
    ${hasError ? 'input-error' : ''}
    ${focused ? 'input-focused' : ''}
    ${disabled ? 'input-disabled' : ''}
  `.trim();
  
  function handleFocus() {
    focused = true;
  }
  
  function handleBlur() {
    focused = false;
  }
  
  export function focus() {
    inputElement?.focus();
  }
</script>

<div class="input-wrapper">
  {#if label}
    <label for={id} class="input-label" class:required>
      {label}
    </label>
  {/if}
  
  <div class="input-container">
    {#if $$slots.prefix}
      <div class="input-prefix">
        <slot name="prefix" />
      </div>
    {/if}
    
    <input
      bind:this={inputElement}
      bind:value
      {id}
      {type}
      {placeholder}
      {required}
      {disabled}
      {readonly}
      class={inputClass}
      on:focus={handleFocus}
      on:blur={handleBlur}
      on:input
      on:change
      on:keydown
      on:keyup
      {...$$restProps}
    />
    
    {#if $$slots.suffix}
      <div class="input-suffix">
        <slot name="suffix" />
      </div>
    {/if}
  </div>
  
  {#if error}
    <div class="input-error-message">
      {error}
    </div>
  {:else if hint}
    <div class="input-hint">
      {hint}
    </div>
  {/if}
</div>

<style>
  .input-wrapper {
    @apply w-full;
  }
  
  .input-label {
    @apply block text-sm font-medium text-gray-700 mb-1;
  }
  
  .input-label.required::after {
    content: ' *';
    @apply text-red-500;
  }
  
  .input-container {
    @apply relative flex items-center;
  }
  
  .input {
    @apply w-full border border-gray-300 rounded-md shadow-sm;
    @apply focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
    @apply transition-colors duration-200;
  }
  
  .input-sm {
    @apply px-2 py-1 text-sm;
  }
  
  .input-md {
    @apply px-3 py-2;
  }
  
  .input-lg {
    @apply px-4 py-3 text-lg;
  }
  
  .input-error {
    @apply border-red-300 focus:ring-red-500 focus:border-red-500;
  }
  
  .input-disabled {
    @apply bg-gray-100 text-gray-500 cursor-not-allowed;
  }
  
  .input-prefix,
  .input-suffix {
    @apply absolute inset-y-0 flex items-center text-gray-400;
    @apply pointer-events-none;
  }
  
  .input-prefix {
    @apply left-3;
  }
  
  .input-suffix {
    @apply right-3;
  }
  
  .input-prefix + .input {
    @apply pl-10;
  }
  
  .input-suffix ~ .input {
    @apply pr-10;
  }
  
  .input-error-message {
    @apply mt-1 text-sm text-red-600;
  }
  
  .input-hint {
    @apply mt-1 text-sm text-gray-500;
  }
</style>'''
                    }
                ]
            },
            {
                "name": "Toast",
                "title": "Svelte Toast",
                "description": "Toast notification component with animations and auto-dismiss.",
                "component_type": "feedback",
                "category": "overlay",
                "framework": "svelte",
                "tags": ["toast", "notification", "svelte", "feedback"],
                "documentation_url": f"{self.get_base_url()}/docs",
                "import_statement": '''<script>
  import { toast } from '$lib/components/Toast';
</script>''',
                "basic_usage": "toast.success('Success message');",
                "examples": [
                    {
                        "title": "Toast System Implementation",
                        "description": "Complete toast notification system with store",
                        "code": '''// stores/toast.js
import { writable } from 'svelte/store';

function createToastStore() {
  const { subscribe, update } = writable([]);
  
  function addToast(toast) {
    const id = Math.random().toString(36);
    const newToast = { id, ...toast };
    
    update(toasts => [...toasts, newToast]);
    
    if (toast.duration !== 0) {
      setTimeout(() => {
        removeToast(id);
      }, toast.duration || 5000);
    }
    
    return id;
  }
  
  function removeToast(id) {
    update(toasts => toasts.filter(t => t.id !== id));
  }
  
  return {
    subscribe,
    success: (message, options = {}) => addToast({ 
      type: 'success', 
      message, 
      ...options 
    }),
    error: (message, options = {}) => addToast({ 
      type: 'error', 
      message, 
      ...options 
    }),
    warning: (message, options = {}) => addToast({ 
      type: 'warning', 
      message, 
      ...options 
    }),
    info: (message, options = {}) => addToast({ 
      type: 'info', 
      message, 
      ...options 
    }),
    remove: removeToast,
    clear: () => update(() => [])
  };
}

export const toast = createToastStore();'''
                    },
                    {
                        "title": "Toast Container Component",
                        "description": "Toast container with animations",
                        "code": '''<!-- ToastContainer.svelte -->
<script>
  import { fly } from 'svelte/transition';
  import { toast } from '$lib/stores/toast.js';
  
  function getIcon(type) {
    switch (type) {
      case 'success': return '✓';
      case 'error': return '✕';
      case 'warning': return '⚠';
      case 'info': return 'ℹ';
      default: return 'ℹ';
    }
  }
</script>

<div class="toast-container">
  {#each $toast as toast (toast.id)}
    <div
      class="toast toast-{toast.type}"
      transition:fly={{ x: 300, duration: 300 }}
    >
      <div class="toast-icon">
        {getIcon(toast.type)}
      </div>
      
      <div class="toast-content">
        {#if toast.title}
          <div class="toast-title">{toast.title}</div>
        {/if}
        <div class="toast-message">{toast.message}</div>
      </div>
      
      <button
        class="toast-close"
        on:click={() => toast.remove(toast.id)}
        aria-label="Close notification"
      >
        ×
      </button>
    </div>
  {/each}
</div>

<style>
  .toast-container {
    @apply fixed top-4 right-4 z-50 space-y-2;
    @apply max-w-sm w-full;
  }
  
  .toast {
    @apply flex items-start p-4 rounded-lg shadow-lg;
    @apply bg-white border-l-4;
  }
  
  .toast-success {
    @apply border-green-500;
  }
  
  .toast-error {
    @apply border-red-500;
  }
  
  .toast-warning {
    @apply border-yellow-500;
  }
  
  .toast-info {
    @apply border-blue-500;
  }
  
  .toast-icon {
    @apply flex-shrink-0 w-6 h-6 flex items-center justify-center;
    @apply rounded-full text-white text-sm font-bold mr-3;
  }
  
  .toast-success .toast-icon {
    @apply bg-green-500;
  }
  
  .toast-error .toast-icon {
    @apply bg-red-500;
  }
  
  .toast-warning .toast-icon {
    @apply bg-yellow-500;
  }
  
  .toast-info .toast-icon {
    @apply bg-blue-500;
  }
  
  .toast-content {
    @apply flex-1;
  }
  
  .toast-title {
    @apply font-semibold text-gray-900 mb-1;
  }
  
  .toast-message {
    @apply text-gray-700;
  }
  
  .toast-close {
    @apply ml-3 text-gray-400 hover:text-gray-600;
    @apply text-xl font-bold flex-shrink-0;
  }
</style>'''
                    },
                    {
                        "title": "Toast Usage Examples",
                        "description": "How to use the toast system",
                        "code": '''<!-- App.svelte -->
<script>
  import ToastContainer from '$lib/components/ToastContainer.svelte';
  import Button from '$lib/components/Button.svelte';
  import { toast } from '$lib/stores/toast.js';
  
  function showSuccess() {
    toast.success('Operation completed successfully!');
  }
  
  function showError() {
    toast.error('Something went wrong. Please try again.');
  }
  
  function showWarning() {
    toast.warning('This action cannot be undone.');
  }
  
  function showInfo() {
    toast.info('New update available.');
  }
  
  function showCustom() {
    toast.success('Custom toast with title', {
      title: 'Success!',
      duration: 8000
    });
  }
</script>

<main class="p-8">
  <h1 class="text-2xl font-bold mb-6">Toast Examples</h1>
  
  <div class="space-x-4">
    <Button variant="success" on:click={showSuccess}>
      Show Success
    </Button>
    
    <Button variant="danger" on:click={showError}>
      Show Error
    </Button>
    
    <Button variant="warning" on:click={showWarning}>
      Show Warning
    </Button>
    
    <Button variant="info" on:click={showInfo}>
      Show Info
    </Button>
    
    <Button variant="primary" on:click={showCustom}>
      Show Custom
    </Button>
  </div>
</main>

<!-- Toast container should be at the root level -->
<ToastContainer />'''
                    }
                ]
            }
        ]