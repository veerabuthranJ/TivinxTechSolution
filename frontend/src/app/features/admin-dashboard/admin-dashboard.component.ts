import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { DashboardService } from '../../core/services/dashboard.service';
import { DashboardStats } from '../../shared/models/api-response.model';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule, RouterModule,
    MatCardModule, MatIconModule, MatTableModule,
    MatButtonModule, MatProgressSpinnerModule, MatChipsModule
  ],
  templateUrl: './admin-dashboard.component.html',
  styleUrl: './admin-dashboard.component.scss'
})
export class AdminDashboardComponent implements OnInit {
  private dashboardService = inject(DashboardService);

  stats: DashboardStats | null = null;
  loading = true;
  error = '';

  statCards: { label: string; icon: string; key: string; color: string }[] = [
    { label: 'Total Users', icon: 'people', key: 'total_users', color: '#1976d2' },
    { label: 'Pending Approvals', icon: 'pending_actions', key: 'pending_users', color: '#ff9800' },
    { label: 'Approved Users', icon: 'check_circle', key: 'approved_users', color: '#4caf50' },
    { label: 'Published Content', icon: 'video_library', key: 'published_content', color: '#9c27b0' },
    { label: 'Total Content', icon: 'library_books', key: 'total_content', color: '#00bcd4' },
    { label: 'Categories', icon: 'category', key: 'total_categories', color: '#607d8b' },
  ];

  userColumns = ['full_name', 'email', 'status', 'created_at'];
  contentColumns = ['title', 'category_name', 'status', 'created_at'];

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.loading = true;
    this.dashboardService.getStats().subscribe({
      next: (data) => {
        this.stats = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load dashboard statistics.';
        this.loading = false;
      }
    });
  }

  getStatValue(key: string): number {
    return (this.stats as any)?.[key] ?? 0;
  }
}
