import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { ContentService } from '../../../core/services/content.service';
import { CategoryService } from '../../../core/services/category.service';
import { NotificationService } from '../../../core/services/notification.service';
import { Category } from '../../../shared/models/category.model';

@Component({
  selector: 'app-content-form',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule, RouterModule,
    MatCardModule, MatFormFieldModule, MatInputModule,
    MatButtonModule, MatIconModule, MatSelectModule,
    MatChipsModule, MatSlideToggleModule, MatProgressSpinnerModule
  ],
  templateUrl: './content-form.component.html',
  styleUrl: './content-form.component.scss'
})
export class ContentFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private contentService = inject(ContentService);
  private categoryService = inject(CategoryService);
  private notification = inject(NotificationService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  isEdit = false;
  contentId = '';
  loading = false;
  saving = false;
  categories: Category[] = [];
  tags: string[] = [];
  thumbnailPreview = '';
  readonly separatorKeyCodes = [ENTER, COMMA] as const;

  form = this.fb.group({
    title: ['', [Validators.required, Validators.minLength(3)]],
    description: ['', [Validators.required]],
    youtube_url: ['', [Validators.required]],
    category_id: ['', [Validators.required]],
    status: ['unpublished']
  });

  ngOnInit(): void {
    this.loadCategories();
    this.contentId = this.route.snapshot.params['id'];
    if (this.contentId) {
      this.isEdit = true;
      this.loadContent();
    }

    this.form.get('youtube_url')?.valueChanges.subscribe(url => {
      if (url) {
        const videoId = this.extractVideoId(url);
        if (videoId) {
          this.thumbnailPreview = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
        } else {
          this.thumbnailPreview = '';
        }
      }
    });
  }

  loadCategories(): void {
    this.categoryService.getCategories().subscribe({
      next: (data) => this.categories = data.results,
      error: () => this.notification.error('Failed to load categories')
    });
  }

  loadContent(): void {
    this.loading = true;
    this.contentService.getAdminContentById(this.contentId).subscribe({
      next: (content) => {
        this.form.patchValue({
          title: content.title,
          description: content.description,
          youtube_url: content.youtube_url,
          category_id: content.category_id,
          status: content.status
        });
        this.tags = content.tags || [];
        this.loading = false;
      },
      error: () => {
        this.notification.error('Failed to load content');
        this.loading = false;
      }
    });
  }

  extractVideoId(url: string): string {
    const patterns = [
      /(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})/,
      /(?:youtu\.be\/)([a-zA-Z0-9_-]{11})/,
      /(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
      /(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})/
    ];
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return '';
  }

  addTag(event: any): void {
    const value = (event.value || '').trim();
    if (value && !this.tags.includes(value)) {
      this.tags.push(value);
    }
    if (event.chipInput) {
      event.chipInput.clear();
    }
  }

  removeTag(tag: string): void {
    this.tags = this.tags.filter(t => t !== tag);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.saving = true;

    const formValue = this.form.value;
    const data: any = {
      ...formValue,
      tags: this.tags
    };

    const request = this.isEdit
      ? this.contentService.updateContent(this.contentId, data)
      : this.contentService.createContent(data);

    request.subscribe({
      next: () => {
        this.saving = false;
        this.notification.success(this.isEdit ? 'Content updated' : 'Content created');
        this.router.navigate(['/admin/content']);
      },
      error: (err) => {
        this.saving = false;
        this.notification.error(err.error?.error || 'Failed to save content');
      }
    });
  }
}
