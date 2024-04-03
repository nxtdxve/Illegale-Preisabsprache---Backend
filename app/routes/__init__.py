from re import sub
from flask import Blueprint

product_bp = Blueprint('product_bp', __name__)
retailer_bp = Blueprint('retailer_bp', __name__)
subscription_bp = Blueprint('subscription_bp', __name__)
notification_bp = Blueprint('notification_bp', __name__)

from .product_routes import *
from .retailer_routes import *
from .subscription_routes import *
from .notification_routes import *
