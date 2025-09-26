"""Angular Material component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class AngularMaterialIngestionModule(BaseIngestionModule):
    """Angular Material component ingestion."""
    
    def get_namespace(self) -> str:
        return "angular-material"
    
    def get_framework(self) -> str:
        return "angular"
    
    def get_base_url(self) -> str:
        return "https://material.angular.io"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Angular Material components."""
        return [
            {
                "name": "MatButton",
                "title": "Angular Material Button",
                "description": "Material Design button with elevation and ink ripples.",
                "component_type": "button",
                "category": "form",
                "framework": "angular",
                "tags": ["button", "material", "angular", "form"],
                "documentation_url": f"{self.get_base_url()}/components/button",
                "import_statement": '''import { MatButtonModule } from '@angular/material/button';

@NgModule({
  imports: [MatButtonModule],
})
export class AppModule { }''',
                "basic_usage": '<button mat-button>Basic</button>',
                "variants": {
                    "basic": '<button mat-button>Basic</button>',
                    "raised": '<button mat-raised-button>Raised</button>',
                    "stroked": '<button mat-stroked-button>Stroked</button>',
                    "flat": '<button mat-flat-button>Flat</button>',
                    "primary": '<button mat-raised-button color="primary">Primary</button>',
                    "accent": '<button mat-raised-button color="accent">Accent</button>',
                    "warn": '<button mat-raised-button color="warn">Warn</button>',
                    "disabled": '<button mat-raised-button disabled>Disabled</button>',
                    "icon": '<button mat-icon-button><mat-icon>favorite</mat-icon></button>',
                    "fab": '<button mat-fab><mat-icon>add</mat-icon></button>',
                    "mini-fab": '<button mat-mini-fab><mat-icon>add</mat-icon></button>',
                    "extended-fab": '<button mat-fab extended><mat-icon>add</mat-icon>Add Item</button>'
                },
                "examples": [
                    {
                        "title": "Button Types",
                        "description": "Different Material button types",
                        "code": '''<!-- Basic Buttons -->
<button mat-button>Basic</button>
<button mat-raised-button>Raised</button>
<button mat-stroked-button>Stroked</button>
<button mat-flat-button>Flat</button>

<!-- Colored Buttons -->
<button mat-raised-button color="primary">Primary</button>
<button mat-raised-button color="accent">Accent</button>
<button mat-raised-button color="warn">Warn</button>

<!-- Icon Buttons -->
<button mat-icon-button>
  <mat-icon>favorite</mat-icon>
</button>

<!-- FAB Buttons -->
<button mat-fab>
  <mat-icon>add</mat-icon>
</button>

<button mat-mini-fab>
  <mat-icon>add</mat-icon>
</button>'''
                    }
                ]
            },
            {
                "name": "MatCard",
                "title": "Angular Material Card",
                "description": "Material Design card container for content.",
                "component_type": "display",
                "category": "layout",
                "framework": "angular",
                "tags": ["card", "material", "angular", "container"],
                "documentation_url": f"{self.get_base_url()}/components/card",
                "import_statement": '''import { MatCardModule } from '@angular/material/card';

@NgModule({
  imports: [MatCardModule],
})
export class AppModule { }''',
                "basic_usage": '''<mat-card>
  <mat-card-content>
    Simple card
  </mat-card-content>
</mat-card>''',
                "examples": [
                    {
                        "title": "Advanced Card",
                        "description": "Card with header, content, and actions",
                        "code": '''<mat-card class="example-card">
  <mat-card-header>
    <div mat-card-avatar class="example-header-image"></div>
    <mat-card-title>Shiba Inu</mat-card-title>
    <mat-card-subtitle>Dog Breed</mat-card-subtitle>
  </mat-card-header>
  <img mat-card-image src="https://material.angular.io/assets/img/examples/shiba2.jpg" alt="Photo of a Shiba Inu">
  <mat-card-content>
    <p>
      The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog from Japan.
    </p>
  </mat-card-content>
  <mat-card-actions>
    <button mat-button>LIKE</button>
    <button mat-button>SHARE</button>
  </mat-card-actions>
</mat-card>'''
                    }
                ]
            },
            {
                "name": "MatDialog",
                "title": "Angular Material Dialog",
                "description": "Material Design modal dialog service.",
                "component_type": "overlay",
                "category": "overlay",
                "framework": "angular",
                "tags": ["dialog", "modal", "material", "angular"],
                "documentation_url": f"{self.get_base_url()}/components/dialog",
                "import_statement": '''import { MatDialogModule } from '@angular/material/dialog';

@NgModule({
  imports: [MatDialogModule],
})
export class AppModule { }''',
                "basic_usage": '''<button mat-raised-button (click)="openDialog()">Open dialog</button>''',
                "examples": [
                    {
                        "title": "Dialog Implementation",
                        "description": "Complete dialog service implementation",
                        "code": '''// main-component.ts
import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog-demo',
  template: \`
    <button mat-raised-button (click)="openDialog()">Open Dialog</button>
  \`
})
export class DialogDemoComponent {
  constructor(public dialog: MatDialog) {}
  
  openDialog(): void {
    const dialogRef = this.dialog.open(DialogContentComponent, {
      width: '250px',
      data: { name: 'John', animal: 'Dog' }
    });
    
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      if (result) {
        console.log('Result:', result);
      }
    });
  }
}

// dialog-content.component.ts
import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface DialogData {
  animal: string;
  name: string;
}

@Component({
  selector: 'app-dialog-content',
  template: \`
    <h1 mat-dialog-title>Hi {{data.name}}</h1>
    <div mat-dialog-content>
      <p>What's your favorite animal?</p>
      <mat-form-field>
        <mat-label>Favorite Animal</mat-label>
        <input matInput [(ngModel)]="data.animal">
      </mat-form-field>
    </div>
    <div mat-dialog-actions>
      <button mat-button (click)="onNoClick()">No Thanks</button>
      <button mat-button [mat-dialog-close]="data.animal" cdkFocusInitial>Ok</button>
    </div>
  \`
})
export class DialogContentComponent {
  constructor(
    public dialogRef: MatDialogRef<DialogContentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}
  
  onNoClick(): void {
    this.dialogRef.close();
  }
}'''
                    }
                ]
            },
            {
                "name": "MatFormField",
                "title": "Angular Material Form Field",
                "description": "Material Design form field wrapper for input components.",
                "component_type": "input",
                "category": "form",
                "framework": "angular",
                "tags": ["form", "input", "material", "angular"],
                "documentation_url": f"{self.get_base_url()}/components/form-field",
                "import_statement": '''import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@NgModule({
  imports: [MatFormFieldModule, MatInputModule],
})
export class AppModule { }''',
                "basic_usage": '''<mat-form-field>
  <mat-label>Input</mat-label>
  <input matInput>
</mat-form-field>''',
                "variants": {
                    "fill": '''<mat-form-field appearance="fill">
  <mat-label>Fill</mat-label>
  <input matInput>
</mat-form-field>''',
                    "outline": '''<mat-form-field appearance="outline">
  <mat-label>Outline</mat-label>
  <input matInput>
</mat-form-field>''',
                    "legacy": '''<mat-form-field appearance="legacy">
  <mat-label>Legacy</mat-label>
  <input matInput>
</mat-form-field>''',
                    "standard": '''<mat-form-field appearance="standard">
  <mat-label>Standard</mat-label>
  <input matInput>
</mat-form-field>''',
                    "with-icon": '''<mat-form-field>
  <mat-label>Input with icon</mat-label>
  <input matInput>
  <mat-icon matSuffix>sentiment_very_satisfied</mat-icon>
</mat-form-field>''',
                    "with-hint": '''<mat-form-field>
  <mat-label>Input with hint</mat-label>
  <input matInput>
  <mat-hint>Hint text</mat-hint>
</mat-form-field>''',
                    "with-error": '''<mat-form-field>
  <mat-label>Input with error</mat-label>
  <input matInput [formControl]="emailFormControl">
  <mat-error *ngIf="emailFormControl.hasError('email') && !emailFormControl.hasError('required')">
    Please enter a valid email address
  </mat-error>
  <mat-error *ngIf="emailFormControl.hasError('required')">
    Email is <strong>required</strong>
  </mat-error>
</mat-form-field>'''
                },
                "examples": [
                    {
                        "title": "Form with Validation",
                        "description": "Complete form with Material form fields",
                        "code": '''// component.ts
import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-form-demo',
  template: \`
    <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
      <mat-form-field appearance="outline">
        <mat-label>Name</mat-label>
        <input matInput formControlName="name" required>
        <mat-icon matSuffix>person</mat-icon>
        <mat-error *ngIf="userForm.get('name')?.hasError('required')">
          Name is required
        </mat-error>
      </mat-form-field>
      
      <mat-form-field appearance="outline">
        <mat-label>Email</mat-label>
        <input matInput formControlName="email" type="email" required>
        <mat-icon matSuffix>email</mat-icon>
        <mat-error *ngIf="userForm.get('email')?.hasError('required')">
          Email is required
        </mat-error>
        <mat-error *ngIf="userForm.get('email')?.hasError('email')">
          Please enter a valid email
        </mat-error>
      </mat-form-field>
      
      <mat-form-field appearance="outline">
        <mat-label>Password</mat-label>
        <input matInput formControlName="password" [type]="hidePassword ? 'password' : 'text'" required>
        <button mat-icon-button matSuffix (click)="hidePassword = !hidePassword" type="button">
          <mat-icon>{{hidePassword ? 'visibility_off' : 'visibility'}}</mat-icon>
        </button>
        <mat-error *ngIf="userForm.get('password')?.hasError('required')">
          Password is required
        </mat-error>
        <mat-error *ngIf="userForm.get('password')?.hasError('minlength')">
          Password must be at least 8 characters
        </mat-error>
      </mat-form-field>
      
      <button mat-raised-button color="primary" type="submit" [disabled]="userForm.invalid">
        Submit
      </button>
    </form>
  \`
})
export class FormDemoComponent {
  hidePassword = true;
  
  userForm = new FormGroup({
    name: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(8)])
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
                "name": "MatToolbar",
                "title": "Angular Material Toolbar",
                "description": "Material Design toolbar for headers and navigation.",
                "component_type": "navigation",
                "category": "navigation",
                "framework": "angular",
                "tags": ["toolbar", "navigation", "material", "angular"],
                "documentation_url": f"{self.get_base_url()}/components/toolbar",
                "import_statement": '''import { MatToolbarModule } from '@angular/material/toolbar';

@NgModule({
  imports: [MatToolbarModule],
})
export class AppModule { }''',
                "basic_usage": '''<mat-toolbar>
  <span>My Application</span>
</mat-toolbar>''',
                "variants": {
                    "primary": '''<mat-toolbar color="primary">
  <span>Primary Toolbar</span>
</mat-toolbar>''',
                    "accent": '''<mat-toolbar color="accent">
  <span>Accent Toolbar</span>
</mat-toolbar>''',
                    "warn": '''<mat-toolbar color="warn">
  <span>Warn Toolbar</span>
</mat-toolbar>''',
                    "with-menu": '''<mat-toolbar color="primary">
  <button mat-icon-button>
    <mat-icon>menu</mat-icon>
  </button>
  <span>My App</span>
  <span class="spacer"></span>
  <button mat-icon-button>
    <mat-icon>favorite</mat-icon>
  </button>
  <button mat-icon-button>
    <mat-icon>share</mat-icon>
  </button>
</mat-toolbar>'''
                },
                "examples": [
                    {
                        "title": "App Toolbar with Menu",
                        "description": "Complete app toolbar with navigation",
                        "code": '''<mat-toolbar color="primary">
  <button mat-icon-button (click)="toggleSidenav()">
    <mat-icon>menu</mat-icon>
  </button>
  
  <span>My Application</span>
  
  <!-- Spacer to push content to the right -->
  <span class="spacer"></span>
  
  <button mat-icon-button [matMenuTriggerFor]="userMenu">
    <mat-icon>account_circle</mat-icon>
  </button>
  
  <mat-menu #userMenu="matMenu">
    <button mat-menu-item>
      <mat-icon>person</mat-icon>
      <span>Profile</span>
    </button>
    <button mat-menu-item>
      <mat-icon>settings</mat-icon>
      <span>Settings</span>
    </button>
    <mat-divider></mat-divider>
    <button mat-menu-item>
      <mat-icon>exit_to_app</mat-icon>
      <span>Logout</span>
    </button>
  </mat-menu>
</mat-toolbar>

<!-- CSS for spacer -->
<style>
  .spacer {
    flex: 1 1 auto;
  }
</style>'''
                    }
                ]
            },
            {
                "name": "MatSnackBar",
                "title": "Angular Material Snack Bar",
                "description": "Material Design snack bar for brief messages.",
                "component_type": "feedback",
                "category": "overlay",
                "framework": "angular",
                "tags": ["snackbar", "notification", "material", "angular"],
                "documentation_url": f"{self.get_base_url()}/components/snack-bar",
                "import_statement": '''import { MatSnackBarModule } from '@angular/material/snack-bar';

@NgModule({
  imports: [MatSnackBarModule],
})
export class AppModule { }''',
                "basic_usage": '''<button mat-raised-button (click)="openSnackBar('Hello!', 'Close')">
  Show snack-bar
</button>''',
                "examples": [
                    {
                        "title": "Snack Bar Implementation",
                        "description": "Component with different snack bar types",
                        "code": '''// component.ts
import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-snackbar-demo',
  template: \`
    <div class="buttons">
      <button mat-raised-button (click)="openSnackBar('Message sent!', 'Close')">
        Show Simple Snack Bar
      </button>
      
      <button mat-raised-button (click)="openSnackBarWithAction()">
        Show Snack Bar with Action
      </button>
      
      <button mat-raised-button (click)="openCustomSnackBar()">
        Show Custom Snack Bar
      </button>
    </div>
  \`
})
export class SnackBarDemoComponent {
  constructor(private snackBar: MatSnackBar) {}
  
  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 3000,
    });
  }
  
  openSnackBarWithAction() {
    const snackBarRef = this.snackBar.open('Item deleted', 'Undo', {
      duration: 5000,
    });
    
    snackBarRef.onAction().subscribe(() => {
      console.log('Undo clicked');
      // Implement undo logic here
    });
  }
  
  openCustomSnackBar() {
    this.snackBar.open('Custom styled message', 'Close', {
      duration: 4000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
      panelClass: ['custom-snackbar']
    });
  }
}

/* Custom CSS for snack bar */
::ng-deep .custom-snackbar {
  background-color: #4caf50 !important;
  color: white !important;
}'''
                    }
                ]
            }
        ]