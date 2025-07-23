from config.database import get_connection

def get_all_blankets():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blankets")
    data = cursor.fetchall()
    conn.close()
    return data

def add_inventory(distributor_id, blanket_id, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO distributor_inventory (distributor_id, blanket_id, stock) VALUES (%s, %s, %s)",
                   (distributor_id, blanket_id, stock))
    conn.commit()
    conn.close()

def get_distributor_inventory(distributor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.name, d.stock
        FROM distributor_inventory d
        JOIN blankets b ON d.blanket_id = b.id
        WHERE d.distributor_id = %s
    """, (distributor_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_pending_orders(distributor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, b.name AS blanket_name, o.quantity, u.username AS seller_name, o.status
        FROM orders o
        JOIN blankets b ON o.blanket_id = b.id
        JOIN users u ON o.seller_id = u.id
        WHERE o.distributor_id = %s AND o.status = 'pending'
    """, (distributor_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def approve_order(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Get order details
        cursor.execute("""
            SELECT distributor_id, blanket_id, quantity
            FROM orders
            WHERE id = %s AND status = 'pending'
        """, (order_id,))
        order = cursor.fetchone()

        if not order:
            return "not_found"

        distributor_id = order['distributor_id']
        blanket_id = order['blanket_id']
        quantity = order['quantity']

        # 2. Check inventory
        cursor.execute("""
            SELECT stock FROM distributor_inventory
            WHERE distributor_id = %s AND blanket_id = %s
        """, (distributor_id, blanket_id))
        inventory = cursor.fetchone()

        if not inventory or inventory['stock'] < quantity:
            return "insufficient_stock"

        # 3. Approve order and subtract stock atomically
        cursor.execute("START TRANSACTION")

        cursor.execute("UPDATE orders SET status = 'approved' WHERE id = %s", (order_id,))
        cursor.execute("""
            UPDATE distributor_inventory
            SET stock = stock - %s
            WHERE distributor_id = %s AND blanket_id = %s
        """, (quantity, distributor_id, blanket_id))

        conn.commit()
        return "approved"

    except Exception as e:
        conn.rollback()
        print(f"Error approving order: {e}")
        return "error"

    finally:
        conn.close()

def get_all_blanket_requests():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blanket_requests ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

