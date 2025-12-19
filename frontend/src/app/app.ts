import { CommonModule } from '@angular/common';
import { Component, HostListener, inject, OnInit } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { RouterLink, RouterOutlet } from '@angular/router';
import { CoffeeService } from './services/coffee-service';
import { SupabaseService } from './services/supabase.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    CommonModule,
    MatIconModule,
    MatBadgeModule,
    MatButtonModule,
    MatMenuModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly coffeeService = inject(CoffeeService);
  private readonly supabaseService = inject(SupabaseService);

  scrolled = false;
  mobileMenuOpen = false;

  readonly cartCount = this.coffeeService.cartCount;

  isAuthenticated(): boolean {
    return this.supabaseService.isAuthenticated;
  }

  isAdmin(): boolean {
    return this.supabaseService.isAdmin;
  }

  get userProfile() {
    return this.supabaseService.profile;
  }

  @HostListener('window:scroll')
  onScroll() {
    this.scrolled = window.scrollY > 50;
  }

  ngOnInit() {
    // Cargar carrito al iniciar
    this.coffeeService.getCart().subscribe();
  }

  toggleMobileMenu() {
    this.mobileMenuOpen = !this.mobileMenuOpen;
  }

  async logout() {
    try {
      await this.supabaseService.signOut();
      window.location.href = '/';
    } catch (error) {
      console.error('Error signing out:', error);
    }
  }
}
