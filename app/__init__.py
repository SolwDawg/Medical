from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config  

# Khởi tạo các đối tượng
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)  # Tải cấu hình từ file config

    # Khởi tạo các phần mở rộng
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Nhập và đăng ký các Blueprint
    from .routes import routes_bp, cart_routes_bp
    

    app.register_blueprint(routes_bp)
    app.register_blueprint(cart_routes_bp)
    # Tạo tất cả các bảng trong cơ sở dữ liệu
    with app.app_context():
       
       db.create_all()   # Tạo các bảng nếu chưa tồn tại

    return app
