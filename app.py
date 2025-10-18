from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import io
import base64

app = Flask(__name__)
model = tf.keras.models.load_model('modelo_bilstm_20251018_105948.h5')

# Ajusta esto a la entrada de tu modelo
IMG_SIZE = (64, 64)  

label_dict = {
    1: "Year 1", 2: "Year 2", 3: "Year 3", 4: "Day 1", 5: "Day 2", 6: "Day 3", 7: "Week 1", 8: "Week", 9: "Yesterday", 10: "Day before yesterday",
    11: "Safe", 12: "Physiotherapy", 13: "Idea", 14: "Stamp", 15: "Record", 16: "Effort", 17: "Defend", 18: "Physical education", 19: "Bodybuilding",
    20: "Battle", 21: "Close", 22: "Screw up", 23: "Bicycle", 24: "Slip", 25: "Always", 26: "Build", 27: "Calumny", 28: "Work", 29: "Television",
    30: "Love", 31: "Learn", 32: "Analyze", 33: "Talk", 34: "Cock", 35: "Hen", 36: "Interact", 37: "Exchange",
    38: "Strong wind", 39: "Weak wind", 40: "Strong rain", 41: "Weak rain", 42: "Run fast", 43: "Run slow", 44: "Takes great care",
    45: "Takes a little care", 46: "Thin", 47: "Fat", 48: "Strong", 49: "Weak", 50: "Arrive", 51: "Win", 52: "Loss",
    53: "Open", 54: "Nothing", 55: "Nobody", 56: "Not"
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    image_data = base64.b64decode(data['image'].split(',')[1])
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    image = image.resize(IMG_SIZE)
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    confidence = float(np.max(prediction[0]))
    label = label_dict.get(int(predicted_class), 'Desconocido')

    return jsonify({'class': int(predicted_class), 'label': label, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)
