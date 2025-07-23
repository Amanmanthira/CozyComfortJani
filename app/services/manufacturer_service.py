from flask import request, flash, redirect, url_for
from config.database import get_connection

def get_all_blankets():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blankets")
    results = cursor.fetchall()
    conn.close()
    return results

def add_blanket(name, material, price, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO blankets (name, material, price, manufacturer_stock) VALUES (%s, %s, %s, %s)",
                   (name, material, price, stock))
    conn.commit()
    conn.close()

def update_request_status():
    request_id = request.form['request_id']
    status = request.form['status']

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE blanket_requests SET status = %s WHERE id = %s", (status, request_id))
        conn.commit()
        flash(f"Request status updated to '{status}'!", "success")
    except Exception as e:
        print(f"Error updating request status: {e}")
        flash("Failed to update request status.", "error")
    finally:
        conn.close()

    return redirect(url_for('manufacturer.dashboard'))

def get_all_blanket_requests():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blanket_requests ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data
