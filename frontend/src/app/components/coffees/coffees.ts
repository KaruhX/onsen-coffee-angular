import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { Coffee } from '../../models';
import { CoffeeService } from '../../services/coffee-service';

@Component({
	selector: 'app-coffees',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './coffees.html',
	styleUrl: './coffees.css',
})
export class Coffees implements OnInit {
	protected readonly cs = inject(CoffeeService)
	coffees = signal<Coffee[]>([])
	
	ngOnInit() {
		this.cs.getCoffees().subscribe((data: any) => { this.coffees.set(data) }) 
	}

}
	