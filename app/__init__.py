from flask import Flask
from config.database import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretkey'
    init_db(app)

    from app.controllers import auth_controller , manufacturer_controller, distributor_controller, seller_controller
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(manufacturer_controller.manufacturer_bp)
    app.register_blueprint(distributor_controller.distributor_bp)
    app.register_blueprint(seller_controller.seller_bp)
    return app
