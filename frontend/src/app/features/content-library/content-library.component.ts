import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Subject, debounceTime, distinctUntilChanged } from 'rxjs';
import { ContentService } from '../../core/services/content.service';
import { CategoryService } from '../../core/services/category.service';
import { Content } from '../../shared/models/content.model';
import { Category } from '../../shared/models/category.model';

@Component({
  selector: 'app-content-library',
  standalone: true,
  imports: [
    CommonModule, FormsModule, RouterModule,
    MatCardModule, MatIconModule, MatButtonModule,
    MatFormFieldModule, MatInputModule, MatChipsModule,
    MatPaginatorModule, MatProgressSpinnerModule
  ],
  templateUrl: './content-library.component.html',
  styleUrl: './content-library.component.scss'
})
export class ContentLibraryComponent implements OnInit {
  private contentService = inject(ContentService);
  private categoryService = inject(CategoryService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  contents: Content[] = [];
  categories: Category[] = [];
  loading = true;
  search = '';
  selectedCategory = '';
  totalCount = 0;
  page = 1;
  pageSize = 12;

  private searchSubject = new Subject<string>();

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['search']) {
        this.search = params['search'];
      }
    });

    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged()
    ).subscribe(() => {
      this.page = 1;
      this.loadContent();
    });

    this.categoryService.getCategories().subscribe({
      next: (data) => this.categories = data.results
    });

    this.loadContent();
  }

  onSearchInput(): void {
    this.searchSubject.next(this.search);
  }

  onCategorySelect(categoryId: string): void {
    this.selectedCategory = this.selectedCategory === categoryId ? '' : categoryId;
    this.page = 1;
    this.loadContent();
  }

  onPage(event: PageEvent): void {
    this.page = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadContent();
  }

  loadContent(): void {
    this.loading = true;
    const params: Record<string, string> = {
      page: this.page.toString(),
      sort: '-created_at'
    };
    if (this.selectedCategory) params['category'] = this.selectedCategory;

    if (this.search) {
      params['q'] = this.search;
      this.contentService.searchContent(params).subscribe({
        next: (data) => {
          this.contents = data.results;
          this.totalCount = data.count;
          this.loading = false;
        },
        error: () => this.loading = false
      });
    } else {
      this.contentService.getPublishedContent(params).subscribe({
        next: (data) => {
          this.contents = data.results;
          this.totalCount = data.count;
          this.loading = false;
        },
        error: () => this.loading = false
      });
    }
  }
}
