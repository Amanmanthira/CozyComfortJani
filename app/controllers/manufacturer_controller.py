from flask import Blueprint, render_template, request, redirect, session
from app.services.manufacturer_service import get_all_blankets, add_blanket, get_all_blanket_requests

manufacturer_bp = Blueprint('manufacturer', __name__)
@manufacturer_bp.route('/manufacturer/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Determine which form was submitted
        if 'name' in request.form:
            # Handle "Add Blanket" form
            name = request.form.get('name')
            material = request.form.get('material')
            price = request.form.get('price')
            stock = request.form.get('stock')
            add_blanket(name, material, price, stock)

        elif 'request_id' in request.form and 'status' in request.form:
            # Handle "Update Blanket Request Status" form
            request_id = request.form.get('request_id')
            status = request.form.get('status')

            from config.database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE blanket_requests SET status = %s WHERE id = %s", (status, request_id))
                conn.commit()
            except Exception as e:
                print(f"Error updating request status: {e}")
            finally:
                conn.close()

        return redirect('/manufacturer/dashboard')

    blankets = get_all_blankets()
    blanket_requests = get_all_blanket_requests()
    return render_template('manufacturer/dashboard.html', blankets=blankets, blanket_requests=blanket_requests)


