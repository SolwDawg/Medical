from . import db
from datetime import datetime

# Models
class User(db.Model):
    __tablename__ = 'users'  # Thêm __tablename__
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(10))  # User/Admin

    carts = db.relationship('Cart', backref='users', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'  # Thêm __tablename__
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(100))
    stock_quantity = db.Column(db.Integer)
    image_url = db.Column(db.String(200))

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

class Order(db.Model):
    __tablename__ = 'orders'  # Thêm __tablename__
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
    total_amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

class OrderDetail(db.Model):
    __tablename__ = 'order_details'  # Thêm __tablename__
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)

class Payment(db.Model):
    __tablename__ = 'payments'  # Thêm __tablename__
    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

class Symptom(db.Model):
    __tablename__ = 'symptoms'  # Thêm __tablename__
    symptom_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

class Disease(db.Model):
    __tablename__ = 'diseases'  # Thêm __tablename__
    disease_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    probability = db.Column(db.Float)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'  # Thêm __tablename__
    recommendation_id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.disease_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
