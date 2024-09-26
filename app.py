from flask import Flask, request, jsonify
from PIL import Image
from rembg import remove
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Read the image file
    image_file = request.files['image']
    image = Image.open(image_file.stream)

    # Remove background
    img_no_bg = remove(image)

    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    img_no_bg.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    print("Successfull api call")
    # Return the image without background as a response
    return (
        img_byte_arr.read(),
        200,
        {'Content-Type': 'image/png'}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
