from . import db
from .models import Cart, Order, OrderDetail, CartItem

def place_order(user_id):
    """Place an order based on the user's cart."""
    # Get the user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        raise ValueError("Cart is empty or does not exist.")

    # Create a new order
    order = Order(user_id=user_id, status='Pending', total_amount=0)
    db.session.add(order)

    total_amount = 0

    # Loop through cart items to create order details
    for item in cart.items:
        order_detail = OrderDetail(order_id=order.order_id,
                                   product_id=item.product_id,
                                   quantity=item.quantity,
                                   unit_price=item.product.price)
        db.session.add(order_detail)
        total_amount += item.quantity * item.product.price

    order.total_amount = total_amount

    # Clear the cart after placing the order
    db.session.commit()
    return order

def get_order_history(user_id):
    """Get all orders for a user."""
    return Order.query.filter_by(user_id=user_id).all()

def cancel_order(order_id):
    """Cancel an order if it hasn't been processed yet."""
    order = Order.query.get(order_id)
    if not order or order.status != 'Pending':
        raise ValueError("Order cannot be canceled.")

    order.status = 'Canceled'
    db.session.commit()
    return order
