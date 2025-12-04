import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { Coffee } from '../../models';
import { CoffeeService } from '../../services/coffee-service';
import { Router } from '@angular/router';

@Component({
	selector: 'app-coffees',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './coffees.html',
})
export class Coffees implements OnInit {
	protected readonly router = inject(Router)
	protected readonly cs = inject(CoffeeService)
	coffees = signal<Coffee[]>([])

	seeDetails(c: Coffee) {
		this.router.navigate(['/coffee-details', c.id])		
	}
	
	ngOnInit() {
		this.cs.getCoffees().subscribe((data: any) => { this.coffees.set(data) }) 
	}

}
	