from flask import Blueprint, request, jsonify
from app.database.db_connection import mongo
from bson import ObjectId
from . import subscription_bp

@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    product_id = data.get('product_id')
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not product_id or not (email or phone_number):
        return jsonify({"error": "Produkt-ID und mindestens eine Kontaktmethode (E-Mail oder Telefonnummer) sind erforderlich."}), 400

    # Überprüfe, ob das Produkt existiert, ausser wenn das Wildcard-Abonnement gewählt wird
    if product_id != "*" and not mongo.db.products.find_one({"_id": ObjectId(product_id)}):
        return jsonify({"error": "Produkt nicht gefunden."}), 404

    # Füge das Abonnement hinzu
    mongo.db.subscriptions.insert_one(data)
    return jsonify({"message": "Erfolgreich abonniert."}), 201

@subscription_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.json
    product_id = data.get('product_id')
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not product_id or not (email or phone_number):
        return jsonify({"error": "Produkt-ID und mindestens eine Kontaktmethode (E-Mail oder Telefonnummer) sind erforderlich."}), 400
    
    # Entferne das Abonnement
    delete_result = mongo.db.subscriptions.delete_one(data)
    if delete_result.deleted_count == 0:
        return jsonify({"error": "Abonnement nicht gefunden oder bereits gekündigt."}), 404

    return jsonify({"message": "Abonnement erfolgreich gekündigt."}), 200