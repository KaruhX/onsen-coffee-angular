from flask import Blueprint, jsonify, session, request
import sys
from pathlib import Path

# Agregar backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import repository.store_repo as repo

api = Blueprint('api', __name__)

def register_routes(app):
    app.register_blueprint(api, url_prefix='/api')

@api.route("/")
def init_rest():
    return jsonify({"status": "ok", "message": "Onsen Coffee API - Supabase Edition"})

# ============ PRODUCTS ENDPOINTS ============

@api.route("/coffees")
def obtainCoffees():
    return jsonify(repo.obtainCoffees())

@api.route("/coffees/<int:coffee_id>")
def obtainCoffeeById(coffee_id):
    return jsonify(repo.obtainCoffeeById(coffee_id))

@api.route("/products/search", methods=["GET"])
def searchProducts():
    try:
        query = request.args.get('q')
        category = request.args.get('category')
        roast = request.args.get('roast')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        featured = request.args.get('featured', type=lambda x: x.lower() == 'true')
        is_new = request.args.get('new', type=lambda x: x.lower() == 'true')
        
        products = repo.searchProducts(
            query=query,
            category=category,
            roast=roast,
            min_price=min_price,
            max_price=max_price,
            featured=featured,
            is_new=is_new
        )
        
        return jsonify({
            "success": True,
            "data": products,
            "count": len(products)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/products/slug/<slug>")
def getProductBySlug(slug):
    try:
        product = repo.getProductBySlug(slug)
        if not product:
            return jsonify({"success": False, "error": "Producto no encontrado"}), 404
        return jsonify({"success": True, "data": product})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/products/featured")
def getFeaturedProducts():
    try:
        products = repo.searchProducts(featured=True)
        return jsonify({"success": True, "data": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/products/new")
def getNewProducts():
    try:
        products = repo.searchProducts(is_new=True)
        return jsonify({"success": True, "data": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============ CART ENDPOINTS ============

@api.route("/cart", methods=["GET"])
def getCart():
    cart = session.get('cart', [])
    if not isinstance(cart, list):
        cart = []
        session['cart'] = cart
    
    # Enriquecer el carrito con datos de productos
    enriched_cart = []
    for item in cart:
        coffee_id = item.get('coffeeId')
        if coffee_id:
            coffee = repo.obtainCoffeeById(coffee_id)
            if coffee and not coffee.get('error'):
                enriched_item = {
                    'id': coffee.get('id'),
                    'name': coffee.get('name', 'Producto sin nombre'),
                    'price': coffee.get('price', 0),
                    'image_url': coffee.get('image_url'),
                    'origin': coffee.get('origin', 'Origen desconocido'),
                    'quantity': item.get('quantity', 1)
                }
                enriched_cart.append(enriched_item)
    
    return jsonify(enriched_cart)

@api.route("/cart", methods=["POST"])
def addToCart():
    cart = session.get('cart', [])
    if not isinstance(cart, list):
        cart = []

    data = request.get_json()
    coffee_id = data.get("coffeeId")
    quantity = data.get("quantity", 1)

    found = False
    for item in cart:
        if item.get('coffeeId') == coffee_id:
            item['quantity'] += quantity
            found = True
            break
    
    if not found:
        cart.append({'coffeeId': coffee_id, 'quantity': quantity})

    session['cart'] = cart
    
    # Devolver carrito enriquecido
    enriched_cart = []
    for item in cart:
        cid = item.get('coffeeId')
        if cid:
            coffee = repo.obtainCoffeeById(cid)
            if coffee and not coffee.get('error'):
                enriched_item = {
                    'id': coffee.get('id'),
                    'name': coffee.get('name', 'Producto sin nombre'),
                    'price': coffee.get('price', 0),
                    'image_url': coffee.get('image_url'),
                    'origin': coffee.get('origin', 'Origen desconocido'),
                    'quantity': item.get('quantity', 1)
                }
                enriched_cart.append(enriched_item)
    
    return jsonify({"status": "ok", "cart": enriched_cart})

@api.route("/cart/<int:coffee_id>", methods=["PUT"])
def updateCartItem(coffee_id):
    cart = session.get('cart', [])
    if not isinstance(cart, list):
        cart = []

    data = request.get_json()
    quantity = data.get("quantity", 1)

    for item in cart:
        if item.get('coffeeId') == coffee_id:
            item['quantity'] = quantity
            break

    session['cart'] = cart
    
    # Devolver carrito enriquecido
    enriched_cart = []
    for item in cart:
        cid = item.get('coffeeId')
        if cid:
            coffee = repo.obtainCoffeeById(cid)
            if coffee and not coffee.get('error'):
                enriched_item = {
                    'id': coffee.get('id'),
                    'name': coffee.get('name', 'Producto sin nombre'),
                    'price': coffee.get('price', 0),
                    'image_url': coffee.get('image_url'),
                    'origin': coffee.get('origin', 'Origen desconocido'),
                    'quantity': item.get('quantity', 1)
                }
                enriched_cart.append(enriched_item)
    
    return jsonify({"status": "ok", "cart": enriched_cart})

@api.route("/cart/<int:coffee_id>", methods=["DELETE"])
def removeFromCart(coffee_id):
    cart = session.get('cart', [])
    if not isinstance(cart, list):
        cart = []
    cart = [item for item in cart if item.get('coffeeId') != coffee_id]
    session['cart'] = cart
    
    # Devolver carrito enriquecido
    enriched_cart = []
    for item in cart:
        cid = item.get('coffeeId')
        if cid:
            coffee = repo.obtainCoffeeById(cid)
            if coffee and not coffee.get('error'):
                enriched_item = {
                    'id': coffee.get('id'),
                    'name': coffee.get('name', 'Producto sin nombre'),
                    'price': coffee.get('price', 0),
                    'image_url': coffee.get('image_url'),
                    'origin': coffee.get('origin', 'Origen desconocido'),
                    'quantity': item.get('quantity', 1)
                }
                enriched_cart.append(enriched_item)
    
    return jsonify({"status": "ok", "cart": enriched_cart})

@api.route("/cart", methods=["DELETE"])
def clearCart():
    session['cart'] = []
    return jsonify({"status": "ok", "cart": []})

# ============ ORDERS ENDPOINTS ============

@api.route("/orders", methods=["POST"])
def createOrder():
    try:
        data = request.get_json()
        required_fields = ['customer_name', 'customer_email', 'shipping_address', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"El campo {field} es requerido"}), 400
        
        if not data.get('items') or len(data.get('items', [])) == 0:
            return jsonify({"error": "El carrito está vacío"}), 400
        
        result = repo.registerOrder(data)
        session['cart'] = []
        return jsonify(result)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error al procesar pedido: {str(e)}"}), 500

@api.route("/orders/<int:order_id>")
def getOrder(order_id):
    order = repo.getOrderById(order_id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    return jsonify(order)

@api.route("/orders/by-email/<email>")
def getOrdersByEmail(email):
    orders = repo.getOrdersByEmail(email)
    return jsonify(orders)

@api.route("/orders")
def getAllOrders():
    orders = repo.getAllOrders()
    return jsonify(orders)

@api.route("/orders/<int:order_id>/status", methods=["PUT"])
def updateOrderStatus(order_id):
    data = request.get_json()
    status = data.get('status')
    tracking_number = data.get('tracking_number')
    
    valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
    if status not in valid_statuses:
        return jsonify({"error": f"Estado no válido"}), 400
    
    result = repo.updateOrderStatus(order_id, status, tracking_number)
    return jsonify(result)

# ============ CONTACT MESSAGES ============

@api.route("/contact", methods=["POST"])
def createContactMessage():
    try:
        data = request.get_json()
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"El campo {field} es requerido"}), 400
        
        result = repo.createContactMessage(data)
        return jsonify({
            "success": True,
            "message": "Mensaje enviado correctamente. Te responderemos pronto.",
            "data": result
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/contact", methods=["GET"])
def getAllContactMessages():
    try:
        status = request.args.get('status')
        messages = repo.getAllContactMessages(status)
        return jsonify({"success": True, "data": messages})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/contact/<int:message_id>")
def getContactMessage(message_id):
    try:
        message = repo.getContactMessageById(message_id)
        if not message:
            return jsonify({"success": False, "error": "Mensaje no encontrado"}), 404
        return jsonify({"success": True, "data": message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/contact/<int:message_id>/status", methods=["PUT"])
def updateContactMessageStatus(message_id):
    try:
        data = request.get_json()
        status = data.get('status')
        valid_statuses = ['new', 'read', 'replied', 'archived']
        if status not in valid_statuses:
            return jsonify({"success": False, "error": "Estado no válido"}), 400
        
        result = repo.updateContactMessageStatus(message_id, status)
        if not result:
            return jsonify({"success": False, "error": "Mensaje no encontrado"}), 404
        
        return jsonify({"success": True, "message": "Estado actualizado", "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============ REVIEWS ============

@api.route("/products/<int:product_id>/reviews", methods=["GET"])
def getProductReviews(product_id):
    try:
        reviews = repo.getProductReviews(product_id)
        return jsonify({"success": True, "data": reviews})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api.route("/products/<int:product_id>/reviews", methods=["POST"])
def createProductReview(product_id):
    try:
        data = request.get_json()
        data['product_id'] = product_id
        required_fields = ['name', 'rating', 'comment']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"El campo {field} es requerido"}), 400
        
        try:
            rating = int(data.get('rating'))
            if rating < 1 or rating > 5:
                raise ValueError()
        except:
            return jsonify({"success": False, "error": "El rating debe ser un número entre 1 y 5"}), 400
        
        result = repo.createProductReview(data)
        if 'error' in result:
            return jsonify({"success": False, "error": result['error']}), 400
        
        return jsonify({"success": True, "message": "Review creada exitosamente", "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============ USERS ============

@api.route("/users")
def obtainUsers():
    return jsonify(repo.obtainUsers())

