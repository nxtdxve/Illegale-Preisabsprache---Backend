import email
from .email_service import send_email
from app.database.db_connection import mongo
from bson import ObjectId
from datetime import datetime, timedelta

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
    last_week = datetime.now() - timedelta(days=7)
    subscriptions = mongo.db.subscriptions.find({"product_id": "*"})
    email_list = [sub['email'] for sub in subscriptions if 'email' in sub]

    # Preisänderungen der letzten Woche
    price_changes = mongo.db.price_records.find({"timestamp": {"$gte": last_week}})

    if price_changes.count() > 0:
        message_parts = []
        # Informationen für jede Preisänderung
        for change in price_changes:
            product = mongo.db.products.find_one({"_id": change['product_id']})
            retailer = mongo.db.retailers.find_one({"_id": change['retailer_id']})

            if product and retailer:
                # Formatierung der Nachricht
                message_part = f"Der Preis für {product['name']} bei {retailer['name']} hat sich geändert: CHF {change['price'].to_decimal()}"
                message_parts.append(message_part)

        message = "Hier sind die Preisänderungen der letzten Woche:\n" + "\n".join(message_parts)
    else:
        message = "Keine Preisänderungen in der letzten Woche."

    if email_list:
        send_email(email_list, "Wöchentliche Preisaktualisierungen", message, "Weekly Update")
    else:
        print("Keine Abonnements mit E-Mail gefunden.")

