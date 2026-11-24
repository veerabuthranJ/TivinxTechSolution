import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { CategoryService } from '../../core/services/category.service';
import { NotificationService } from '../../core/services/notification.service';
import { ConfirmDialogComponent } from '../../shared/components/confirm-dialog/confirm-dialog.component';
import { CategoryDialogComponent } from './category-dialog/category-dialog.component';
import { Category } from '../../shared/models/category.model';

@Component({
  selector: 'app-category-management',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule, MatTableModule, MatButtonModule, MatIconModule,
    MatProgressSpinnerModule, MatTooltipModule
  ],
  templateUrl: './category-management.component.html',
  styleUrl: './category-management.component.scss'
})
export class CategoryManagementComponent implements OnInit {
  private categoryService = inject(CategoryService);
  private notification = inject(NotificationService);
  private dialog = inject(MatDialog);

  categories: Category[] = [];
  loading = true;
  columns = ['name', 'description', 'created_at', 'actions'];

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(): void {
    this.loading = true;
    this.categoryService.getCategories().subscribe({
      next: (data) => {
        this.categories = data.results;
        this.loading = false;
      },
      error: () => {
        this.notification.error('Failed to load categories');
        this.loading = false;
      }
    });
  }

  openDialog(category?: Category): void {
    const dialogRef = this.dialog.open(CategoryDialogComponent, {
      width: '450px',
      data: category ? { ...category } : null
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        const request = category
          ? this.categoryService.updateCategory(category.id, result)
          : this.categoryService.createCategory(result);

        request.subscribe({
          next: () => {
            this.notification.success(category ? 'Category updated' : 'Category created');
            this.loadCategories();
          },
          error: (err) => this.notification.error(err.error?.error || 'Failed to save category')
        });
      }
    });
  }

  deleteCategory(category: Category): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete Category',
        message: `Are you sure you want to delete "${category.name}"?`,
        confirmText: 'Delete'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.categoryService.deleteCategory(category.id).subscribe({
          next: () => {
            this.notification.success('Category deleted');
            this.loadCategories();
          },
          error: (err) => this.notification.error(err.error?.error || 'Failed to delete category')
        });
      }
    });
  }
}
