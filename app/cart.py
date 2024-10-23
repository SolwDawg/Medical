from . import db
from .models import Cart, CartItem, Product



def create_cart(user_id):
    """Create a new cart for the user."""
    new_cart = Cart(user_id=user_id)
    db.session.add(new_cart)
    db.session.commit()
    return new_cart

def add_item_to_cart(cart_id, product_id, quantity):
    """Add an item to the cart."""
    item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    return item

def remove_item_from_cart(cart_item_id):
    """Remove an item from the cart."""
    item = CartItem.query.get(cart_item_id)
    if item:
        db.session.delete(item)
        db.session.commit()

def get_cart_items(cart_id):
    """Retrieve all items in the cart."""
    return CartItem.query.filter_by(cart_id=cart_id).all()
