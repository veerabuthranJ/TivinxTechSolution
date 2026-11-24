import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { ContentService } from '../../../core/services/content.service';
import { NotificationService } from '../../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../../shared/components/confirm-dialog/confirm-dialog.component';
import { Content } from '../../../shared/models/content.model';

@Component({
  selector: 'app-content-list',
  standalone: true,
  imports: [
    CommonModule, FormsModule, RouterModule,
    MatCardModule, MatTableModule, MatButtonModule, MatIconModule,
    MatFormFieldModule, MatInputModule, MatSelectModule, MatPaginatorModule,
    MatProgressSpinnerModule, MatTooltipModule
  ],
  templateUrl: './content-list.component.html',
  styleUrl: './content-list.component.scss'
})
export class ContentListComponent implements OnInit {
  private contentService = inject(ContentService);
  private notification = inject(NotificationService);
  private dialog = inject(MatDialog);

  contents: Content[] = [];
  loading = true;
  search = '';
  statusFilter = '';
  totalCount = 0;
  page = 1;
  pageSize = 20;

  columns = ['thumbnail', 'title', 'category_name', 'status', 'created_at', 'actions'];

  ngOnInit(): void {
    this.loadContent();
  }

  loadContent(): void {
    this.loading = true;
    const params: Record<string, string> = { page: this.page.toString() };
    if (this.search) params['search'] = this.search;
    if (this.statusFilter) params['status'] = this.statusFilter;

    this.contentService.getAdminContent(params).subscribe({
      next: (data) => {
        this.contents = data.results;
        this.totalCount = data.count;
        this.loading = false;
      },
      error: () => {
        this.notification.error('Failed to load content');
        this.loading = false;
      }
    });
  }

  onSearch(): void {
    this.page = 1;
    this.loadContent();
  }

  onStatusFilter(): void {
    this.page = 1;
    this.loadContent();
  }

  onPage(event: PageEvent): void {
    this.page = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadContent();
  }

  togglePublish(content: Content): void {
    const newStatus = content.status === 'published' ? 'unpublished' : 'published';
    this.contentService.updateContent(content.id, { status: newStatus }).subscribe({
      next: () => {
        this.notification.success(`Content ${newStatus}`);
        this.loadContent();
      },
      error: () => this.notification.error('Failed to update content')
    });
  }

  deleteContent(content: Content): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete Content',
        message: `Are you sure you want to delete "${content.title}"?`,
        confirmText: 'Delete'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.contentService.deleteContent(content.id).subscribe({
          next: () => {
            this.notification.success('Content deleted');
            this.loadContent();
          },
          error: () => this.notification.error('Failed to delete content')
        });
      }
    });
  }
}
