import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CoffeeService } from '../../services/coffee-service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './cart.html',
})
export class Cart implements OnInit {
  private readonly coffeeService = inject(CoffeeService);
  private readonly router = inject(Router);

  readonly cart = this.coffeeService.cart;
  readonly cartCount = this.coffeeService.cartCount;
  readonly cartTotal = this.coffeeService.cartTotal;

  ngOnInit(): void {
    this.coffeeService.getCart().subscribe();
  }

  updateQuantity(coffeeId: number, quantity: number): void {
    if (quantity <= 0) {
      this.removeItem(coffeeId);
      return;
    }
    this.coffeeService.updateCartItem(coffeeId, quantity).subscribe();
  }

  removeItem(coffeeId: number): void {
    this.coffeeService.removeFromCart(coffeeId).subscribe();
  }

  clearCart(): void {
    this.coffeeService.clearCart().subscribe();
  }

  proceedToCheckout() {
    this.router.navigate(['checkout']);
  }
}
