from flask import Blueprint, request, jsonify
from app.database.db_connection import mongo
from bson import ObjectId
from . import subscription_bp

def subscribe():
    data = request.json
    product_id = data.get('product_id')
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not product_id or not (email or phone_number):
        return jsonify({"error": "Produkt-ID und mindestens eine Kontaktmethode (E-Mail oder Telefonnummer) sind erforderlich."}), 400

    # Konvertiere product_id zu ObjectId, wenn es kein Wildcard ist
    if product_id != "*":
        if not mongo.db.products.find_one({"_id": ObjectId(product_id)}):
            return jsonify({"error": "Produkt nicht gefunden."}), 404
        data['product_id'] = ObjectId(product_id)  # Speichere als ObjectId

    # Prüfe auf bestehendes Abonnement
    existing_subscription = mongo.db.subscriptions.find_one({
        "product_id": data['product_id'],
        "email": email,
        "phone_number": phone_number
    })

    if existing_subscription:
        return jsonify({"error": "Abonnement bereits vorhanden."}), 409

    # Füge das Abonnement hinzu
    mongo.db.subscriptions.insert_one(data)
    return jsonify({"message": "Erfolgreich abonniert."}), 201

@subscription_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.json
    product_id = data.get('product_id')
    email = data.get('email')

    if not product_id or not email:
        return jsonify({"error": "Produkt-ID und mindestens eine E-Mail sind erforderlich."}), 400
    
    if product_id != "*":
        data['product_id'] = ObjectId(product_id)  # Konvertiere für die Konsistenz

    # Entferne das Abonnement
    delete_result = mongo.db.subscriptions.delete_one({"product_id": data['product_id'], "email": email})
    if delete_result.deleted_count == 0:
        return jsonify({"error": "Abonnement nicht gefunden oder bereits gekündigt."}), 404

    return jsonify({"message": "Abonnement erfolgreich gekündigt."}), 200
