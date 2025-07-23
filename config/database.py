import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='cozy_comfort',
        auth_plugin='mysql_native_password'  # FIXED here
    )

def init_db(app):
    pass
