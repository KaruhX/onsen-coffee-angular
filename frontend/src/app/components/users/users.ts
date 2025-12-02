import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { UserService } from '../../services/user-service';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './users.html',
  styleUrl: './users.css',
})
export class Users implements OnInit {
  protected readonly us = inject(UserService);
  users = signal<any[]>([]);

  ngOnInit() {
    this.us.getUsers().subscribe((data: any) => {
      this.users.set(data);
    });
  }
}
