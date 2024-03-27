from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']
    

@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        #Return all products wrapped in an object with a 'prodcuts' key
        return jsonify({"products":products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        #If a specific product is requested,
        #wrap it in an object with a 'products' key
        #