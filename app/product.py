from flask import request, jsonify
from flask_restful import Resource
from .database import Product
from . import db

class ProductList(Resource):
    def get(self):
        products = Product.query.all()
        return jsonify([{'product_id': p.product_id, 'name': p.name, 'description': p.description,
                         'price': p.price, 'brand': p.brand, 'category': p.category,
                         'stock_quantity': p.stock_quantity, 'image_url': p.image_url} for p in products])

    def post(self):
        data = request.get_json()
        new_product = Product(name=data['name'], description=data['description'],
                              price=data['price'], brand=data['brand'],
                              category=data['category'], stock_quantity=data['stock_quantity'],
                              image_url=data['image_url'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully"}), 201

class ProductDetail(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return jsonify({'product_id': product.product_id, 'name': product.name,
                        'description': product.description, 'price': product.price,
                        'brand': product.brand, 'category': product.category,
                        'stock_quantity': product.stock_quantity, 'image_url': product.image_url})

    def put(self, product_id):
        data = request.get_json()
        product = Product.query.get_or_404(product_id)
        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.brand = data['brand']
        product.category = data['category']
        product.stock_quantity = data['stock_quantity']
        product.image_url = data['image_url']
        db.session.commit()
        return jsonify({"message": "Product updated successfully"})

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
