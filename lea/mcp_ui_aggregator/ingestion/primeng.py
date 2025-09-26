"""PrimeNG (Angular) component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class PrimeNGIngestionModule(BaseIngestionModule):
    """PrimeNG Angular component ingestion."""
    
    def get_namespace(self) -> str:
        return "primeng"
    
    def get_framework(self) -> str:
        return "angular"
    
    def get_base_url(self) -> str:
        return "https://primeng.org"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """PrimeNG Angular components."""
        return [
            {
                "name": "Button",
                "title": "PrimeNG Button",
                "description": "Button is an extension to standard button element with icons and theming.",
                "component_type": "button",
                "category": "form",
                "framework": "angular",
                "tags": ["button", "primeng", "angular", "form"],
                "documentation_url": f"{self.get_base_url()}/button",
                "import_statement": '''import { ButtonModule } from 'primeng/button';

@NgModule({
  imports: [ButtonModule],
})
export class AppModule { }''',
                "basic_usage": '<p-button label="Click" (onClick)="handleClick()"></p-button>',
                "variants": {
                    "primary": '<p-button label="Primary" severity="primary"></p-button>',
                    "secondary": '<p-button label="Secondary" severity="secondary"></p-button>',
                    "success": '<p-button label="Success" severity="success"></p-button>',
                    "info": '<p-button label="Info" severity="info"></p-button>',
                    "warning": '<p-button label="Warning" severity="warning"></p-button>',
                    "help": '<p-button label="Help" severity="help"></p-button>',
                    "danger": '<p-button label="Danger" severity="danger"></p-button>',
                    "outlined": '<p-button label="Outlined" [outlined]="true"></p-button>',
                    "text": '<p-button label="Text" [text]="true"></p-button>',
                    "raised": '<p-button label="Raised" [raised]="true"></p-button>',
                    "rounded": '<p-button label="Rounded" [rounded]="true"></p-button>',
                    "loading": '<p-button label="Loading" [loading]="true"></p-button>',
                    "disabled": '<p-button label="Disabled" [disabled]="true"></p-button>',
                    "with-icon": '<p-button label="Search" icon="pi pi-search"></p-button>',
                    "icon-only": '<p-button icon="pi pi-check" [rounded]="true"></p-button>'
                },
                "examples": [
                    {
                        "title": "Button with Icon Positions",
                        "description": "Icons can be placed at different positions",
                        "code": '''<!-- Left Icon -->
<p-button label="Search" icon="pi pi-search"></p-button>

<!-- Right Icon -->
<p-button label="Search" icon="pi pi-search" iconPos="right"></p-button>

<!-- Icon Only -->
<p-button icon="pi pi-check" [rounded]="true"></p-button>

<!-- Loading -->
<p-button label="Loading" [loading]="loading" (onClick)="load()"></p-button>'''
                    },
                    {
                        "title": "Button Group",
                        "description": "Buttons can be grouped together",
                        "code": '''<div class="p-buttonset">
  <p-button label="Save" icon="pi pi-check"></p-button>
  <p-button label="Delete" icon="pi pi-trash" severity="danger"></p-button>
  <p-button label="Cancel" icon="pi pi-times" severity="secondary"></p-button>
</div>'''
                    }
                ]
            },
            {
                "name": "Card",
                "title": "PrimeNG Card",
                "description": "Card is a flexible container component.",
                "component_type": "display",
                "category": "panel",
                "framework": "angular",
                "tags": ["card", "primeng", "angular", "container"],
                "documentation_url": f"{self.get_base_url()}/card",
                "import_statement": '''import { CardModule } from 'primeng/card';

@NgModule({
  imports: [CardModule],
})
export class AppModule { }''',
                "basic_usage": '''<p-card header="Card Title">
  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
</p-card>''',
                "examples": [
                    {
                        "title": "Advanced Card",
                        "description": "Card with header, subheader, and footer",
                        "code": '''<p-card header="Advanced Card" subheader="Subtitle">
  <ng-template pTemplate="header">
    <img alt="Card" src="https://primefaces.org/cdn/primeng/images/usercard.png" />
  </ng-template>
  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
  <ng-template pTemplate="footer">
    <div class="flex gap-3 mt-1">
      <p-button label="Save" class="w-full" severity="secondary" [outlined]="true"></p-button>
      <p-button label="Cancel" class="w-full"></p-button>
    </div>
  </ng-template>
</p-card>'''
                    }
                ]
            },
            {
                "name": "Dialog",
                "title": "PrimeNG Dialog",
                "description": "Dialog is a container to display content in an overlay window.",
                "component_type": "overlay",
                "category": "overlay",
                "framework": "angular",
                "tags": ["dialog", "modal", "primeng", "angular"],
                "documentation_url": f"{self.get_base_url()}/dialog",
                "import_statement": '''import { DialogModule } from 'primeng/dialog';

@NgModule({
  imports: [DialogModule],
})
export class AppModule { }''',
                "basic_usage": '''<p-button (onClick)="showDialog()" label="Show"></p-button>
<p-dialog header="Header" [(visible)]="visible" [style]="{width: '50vw'}">
  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
  <ng-template pTemplate="footer">
    <p-button label="No" severity="secondary" [text]="true" (onClick)="visible = false"></p-button>
    <p-button label="Yes" (onClick)="visible = false"></p-button>
  </ng-template>
</p-dialog>''',
                "examples": [
                    {
                        "title": "Component Implementation",
                        "description": "Complete component with dialog",
                        "code": '''// component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-dialog-demo',
  template: \`
    <p-button (onClick)="showDialog()" label="Show"></p-button>
    <p-dialog 
      header="Confirm Action" 
      [(visible)]="visible" 
      [style]="{width: '400px'}"
      [modal]="true"
      [draggable]="false"
      [resizable]="false">
      <p>Are you sure you want to proceed?</p>
      <ng-template pTemplate="footer">
        <p-button 
          label="Cancel" 
          severity="secondary" 
          [text]="true" 
          (onClick)="visible = false">
        </p-button>
        <p-button 
          label="Confirm" 
          (onClick)="confirm()">
        </p-button>
      </ng-template>
    </p-dialog>
  \`
})
export class DialogDemoComponent {
  visible: boolean = false;
  
  showDialog() {
    this.visible = true;
  }
  
  confirm() {
    this.visible = false;
    // Add confirmation logic here
  }
}'''
                    }
                ]
            },
            {
                "name": "InputText",
                "title": "PrimeNG InputText",
                "description": "InputText renders a text field to enter data.",
                "component_type": "input",
                "category": "form",
                "framework": "angular",
                "tags": ["input", "text", "primeng", "angular", "form"],
                "documentation_url": f"{self.get_base_url()}/inputtext",
                "import_statement": '''import { InputTextModule } from 'primeng/inputtext';
import { FormsModule } from '@angular/forms';

@NgModule({
  imports: [InputTextModule, FormsModule],
})
export class AppModule { }''',
                "basic_usage": '<input type="text" pInputText [(ngModel)]="value" />',
                "variants": {
                    "disabled": '<input type="text" pInputText [disabled]="true" placeholder="Disabled" />',
                    "invalid": '<input type="text" pInputText class="ng-invalid ng-dirty" placeholder="Invalid" />',
                    "filled": '<input type="text" pInputText [style]="{\'background-color\': \'#f8f9fa\'}" placeholder="Filled" />',
                    "with-icon": '''<span class="p-input-icon-left">
  <i class="pi pi-search"></i>
  <input type="text" pInputText placeholder="Search" />
</span>''',
                    "with-right-icon": '''<span class="p-input-icon-right">
  <input type="text" pInputText placeholder="Search" />
  <i class="pi pi-spin pi-spinner"></i>
</span>'''
                },
                "examples": [
                    {
                        "title": "Form with Validation",
                        "description": "Input text with form validation",
                        "code": '''// component.ts
import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-input-demo',
  template: \`
    <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
      <div class="field">
        <label for="username">Username</label>
        <input 
          id="username"
          type="text" 
          pInputText 
          formControlName="username"
          [class.ng-invalid]="userForm.get('username')?.invalid && userForm.get('username')?.touched"
          placeholder="Enter username" />
        <small *ngIf="userForm.get('username')?.invalid && userForm.get('username')?.touched" 
               class="p-error">Username is required.</small>
      </div>
      
      <div class="field">
        <label for="email">Email</label>
        <span class="p-input-icon-left">
          <i class="pi pi-envelope"></i>
          <input 
            id="email"
            type="email" 
            pInputText 
            formControlName="email"
            placeholder="Enter email" />
        </span>
        <small *ngIf="userForm.get('email')?.invalid && userForm.get('email')?.touched" 
               class="p-error">Valid email is required.</small>
      </div>
      
      <p-button type="submit" label="Submit" [disabled]="userForm.invalid"></p-button>
    </form>
  \`
})
export class InputDemoComponent {
  userForm = new FormGroup({
    username: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email])
  });
  
  onSubmit() {
    if (this.userForm.valid) {
      console.log(this.userForm.value);
    }
  }
}'''
                    }
                ]
            },
            {
                "name": "Menubar",
                "title": "PrimeNG Menubar",
                "description": "Menubar is a horizontal menu component.",
                "component_type": "navigation",
                "category": "menu",
                "framework": "angular",
                "tags": ["menubar", "navigation", "primeng", "angular"],
                "documentation_url": f"{self.get_base_url()}/menubar",
                "import_statement": '''import { MenubarModule } from 'primeng/menubar';

@NgModule({
  imports: [MenubarModule],
})
export class AppModule { }''',
                "basic_usage": '''<p-menubar [model]="items">
  <ng-template pTemplate="start">
    <img src="https://primefaces.org/cdn/primeng/images/logo.png" height="40" class="mr-2">
  </ng-template>
  <ng-template pTemplate="end">
    <p-button icon="pi pi-search" [text]="true" severity="secondary"></p-button>
  </ng-template>
</p-menubar>''',
                "examples": [
                    {
                        "title": "Complete Menubar Implementation",
                        "description": "Menubar with nested items and actions",
                        "code": '''// component.ts
import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-menubar-demo',
  template: \`
    <p-menubar [model]="items">
      <ng-template pTemplate="start">
        <img src="assets/logo.png" height="40" class="mr-2" alt="Logo">
      </ng-template>
      <ng-template pTemplate="end">
        <div class="flex align-items-center gap-2">
          <p-button icon="pi pi-search" [text]="true" severity="secondary"></p-button>
          <p-button icon="pi pi-user" [text]="true" severity="secondary"></p-button>
        </div>
      </ng-template>
    </p-menubar>
  \`
})
export class MenubarDemoComponent implements OnInit {
  items: MenuItem[] = [];
  
  ngOnInit() {
    this.items = [
      {
        label: 'File',
        icon: 'pi pi-file',
        items: [
          {
            label: 'New',
            icon: 'pi pi-plus',
            command: () => this.newFile()
          },
          {
            label: 'Open',
            icon: 'pi pi-folder-open'
          },
          { separator: true },
          {
            label: 'Quit',
            icon: 'pi pi-times'
          }
        ]
      },
      {
        label: 'Edit',
        icon: 'pi pi-pencil',
        items: [
          {
            label: 'Copy',
            icon: 'pi pi-copy'
          },
          {
            label: 'Paste',
            icon: 'pi pi-clipboard'
          }
        ]
      },
      {
        label: 'View',
        icon: 'pi pi-eye'
      },
      {
        label: 'Help',
        icon: 'pi pi-question',
        items: [
          {
            label: 'About',
            icon: 'pi pi-info-circle'
          }
        ]
      }
    ];
  }
  
  newFile() {
    console.log('Creating new file...');
  }
}'''
                    }
                ]
            },
            {
                "name": "Toast",
                "title": "PrimeNG Toast",
                "description": "Toast is used to display messages in an overlay.",
                "component_type": "feedback",
                "category": "messages",
                "framework": "angular",
                "tags": ["toast", "notification", "primeng", "angular"],
                "documentation_url": f"{self.get_base_url()}/toast",
                "import_statement": '''import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@NgModule({
  imports: [ToastModule],
  providers: [MessageService]
})
export class AppModule { }''',
                "basic_usage": '''<p-toast></p-toast>
<p-button (onClick)="show()" label="Show"></p-button>''',
                "examples": [
                    {
                        "title": "Toast Implementation",
                        "description": "Component with different toast types",
                        "code": '''// component.ts
import { Component } from '@angular/core';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-toast-demo',
  template: \`
    <p-toast></p-toast>
    <div class="card flex justify-content-center gap-2">
      <p-button 
        (onClick)="showSuccess()" 
        label="Success" 
        severity="success">
      </p-button>
      <p-button 
        (onClick)="showInfo()" 
        label="Info" 
        severity="info">
      </p-button>
      <p-button 
        (onClick)="showWarn()" 
        label="Warn" 
        severity="warning">
      </p-button>
      <p-button 
        (onClick)="showError()" 
        label="Error" 
        severity="danger">
      </p-button>
    </div>
  \`
})
export class ToastDemoComponent {
  constructor(private messageService: MessageService) {}
  
  showSuccess() {
    this.messageService.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Operation completed successfully'
    });
  }
  
  showInfo() {
    this.messageService.add({
      severity: 'info',
      summary: 'Info',
      detail: 'Information message'
    });
  }
  
  showWarn() {
    this.messageService.add({
      severity: 'warn',
      summary: 'Warning',
      detail: 'This is a warning message'
    });
  }
  
  showError() {
    this.messageService.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Something went wrong'
    });
  }
}'''
                    }
                ]
            }
        ]