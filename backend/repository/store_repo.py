"""
Repositorio de datos para Onsen Coffee - Versión Supabase
Usa el cliente Python de Supabase en lugar de psycopg2
"""

from db.connection_supabase import get_supabase_client

def get_client():
    """Obtiene el cliente de Supabase con permisos de service_role"""
    return get_supabase_client(use_service_key=True)

# ============================================
# PRODUCTS / COFFEES
# ============================================

def obtainCoffees():
    client = get_client()
    response = client.table('products').select('*').eq('is_active', True).execute()
    return response.data

def obtainCoffeeById(coffee_id):
    client = get_client()
    response = client.table('products').select('*').eq('id', coffee_id).eq('is_active', True).execute()
    return response.data[0] if response.data else {"error": "Coffee not found"}

def saveNewCoffee(coffee_data):
    """Guarda un nuevo producto con todos los campos"""
    client = get_client()
    
    # Generar slug si no existe
    slug = coffee_data.get('slug')
    if not slug:
        name = coffee_data.get('name', '')
        slug = name.lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    data = {
        'name': coffee_data.get('name'),
        'slug': slug,
        'description': coffee_data.get('description', ''),
        'short_description': coffee_data.get('short_description'),
        'origin': coffee_data.get('origin'),
        'roast': coffee_data.get('roast', 'medio'),
        'process': coffee_data.get('process'),
        'altitude': coffee_data.get('altitude'),
        'flavor_notes': coffee_data.get('flavor_notes'),
        'price': coffee_data.get('price'),
        'old_price': coffee_data.get('old_price'),
        'weight_grams': coffee_data.get('weight_grams', 250),
        'stock': coffee_data.get('stock', 0),
        'category': coffee_data.get('category', 'coffee'),
        'image_url': coffee_data.get('image_url'),
        'featured': coffee_data.get('featured', False),
        'is_new': coffee_data.get('is_new', False),
        'is_active': True
    }
    
    response = client.table('products').insert(data).execute()
    return {"status": "ok", "id": response.data[0]['id']}

def updateCoffee(coffee_data):
    """Actualiza un producto existente"""
    client = get_client()
    coffee_id = coffee_data.get('id')
    
    if not coffee_id:
        return {"error": "ID de producto requerido"}
    
    # Generar slug si no existe
    slug = coffee_data.get('slug')
    if not slug and coffee_data.get('name'):
        name = coffee_data.get('name', '')
        slug = name.lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    data = {}
    if 'name' in coffee_data: data['name'] = coffee_data['name']
    if slug: data['slug'] = slug
    if 'description' in coffee_data: data['description'] = coffee_data['description']
    if 'short_description' in coffee_data: data['short_description'] = coffee_data['short_description']
    if 'origin' in coffee_data: data['origin'] = coffee_data['origin']
    if 'roast' in coffee_data: data['roast'] = coffee_data['roast']
    if 'process' in coffee_data: data['process'] = coffee_data['process']
    if 'altitude' in coffee_data: data['altitude'] = coffee_data['altitude']
    if 'flavor_notes' in coffee_data: data['flavor_notes'] = coffee_data['flavor_notes']
    if 'price' in coffee_data: data['price'] = coffee_data['price']
    if 'old_price' in coffee_data: data['old_price'] = coffee_data['old_price']
    if 'weight_grams' in coffee_data: data['weight_grams'] = coffee_data['weight_grams']
    if 'stock' in coffee_data: data['stock'] = coffee_data['stock']
    if 'category' in coffee_data: data['category'] = coffee_data['category']
    if 'image_url' in coffee_data: data['image_url'] = coffee_data['image_url']
    if 'featured' in coffee_data: data['featured'] = coffee_data['featured']
    if 'is_new' in coffee_data: data['is_new'] = coffee_data['is_new']
    if 'is_active' in coffee_data: data['is_active'] = coffee_data['is_active']
    
    response = client.table('products').update(data).eq('id', coffee_id).execute()
    return {"status": "ok", "updated": len(response.data)}

def deleteCoffee(coffee_id):
    """Desactiva un producto (soft delete)"""
    client = get_client()
    response = client.table('products').update({'is_active': False}).eq('id', coffee_id).execute()
    return {"status": "ok"}

def searchProducts(query, filters=None):
    """Busca productos por texto y filtros"""
    client = get_client()
    
    # Búsqueda básica por nombre o descripción
    response = client.table('products').select('*').eq('is_active', True)
    
    if query:
        # Supabase no soporta LIKE directamente, así que filtramos en Python
        all_products = response.execute().data
        results = [p for p in all_products if 
                   query.lower() in p.get('name', '').lower() or 
                   query.lower() in p.get('description', '').lower()]
        return results
    
    return response.execute().data

def getProductBySlug(slug):
    """Obtiene un producto por su slug"""
    client = get_client()
    response = client.table('products').select('*').eq('slug', slug).eq('is_active', True).execute()
    return response.data[0] if response.data else None

def getFeaturedProducts(limit=6):
    """Obtiene productos destacados"""
    client = get_client()
    response = client.table('products').select('*').eq('is_active', True).eq('featured', True).limit(limit).execute()
    return response.data

def getNewProducts(limit=6):
    """Obtiene productos nuevos"""
    client = get_client()
    response = client.table('products').select('*').eq('is_active', True).eq('is_new', True).limit(limit).execute()
    return response.data

# ============================================
# USERS - Adaptado para Supabase con profiles
# ============================================

def obtainUsers():
    """Obtiene todos los usuarios (perfiles)"""
    client = get_client()
    response = client.table('profiles').select('id, email, full_name, phone, role, created_at, updated_at').execute()
    return response.data

def obtainUserById(user_id):
    """Obtiene un usuario por ID"""
    client = get_client()
    response = client.table('profiles').select('id, email, full_name, phone, role, address, created_at, updated_at').eq('id', user_id).execute()
    return response.data[0] if response.data else {"error": "User not found"}

def updateUserRole(user_id, role):
    """Actualiza el rol de un usuario"""
    client = get_client()
    response = client.table('profiles').update({'role': role, 'updated_at': 'now()'}).eq('id', user_id).execute()
    return {"status": "ok"}

def deleteUser(user_id):
    """Elimina un usuario (esto también elimina el auth.user asociado por la FK)"""
    client = get_client()
    # En Supabase, eliminar el perfil eliminará el usuario de auth por la FK
    response = client.table('profiles').delete().eq('id', user_id).execute()
    return {"status": "ok"}

# ============================================
# ORDERS
# ============================================

# ============================================
# ORDERS - Adaptado para Supabase
# ============================================

def registerOrder(order_data):
    """Registra un nuevo pedido con sus items"""
    client = get_client()
    
    # Validar campos requeridos
    if not order_data.get('items') or len(order_data.get('items', [])) == 0:
        raise ValueError("El pedido debe contener al menos un producto")
    
    # Calcular total desde los items
    items = order_data.get('items', [])
    total = 0
    for item in items:
        price = float(item.get('price', 0))
        quantity = int(item.get('quantity', 1))
        total += price * quantity
    
    # Crear el pedido
    order_insert = {
        'user_id': order_data.get('user_id'),
        'status': 'pending',
        'total': total,
        'shipping_address': order_data.get('shipping_address', {}),
        'payment_intent': order_data.get('payment_intent')
    }
    
    response = client.table('orders').insert(order_insert).execute()
    order_id = response.data[0]['id']
    
    # Insertar items del pedido
    for item in items:
        item_insert = {
            'order_id': order_id,
            'product_id': item.get('product_id'),
            'quantity': item.get('quantity'),
            'price': item.get('price')
        }
        client.table('order_items').insert(item_insert).execute()
    
    return {"status": "ok", "order_id": order_id, "total": total}

def getOrderById(order_id):
    """Obtiene un pedido con sus items y perfil de usuario"""
    client = get_client()
    
    # Obtener el pedido con información del usuario
    order_response = client.table('orders').select('''
        *,
        profiles:user_id (
            id,
            email,
            full_name,
            phone
        )
    ''').eq('id', order_id).execute()
    
    if not order_response.data:
        return {"error": "Order not found"}
    
    order = order_response.data[0]
    
    # Obtener los items del pedido con información del producto
    items_response = client.table('order_items').select('''
        *,
        products (
            id,
            name,
            image,
            slug
        )
    ''').eq('order_id', order_id).execute()
    
    order['items'] = items_response.data
    
    return order

def getAllOrders():
    """Obtiene todos los pedidos con información de usuario e items"""
    client = get_client()
    response = client.table('orders').select('''
        *,
        profiles:user_id (
            id,
            email,
            full_name,
            phone
        )
    ''').order('created_at', desc=True).execute()
    
    # Obtener items para cada pedido
    orders = response.data
    for order in orders:
        items_response = client.table('order_items').select('''
            *,
            products (
                id,
                name,
                image,
                slug
            )
        ''').eq('order_id', order['id']).execute()
        order['items'] = items_response.data
    
    return orders

def obtainOrders(status_filter='all'):
    """Obtiene pedidos con filtro opcional de estado"""
    client = get_client()
    
    query = client.table('orders').select('''
        *,
        profiles:user_id (
            id,
            email,
            full_name,
            phone
        )
    ''')
    
    if status_filter and status_filter != 'all':
        query = query.eq('status', status_filter)
    
    response = query.order('created_at', desc=True).execute()
    
    # Obtener items para cada pedido
    orders = response.data
    for order in orders:
        items_response = client.table('order_items').select('''
            *,
            products (
                id,
                name,
                image,
                slug
            )
        ''').eq('order_id', order['id']).execute()
        order['items'] = items_response.data
    
    return orders

def updateOrderStatus(order_id, status):
    """Actualiza el estado de un pedido"""
    client = get_client()
    response = client.table('orders').update({'status': status}).eq('id', order_id).execute()
    return {"status": "ok"}

def deleteOrder(order_id):
    """Elimina un pedido y sus items (cascade delete en Supabase)"""
    client = get_client()
    # Los items se eliminan automáticamente por la FK con ON DELETE CASCADE
    response = client.table('orders').delete().eq('id', order_id).execute()
    return {"status": "ok"}

# ============================================
# CONTACT MESSAGES
# ============================================

def createContactMessage(data):
    """Crea un mensaje de contacto"""
    client = get_client()
    
    message_data = {
        'name': data.get('name'),
        'email': data.get('email'),
        'subject': data.get('subject'),
        'message': data.get('message'),
        'status': 'new'
    }
    
    response = client.table('contact_messages').insert(message_data).execute()
    return {"status": "ok", "id": response.data[0]['id']}

def getAllContactMessages(status_filter=None):
    """Obtiene todos los mensajes de contacto"""
    client = get_client()
    
    if status_filter:
        response = client.table('contact_messages').select('*').eq('status', status_filter).order('created_at', desc=True).execute()
    else:
        response = client.table('contact_messages').select('*').order('created_at', desc=True).execute()
    
    return response.data

def updateContactMessageStatus(message_id, status):
    """Actualiza el estado de un mensaje de contacto"""
    client = get_client()
    response = client.table('contact_messages').update({'status': status}).eq('id', message_id).execute()
    return {"status": "ok"}

def deleteContactMessage(message_id):
    """Elimina un mensaje de contacto"""
    client = get_client()
    response = client.table('contact_messages').delete().eq('id', message_id).execute()
    return {"status": "ok"}

# ============================================
# PRODUCT REVIEWS
# ============================================

def createProductReview(data):
    """Crea una reseña de producto"""
    client = get_client()
    
    review_data = {
        'product_id': data.get('product_id'),
        'user_id': data.get('user_id'),
        'name': data.get('name'),
        'rating': data.get('rating'),
        'comment': data.get('comment')
    }
    
    response = client.table('product_reviews').insert(review_data).execute()
    
    # Actualizar el rating promedio del producto
    updateProductRating(data.get('product_id'))
    
    return {"status": "ok", "id": response.data[0]['id']}

def getProductReviews(product_id):
    """Obtiene las reseñas de un producto"""
    client = get_client()
    response = client.table('product_reviews').select('*').eq('product_id', product_id).order('created_at', desc=True).execute()
    return response.data

def updateProductRating(product_id):
    """Actualiza el rating promedio y contador de reseñas de un producto"""
    client = get_client()
    
    # Obtener todas las reseñas del producto
    reviews = client.table('product_reviews').select('rating').eq('product_id', product_id).execute()
    
    if not reviews.data:
        # Sin reseñas, establecer rating a 0
        client.table('products').update({'rating': 0, 'reviews_count': 0}).eq('id', product_id).execute()
        return
    
    # Calcular promedio
    total = sum([r['rating'] for r in reviews.data])
    count = len(reviews.data)
    avg_rating = round(total / count, 1)
    
    # Actualizar producto
    client.table('products').update({
        'rating': avg_rating,
        'reviews_count': count
    }).eq('id', product_id).execute()

def deleteProductReview(review_id):
    """Elimina una reseña de producto"""
    client = get_client()
    
    # Obtener el product_id antes de eliminar
    review = client.table('product_reviews').select('product_id').eq('id', review_id).execute()
    
    if review.data:
        product_id = review.data[0]['product_id']
        
        # Eliminar la reseña
        client.table('product_reviews').delete().eq('id', review_id).execute()
        
        # Actualizar rating del producto
        updateProductRating(product_id)
    
    return {"status": "ok"}
