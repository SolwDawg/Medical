from . import db
from .models import Cart, CartItem, Product

def add_item_to_cart(user_id, product_id, quantity):
    """Thêm sản phẩm vào giỏ hàng."""
    
    # Tìm giỏ hàng của người dùng
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        # Tạo giỏ hàng mới nếu chưa có
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    
    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()
    
    if cart_item:
        # Nếu đã có thì cập nhật số lượng
        cart_item.quantity += quantity
    else:
        # Nếu chưa có thì thêm mới
        cart_item = CartItem(cart_id=cart.cart_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    return cart_item


def remove_item_from_cart(cart_id, product_id, quantity):
    """Remove a specified quantity of an item from the cart."""
    # Tìm item trong giỏ hàng
    item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
    if item:
        # Giảm số lượng
        item.quantity -= quantity
        if item.quantity <= 0:
            # Nếu số lượng <= 0, xóa sản phẩm khỏi giỏ hàng
            db.session.delete(item)
            message = 'Item removed from cart because quantity is zero'
        else:
            message = f'Quantity updated, new quantity is {item.quantity}'
        
        db.session.commit()
        return {'message': message}, 200
    else:
        raise ValueError('Item not found in cart')