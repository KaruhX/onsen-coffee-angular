export interface Coffee {
  id: number;
  name: string;
  origin: string;
  roast: 'claro' | 'medio' | 'oscuro';
  process: string;
  flavor_notes: string;
  description: string;
  price: number;
  weight_grams: number;
  stock: number;
  image_url: string;
  is_active: boolean;
  created_at: string;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  role: 'customer' | 'admin';
  is_active: boolean;
  created_at: string;
}

export interface Order {
  id: number;
  user_id: number;
  status: 'pending' | 'paid' | 'shipped' | 'delivered' | 'cancelled';
  subtotal: number;
  shipping_cost: number;
  total: number;
  shipping_address: string;
  created_at: string;
}

export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
}

export interface CartItem {
  coffeeId: number;
  quantity: number;
  coffee?: Coffee;
}
