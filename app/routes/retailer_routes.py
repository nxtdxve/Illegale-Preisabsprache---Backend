from flask import jsonify, Response
from bson.json_util import dumps
from app.database.db_connection import mongo
from bson.objectid import ObjectId
from . import retailer_bp


@retailer_bp.route('/retailers', methods=['GET'])
def list_retailers():
    retailers = mongo.db.retailers.find()
    return Response(dumps(retailers), mimetype='application/json')

""" @retailer_bp.route('/retailers', methods=['POST'])
def add_retailer():
    retailer_data = request.json
    result = mongo.db.retailers.insert_one(retailer_data)
    return jsonify({'message': 'Retailer added successfully', 'retailerId': str(result.inserted_id)}) """

@retailer_bp.route('/retailers/<id>', methods=['GET'])
def get_retailer(id):
    retailer = mongo.db.retailers.find_one({'_id': ObjectId(id)})
    if retailer:
        return Response(dumps(retailer), mimetype='application/json')
    else:
        return jsonify({'error': 'Retailer not found'}), 404
