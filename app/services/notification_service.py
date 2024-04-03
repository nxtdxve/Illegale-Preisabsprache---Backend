from .email_service import send_email
from .sms_service import send_sms
from app.database.db_connection import mongo
from bson import ObjectId

def send_price_change_notifications(product_id, new_price, retailer):
    subscriptions = mongo.db.subscriptions.find({"product_id": ObjectId(product_id)})
    
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        print("Produkt nicht gefunden.")
        return

    message = f"Der Preis für {product['name']} hat sich geändert. Neuer Preis bei {retailer}: CHF{new_price}"

    for subscription in subscriptions:
        if subscription.get('email'):
            send_email(subscription['email'], "Preisänderung", message)
        if subscription.get('phone_number'):
            send_sms(subscription['phone_number'], message)
