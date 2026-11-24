import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTabsModule } from '@angular/material/tabs';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { UserManagementService } from '../../core/services/user-management.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../shared/components/confirm-dialog/confirm-dialog.component';
import { User } from '../../shared/models/user.model';
import { RejectDialogComponent } from './reject-dialog.component';

@Component({
  selector: 'app-user-management',
  standalone: true,
  imports: [
    CommonModule, FormsModule,
    MatCardModule, MatTableModule, MatButtonModule, MatIconModule,
    MatFormFieldModule, MatInputModule, MatTabsModule, MatPaginatorModule,
    MatProgressSpinnerModule, MatDialogModule, MatTooltipModule
  ],
  templateUrl: './user-management.component.html',
  styleUrl: './user-management.component.scss'
})
export class UserManagementComponent implements OnInit {
  private userService = inject(UserManagementService);
  private notification = inject(NotificationService);
  private dialog = inject(MatDialog);

  users: User[] = [];
  loading = true;
  search = '';
  currentTab = '';
  totalCount = 0;
  page = 1;
  pageSize = 20;

  columns = ['full_name', 'email', 'status', 'created_at', 'actions'];
  tabs = ['All', 'Pending', 'Approved', 'Rejected', 'Disabled'];

  ngOnInit(): void {
    this.loadUsers();
  }

  onTabChange(index: number): void {
    this.currentTab = index === 0 ? '' : this.tabs[index].toUpperCase();
    this.page = 1;
    this.loadUsers();
  }

  onSearch(): void {
    this.page = 1;
    this.loadUsers();
  }

  onPage(event: PageEvent): void {
    this.page = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading = true;
    const params: Record<string, string> = { page: this.page.toString() };
    if (this.currentTab) params['status'] = this.currentTab;
    if (this.search) params['search'] = this.search;

    this.userService.getUsers(params).subscribe({
      next: (data) => {
        this.users = data.results;
        this.totalCount = data.count;
        this.loading = false;
      },
      error: () => {
        this.notification.error('Failed to load users');
        this.loading = false;
      }
    });
  }

  approve(user: User): void {
    this.userService.approveUser(user.id).subscribe({
      next: () => {
        this.notification.success(`${user.full_name} has been approved`);
        this.loadUsers();
      },
      error: () => this.notification.error('Failed to approve user')
    });
  }

  reject(user: User): void {
    const dialogRef = this.dialog.open(RejectDialogComponent, {
      width: '400px',
      data: { userName: user.full_name }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result !== undefined) {
        this.userService.rejectUser(user.id, result).subscribe({
          next: () => {
            this.notification.success(`${user.full_name} has been rejected`);
            this.loadUsers();
          },
          error: () => this.notification.error('Failed to reject user')
        });
      }
    });
  }

  disable(user: User): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Disable User',
        message: `Are you sure you want to disable ${user.full_name}?`,
        confirmText: 'Disable'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.userService.disableUser(user.id).subscribe({
          next: () => {
            this.notification.success(`${user.full_name} has been disabled`);
            this.loadUsers();
          },
          error: () => this.notification.error('Failed to disable user')
        });
      }
    });
  }

  activate(user: User): void {
    this.userService.activateUser(user.id).subscribe({
      next: () => {
        this.notification.success(`${user.full_name} has been activated`);
        this.loadUsers();
      },
      error: () => this.notification.error('Failed to activate user')
    });
  }
}
