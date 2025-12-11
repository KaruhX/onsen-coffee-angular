import { CommonModule, TitleCasePipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Coffee } from '../../model/models';
import { CoffeeService } from '../../services/coffee-service';

@Component({
  selector: 'app-coffees',
  standalone: true,
  imports: [CommonModule, TitleCasePipe],
  templateUrl: './coffees.html',
})
export class Coffees implements OnInit {
  protected readonly router = inject(Router);
  protected readonly cs = inject(CoffeeService);
  coffees = signal<Coffee[]>([]);

  private defaultImages = [
    'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=80',
    'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80',
    'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&q=80',
    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80',
    'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80',
    'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=800&q=80',
  ];

  getDefaultImage(index: number): string {
    return this.defaultImages[index % this.defaultImages.length];
  }

  seeDetails(c: Coffee) {
    this.router.navigate(['/coffee-details', c.id]);
  }

  ngOnInit() {
    this.cs.getCoffees().subscribe((data: any) => {
      this.coffees.set(data);
    });
  }
}
