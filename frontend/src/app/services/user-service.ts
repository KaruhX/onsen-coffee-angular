import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  protected readonly http = inject(HttpClient);
  protected readonly apiUrl = '/api';

  getUsers() {
    return this.http.get(`${this.apiUrl}/users`);
  }
}
