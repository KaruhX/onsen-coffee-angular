import { Routes } from '@angular/router';
import { Cart } from './components/cart/cart';
import { Coffees } from './components/coffees/coffees';
import { Users } from './components/users/users';
import { CoffeeDetails } from './components/coffee-details/coffee-details';

export const routes: Routes = [
    {path: 'coffees', component: Coffees},
    {path: 'users', component: Users},
    {path: 'cart', component: Cart},
    {path: 'coffee-details/:id', component: CoffeeDetails},
    {path: '', redirectTo: 'coffees', pathMatch: 'full'}
];
