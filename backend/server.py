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
        #Return all products wrapped in an object with a 'products' key
        return jsonify({"products":products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        #If a specific product is requested,
        #wrap it in an object with a 'products' key
        #Note: you might want to change this
        #if you want to return a single product not wrapped in a list
        return jsonify(product) if product else ('', 404)
    
@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

@app.route('/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            updated_product = request.json
            product.update(updated_product)
            with open('products.json', 'w') as f:
                json.dump({"products": products}, f)
            return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/products/remove/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = load_products()
    for index, product in enumerate(products):
        if product['id'] == product_id:
            del products[index]
            with open('products.json', 'w') as f:
                json.dump({"products": products}, f)
            return jsonify({"message": "Product removed successfully"}), 200
    return jsonify({"error": "Product not found"}), 404




@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

if __name__ == '__main__':
    app.run(debug=True)
