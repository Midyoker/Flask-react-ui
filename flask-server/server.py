from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

# Load the trained model
model = load_model('models/terrain_model.h5')

def preprocess_image_data(image_data):
    # Open the image using PIL's Image module
    img = Image.open(BytesIO(image_data.read()))
    # Resize the image to the target size
    img = img.resize((64, 64))  # Adjust target size as needed
    # Convert the image to an array
    img_array = np.array(img)
    # Expand the dimensions to match the model's expected input shape
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize the image
    img_array = img_array / 255.0
    return img_array

def decode_prediction(prediction):
    # Assuming prediction is a one-hot encoded array
    # You can decode it based on the index with the highest probability
    # Assuming you have a list of class labels
    class_labels = ['class1', 'class2', 'class3', 'class4']
    decoded_prediction = class_labels[np.argmax(prediction)]
    return decoded_prediction

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        image_data = request.files['image']
        
        # Check if the file is empty
        if image_data.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            processed_data = preprocess_image_data(image_data)
            prediction = model.predict(processed_data)
            decoded_prediction = decode_prediction(prediction)
            
            # Serve the graph image file
            graph_image_path = 'graph.jpg'
            return jsonify({'prediction': decoded_prediction, 'graph': f'http://127.0.0.1:5000/{graph_image_path}'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405

@app.route('/graph.jpg')
def get_graph():
    graph_image_path = os.path.join('models', 'graph.jpg')
    return send_file(graph_image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
