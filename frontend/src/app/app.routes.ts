import { Routes } from '@angular/router';
import { LayoutComponent } from './shared/components/layout/layout.component';
import { authGuard } from './core/guards/auth.guard';
import { adminGuard } from './core/guards/admin.guard';

export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./features/authentication/login/login.component').then(m => m.LoginComponent) },
  { path: 'register', loadComponent: () => import('./features/authentication/register/register.component').then(m => m.RegisterComponent) },
  { path: 'pending-approval', loadComponent: () => import('./features/authentication/pending-approval/pending-approval.component').then(m => m.PendingApprovalComponent) },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: 'dashboard', loadComponent: () => import('./features/user-dashboard/user-dashboard.component').then(m => m.UserDashboardComponent) },
      { path: 'content', loadComponent: () => import('./features/content-library/content-library.component').then(m => m.ContentLibraryComponent) },
      { path: 'content/:id', loadComponent: () => import('./features/video-player/video-player.component').then(m => m.VideoPlayerComponent) },
      { path: 'profile', loadComponent: () => import('./features/profile/profile.component').then(m => m.ProfileComponent) },
      { path: 'change-password', loadComponent: () => import('./features/profile/change-password/change-password.component').then(m => m.ChangePasswordComponent) },
      {
        path: 'admin',
        canActivate: [adminGuard],
        children: [
          { path: 'dashboard', loadComponent: () => import('./features/admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent) },
          { path: 'users', loadComponent: () => import('./features/user-management/user-management.component').then(m => m.UserManagementComponent) },
          { path: 'content', loadComponent: () => import('./features/content-management/content-list/content-list.component').then(m => m.ContentListComponent) },
          { path: 'content/add', loadComponent: () => import('./features/content-management/content-form/content-form.component').then(m => m.ContentFormComponent) },
          { path: 'content/edit/:id', loadComponent: () => import('./features/content-management/content-form/content-form.component').then(m => m.ContentFormComponent) },
          { path: 'categories', loadComponent: () => import('./features/category-management/category-management.component').then(m => m.CategoryManagementComponent) },
          { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
        ]
      },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  },
  { path: '**', redirectTo: '' }
];
