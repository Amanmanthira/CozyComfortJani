import os
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app.services.distributor_service import get_all_blankets, add_inventory, get_distributor_inventory, get_all_blanket_requests 
from app.models.order_model import get_pending_orders, get_approved_orders, approve_order
from config.database import get_connection

distributor_bp = Blueprint('distributor', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@distributor_bp.route('/distributor/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = session['user']
    distributor_id = user['id']

    if request.method == 'POST':
        # ✅ Add to Inventory Form
        if 'blanket_id' in request.form:
            blanket_id = request.form['blanket_id']
            stock = request.form['stock']
            add_inventory(distributor_id, blanket_id, stock)
            flash("✅ Inventory updated!", "success")
            return redirect(url_for('distributor.dashboard'))

        # ✅ Approve Order
        elif 'approve_order_id' in request.form:
            order_id = request.form['approve_order_id']
            result = approve_order(order_id)

            if result == "approved":
                flash("✅ Order approved successfully!", "success")
            elif result == "insufficient_stock":
                flash("❌ Not enough stock to approve this order.", "error")
            elif result == "not_found":
                flash("⚠️ Order not found.", "warning")
            else:
                flash("⚠️ Something went wrong.", "error")

            return redirect(url_for('distributor.dashboard'))

        # ✅ Request New Blanket with Description and Image
        elif 'name' in request.form and 'description' in request.form:
            name = request.form['name']
            material = request.form.get('material', '')
            quantity = request.form['quantity']
            description = request.form['description']
            image_file = request.files.get('image')

            image_path = None
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO blanket_requests (distributor_id, name, material, quantity, description, image)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (distributor_id, name, material, quantity, description, image_path))
                conn.commit()
                flash("✅ Blanket request submitted successfully!", "success")
            except Exception as e:
                print(f"Error submitting blanket request: {e}")
                flash("❌ Failed to submit blanket request.", "error")
            finally:
                conn.close()

            return redirect(url_for('distributor.dashboard'))

    # GET method
    all_blankets = get_all_blankets()
    inventory = get_distributor_inventory(distributor_id)
    orders = get_pending_orders(distributor_id)
    approved_orders = get_approved_orders(distributor_id)
    all_blanket_requests = get_all_blanket_requests()

    return render_template(
        'distributor/dashboard.html',
        blankets=all_blankets,
        inventory=inventory,
        orders=orders,
        approved_orders=approved_orders,
        blanket_requests=all_blanket_requests

    )
