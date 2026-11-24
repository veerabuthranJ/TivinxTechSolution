import { Component, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule, MatSidenav } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../models/user.model';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [
    CommonModule, RouterModule,
    MatToolbarModule, MatSidenavModule, MatListModule,
    MatIconModule, MatButtonModule, MatMenuModule, MatDividerModule
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss'
})
export class LayoutComponent implements OnInit {
  private authService = inject(AuthService);
  private breakpointObserver = inject(BreakpointObserver);
  router = inject(Router);

  @ViewChild('sidenav') sidenav!: MatSidenav;

  user: User | null = null;
  isMobile = false;

  adminNav = [
    { label: 'Dashboard', icon: 'dashboard', route: '/admin/dashboard' },
    { label: 'Users', icon: 'people', route: '/admin/users' },
    { label: 'Content', icon: 'video_library', route: '/admin/content' },
    { label: 'Categories', icon: 'category', route: '/admin/categories' },
  ];

  userNav = [
    { label: 'Dashboard', icon: 'dashboard', route: '/dashboard' },
    { label: 'Content Library', icon: 'video_library', route: '/content' },
  ];

  ngOnInit(): void {
    this.user = this.authService.getUser();
    this.breakpointObserver.observe([Breakpoints.Handset]).subscribe(result => {
      this.isMobile = result.matches;
    });
  }

  get navItems() {
    return this.user?.role === 'ADMIN' ? this.adminNav : this.userNav;
  }

  get isAdmin(): boolean {
    return this.user?.role === 'ADMIN';
  }

  logout(): void {
    this.authService.logout();
  }

  onNavClick(): void {
    if (this.isMobile && this.sidenav) {
      this.sidenav.close();
    }
  }
}
