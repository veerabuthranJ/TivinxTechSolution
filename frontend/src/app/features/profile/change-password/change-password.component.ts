import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-change-password',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule, RouterModule,
    MatCardModule, MatFormFieldModule, MatInputModule,
    MatButtonModule, MatIconModule, MatProgressSpinnerModule
  ],
  template: `
    <div class="change-password-page">
      <h2 class="page-title">Change Password</h2>
      <mat-card class="form-card">
        <mat-card-content>
          <form [formGroup]="form" (ngSubmit)="onSubmit()">
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Current Password</mat-label>
              <input matInput formControlName="current_password" type="password">
              @if (form.get('current_password')?.hasError('required') && form.get('current_password')?.touched) {
                <mat-error>Current password is required</mat-error>
              }
            </mat-form-field>

            <mat-form-field appearance="outline" class="full-width">
              <mat-label>New Password</mat-label>
              <input matInput formControlName="new_password" type="password">
              @if (form.get('new_password')?.hasError('required') && form.get('new_password')?.touched) {
                <mat-error>New password is required</mat-error>
              }
              @if (form.get('new_password')?.hasError('minlength') && form.get('new_password')?.touched) {
                <mat-error>Password must be at least 8 characters</mat-error>
              }
            </mat-form-field>

            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Confirm New Password</mat-label>
              <input matInput formControlName="confirm_password" type="password">
              @if (form.get('confirm_password')?.hasError('required') && form.get('confirm_password')?.touched) {
                <mat-error>Please confirm your new password</mat-error>
              }
              @if (form.get('confirm_password')?.hasError('passwordMismatch') && form.get('confirm_password')?.touched) {
                <mat-error>Passwords do not match</mat-error>
              }
            </mat-form-field>

            <div class="form-actions">
              <button mat-button type="button" routerLink="/profile">Cancel</button>
              <button mat-raised-button color="primary" type="submit" [disabled]="saving">
                @if (saving) {
                  <mat-spinner diameter="20"></mat-spinner>
                } @else {
                  Change Password
                }
              </button>
            </div>
          </form>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .change-password-page { max-width: 500px; }
    .page-title { font-size: 24px; font-weight: 500; margin-bottom: 24px; color: #333; }
    .form-card { border-radius: 12px !important; padding: 8px; }
    .full-width { width: 100%; }
    .form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 16px; }
  `]
})
export class ChangePasswordComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private notification = inject(NotificationService);
  private router = inject(Router);

  saving = false;

  form = this.fb.group({
    current_password: ['', [Validators.required]],
    new_password: ['', [Validators.required, Validators.minLength(8)]],
    confirm_password: ['', [Validators.required]]
  }, { validators: this.passwordMatchValidator });

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('new_password');
    const confirm = control.get('confirm_password');
    if (password && confirm && password.value !== confirm.value) {
      confirm.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.saving = true;
    this.authService.changePassword(this.form.value as any).subscribe({
      next: () => {
        this.saving = false;
        this.notification.success('Password changed successfully');
        this.router.navigate(['/profile']);
      },
      error: (err) => {
        this.saving = false;
        this.notification.error(err.error?.error || 'Failed to change password');
      }
    });
  }
}
