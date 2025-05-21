from flask import Flask, request, jsonify, send_from_directory
from embed_utils import encode_text, encode_image, load_faiss_index, search_similar
from PIL import Image
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)

index, metadata = load_faiss_index()

@app.route('/search', methods=['POST'])
def search():
    if 'query_text' in request.form and request.form['query_text']:
        query = request.form['query_text']
        emb = encode_text(query)
    elif 'query_image' in request.files:
        image = Image.open(request.files['query_image'])
        emb = encode_image(image)
    else:
        return jsonify({'error': 'Invalid input'}), 400

    results = search_similar(emb, index, metadata)
    return jsonify({'results': results})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True,port=5010)
