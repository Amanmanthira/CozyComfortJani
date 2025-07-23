from flask import Blueprint, render_template, request, session
from app.services.seller_service import get_distributor_stock, place_order, get_orders , get_approved_orders

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/seller/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = session['user']
    seller_id = user['id']

    if request.method == 'POST':
        blanket_id = request.form['blanket_id']
        quantity = request.form['quantity']
        place_order(seller_id, blanket_id, quantity)

    stock = get_distributor_stock()
    orders = get_orders(seller_id)  # all orders (pending + approved)
    approved_orders = get_approved_orders(seller_id)  # only approved orders

    return render_template(
        'seller/dashboard.html',
        stock=stock,
        orders=orders,
        approved_orders=approved_orders
    )

