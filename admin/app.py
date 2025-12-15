import sys
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Agregar el directorio backend al path para importar módulos
ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Importar repositorio del backend
import repository.store_repo as store_repo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'onsen-coffee-admin-key')
CORS(app)

# ========== RUTA PRINCIPAL ==========
@app.route('/admin')
@app.route('/admin/')
def admin_dashboard():
    return render_template('dashboard.html')

# ========== RUTAS DE PEDIDOS ==========

@app.route('/admin/api/orders', methods=['GET'])
def get_orders():
    try:
        status_filter = request.args.get('status', 'all')
        orders = store_repo.obtainOrders(status_filter)
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    try:
        data = request.get_json()
        status = data.get('status')
        store_repo.updateOrderStatus(order_id, status)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        store_repo.deleteOrder(order_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== RUTAS DE USUARIOS ==========

@app.route('/admin/api/users', methods=['GET'])
def get_users():
    try:
        users = store_repo.obtainUsers()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        result = store_repo.createUser(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    try:
        data = request.get_json()
        role = data.get('role')
        store_repo.updateUserRole(user_id, role)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        store_repo.deleteUser(user_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== RUTAS DE PRODUCTOS (COFFEES) ==========

@app.route('/admin/api/coffees', methods=['GET'])
def get_coffees():
    try:
        coffees = store_repo.obtainCoffees()
        return jsonify(coffees)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/coffees')
def admin_coffees():
    try:
        coffees = store_repo.obtainCoffees()
        return render_template('index-admin.html', coffees=coffees)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/register-coffee')
def register_coffee():
    available_images = [
        {'name': 'Café 1', 'url': '/static/assets/coffee-1.jpg'},
        {'name': 'Café 2', 'url': '/static/assets/coffee-2.jpg'},
        {'name': 'Café 3', 'url': '/static/assets/coffee-3.jpg'},
        {'name': 'Café 4', 'url': '/static/assets/coffee-4.jpg'},
        {'name': 'Café 5', 'url': '/static/assets/coffee-5.jpg'},
        {'name': 'Café 6', 'url': '/static/assets/coffee-6.jpg'},
    ]
    return render_template('register-coffee.html', available_images=available_images)

@app.route('/admin/save-new-coffee', methods=['POST'])
def save_new_coffee():
    try:
        coffee_data = request.form.to_dict()
        
        # Si se subió un archivo de imagen, manejarlo
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                upload_path = os.path.join(os.path.dirname(__file__), '../backend/static/assets', filename)
                file.save(upload_path)
                coffee_data['image_url'] = f'/static/assets/{filename}'
        
        # Si no se subió archivo, usar la imagen seleccionada
        if 'image_url' not in coffee_data or coffee_data['image_url'] == '':
            if 'selected_image' in coffee_data and coffee_data['selected_image']:
                coffee_data['image_url'] = coffee_data['selected_image']
        
        store_repo.saveNewCoffee(coffee_data)
        return jsonify({"message": "Coffee registered successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/update-coffee/<int:coffee_id>')
def update_coffee_form(coffee_id):
    try:
        coffee = store_repo.obtainCoffeeById(coffee_id)
        if 'error' in coffee:
            return "Producto no encontrado", 404
            
        available_images = [
            {'name': 'Café 1', 'url': '/static/assets/coffee-1.jpg'},
            {'name': 'Café 2', 'url': '/static/assets/coffee-2.jpg'},
            {'name': 'Café 3', 'url': '/static/assets/coffee-3.jpg'},
            {'name': 'Café 4', 'url': '/static/assets/coffee-4.jpg'},
            {'name': 'Café 5', 'url': '/static/assets/coffee-5.jpg'},
            {'name': 'Café 6', 'url': '/static/assets/coffee-6.jpg'},
        ]
        return render_template('update-coffee.html', product=coffee, available_images=available_images)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/update-coffee/<int:coffee_id>', methods=['POST'])
def update_coffee(coffee_id):
    try:
        coffee_data = request.form.to_dict()
        coffee_data['id'] = coffee_id
        
        # Manejar imagen
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename:
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                upload_path = os.path.join(os.path.dirname(__file__), '../backend/static/assets', filename)
                file.save(upload_path)
                coffee_data['image_url'] = f'/static/assets/{filename}'
        
        # Si no se subió archivo, usar la imagen seleccionada
        if 'image_url' not in coffee_data or coffee_data['image_url'] == '':
            if 'selected_image' in coffee_data and coffee_data['selected_image']:
                coffee_data['image_url'] = coffee_data['selected_image']
        
        store_repo.updateCoffee(coffee_data)
        return jsonify({"message": "Coffee updated successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/delete/<int:coffee_id>')
def delete_coffee_route(coffee_id):
    try:
        store_repo.deleteCoffee(coffee_id)
        return jsonify({"message": "Coffee deleted successfully"})
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/admin/api/coffees/<int:coffee_id>', methods=['DELETE'])
def delete_coffee_api(coffee_id):
    try:
        store_repo.deleteCoffee(coffee_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
