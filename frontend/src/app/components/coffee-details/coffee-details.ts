import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Coffee } from '../../models';
import { CoffeeService } from '../../services/coffee-service';

@Component({
  selector: 'app-coffee-details',
  imports: [CommonModule],
  templateUrl: './coffee-details.html',
})
export class CoffeeDetails implements OnInit {
  protected readonly activatedRoute = inject(ActivatedRoute);
  protected readonly coffeeService = inject(CoffeeService);
  protected readonly coffee = signal<Coffee | null>(null);
  protected coffee_id = -1;
  
  ngOnInit() {
    // Fetch coffee details using coffee_id
    this.coffee_id = Number(this.activatedRoute.snapshot.paramMap.get('id'));
    console.log('Coffee ID:', this.coffee_id);
    this.coffeeService.getCoffeeById(this.coffee_id).subscribe((data: any) => {
      this.coffee.set(data);
      console.log('Coffee Details:', data);
    });
  }
}
