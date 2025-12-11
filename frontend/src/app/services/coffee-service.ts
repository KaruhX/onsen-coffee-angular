import { HttpClient } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { forkJoin, map, Observable, tap } from 'rxjs';
import { CartItem, CheckoutData, Coffee, Order } from '../model/models';

@Injectable({
  providedIn: 'root',
})
export class CoffeeService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/api';
  private cartItems = signal<CartItem[]>([]);
  private coffees = signal<Coffee[]>([]);

  readonly cart = this.cartItems.asReadonly();
  readonly cartCount = computed(() =>
    this.cartItems().reduce((sum, item) => sum + item.quantity, 0)
  );
  readonly cartTotal = computed(() =>
    this.cartItems().reduce((sum, item) => sum + (item.coffee?.price || 0) * item.quantity, 0)
  );
  readonly shippingCost = computed(() => (this.cartTotal() > 0 ? 4.99 : 0));
  readonly orderTotal = computed(() => this.cartTotal() + this.shippingCost());

  getCoffees(): Observable<Coffee[]> {
    return this.http
      .get<Coffee[]>(`${this.apiUrl}/coffees`)
      .pipe(tap((coffees) => this.coffees.set(coffees)));
  }

  getCoffeeById(id: number): Observable<Coffee> {
    return this.http.get<Coffee>(`${this.apiUrl}/coffees/${id}`);
  }

  getCart(): Observable<CartItem[]> {
    return forkJoin({
      cart: this.http.get<CartItem[]>(`${this.apiUrl}/cart`),
      coffees: this.coffees().length ? [this.coffees()] : this.getCoffees(),
    }).pipe(
      map(({ cart, coffees }) => {
        const coffeeList = Array.isArray(coffees) ? coffees : [coffees];
        return cart.map((item) => ({
          ...item,
          coffee: coffeeList.find((c) => c.id === item.coffeeId),
        }));
      }),
      tap((items) => this.cartItems.set(items))
    );
  }

  private enrichCart(cart: CartItem[]): CartItem[] {
    return cart.map((item) => ({
      ...item,
      coffee: this.coffees().find((c) => c.id === item.coffeeId),
    }));
  }

  addToCart(
    coffeeId: number,
    quantity: number = 1
  ): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .post<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart`, { coffeeId, quantity })
      .pipe(tap((res) => this.cartItems.set(this.enrichCart(res.cart))));
  }

  updateCartItem(
    coffeeId: number,
    quantity: number
  ): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .put<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart/${coffeeId}`, { quantity })
      .pipe(tap((res) => this.cartItems.set(this.enrichCart(res.cart))));
  }

  removeFromCart(coffeeId: number): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .delete<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart/${coffeeId}`)
      .pipe(tap((res) => this.cartItems.set(this.enrichCart(res.cart))));
  }

  clearCart(): Observable<{ status: string; cart: CartItem[] }> {
    return this.http
      .delete<{ status: string; cart: CartItem[] }>(`${this.apiUrl}/cart`)
      .pipe(tap((res) => this.cartItems.set(this.enrichCart(res.cart))));
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
