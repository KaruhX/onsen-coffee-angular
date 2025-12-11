import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Coffee } from '../../model/models';
import { CoffeeService } from '../../services/coffee-service';

@Component({
  selector: 'app-coffee-details',
  imports: [CommonModule, RouterLink],
  templateUrl: './coffee-details.html',
})
export class CoffeeDetails implements OnInit {
  protected readonly activatedRoute = inject(ActivatedRoute);
  protected readonly coffeeService = inject(CoffeeService);
  protected readonly coffee = signal<Coffee | null>(null);
  protected coffee_id = -1;

  private defaultImages = [
    'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=80',
    'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80',
    'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&q=80',
    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80',
    'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80',
    'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=800&q=80',
  ];

  getDefaultImage(): string {
    return this.defaultImages[this.coffee_id % this.defaultImages.length];
  }

  protected addToCart(coffeeId: number) {
    this.coffeeService.addToCart(coffeeId, 1).subscribe(() => {
      console.log(`Coffee with ID ${coffeeId} added to cart.`);
    });
  }

  ngOnInit() {
    this.coffee_id = Number(this.activatedRoute.snapshot.paramMap.get('id'));
    console.log('Coffee ID:', this.coffee_id);
    this.coffeeService.getCoffeeById(this.coffee_id).subscribe((data: any) => {
      this.coffee.set(data);
      console.log('Coffee Details:', data);
    });
  }
}
