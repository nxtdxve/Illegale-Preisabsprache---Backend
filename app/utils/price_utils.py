from bson import ObjectId
from app.database.db_connection import mongo
from bson.decimal128 import Decimal128
from decimal import Decimal
from datetime import datetime

def get_price_details(product_id):
    if isinstance(product_id, str):
        product_id = ObjectId(product_id)
    
    # Hole alle Preisdatensätze für das Produkt
    all_price_records = list(mongo.db.price_records.find({"product_id": product_id}, {'_id': 0}).sort("timestamp", -1))
    
    # Konvertiere Decimal128 zu Decimal für alle Preise und bestimme die "all time" Preise
    prices = [record['price'].to_decimal() for record in all_price_records]
    highest_price_all_time = str(max(prices)) if prices else None
    lowest_price_all_time = str(min(prices)) if prices else None

    # Bestimme die letzten Preise pro Einzelhändler
    last_prices = {}
    for record in all_price_records:
        retailer_id = str(record['retailer_id'])
        if retailer_id not in last_prices:
            last_prices[retailer_id] = record['price'].to_decimal()

    # Ermittle aus diesen letzten Preisen die "current" Preise
    if last_prices.values():
        highest_price_current = str(max(last_prices.values()))
        lowest_price_current = str(min(last_prices.values()))
    else:
        highest_price_current = lowest_price_current = None

    # Preisdatensätze für die Antwort vorbereiten
    price_records_formatted = [
        {
            "retailer_id": str(record["retailer_id"]),
            "price": str(record["price"].to_decimal()),
            "timestamp": record["timestamp"].isoformat() if isinstance(record["timestamp"], datetime) else str(record["timestamp"])
        } for record in all_price_records
    ]

    # Bereite die finale Antwort vor
    price_details = {
        'highest_price_all_time': highest_price_all_time,
        'lowest_price_all_time': lowest_price_all_time,
        'highest_price_current': highest_price_current,
        'lowest_price_current': lowest_price_current,
        'price_records': price_records_formatted
    }

    return price_details
