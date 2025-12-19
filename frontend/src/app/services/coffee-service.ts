import { HttpClient } from '@angular/common/http';
import { computed, Injectable, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { CartItem, CheckoutData, Coffee, Order } from '../model/models';
import { SupabaseService } from './supabase.service';

@Injectable({
  providedIn: 'root',
})
export class CoffeeService {
  private readonly apiUrl = '/api';
  private cartItems = signal<CartItem[]>([]);
  private coffees = signal<Coffee[]>([]);

  constructor(private readonly http: HttpClient, private readonly supabase: SupabaseService) {}

  readonly cart = this.cartItems.asReadonly();
  readonly cartCount = computed(() =>
    this.cartItems().reduce((sum, item) => sum + item.quantity, 0)
  );
  readonly cartTotal = computed(() =>
    this.cartItems().reduce((sum, item) => sum + item.price * item.quantity, 0)
  );
  readonly shippingCost = computed(() => 0); // Envío gratis
  readonly orderTotal = computed(() => this.cartTotal() + this.shippingCost());

  // Obtener productos desde el backend Python
  getCoffees(): Observable<Coffee[]> {
    return this.http
      .get<Coffee[]>(`${this.apiUrl}/coffees`)
      .pipe(tap((products) => this.coffees.set(products)));
  }

  getCoffeeById(id: number): Observable<Coffee> {
    return this.http.get<Coffee>(`${this.apiUrl}/coffees/${id}`);
  }

  getCoffeeBySlug(slug: string): Observable<Coffee> {
    return this.http.get<Coffee>(`${this.apiUrl}/coffees/slug/${slug}`);
  }

  getFeaturedCoffees(): Observable<Coffee[]> {
    return this.http.get<Coffee[]>(`${this.apiUrl}/coffees/featured`);
  }

  getCart(): Observable<CartItem[]> {
    return this.http
      .get<CartItem[]>(`${this.apiUrl}/cart`)
      .pipe(tap((items) => this.cartItems.set(items)));
  }

  private enrichCart(cart: CartItem[]): CartItem[] {
    return cart;
  }

  addToCart(
    coffeeId: number,
    quantity: number = 1
  ): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .post<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart`, { coffeeId, quantity })
      .pipe(tap((res) => this.cartItems.set(res.cart)));
  }

  updateCartItem(
    coffeeId: number,
    quantity: number
  ): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .put<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart/${coffeeId}`, { quantity })
      .pipe(tap((res) => this.cartItems.set(res.cart)));
  }

  removeFromCart(coffeeId: number): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .delete<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart/${coffeeId}`)
      .pipe(tap((res) => this.cartItems.set(res.cart)));
  }

  clearCart(): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .delete<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart`)
      .pipe(tap((res) => this.cartItems.set(res.cart)));
  }

  // ============ ORDERS ============

  createOrder(
    checkoutData: CheckoutData
  ): Observable<{ status: string; order_id: number; total: number }> {
    return this.http
      .post<{ status: string; order_id: number; total: number }>(
        `${this.apiUrl}/orders`,
        checkoutData
      )
      .pipe(tap(() => this.cartItems.set([])));
  }

  getOrderById(orderId: number): Observable<Order> {
    return this.http.get<Order>(`${this.apiUrl}/orders/${orderId}`);
  }

  getOrdersByEmail(email: string): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.apiUrl}/orders/by-email/${email}`);
  }

  getAllOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.apiUrl}/orders`);
  }
}
