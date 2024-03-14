from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model('models/terrain_model.h5')

def preprocess_image_data(image_data):
    # Load the image using keras' image module
    img = image.load_img(image_data, target_size=(64, 64))  # Adjust target size as needed
    # Convert the image to an array
    img_array = image.img_to_array(img)
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
            return jsonify({'prediction': decoded_prediction})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

    else:
        return jsonify({'error': 'Method Not Allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)