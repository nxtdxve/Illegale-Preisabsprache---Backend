from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler

from .database.db_connection import init_db
from config import Config
from app.services.notification_service import send_weekly_updates

# initialisiere den Scheduler
scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    init_db(app)

    scheduler.init_app(app)

    @scheduler.task('cron', id='send_weekly_updates', day_of_week='sun', hour=18)
    def schedule_weekly_updates():
        send_weekly_updates()

    scheduler.start()

    from .routes.product_routes import product_bp

    app.register_blueprint(product_bp)
    from .routes.retailer_routes import retailer_bp

    app.register_blueprint(retailer_bp)
    from .routes.subscription_routes import subscription_bp

    app.register_blueprint(subscription_bp)
    from .routes.notification_routes import notification_bp

    app.register_blueprint(notification_bp)

    return app
