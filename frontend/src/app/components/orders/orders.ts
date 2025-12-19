import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { SupabaseService } from '../../services/supabase.service';

interface Order {
  id: number;
  created_at: string;
  status: string;
  total: number;
  shipping_address: any;
  items?: OrderItem[];
}

interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  price: number;
  products?: {
    name: string;
    image: string;
  };
}

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './orders.html',
})
export class OrdersComponent implements OnInit {
  private supabase = inject(SupabaseService);
  private router = inject(Router);

  orders: Order[] = [];
  loading = false;

  ngOnInit() {
    // Verificar si está autenticado
    if (!this.supabase.isAuthenticated) {
      this.router.navigate(['/login']);
      return;
    }

    this.loadOrders();
  }

  async loadOrders() {
    this.loading = true;
    try {
      // Obtener pedidos del usuario actual
      const userOrders = await this.supabase.getUserOrders();
      this.orders = userOrders as Order[];
    } catch (error) {
      console.error('Error loading orders:', error);
    } finally {
      this.loading = false;
    }
  }

  getStatusText(status: string): string {
    const statusMap: Record<string, string> = {
      pending: 'Pendiente',
      confirmed: 'Confirmado',
      processing: 'En proceso',
      shipped: 'Enviado',
      delivered: 'Entregado',
      cancelled: 'Cancelado',
    };
    return statusMap[status] || status;
  }

  getStatusClass(status: string): string {
    const classMap: Record<string, string> = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      processing: 'bg-blue-100 text-blue-800',
      shipped: 'bg-purple-100 text-purple-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    return classMap[status] || 'bg-gray-100 text-gray-800';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  async logout() {
    try {
      await this.supabase.signOut();
      this.router.navigate(['/']);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  }
}
