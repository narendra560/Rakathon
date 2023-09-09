from flask import Flask, request, jsonify, render_template
import psycopg2
import db
import embedder
import object_detector
from collections import defaultdict

app = Flask(__name__)

query_dict = {
    '1':"/Users/narendra/Rakathon/Images/rakathon/sofa/sofa12.jpg",
    '2':"/Users/narendra/Rakathon/Images/rakathon/sofa/sofa13.jpg",
    '3':"/Users/narendra/Rakathon/Images/rakathon/bed/bed2.png",
    '4':"/Users/narendra/Rakathon/Images/rakathon/bed/bed4.jpg",
    '5':"/Users/narendra/Rakathon/Images/rakathon/chair/c1.jpg",
    '6':"/Users/narendra/Rakathon/Images/rakathon/chair/c2.jpg",
    '7':"/Users/narendra/Rakathon/Images/rakathon/table/t1.jpg"
}
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def products():
    return render_template('content.html')


@app.route('/add/product', methods=['POST'])
def add_new_product():
    try:
        data = request.json
        product_id = db.get_product_id()
        name = data.get('name')
        description = data.get('description')
        product_type = data.get('product_type').lower()
        images = data.get('images')
        embedding = None
        try:
             embedding = object_detector.find_product_embedding(images[0])
             embedding_bytes = embedding.tobytes()
             embedding = embedding_bytes.hex() 
        except Exception as e:
                print("Embedding error:", e)
                return jsonify({'message': 'Some issue with the image occured'}), 500
        
        price = data.get('price')
        status = data.get('status')
        result = db.add_product(product_id, name, description, product_type, images, embedding, price, status)
        if result:
            return jsonify({'message': 'Product inserted successfully','product_id':product_id}), 201
        else:
            return jsonify({'message': 'Failed to insert product'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get/products', methods=['GET'])
def get_products():
    try:
        query = request.args.get('query')
        print("query "+query)
        result = defaultdict(list)
        if(query == None):
            types = db.fetch_distinct_types()
            for type in types:
                products = db.get_products_by_type(type)
                result[type] = products
        else:
            embeddings = object_detector.find_embeddings_for_query(query_dict[query])
            for c in embeddings:
                products = embedder.fetch_similar_for_class(c,embeddings[c])
                products = [find_product(p[0]) for p in products]
                result[c] = products
        return jsonify(result), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
def find_product(id):
    try:
        product = db.get_product_by_id(id)
        return product
    except Exception as e:
        return None
    
if __name__ == '__main__':
    app.run(debug=True)
