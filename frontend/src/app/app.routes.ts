import { Routes } from '@angular/router';
import { Cart } from './components/cart/cart';
import { Checkout } from './components/checkout/checkout';
import { CoffeeDetails } from './components/coffee-details/coffee-details';
import { Coffees } from './components/coffees/coffees';
import { Home } from './components/home/home';
import { LoginComponent } from './components/login/login';
import { OrdersComponent } from './components/orders/orders';
import { RegisterComponent } from './components/register/register';
import { Users } from './components/users/users';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'coffees', component: Coffees },
  { path: 'users', component: Users },
  { path: 'cart', component: Cart },
  { path: 'checkout', component: Checkout },
  { path: 'coffee-details/:id', component: CoffeeDetails },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'orders', component: OrdersComponent },
];
