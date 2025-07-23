from config.database import get_connection

def get_pending_orders(distributor_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)   # <-- add dictionary=True here
    cursor.execute("""
        SELECT o.id, s.username AS seller_name, b.name AS blanket_name, o.quantity
        FROM orders o
        JOIN users s ON o.seller_id = s.id
        JOIN blankets b ON o.blanket_id = b.id
        WHERE o.distributor_id = %s AND o.status = 'pending'
    """, (distributor_id,))
    results = cursor.fetchall()
    db.close()
    return results


def approve_order(order_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status = 'approved' WHERE id = %s", (order_id,))
    db.commit()

def get_approved_orders(distributor_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)  # Add dictionary=True here
    cursor.execute("""
        SELECT o.id, s.username AS seller_name, b.name AS blanket_name, o.quantity
        FROM orders o
        JOIN users s ON o.seller_id = s.id
        JOIN blankets b ON o.blanket_id = b.id
        WHERE o.distributor_id = %s AND o.status = 'approved'
    """, (distributor_id,))
    results = cursor.fetchall()
    db.close()
    return results
