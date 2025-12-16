# -*- coding: utf-8 -*-
"""
Schema de Base de Datos para Onsen Coffee - E-commerce de Café de Especialidad
Usando Supabase (PostgreSQL)
"""

from .connection_supabase import get_db_connection

def get_connection():
    """Obtiene conexión a la base de datos de Supabase"""
    return get_db_connection()

def create_tables():
    """Crea las 6 tablas principales del e-commerce en PostgreSQL/Supabase"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. USUARIOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            role VARCHAR(20) DEFAULT 'customer' CHECK(role IN ('customer', 'admin')),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. PRODUCTOS (Cafés)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(255) UNIQUE NOT NULL,
            description TEXT,
            short_description TEXT,
            origin VARCHAR(100),
            roast VARCHAR(50) CHECK(roast IN ('claro', 'medio', 'oscuro')),
            process VARCHAR(50),
            altitude VARCHAR(50),
            flavor_notes TEXT,
            price DECIMAL(10,2) NOT NULL,
            old_price DECIMAL(10,2),
            weight_grams INTEGER DEFAULT 250,
            stock INTEGER DEFAULT 0,
            category VARCHAR(50) DEFAULT 'coffee',
            image_url TEXT,
            featured BOOLEAN DEFAULT FALSE,
            is_new BOOLEAN DEFAULT FALSE,
            rating DECIMAL(3,2) DEFAULT 0.0,
            reviews_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. PEDIDOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status VARCHAR(30) DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
            subtotal DECIMAL(10,2) NOT NULL,
            shipping_cost DECIMAL(10,2) DEFAULT 4.99,
            total DECIMAL(10,2) NOT NULL,
            customer_name VARCHAR(200) NOT NULL,
            customer_email VARCHAR(255) NOT NULL,
            customer_phone VARCHAR(30),
            shipping_address TEXT NOT NULL,
            shipping_city VARCHAR(100),
            shipping_postal_code VARCHAR(20),
            shipping_country VARCHAR(100) DEFAULT 'España',
            payment_method VARCHAR(50) DEFAULT 'card' CHECK(payment_method IN ('card', 'paypal', 'transfer', 'cash_on_delivery')),
            payment_status VARCHAR(30) DEFAULT 'pending' CHECK(payment_status IN ('pending', 'completed', 'failed', 'refunded')),
            tracking_number VARCHAR(100),
            notes TEXT,
            estimated_delivery DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 4. ITEMS DEL PEDIDO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL
        )
    ''')
    
    # 5. MENSAJES DE CONTACTO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            email VARCHAR(255) NOT NULL,
            subject VARCHAR(300) NOT NULL,
            message TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'new' CHECK(status IN ('new', 'read', 'replied', 'archived')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 6. REVIEWS DE PRODUCTOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_reviews (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            name VARCHAR(200) NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Índices
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_contact_status ON contact_messages(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reviews_product ON product_reviews(product_id)')
    
    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente!")

def insert_seed_data():
    """Inserta datos de ejemplo"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Usuarios de ejemplo
    users = [
        ('admin@onsencoffee.com', 'hashed_admin123', 'Carlos', 'Mendoza', '5551234567', 'admin'),
        ('maria@example.com', 'hashed_pass123', 'María', 'García', '5559876543', 'customer'),
        ('juan@example.com', 'hashed_pass456', 'Juan', 'López', '5554567890', 'customer'),
        ('ana@example.com', 'hashed_pass789', 'Ana', 'Martínez', '5553216549', 'customer'),
        ('pedro@example.com', 'hashed_pass321', 'Pedro', 'Sánchez', '5557894561', 'customer')
    ]
    
    for user in users:
        cursor.execute('''
            INSERT INTO users (email, password_hash, first_name, last_name, phone, role)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        ''', user)
    
    # Productos de ejemplo con nuevos campos
    products = [
        ('Ethiopian Yirgacheffe', 'ethiopian-yirgacheffe', 'Café de especialidad con notas brillantes y cuerpo ligero', 'Notas florales y cítricas', 'Etiopía', 'medio', 'Lavado', '1800-2000m', 'Floral, cítrico, bergamota, té negro', 32.99, None, 250, 50, 'coffee', 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=80', True, False, 4.5, 28),
        ('Colombian Geisha', 'colombian-geisha', 'Geisha excepcional de finca de altura con perfil único', 'Variedad Geisha premium', 'Colombia', 'claro', 'Honey', '1600-1900m', 'Jazmín, durazno, miel, floral', 45.00, 52.00, 250, 30, 'coffee', 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80', True, True, 4.8, 42),
        ('Kenyan AA', 'kenyan-aa', 'Acidez vibrante y compleja con notas frutales intensas', 'Grado AA de Kenia', 'Kenia', 'medio', 'Lavado', '1500-2100m', 'Grosella, tomate, vino tinto, cítricos', 38.50, None, 250, 40, 'coffee', 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&q=80', True, False, 4.6, 35),
        ('Sumatra Mandheling', 'sumatra-mandheling', 'Cuerpo intenso y notas profundas con baja acidez', 'Proceso húmedo descascarado', 'Indonesia', 'oscuro', 'Wet-hulled', '1100-1500m', 'Chocolate oscuro, terroso, especias, hierbas', 34.99, None, 250, 45, 'coffee', 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80', False, False, 4.3, 22),
        ('Costa Rica Tarrazú', 'costa-rica-tarrazu', 'Balance perfecto y dulzura natural del Valle Central', 'Región Tarrazú premium', 'Costa Rica', 'medio', 'Lavado', '1200-1700m', 'Manzana verde, caramelo, nuez, miel', 36.00, None, 250, 35, 'coffee', 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80', False, True, 4.4, 19),
        ('Guatemala Antigua', 'guatemala-antigua', 'Cuerpo completo con final dulce y notas achocolatadas', 'Antigua clásico', 'Guatemala', 'medio', 'Lavado', '1500-1800m', 'Chocolate con leche, nuez, cítrico suave', 33.50, None, 250, 60, 'coffee', 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=800&q=80', False, False, 4.2, 31),
        ('Brazil Santos', 'brazil-santos', 'Suave y equilibrado, ideal para espresso', 'Proceso natural brasileño', 'Brasil', 'oscuro', 'Natural', '900-1200m', 'Nuez, chocolate, caramelo, baja acidez', 30.00, 34.00, 250, 80, 'coffee', 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=80', False, False, 4.1, 45),
        ('Panama Geisha', 'panama-geisha', 'El café más exclusivo del mundo con perfil excepcional', 'Geisha de Panamá', 'Panamá', 'claro', 'Lavado', '1600-2000m', 'Jazmín, bergamota, tropical, mango', 49.99, None, 250, 15, 'coffee', 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80', True, True, 4.9, 67)
    ]
    
    for product in products:
        cursor.execute('''
            INSERT INTO products (name, slug, description, short_description, origin, roast, process, altitude, 
                                flavor_notes, price, old_price, weight_grams, stock, category, image_url, 
                                featured, is_new, rating, reviews_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO NOTHING
        ''', product)
    
    # Pedidos de ejemplo para testing (siempre se crean en cada despliegue)
    # Limpiamos pedidos anteriores para evitar duplicados
    cursor.execute('DELETE FROM order_items')
    cursor.execute('DELETE FROM orders')
    
    # Pedido 1: María - 2x Ethiopian Yirgacheffe
    cursor.execute('''
        INSERT INTO orders (user_id, status, subtotal, shipping_cost, total, customer_name, 
                           customer_email, customer_phone, shipping_address, shipping_city,
                           shipping_postal_code, shipping_country)
        VALUES (NULL, 'pending', 65.98, 4.99, 70.97, 'María García', 'maria@gmail.com', 
                '+34 611 222 333', 'Avenida Principal 45', 'Barcelona', '08001', 'España')
        RETURNING id
    ''')
    order_id = cursor.fetchone()['id']
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 1, 2, 32.99)', (order_id,))
    
    # Pedido 2: Carlos - 3x Colombian Geisha + 1x Kenyan AA
    cursor.execute('''
        INSERT INTO orders (user_id, status, subtotal, shipping_cost, total, customer_name, 
                           customer_email, customer_phone, shipping_address, shipping_city,
                           shipping_postal_code, shipping_country)
        VALUES (NULL, 'processing', 173.50, 4.99, 178.49, 'Carlos Ruiz', 'carlos@outlook.com',
                '+34 622 333 444', 'Plaza Mayor 12', 'Valencia', '46001', 'España')
        RETURNING id
    ''')
    order_id = cursor.fetchone()['id']
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 2, 3, 45.00)', (order_id,))
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 3, 1, 38.50)', (order_id,))
    
    # Pedido 3: Ana - 1x Ethiopian Yirgacheffe
    cursor.execute('''
        INSERT INTO orders (user_id, status, subtotal, shipping_cost, total, customer_name, 
                           customer_email, customer_phone, shipping_address, shipping_city,
                           shipping_postal_code, shipping_country)
        VALUES (NULL, 'delivered', 32.99, 4.99, 37.98, 'Ana Martínez', 'ana@yahoo.com',
                '+34 633 444 555', 'Calle Sol 78', 'Sevilla', '41001', 'España')
        RETURNING id
    ''')
    order_id = cursor.fetchone()['id']
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 1, 1, 32.99)', (order_id,))
    
    # Pedido 4: Juan - Colombian Geisha + Costa Rica + Sumatra
    cursor.execute('''
        INSERT INTO orders (user_id, status, subtotal, shipping_cost, total, customer_name, 
                           customer_email, customer_phone, shipping_address, shipping_city,
                           shipping_postal_code, shipping_country)
        VALUES (NULL, 'pending', 115.99, 4.99, 120.98, 'Juan Pérez', 'juan@test.com',
                '+34 644 555 666', 'Gran Vía 234', 'Madrid', '28001', 'España')
        RETURNING id
    ''')
    order_id = cursor.fetchone()['id']
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 2, 1, 45.00)', (order_id,))
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 5, 1, 36.00)', (order_id,))
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 4, 1, 34.99)', (order_id,))
    
    # Pedido 5: Laura - Mix de cafés
    cursor.execute('''
        INSERT INTO orders (user_id, status, subtotal, shipping_cost, total, customer_name, 
                           customer_email, customer_phone, shipping_address, shipping_city,
                           shipping_postal_code, shipping_country)
        VALUES (NULL, 'shipped', 142.48, 0.00, 142.48, 'Laura Fernández', 'laura@example.com',
                '+34 655 777 888', 'Paseo de Gracia 89', 'Barcelona', '08007', 'España')
        RETURNING id
    ''')
    order_id = cursor.fetchone()['id']
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 3, 2, 38.50)', (order_id,))
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 6, 2, 33.50)', (order_id,))
    
    # Pedido 6: Miguel - Pedido grande
    cursor.execute('''
        INSERT INTO orders (user_id, status, subtotal, shipping_cost, total, customer_name, 
                           customer_email, customer_phone, shipping_address, shipping_city,
                           shipping_postal_code, shipping_country)
        VALUES (NULL, 'delivered', 269.94, 0.00, 269.94, 'Miguel Torres', 'miguel@company.com',
                '+34 666 888 999', 'Calle Mayor 156', 'Málaga', '29015', 'España')
        RETURNING id
    ''')
    order_id = cursor.fetchone()['id']
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 1, 3, 32.99)', (order_id,))
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 4, 2, 34.99)', (order_id,))
    cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, 7, 3, 30.00)', (order_id,))
    
    conn.commit()
    conn.close()
    print("✅ Datos de ejemplo insertados!")

if __name__ == '__main__':
    create_tables()
    insert_seed_data()

