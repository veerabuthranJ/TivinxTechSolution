import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { User } from '../../shared/models/user.model';
import { PaginatedResponse } from '../../shared/models/api-response.model';

@Injectable({ providedIn: 'root' })
export class UserManagementService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBaseUrl}/admin/users`;

  getUsers(params?: Record<string, string>): Observable<PaginatedResponse<User>> {
    let httpParams = new HttpParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) httpParams = httpParams.set(key, value);
      });
    }
    return this.http.get<PaginatedResponse<User>>(`${this.apiUrl}/`, { params: httpParams });
  }

  getPendingUsers(): Observable<{ results: User[]; count: number }> {
    return this.http.get<{ results: User[]; count: number }>(`${this.apiUrl}/pending/`);
  }

  getUserById(id: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}/`);
  }

  approveUser(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/approve/`, {});
  }

  rejectUser(id: string, reason?: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/reject/`, { reason });
  }

  disableUser(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/disable/`, {});
  }

  activateUser(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/activate/`, {});
  }
}
