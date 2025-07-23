from config.database import get_connection

def get_distributor_stock():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.id AS distributor_id, b.id AS blanket_id, b.name, d.stock
        FROM distributor_inventory d
        JOIN blankets b ON d.blanket_id = b.id
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def place_order(seller_id, blanket_id, quantity):
    distributor_id = get_distributor_id_for_seller(seller_id)
    if distributor_id is None:
        raise ValueError("Seller does not have an assigned distributor")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (seller_id, distributor_id, blanket_id, quantity, status) VALUES (%s, %s, %s, %s, 'pending')",
        (seller_id, distributor_id, blanket_id, quantity)
    )
    conn.commit()
    conn.close()


def get_orders(seller_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, b.name, o.quantity, o.status
        FROM orders o
        JOIN blankets b ON o.blanket_id = b.id
        WHERE o.seller_id = %s
    """, (seller_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_distributor_id_for_seller(seller_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT distributor_id FROM users WHERE id = %s", (seller_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def get_approved_orders(seller_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, b.name, o.quantity, o.status
        FROM orders o
        JOIN blankets b ON o.blanket_id = b.id
        WHERE o.seller_id = %s AND o.status = 'approved'
        ORDER BY o.id DESC
    """, (seller_id,))
    results = cursor.fetchall()
    conn.close()
    return results
