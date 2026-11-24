import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  template: `
    <div style="text-align: center; padding: 48px;">
      <h1>Company Content Portal</h1>
      <p>Phase 1 — Project Setup Complete</p>
      <p>Backend health: check /api/health/</p>
    </div>
  `
})
export class HomeComponent {}
