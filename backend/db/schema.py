# -*- coding: utf-8 -*-
"""
Schema de Base de Datos para Onsen Coffee - E-commerce de Café de Especialidad
"""

import os
import sqlite3
import tempfile

# Ruta en /tmp para funcionar en entornos serverless de solo lectura
DB_PATH = os.path.join(tempfile.gettempdir(), 'onsen-coffee.db')

def get_connection():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    """Crea las 6 tablas principales del e-commerce"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. USUARIOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            role VARCHAR(20) DEFAULT 'customer' CHECK(role IN ('customer', 'admin')),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. PRODUCTOS (Cafés)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            origin VARCHAR(100),
            roast VARCHAR(50) CHECK(roast IN ('claro', 'medio', 'oscuro')),
            process VARCHAR(50),
            flavor_notes TEXT,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            weight_grams INTEGER DEFAULT 250,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. PEDIDOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    ''')
    
    # 4. ITEMS DEL PEDIDO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Índices
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)')
    
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
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users (email, password_hash, first_name, last_name, phone, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users)
    
    # Productos de ejemplo
    products = [
        ('Ethiopian Yirgacheffe', 'Etiopía', 'medio', 'Lavado', 'Floral, cítrico, bergamota', 'Café de especialidad con notas brillantes', 32.99, 250, 50, 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=80'),
        ('Colombian Geisha', 'Colombia', 'claro', 'Honey', 'Jazmín, durazno, miel', 'Geisha excepcional de finca de altura', 45.00, 250, 30, 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80'),
        ('Kenyan AA', 'Kenia', 'medio', 'Lavado', 'Grosella, tomate, vino', 'Acidez vibrante y compleja', 38.50, 250, 40, 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&q=80'),
        ('Sumatra Mandheling', 'Indonesia', 'oscuro', 'Wet-hulled', 'Chocolate, terroso, especias', 'Cuerpo intenso y notas profundas', 34.99, 250, 45, 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&q=80'),
        ('Costa Rica Tarrazú', 'Costa Rica', 'medio', 'Lavado', 'Manzana verde, caramelo, nuez', 'Balance perfecto y dulzura natural', 36.00, 250, 35, 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80'),
        ('Guatemala Antigua', 'Guatemala', 'medio', 'Lavado', 'Chocolate, nuez, cítrico', 'Cuerpo completo con final dulce', 33.50, 250, 60, 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=800&q=80'),
        ('Brazil Santos', 'Brasil', 'oscuro', 'Natural', 'Nuez, chocolate, bajo en acidez', 'Suave y equilibrado para espresso', 30.00, 250, 80, 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=80'),
        ('Panama Geisha', 'Panamá', 'claro', 'Lavado', 'Jazmín, bergamota, tropical', 'El café más exclusivo del mundo', 49.99, 250, 15, 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&q=80')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO products (name, origin, roast, process, flavor_notes, description, price, weight_grams, stock, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Pedidos de ejemplo
    orders = [
        (2, 'delivered', 599.00, 99.00, 698.00, 'Av. Reforma 123, CDMX, CP 06600'),
        (2, 'shipped', 450.00, 99.00, 549.00, 'Av. Reforma 123, CDMX, CP 06600'),
        (3, 'paid', 920.00, 0.00, 920.00, 'Calle Juárez 456, Guadalajara, CP 44100'),
        (4, 'pending', 285.00, 99.00, 384.00, 'Blvd. Independencia 789, Monterrey, CP 64000'),
        (5, 'delivered', 1780.00, 0.00, 1780.00, 'Calle 5 de Mayo 321, Puebla, CP 72000'),
        (3, 'cancelled', 320.00, 99.00, 419.00, 'Calle Juárez 456, Guadalajara, CP 44100')
    ]
    
    # No insertamos órdenes de ejemplo, solo clientes y productos
    # Los pedidos se crean a través del flujo de checkout
    
    conn.commit()
    conn.close()
    print("✅ Datos de ejemplo insertados!")

if __name__ == '__main__':
    create_tables()
    insert_seed_data()

