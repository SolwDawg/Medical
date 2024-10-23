from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



# Models
# class User(db.Model):
#     __tablename__ = 'users'
#     user_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(200))
#     address = db.Column(db.String(200))
#     phone = db.Column(db.String(20))
#     role = db.Column(db.String(10), default="user")  # User/Admin

# class Product(db.Model):
#     __tablename__ = 'products'
#     product_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     description = db.Column(db.String(500))
#     price = db.Column(db.Float)
#     brand = db.Column(db.String(100))
#     category = db.Column(db.String(100))
#     stock_quantity = db.Column(db.Integer)
#     image_url = db.Column(db.String(200))

# class Order(db.Model):
#     __tablename__ = 'orders'
#     order_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     order_date = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.Column(db.String(20))
#     total_amount = db.Column(db.Float)

# class OrderDetail(db.Model):
#     __tablename__ = 'orderdetail'
#     order_detail_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
#     quantity = db.Column(db.Integer)
#     unit_price = db.Column(db.Float)

# class Payment(db.Model):
#     __tablename__ = 'payments'
#     payment_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
#     payment_method = db.Column(db.String(50))
#     payment_status = db.Column(db.String(20))
#     payment_date = db.Column(db.DateTime, default=datetime.utcnow)

# class Symptom(db.Model):
#     __tablename__ = 'symptoms'
#     symptom_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     description = db.Column(db.String(500))

# class Disease(db.Model):
#     __tablename__ = 'diseases'
#     disease_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     description = db.Column(db.String(500))
#     probability = db.Column(db.Float)

# class Recommendation(db.Model):
#     __tablename__ = 'recommendation'
#     recommendation_id = db.Column(db.Integer, primary_key=True)
#     disease_id = db.Column(db.Integer, db.ForeignKey('disease.disease_id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))

# class Cart(db.Model):
#     __tablename__ = 'carts'
#     cart_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     total_price = db.Column(db.Float, default=0.0)

#     items = db.relationship('CartItem', backref='cart', lazy=True)

# class CartItem(db.Model):
#     __tablename__ = 'cart_items'
#     cart_item_id = db.Column(db.Integer, primary_key=True)
#     cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=False)  
#     product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)  
#     quantity = db.Column(db.Integer, default=1)
#     unit_price = db.Column(db.Float, nullable=False)  

    
#     product = db.relationship('Product', backref='cart_items', lazy=True)
