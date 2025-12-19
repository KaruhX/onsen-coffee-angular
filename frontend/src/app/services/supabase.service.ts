import { Injectable } from '@angular/core';
import { createClient, SupabaseClient, User } from '@supabase/supabase-js';
import { BehaviorSubject } from 'rxjs';

export interface Profile {
  id: string;
  full_name: string | null;
  avatar_url: string | null;
  email: string | null;
  role: 'customer' | 'admin';
  phone: string | null;
  address: any | null;
  created_at?: string;
  updated_at?: string;
}

const SUPABASE_URL = 'https://kvylferkavxxgtsuxlmh.supabase.co';
const SUPABASE_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2eWxmZXJrYXZ4eGd0c3V4bG1oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc3Njk4NzEsImV4cCI6MjA2MzM0NTg3MX0.NWy4ZlzD7SXOxFO3HBNBab1BX_OvoDwDvfv7LGxHfh4';

@Injectable({
  providedIn: 'root',
})
export class SupabaseService {
  private supabase: SupabaseClient;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  private currentProfileSubject = new BehaviorSubject<Profile | null>(null);

  public currentUser$ = this.currentUserSubject.asObservable();
  public currentProfile$ = this.currentProfileSubject.asObservable();

  constructor() {
    this.supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
    this.loadUser();
  }

  private async loadUser() {
    const { data } = await this.supabase.auth.getSession();
    if (data.session?.user) {
      this.currentUserSubject.next(data.session.user);
      await this.loadProfile(data.session.user.id);
    }

    // Escuchar cambios en la autenticación
    this.supabase.auth.onAuthStateChange(async (event, session) => {
      if (session?.user) {
        this.currentUserSubject.next(session.user);
        await this.loadProfile(session.user.id);
      } else {
        this.currentUserSubject.next(null);
        this.currentProfileSubject.next(null);
      }
    });
  }

  private async loadProfile(userId: string) {
    try {
      const { data, error } = await this.supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single();

      if (error) throw error;
      this.currentProfileSubject.next(data as Profile);
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  }

  get user(): User | null {
    return this.currentUserSubject.value;
  }

  get profile(): Profile | null {
    return this.currentProfileSubject.value;
  }

  get isAuthenticated(): boolean {
    return this.currentUserSubject.value !== null;
  }

  get isAdmin(): boolean {
    return this.currentProfileSubject.value?.role === 'admin';
  }

  // Autenticación
  async signUp(email: string, password: string, fullName: string) {
    const { data, error } = await this.supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
        },
      },
    });

    if (error) throw error;

    // Crear perfil si no existe
    if (data.user) {
      await this.createProfile(data.user.id, email, fullName);
    }

    return data;
  }

  async signIn(email: string, password: string) {
    const { data, error } = await this.supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) throw error;
    return data;
  }

  async signOut() {
    const { error } = await this.supabase.auth.signOut();
    if (error) throw error;
  }

  async resetPassword(email: string) {
    const { error } = await this.supabase.auth.resetPasswordForEmail(email);
    if (error) throw error;
  }

  async updatePassword(newPassword: string) {
    const { error } = await this.supabase.auth.updateUser({
      password: newPassword,
    });
    if (error) throw error;
  }

  // Perfiles
  private async createProfile(userId: string, email: string, fullName: string) {
    const { error } = await this.supabase.from('profiles').insert({
      id: userId,
      email,
      full_name: fullName,
      role: 'customer',
    });

    if (error) throw error;
  }

  async updateProfile(updates: Partial<Profile>) {
    if (!this.user) throw new Error('No user logged in');

    const { data, error } = await this.supabase
      .from('profiles')
      .update({
        ...updates,
        updated_at: new Date().toISOString(),
      })
      .eq('id', this.user.id)
      .select()
      .single();

    if (error) throw error;
    this.currentProfileSubject.next(data as Profile);
    return data;
  }

  // Base de datos - Helpers genéricos
  getClient(): SupabaseClient {
    return this.supabase;
  }

  from(table: string) {
    return this.supabase.from(table);
  }

  // Productos
  async getProducts() {
    const { data, error } = await this.supabase
      .from('products')
      .select('*')
      .eq('is_active', true)
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data || [];
  }

  async getProductById(id: number) {
    const { data, error } = await this.supabase.from('products').select('*').eq('id', id).single();

    if (error) throw error;
    return data;
  }

  async getProductBySlug(slug: string) {
    const { data, error } = await this.supabase
      .from('products')
      .select('*')
      .eq('slug', slug)
      .single();

    if (error) throw error;
    return data;
  }

  async getFeaturedProducts() {
    const { data, error } = await this.supabase
      .from('products')
      .select('*')
      .eq('featured', true)
      .eq('is_active', true)
      .limit(6);

    if (error) throw error;
    return data;
  }

  // Pedidos
  async createOrder(orderData: {
    total: number;
    shipping_address: any;
    items: Array<{ product_id: number; quantity: number; price: number }>;
  }) {
    if (!this.user) throw new Error('Must be logged in to create order');

    // Crear pedido
    const { data: order, error: orderError } = await this.supabase
      .from('orders')
      .insert({
        user_id: this.user.id,
        status: 'pending',
        total: orderData.total,
        shipping_address: orderData.shipping_address,
      })
      .select()
      .single();

    if (orderError) throw orderError;

    // Crear items del pedido
    const orderItems = orderData.items.map((item) => ({
      order_id: order.id,
      product_id: item.product_id,
      quantity: item.quantity,
      price: item.price,
    }));

    const { error: itemsError } = await this.supabase.from('order_items').insert(orderItems);

    if (itemsError) throw itemsError;

    return order;
  }

  async getUserOrders() {
    if (!this.user) throw new Error('Must be logged in');

    const { data, error } = await this.supabase
      .from('orders')
      .select(
        `
        *,
        order_items (
          *,
          products (*)
        )
      `
      )
      .eq('user_id', this.user.id)
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  }

  async getAllOrders() {
    if (!this.isAdmin) throw new Error('Admin access required');

    const { data, error } = await this.supabase
      .from('orders')
      .select(
        `
        *,
        profiles (full_name, email),
        order_items (
          *,
          products (name, image)
        )
      `
      )
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  }

  async updateOrderStatus(orderId: number, status: string) {
    if (!this.isAdmin) throw new Error('Admin access required');

    const { data, error } = await this.supabase
      .from('orders')
      .update({ status })
      .eq('id', orderId)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  // Newsletter
  async subscribeNewsletter(email: string, source: string = 'website') {
    const { data, error } = await this.supabase.from('newsletter_subscribers').insert({
      email,
      source,
      status: 'active',
    });

    if (error) {
      if (error.code === '23505') {
        // unique constraint violation
        throw new Error('Email already subscribed');
      }
      throw error;
    }
    return data;
  }

  // Contacto
  async sendContactMessage(messageData: {
    name: string;
    email: string;
    subject: string;
    message: string;
  }) {
    const { data, error } = await this.supabase.from('contact_messages').insert({
      ...messageData,
      status: 'new',
    });

    if (error) throw error;
    return data;
  }

  // Reviews
  async createReview(productId: number, rating: number, title: string, content: string) {
    if (!this.user) throw new Error('Must be logged in to review');

    const { data, error } = await this.supabase.from('product_reviews').insert({
      product_id: productId,
      user_id: this.user.id,
      rating,
      title,
      content,
      status: 'pending',
    });

    if (error) throw error;
    return data;
  }

  async getProductReviews(productId: number) {
    const { data, error } = await this.supabase
      .from('product_reviews')
      .select(
        `
        *,
        profiles (full_name, avatar_url)
      `
      )
      .eq('product_id', productId)
      .eq('status', 'approved')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  }
}
