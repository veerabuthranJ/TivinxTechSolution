import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../core/services/auth.service';
import { ContentService } from '../../core/services/content.service';
import { Content } from '../../shared/models/content.model';

@Component({
  selector: 'app-user-dashboard',
  standalone: true,
  imports: [
    CommonModule, FormsModule, RouterModule,
    MatCardModule, MatIconModule, MatButtonModule,
    MatFormFieldModule, MatInputModule, MatChipsModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './user-dashboard.component.html',
  styleUrl: './user-dashboard.component.scss'
})
export class UserDashboardComponent implements OnInit {
  private authService = inject(AuthService);
  private contentService = inject(ContentService);
  private router = inject(Router);

  userName = '';
  recentContent: Content[] = [];
  totalContent = 0;
  loading = true;
  searchQuery = '';

  ngOnInit(): void {
    const user = this.authService.getUser();
    this.userName = user?.full_name || 'User';
    this.loadContent();
  }

  loadContent(): void {
    this.contentService.getPublishedContent({ sort: '-created_at' }).subscribe({
      next: (data) => {
        this.recentContent = data.results.slice(0, 8);
        this.totalContent = data.count;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/content'], { queryParams: { search: this.searchQuery } });
    }
  }
}
