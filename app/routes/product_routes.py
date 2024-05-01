import re
from urllib.parse import urlparse

from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Response, jsonify, request

from app.database.db_connection import mongo
from app.utils.auth_utils import require_api_key
from app.utils.price_utils import get_price_details
from app.utils.url_utils import extract_domain

from . import product_bp


@product_bp.route("/products", methods=["GET"])
def list_products():
    """ """
    products = mongo.db.products.find({})
    result = []

    for product in products:
        product_details = {
            "_id": str(product["_id"]),
            "name": product["name"],
            "category": product["category"],
            "retailer_urls": product["retailer_urls"],
            # Hole Preisdetails und füge sie dem Produkt hinzu
            "price_details": get_price_details(product["_id"]),
        }
        result.append(product_details)

    return Response(dumps(result), mimetype="application/json")


@product_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """

    :param product_id: 

    """
    try:
        oid = ObjectId(product_id)
    except:
        return jsonify({"error": "Ungültige Produkt-ID"}), 400

    product = mongo.db.products.find_one({"_id": oid})
    if not product:
        return jsonify({"error": "Produkt nicht gefunden"}), 404

    price_details = get_price_details(oid)

    product_details = {
        "_id": str(product["_id"]),
        "name": product["name"],
        "category": product["category"],
        "retailer_urls": product.get("retailer_urls", []),
        "price_details": price_details,
    }

    return Response(dumps(product_details), mimetype="application/json")


@product_bp.route("/products", methods=["POST"])
def add_product():
    """ """
    data = request.json
    urls = data.get("retailer_urls", [])

    if len(urls) < 2:
        return (
            jsonify(
                {
                    "error": "Mindestens zwei URLs von verschiedenen Einzelhändlern müssen angegeben werden."
                }
            ),
            400,
        )

    domains = [extract_domain(url["url"]) for url in urls]

    retailer_data = list(
        mongo.db.retailers.find(
            {
                "name": {
                    "$in": [
                        re.compile(f"^{domain}$", re.IGNORECASE) for domain in domains
                    ]
                }
            },
            {"_id": 1, "name": 1},
        )
    )

    if len(retailer_data) != len(set(domains)):
        return (
            jsonify(
                {
                    "error": "Mindestens eine URL entspricht keinem registrierten Einzelhändler."
                }
            ),
            400,
        )

    updated_retailer_urls = []
    for url in urls:
        domain = extract_domain(url["url"])
        retailer = next((r for r in retailer_data if r["name"].lower() == domain), None)
        if retailer:
            updated_retailer_urls.append(
                {"retailer_id": retailer["_id"], "url": url["url"]}
            )

    data["retailer_urls"] = updated_retailer_urls

    # Speichere das neue Produkt in der Datenbank
    result = mongo.db.products.insert_one(data)

    return (
        jsonify(
            {
                "message": "Produkt erfolgreich hinzugefügt",
                "product_id": str(result.inserted_id),
            }
        ),
        201,
    )


@product_bp.route("/products", methods=["DELETE"])
@require_api_key
def delete_product():
    """ """
    data = request.json
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Produkt-ID ist erforderlich."}), 400

    try:
        oid = ObjectId(product_id)
    except:
        return jsonify({"error": "Ungültige Produkt-ID"}), 400

    delete_result = mongo.db.products.delete_one({"_id": oid})
    if delete_result.deleted_count == 0:
        return jsonify({"error": "Produkt nicht gefunden"}), 404

    return jsonify({"message": "Produkt erfolgreich gelöscht"}), 200
