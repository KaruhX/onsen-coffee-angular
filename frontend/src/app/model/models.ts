// ============================================
// PRODUCTOS / CAFÉS
// ============================================

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  short_description?: string;
  origin: string;
  roast: 'claro' | 'medio' | 'oscuro';
  process?: string;
  altitude?: string;
  flavor_notes?: string;
  price: number;
  old_price?: number;
  weight_grams: number;
  stock: number;
  category?: string;
  image_url: string;
  featured?: boolean;
  is_new?: boolean;
  rating?: number;
  reviews_count?: number;
  is_active: boolean;
  created_at: string;
}

// Alias para mantener compatibilidad
export interface Coffee extends Product {}

// ============================================
// USUARIOS
// ============================================

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

// ============================================
// PEDIDOS Y CARRITO
// ============================================

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
  unit_price: number;
  name?: string;
  image_url?: string;
  origin?: string;
}

export interface CartItem extends Product {
  quantity: number; // Propiedades para compatibilidad con código legacy
  coffeeId?: number;
  coffee?: Coffee;
}

// Compatibilidad con código existente
export interface LegacyCartItem {
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

// ============================================
// REVIEWS
// ============================================

export interface Review {
  id: number;
  product_id: number;
  user_id?: number;
  name: string;
  rating: number;
  comment: string;
  created_at: string;
}

// ============================================
// CONTACTO
// ============================================

export type ContactMessageStatus = 'new' | 'read' | 'replied' | 'archived';

export interface ContactMessage {
  id: number;
  name: string;
  email: string;
  subject: string;
  message: string;
  status: ContactMessageStatus;
  created_at: string;
}

export interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface ContactApiResponse {
  success: boolean;
  message?: string;
  data?: ContactMessage | ContactMessage[];
  error?: string;
}
