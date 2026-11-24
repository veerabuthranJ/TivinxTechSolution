import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Content } from '../../shared/models/content.model';
import { PaginatedResponse } from '../../shared/models/api-response.model';

@Injectable({ providedIn: 'root' })
export class ContentService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiBaseUrl;

  getPublishedContent(params?: Record<string, string>): Observable<PaginatedResponse<Content>> {
    let httpParams = new HttpParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) httpParams = httpParams.set(key, value);
      });
    }
    return this.http.get<PaginatedResponse<Content>>(`${this.apiUrl}/content/`, { params: httpParams });
  }

  getContentById(id: string): Observable<Content> {
    return this.http.get<{ content: Content }>(`${this.apiUrl}/content/${id}/`).pipe(
      map(res => res.content)
    );
  }

  searchContent(params: Record<string, string>): Observable<PaginatedResponse<Content>> {
    let httpParams = new HttpParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) httpParams = httpParams.set(key, value);
    });
    return this.http.get<PaginatedResponse<Content>>(`${this.apiUrl}/content/search/`, { params: httpParams });
  }

  getAdminContent(params?: Record<string, string>): Observable<PaginatedResponse<Content>> {
    let httpParams = new HttpParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) httpParams = httpParams.set(key, value);
      });
    }
    return this.http.get<PaginatedResponse<Content>>(`${this.apiUrl}/admin/content/`, { params: httpParams });
  }

  getAdminContentById(id: string): Observable<Content> {
    return this.http.get<{ content: Content }>(`${this.apiUrl}/admin/content/${id}/`).pipe(
      map(res => res.content)
    );
  }

  createContent(data: Partial<Content>): Observable<Content> {
    return this.http.post<Content>(`${this.apiUrl}/admin/content/`, data);
  }

  updateContent(id: string, data: Partial<Content>): Observable<Content> {
    return this.http.put<Content>(`${this.apiUrl}/admin/content/${id}/`, data);
  }

  deleteContent(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/admin/content/${id}/`);
  }
}
