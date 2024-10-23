from flask import request, jsonify
from flask_jwt_extended import create_access_token
from .models import User
from . import db, bcrypt  

def register_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "password", "address", "phone")):
        return jsonify({"message": "Invalid input"}), 400
    
    if User.query.filter_by(email= data['email']).first():
        return jsonify({"message: ": "Email already exits."}),400
    

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    admin_exists = User.query.filter_by(role='admin').first()
    if not admin_exists:
        role = 'admin'
    else:
        role = 'user'  
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        address=data['address'],
        phone=data['phone'],
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User registered successfully with role {role}."}), 201

def login_user():
    data = request.get_json()

    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Invalid input. Please provide email and password."}), 400

    
    user = User.query.filter_by(email=data['email']).first()

    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Tạo JWT token
        access_token = create_access_token(identity=user.user_id)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": user.role  
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401
