export interface User {
  id: string;
  full_name: string;
  email: string;
  role: 'ADMIN' | 'USER';
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'DISABLED';
  created_at: string;
  updated_at?: string;
  approved_at?: string;
  approved_by?: string;
  rejected_at?: string;
  rejected_by?: string;
  disabled_at?: string;
}
