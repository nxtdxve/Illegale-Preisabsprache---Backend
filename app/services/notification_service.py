from .email_service import send_email
from app.database.db_connection import mongo
from bson import ObjectId

def send_price_change_notifications(product_id, new_price, retailer_id):
    subscriptions = mongo.db.subscriptions.find({"product_id": ObjectId(product_id)})
    
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    retailer = mongo.db.retailers.find_one({"_id": ObjectId(retailer_id)})
    if not product:
        print("Produkt nicht gefunden.")
        return
    if not retailer:
        print("Einzelhändler nicht gefunden.")
        return

    message = f"Der Preis für {product['name']} hat sich geändert. Neuer Preis bei {retailer['name']}: CHF{new_price}"
    subject = "Preisänderung!"

    # Sammle alle E-Mail-Adressen in einer Liste
    email_list = [subscription['email'] for subscription in subscriptions if 'email' in subscription]

    # Versende die E-Mail nur, wenn es Abonnements gibt
    if email_list:
        send_email(email_list, subject, message)
    else:
        print("Keine Abonnements mit E-Mail gefunden.")


def send_weekly_updates():
    ...
