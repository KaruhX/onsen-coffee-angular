import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class CoffeeService {
  protected readonly http = inject(HttpClient);
  protected readonly apiUrl = '/api';

  getCoffees() {
    return this.http.get(`${this.apiUrl}/coffees`);
  }

  getCoffeeById(coffee_id: number) {
    return this.http.get(`${this.apiUrl}/coffees/${coffee_id}`);
  }
}
