import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { SupabaseService } from '../../services/supabase.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.html',
})
export class LoginComponent implements OnInit {
  private supabase = inject(SupabaseService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  email = '';
  password = '';
  loading = false;
  errorMessage = '';
  successMessage = '';
  returnUrl = '';

  ngOnInit(): void {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '';
  }

  async onSubmit() {
    if (!this.email || !this.password) {
      this.errorMessage = 'Por favor completa todos los campos';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    try {
      await this.supabase.signIn(this.email, this.password);
      this.successMessage = 'Inicio de sesión exitoso';

      // Redirigir según el rol o returnUrl
      setTimeout(() => {
        if (this.supabase.isAdmin) {
          this.router.navigate(['/admin']);
        } else if (this.returnUrl) {
          this.router.navigate([this.returnUrl]);
        } else {
          this.router.navigate(['/orders']);
        }
      }, 500);
    } catch (error: any) {
      console.error('Error logging in:', error);
      this.errorMessage = error.message || 'Error al iniciar sesión. Verifica tus credenciales.';
    } finally {
      this.loading = false;
    }
  }
}
