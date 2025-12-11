from flask import jsonify, render_template, request, session, url_for
import repository.store_repo as store_repo
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(app):
    admin_route = "/admin/"
    @app.route(admin_route)
    def startAdmin():
        return render_template('index-admin.html')
    
    @app.route(admin_route + "coffees", methods=['GET'])
    def getCoffeesAdmin():
        coffees = store_repo.obtainCoffees()
        # Agregar imágenes de ejemplo si no tienen
        default_images = [
            '/static/assets/coffee-1.jpg',
            '/static/assets/coffee-2.jpg',
            '/static/assets/coffee-3.jpg',
            '/static/assets/coffee-4.jpg',
            '/static/assets/coffee-5.jpg',
            '/static/assets/coffee-6.jpg'
        ]
        for i, coffee in enumerate(coffees):
            if not coffee.get('image_url') or coffee.get('image_url') == '':
                coffee['image_url'] = default_images[i % len(default_images)]
        return render_template('index-admin.html', coffees=coffees)
    
    @app.route(admin_route + "register-coffee")
    def register_coffee():
        # Imágenes disponibles en assets
        available_images = [
            {'name': 'Café 1', 'url': '/static/assets/coffee-1.jpg'},
            {'name': 'Café 2', 'url': '/static/assets/coffee-2.jpg'},
            {'name': 'Café 3', 'url': '/static/assets/coffee-3.jpg'},
            {'name': 'Café 4', 'url': '/static/assets/coffee-4.jpg'},
            {'name': 'Café 5', 'url': '/static/assets/coffee-5.jpg'},
            {'name': 'Café 6', 'url': '/static/assets/coffee-6.jpg'}
        ]
        return render_template('register-coffee.html', available_images=available_images)
    
    @app.route(admin_route + "save-new-coffee", methods=['POST'])
    def save_new_coffee():
        coffee_data = request.form.to_dict()
        
        # Manejar imagen subida
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(os.path.dirname(__file__), '../static/assets', filename)
                file.save(upload_path)
                coffee_data['image_url'] = f'/static/assets/{filename}'
        
        # Si no se subió archivo, usar la imagen seleccionada del dropdown
        if 'image_url' not in coffee_data or coffee_data['image_url'] == '':
            if 'selected_image' in coffee_data and coffee_data['selected_image']:
                coffee_data['image_url'] = coffee_data['selected_image']
        
        store_repo.saveNewCoffee(coffee_data)
        return jsonify({"message": "New coffee registered successfully"})