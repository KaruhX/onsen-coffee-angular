import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CoffeeService } from '../../services/coffee-service';
import { SupabaseService } from '../../services/supabase.service';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule],
  templateUrl: './checkout.html',
})
export class Checkout implements OnInit {
  private readonly coffeeService = inject(CoffeeService);
  private readonly router = inject(Router);
  private readonly fb = inject(FormBuilder);
  private readonly supabase = inject(SupabaseService);

  readonly cart = this.coffeeService.cart;
  readonly cartTotal = this.coffeeService.cartTotal;
  readonly shippingCost = this.coffeeService.shippingCost;
  readonly orderTotal = this.coffeeService.orderTotal;

  checkoutForm: FormGroup;
  isSubmitting = signal(false);
  orderSuccess = signal(false);
  orderId = signal<number | null>(null);
  errorMessage = signal<string | null>(null);

  constructor() {
    this.checkoutForm = this.fb.group({
      customer_name: ['', [Validators.required, Validators.minLength(3)]],
      customer_email: ['', [Validators.required, Validators.email]],
      customer_phone: ['', [Validators.pattern(/^[0-9+\s-]{9,15}$/)]],
      shipping_address: ['', [Validators.required, Validators.minLength(10)]],
      shipping_city: ['', [Validators.required]],
      shipping_postal_code: ['', [Validators.required, Validators.pattern(/^[0-9]{5}$/)]],
      shipping_country: ['España', [Validators.required]],
      payment_method: ['card', [Validators.required]],
      notes: [''],
    });
  }

  ngOnInit(): void {
    // Verificar si está autenticado
    if (!this.supabase.isAuthenticated) {
      this.router.navigate(['/login'], {
        queryParams: { returnUrl: '/checkout' },
      });
      return;
    }

    this.coffeeService.getCart().subscribe();
  }

  get f() {
    return this.checkoutForm.controls;
  }

  submitOrder(): void {
    if (this.checkoutForm.invalid) {
      Object.keys(this.f).forEach((key) => {
        this.f[key].markAsTouched();
      });
      return;
    }

    if (this.cart().length === 0) {
      this.errorMessage.set('El carrito está vacío');
      return;
    }

    this.isSubmitting.set(true);
    this.errorMessage.set(null);

    const checkoutData = {
      ...this.checkoutForm.value,
      items: this.cart().map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price,
      })),
    };

    this.coffeeService.createOrder(checkoutData).subscribe({
      next: (response) => {
        this.isSubmitting.set(false);
        this.orderSuccess.set(true);
        this.orderId.set(response.order_id);
      },
      error: (err) => {
        this.isSubmitting.set(false);
        this.errorMessage.set(err.error?.error || 'Error al procesar el pedido');
      },
    });
  }
}
