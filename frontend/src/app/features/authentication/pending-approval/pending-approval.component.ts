import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-pending-approval',
  standalone: true,
  imports: [RouterModule, MatCardModule, MatIconModule, MatButtonModule],
  template: `
    <div class="pending-container">
      <mat-card class="pending-card">
        <mat-card-content>
          <div class="pending-content">
            <mat-icon class="pending-icon">hourglass_empty</mat-icon>
            <h1>Registration Submitted</h1>
            <p>Your registration has been submitted. Please wait for administrator approval.</p>
            <p class="sub-text">You will be able to log in once an administrator approves your account.</p>
            <a mat-raised-button color="primary" routerLink="/login">Back to Login</a>
          </div>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .pending-container {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 16px;
    }
    .pending-card {
      width: 100%;
      max-width: 480px;
      padding: 40px;
      border-radius: 12px !important;
    }
    .pending-content {
      text-align: center;
    }
    .pending-icon {
      font-size: 64px;
      width: 64px;
      height: 64px;
      color: #ff9800;
      margin-bottom: 16px;
    }
    h1 {
      font-size: 24px;
      font-weight: 500;
      color: #333;
      margin-bottom: 12px;
    }
    p {
      color: #666;
      font-size: 15px;
      line-height: 1.6;
      margin-bottom: 8px;
    }
    .sub-text {
      margin-bottom: 24px;
      font-size: 13px;
    }
  `]
})
export class PendingApprovalComponent {}
