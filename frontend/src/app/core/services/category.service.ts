import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Category } from '../../shared/models/category.model';

@Injectable({ providedIn: 'root' })
export class CategoryService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiBaseUrl;

  getCategories(): Observable<{ results: Category[] }> {
    return this.http.get<{ results: Category[] }>(`${this.apiUrl}/categories/`);
  }

  createCategory(data: { name: string; description: string }): Observable<Category> {
    return this.http.post<Category>(`${this.apiUrl}/admin/categories/`, data);
  }

  updateCategory(id: string, data: { name: string; description: string }): Observable<Category> {
    return this.http.put<Category>(`${this.apiUrl}/admin/categories/${id}/`, data);
  }

  deleteCategory(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/admin/categories/${id}/`);
  }
}
