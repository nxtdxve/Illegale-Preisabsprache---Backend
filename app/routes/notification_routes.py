from flask import request, jsonify
from app.services.notification_service import send_price_change_notifications
from app.utils.auth_utils import require_api_key
from . import notification_bp

@notification_bp.route('/notify_price_change', methods=['POST'])
@require_api_key
def notify_price_change():
    data = request.json
    product_id = data.get('product_id')
    new_price = data.get('new_price')
    retailer = data.get('retailer')
    
    send_price_change_notifications(product_id, new_price, retailer)
    return jsonify({"message": "Benachrichtigungen wurden versendet."}), 200
