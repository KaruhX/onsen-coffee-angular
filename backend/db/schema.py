# -*- coding: utf-8 -*-
"""
Schema de Base de Datos para Onsen Coffee - E-commerce de Café de Especialidad
Usando Supabase (PostgreSQL) con Supabase Auth

NOTA: Las tablas ya están creadas en Supabase. Este archivo solo sirve como documentación.
No es necesario ejecutar ningún script de creación.

========================================
ESTRUCTURA DE LA BASE DE DATOS ACTUAL
========================================
"""

# Las tablas están creadas en Supabase y se acceden mediante el cliente de Supabase
# ubicado en connection_supabase.py

"""
1. PROFILES - Perfiles de usuario (vinculado con Supabase Auth)
   - id: UUID (PK, FK a auth.users)
   - created_at: TIMESTAMP WITH TIME ZONE
   - updated_at: TIMESTAMP WITH TIME ZONE
   - full_name: TEXT
   - avatar_url: TEXT
   - email: TEXT
   - role: TEXT (customer | admin)
   - phone: TEXT
   - address: JSONB

2. PRODUCTS - Catálogo de cafés
   - id: INTEGER (PK)
   - created_at: TIMESTAMP WITH TIME ZONE
   - updated_at: TIMESTAMP WITH TIME ZONE
   - name: TEXT
   - price: NUMERIC
   - description: TEXT
   - short_description: TEXT
   - origin: TEXT
   - roast: TEXT
   - weight: TEXT
   - process: TEXT
   - altitude: TEXT
   - flavor_notes: ARRAY (TEXT[])
   - image: TEXT
   - slug: TEXT (UNIQUE)
   - category: TEXT
   - featured: BOOLEAN
   - new: BOOLEAN
   - stock: INTEGER
   - rating: INTEGER
   - reviews: INTEGER
   - organic: BOOLEAN
   - old_price: NUMERIC
   - is_active: BOOLEAN
   - reviews_count: INTEGER
   - is_new: BOOLEAN

3. ORDERS - Pedidos de clientes
   - id: INTEGER (PK)
   - created_at: TIMESTAMP WITH TIME ZONE
   - user_id: UUID (FK a profiles)
   - status: TEXT (pending | processing | completed | cancelled)
   - total: NUMERIC
   - shipping_address: JSONB
   - payment_intent: TEXT

4. ORDER_ITEMS - Artículos de cada pedido
   - id: INTEGER (PK)
   - created_at: TIMESTAMP WITH TIME ZONE
   - order_id: INTEGER (FK a orders)
   - product_id: INTEGER (FK a products)
   - quantity: INTEGER
   - price: NUMERIC

5. PRODUCT_REVIEWS - Reseñas de productos
   - id: INTEGER (PK)
   - created_at: TIMESTAMP WITH TIME ZONE
   - product_id: INTEGER (FK a products)
   - user_id: UUID (FK a profiles)
   - rating: INTEGER (1-5)
   - title: TEXT
   - content: TEXT
   - status: TEXT (pending | approved | rejected)

6. CONTACT_MESSAGES - Mensajes de contacto
   - id: INTEGER (PK)
   - created_at: TIMESTAMP WITH TIME ZONE
   - name: TEXT
   - email: TEXT
   - subject: TEXT
   - message: TEXT
   - status: TEXT (new | read | replied | archived)

7. NEWSLETTER_SUBSCRIBERS - Suscriptores del newsletter
   - id: INTEGER (PK)
   - created_at: TIMESTAMP WITH TIME ZONE
   - email: TEXT (UNIQUE)
   - status: TEXT (active | unsubscribed)
   - source: TEXT

========================================
ACCESO A LA BASE DE DATOS
========================================

Para trabajar con estas tablas, usa el cliente de Supabase:

from backend.db.connection_supabase import get_supabase_client

# Cliente público (para operaciones normales)
supabase = get_supabase_client()

# Cliente admin (para operaciones administrativas)
supabase_admin = get_supabase_client(use_service_key=True)

# Ejemplos de uso:
# - Obtener productos: supabase.table('products').select('*').execute()
# - Crear pedido: supabase.table('orders').insert(data).execute()
# - Actualizar perfil: supabase.table('profiles').update(data).eq('id', user_id).execute()
"""

