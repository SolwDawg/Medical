from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import register_user, login_user
from .models import Cart, CartItem, Product
from .cart import  add_item_to_cart, remove_item_from_cart
from .order import place_order, get_order_history, cancel_order
from . import db

# Blueprint cho các route chính
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/register', methods=['POST'])
def register():
    return register_user()

@routes_bp.route('/login', methods=['POST'])
def login():
    return login_user()

@routes_bp.route('/products', methods=['GET'])
@jwt_required()
def list_products():
    products = Product.query.all()
    result = [{
        "product_id": product.product_id, 
        "name": product.name, 
        "price": product.price, 
        "description": product.description, 
        "image_url": product.image_url
    } for product in products]
    return jsonify(result), 200

@routes_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "description", "price", "brand", "category", "stock_quantity", "image_url")):
        return jsonify({"message": "Invalid input"}), 400

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        brand=data['brand'],
        category=data['category'],
        stock_quantity=data['stock_quantity'],
        image_url=data['image_url']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully", "product_id": new_product.product_id}), 201

@routes_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get_or_404(product_id)

    if not data:
        return jsonify({"message": "Invalid input"}), 400

    # Update fields if provided
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'brand' in data:
        product.brand = data['brand']
    if 'category' in data:
        product.category = data['category']
    if 'stock_quantity' in data:
        product.stock_quantity = data['stock_quantity']
    if 'image_url' in data:
        product.image_url = data['image_url']

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

@routes_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

# Blueprint cho các route liên quan đến giỏ hàng
cart_routes_bp = Blueprint('cart_routes', __name__)

@routes_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart_route():
    user_id = get_jwt_identity()  # Lấy user_id từ JWT
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)  # Mặc định là 1 nếu không có thông tin

    try:
        cart_item = add_item_to_cart(user_id, product_id, quantity)
        return jsonify({
            'cart_item_id': cart_item.cart_item_id,
            'product_id': cart_item.product_id,
            'quantity': cart_item.quantity
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@routes_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        return jsonify({'items': []}), 200

    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    items = []

    for item in cart_items:
        product = Product.query.get(item.product_id)
        items.append({
            'cart_item_id': item.cart_item_id,
            'product_id': item.product_id,
            'product_name': product.name,
            'product_image': product.image_url,
            'quantity': item.quantity,
            'price': product.price,
            'total_price': product.price * item.quantity
        })

    return jsonify({'items': items}), 200

@routes_bp.route('/cart/<int:cart_id>/remove', methods=['PATCH'])
@jwt_required()
def remove_from_cart_route(cart_id):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    try:
        result = remove_item_from_cart(cart_id, product_id, quantity)
        return jsonify(result[0]), result[1]
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    
    routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/order', methods=['POST'])
@jwt_required()
def create_order_route():
    user_id = get_jwt_identity()
    try:
        order = place_order(user_id)
        return jsonify({'message': 'Order placed successfully!', 'order_id': order.order_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@routes_bp.route('/order/history', methods=['GET'])
@jwt_required()
def order_history_route():
    user_id = get_jwt_identity()
    orders = get_order_history(user_id)
    return jsonify([{'order_id': order.order_id, 'total_amount': order.total_amount, 'status': order.status} for order in orders]), 200

@routes_bp.route('/order/<int:order_id>/cancel', methods=['DELETE'])
@jwt_required()
def cancel_order_route(order_id):
    try:
        order = cancel_order(order_id)
        return jsonify({'message': 'Order canceled successfully!'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400