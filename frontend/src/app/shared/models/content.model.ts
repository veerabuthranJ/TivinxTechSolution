export interface Content {
  id: string;
  title: string;
  description: string;
  youtube_url: string;
  youtube_video_id: string;
  thumbnail_url: string;
  category_id: string;
  category_name?: string;
  tags: string[];
  status: 'published' | 'unpublished';
  created_by: string;
  created_at: string;
  updated_at?: string;
}
