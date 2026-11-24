export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  page: number;
  pages: number;
}

export interface DashboardStats {
  total_users: number;
  approved_users: number;
  pending_users: number;
  rejected_users: number;
  disabled_users: number;
  total_content: number;
  published_content: number;
  unpublished_content: number;
  total_categories: number;
  recent_users: any[];
  recent_content: any[];
}
