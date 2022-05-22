import { Component, Inject } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-auth-button',
  template: `

  <ng-container *ngIf="auth.isAuthenticated$ | async; else loggedOut">
    <mat-list-item>
      <button mat-button (click)="auth.logout({ returnTo: document.location.origin })" style='width: 100%; text-align: left;'>
        <mat-icon>logout</mat-icon>
        Log out
      </button>
    </mat-list-item>
  </ng-container>

  <ng-template #loggedOut>
    <mat-list-item>
      <button mat-button (click)="auth.loginWithRedirect()" style='width: 100%; text-align: left;'>
        <mat-icon>login</mat-icon>
        Log in
      </button>
    </mat-list-item>
  </ng-template>
  `,
  styles: [],
})
export class AuthButtonComponent {
  constructor(@Inject(DOCUMENT) public document: Document, public auth: AuthService) {}
}