from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import register_user, login_user
from .models import Product
from .cart import create_cart, add_item_to_cart, remove_item_from_cart, get_cart_items
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

@cart_routes_bp.route('/cart/create/<int:user_id>', methods=['POST'])
@jwt_required()  # Thêm yêu cầu JWT nếu cần
def create_cart_route(user_id):
    cart = create_cart(user_id)
    return jsonify({'cart_id': cart.cart_id}), 201

@routes_bp.route('/cart/<int:cart_id>/add', methods=['POST'])
@jwt_required()
def add_item_route(cart_id):    
    data = request.json
    product_id = data['product_id']
    quantity = data.get('quantity', 1)

    # Gọi hàm add_item_to_cart và nhận đối tượng CartItem
    item = add_item_to_cart(cart_id, product_id, quantity)

    # Sử dụng item.cart_item_id để lấy id của cart item
    return jsonify({'cart_item_id': item.cart_item_id}), 201

@cart_routes_bp.route('/cart/item/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()  # Thêm yêu cầu JWT nếu cần
def remove_item_route(cart_item_id):
    remove_item_from_cart(cart_item_id)
    return jsonify({'message': 'Item removed successfully'}), 204

@cart_routes_bp.route('/cart/<int:cart_id>/items', methods=['GET'])
@jwt_required()  # Thêm yêu cầu JWT nếu cần
def get_cart_items_route(cart_id):
    items = get_cart_items(cart_id)
    return jsonify([{'cart_item_id': item.cart_item_id, 'product_id': item.product_id, 'quantity': item.quantity} for item in items]), 200


