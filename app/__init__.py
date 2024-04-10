from flask import Flask
from flask_cors import CORS
from .database.db_connection import init_db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    
    init_db(app)
    
    from .routes.product_routes import product_bp
    app.register_blueprint(product_bp)
    from .routes.retailer_routes import retailer_bp
    app.register_blueprint(retailer_bp)
    from .routes.subscription_routes import subscription_bp
    app.register_blueprint(subscription_bp)
    from .routes.notification_routes import notification_bp
    app.register_blueprint(notification_bp)
    
    return app
