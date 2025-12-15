from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import os
from dotenv import load_dotenv
from prisma import Prisma
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

db = Prisma()

@app.before_request
async def before_request():
    if not db.is_connected():
        await db.connect()

@app.teardown_appcontext
async def teardown_db(exception=None):
    if db.is_connected():
        await db.disconnect()

# ========== RUTA PRINCIPAL ==========
@app.route('/admin')
def admin_dashboard():
    return render_template('dashboard.html')

# ========== RUTAS DE PEDIDOS ==========

@app.route('/admin/api/orders', methods=['GET'])
async def get_orders():
    try:
        status_filter = request.args.get('status', 'all')
        
        if status_filter == 'all':
            orders = await db.order.find_many(
                include={'items': {'include': {'product': True}}},
                order={'createdAt': 'desc'}
            )
        else:
            orders = await db.order.find_many(
                where={'status': status_filter},
                include={'items': {'include': {'product': True}}},
                order={'createdAt': 'desc'}
            )
        
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                'id': order.id,
                'customerName': order.customerName,
                'customerEmail': order.customerEmail,
                'total': float(order.total),
                'status': order.status,
                'createdAt': order.createdAt.isoformat(),
                'items': [
                    {
                        'name': item.product.name,
                        'quantity': item.quantity,
                        'price': float(item.price)
                    }
                    for item in order.items
                ]
            })
        
        return jsonify(formatted_orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/orders/<order_id>', methods=['PATCH'])
async def update_order(order_id):
    try:
        data = request.get_json()
        status = data.get('status')
        
        await db.order.update(
            where={'id': order_id},
            data={'status': status}
        )
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/orders/<order_id>', methods=['DELETE'])
async def delete_order(order_id):
    try:
        await db.order.delete(where={'id': order_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== RUTAS DE USUARIOS ==========

@app.route('/admin/api/users', methods=['GET'])
async def get_users():
    try:
        users = await db.user.find_many(order={'createdAt': 'desc'})
        
        formatted_users = [
            {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'createdAt': user.createdAt.isoformat()
            }
            for user in users
        ]
        
        return jsonify(formatted_users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/users/<user_id>', methods=['PATCH'])
async def update_user(user_id):
    try:
        data = request.get_json()
        role = data.get('role')
        
        await db.user.update(
            where={'id': user_id},
            data={'role': role}
        )
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/users/<user_id>', methods=['DELETE'])
async def delete_user(user_id):
    try:
        await db.user.delete(where={'id': user_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== RUTAS DE PRODUCTOS (COFFEES) ==========

@app.route('/admin/api/coffees', methods=['GET'])
async def get_coffees():
    try:
        coffees = await db.coffee.find_many(order={'createdAt': 'desc'})
        
        formatted_coffees = [
            {
                'id': coffee.id,
                'name': coffee.name,
                'origin': coffee.origin,
                'roast': coffee.roast,
                'process': coffee.process,
                'flavor_notes': coffee.flavor_notes,
                'description': coffee.description,
                'price': float(coffee.price),
                'weight_grams': coffee.weight_grams,
                'stock': coffee.stock,
                'image_url': coffee.image_url,
                'is_active': coffee.is_active,
                'createdAt': coffee.createdAt.isoformat()
            }
            for coffee in coffees
        ]
        
        return jsonify(formatted_coffees)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/coffees')
async def admin_coffees():
    try:
        coffees = await db.coffee.find_many(order={'createdAt': 'desc'})
        return render_template('index-admin.html', coffees=coffees)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/register-coffee')
def register_coffee():
    available_images = [
        {'name': 'Café 1', 'url': '/static/images/coffee1.jpg'},
        {'name': 'Café 2', 'url': '/static/images/coffee2.jpg'},
        {'name': 'Café 3', 'url': '/static/images/coffee3.jpg'},
        {'name': 'Café 4', 'url': '/static/images/coffee4.jpg'},
        {'name': 'Café 5', 'url': '/static/images/coffee5.jpg'},
        {'name': 'Café 6', 'url': '/static/images/coffee6.jpg'},
    ]
    return render_template('register-coffee.html', available_images=available_images)

@app.route('/admin/save-new-coffee', methods=['POST'])
async def save_new_coffee():
    try:
        name = request.form.get('name')
        origin = request.form.get('origin')
        roast = request.form.get('roast')
        process = request.form.get('process')
        flavor_notes = request.form.get('flavor_notes')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        weight_grams = int(request.form.get('weight_grams'))
        stock = int(request.form.get('stock'))
        is_active = request.form.get('is_active') == 'on'
        
        # Manejar imagen
        image_url = None
        if 'selected_image' in request.form and request.form.get('selected_image'):
            image_url = request.form.get('selected_image')
        elif 'image_url' in request.form and request.form.get('image_url'):
            image_url = request.form.get('image_url')
        elif 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                filename = f"coffee_{int(datetime.now().timestamp())}_{file.filename}"
                filepath = os.path.join('static/uploads', filename)
                os.makedirs('static/uploads', exist_ok=True)
                file.save(filepath)
                image_url = f'/static/uploads/{filename}'
        
        await db.coffee.create(
            data={
                'name': name,
                'origin': origin,
                'roast': roast,
                'process': process,
                'flavor_notes': flavor_notes,
                'description': description,
                'price': price,
                'weight_grams': weight_grams,
                'stock': stock,
                'image_url': image_url,
                'is_active': is_active
            }
        )
        
        return redirect('/admin/coffees')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/update/<coffee_id>')
async def update_coffee_form(coffee_id):
    try:
        coffee = await db.coffee.find_unique(where={'id': coffee_id})
        if not coffee:
            return "Producto no encontrado", 404
            
        available_images = [
            {'name': 'Café 1', 'url': '/static/images/coffee1.jpg'},
            {'name': 'Café 2', 'url': '/static/images/coffee2.jpg'},
            {'name': 'Café 3', 'url': '/static/images/coffee3.jpg'},
            {'name': 'Café 4', 'url': '/static/images/coffee4.jpg'},
            {'name': 'Café 5', 'url': '/static/images/coffee5.jpg'},
            {'name': 'Café 6', 'url': '/static/images/coffee6.jpg'},
        ]
        return render_template('update-coffee.html', product=coffee, available_images=available_images)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/update-coffee/<coffee_id>', methods=['POST'])
async def update_coffee(coffee_id):
    try:
        name = request.form.get('name')
        origin = request.form.get('origin')
        roast = request.form.get('roast')
        process = request.form.get('process')
        flavor_notes = request.form.get('flavor_notes')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        weight_grams = int(request.form.get('weight_grams'))
        stock = int(request.form.get('stock'))
        is_active = request.form.get('is_active') == 'on'
        
        # Manejar imagen
        image_url = request.form.get('current_image')
        if 'selected_image' in request.form and request.form.get('selected_image'):
            image_url = request.form.get('selected_image')
        elif 'image_url' in request.form and request.form.get('image_url'):
            image_url = request.form.get('image_url')
        elif 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                filename = f"coffee_{int(datetime.now().timestamp())}_{file.filename}"
                filepath = os.path.join('static/uploads', filename)
                os.makedirs('static/uploads', exist_ok=True)
                file.save(filepath)
                image_url = f'/static/uploads/{filename}'
        
        await db.coffee.update(
            where={'id': coffee_id},
            data={
                'name': name,
                'origin': origin,
                'roast': roast,
                'process': process,
                'flavor_notes': flavor_notes,
                'description': description,
                'price': price,
                'weight_grams': weight_grams,
                'stock': stock,
                'image_url': image_url,
                'is_active': is_active
            }
        )
        
        return redirect('/admin/coffees')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/delete/<coffee_id>')
async def delete_coffee_route(coffee_id):
    try:
        await db.coffee.delete(where={'id': coffee_id})
        return redirect('/admin/coffees')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/api/coffees/<coffee_id>', methods=['DELETE'])
async def delete_coffee_api(coffee_id):
    try:
        await db.coffee.delete(where={'id': coffee_id})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
