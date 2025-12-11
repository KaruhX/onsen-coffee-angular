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
  id?: number;
  user_id?: number;
  status?: 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  subtotal?: number;
  shipping_cost?: number;
  total?: number;
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  shipping_address: string;
  shipping_city?: string;
  shipping_postal_code?: string;
  shipping_country?: string;
  payment_method?: 'card' | 'paypal' | 'transfer' | 'cash_on_delivery';
  payment_status?: 'pending' | 'completed' | 'failed' | 'refunded';
  tracking_number?: string;
  notes?: string;
  estimated_delivery?: string;
  created_at?: string;
  updated_at?: string;
  items?: OrderItem[];
}

export interface OrderItem {
  id?: number;
  order_id?: number;
  product_id: number;
  quantity: number;
  price: number;
  name?: string;
  image_url?: string;
  origin?: string;
}

export interface CartItem {
  coffeeId: number;
  quantity: number;
  coffee?: Coffee;
}

export interface CheckoutData {
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  shipping_address: string;
  shipping_city: string;
  shipping_postal_code: string;
  shipping_country: string;
  payment_method: 'card' | 'paypal' | 'transfer' | 'cash_on_delivery';
  notes: string;
  items: { product_id: number; quantity: number; price: number }[];
}
