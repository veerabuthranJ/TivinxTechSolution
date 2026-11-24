import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ContentService } from '../../core/services/content.service';
import { Content } from '../../shared/models/content.model';
import { SafeUrlPipe } from '../../shared/pipes/safe-url.pipe';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [
    CommonModule, RouterModule,
    MatCardModule, MatIconModule, MatButtonModule,
    MatChipsModule, MatProgressSpinnerModule, SafeUrlPipe
  ],
  templateUrl: './video-player.component.html',
  styleUrl: './video-player.component.scss'
})
export class VideoPlayerComponent implements OnInit {
  private contentService = inject(ContentService);
  private route = inject(ActivatedRoute);

  content: Content | null = null;
  loading = true;
  error = '';

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    this.contentService.getContentById(id).subscribe({
      next: (data) => {
        this.content = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Content not found or unavailable.';
        this.loading = false;
      }
    });
  }

  get embedUrl(): string {
    return `https://www.youtube.com/embed/${this.content?.youtube_video_id}`;
  }
}
