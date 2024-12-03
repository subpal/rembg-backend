from flask import Flask, request, jsonify
from PIL import Image
from rembg import remove
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        # Read the image file
        image_file = request.files['image']
        image = Image.open(image_file.stream)

        # Remove background
        img_no_bg = remove(image)

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        scale_percentage = 50
        new_width = int(img_no_bg.width * scale_percentage / 100)
        new_height = int(img_no_bg.height * scale_percentage / 100)
        img_no_bg = img_no_bg.resize((new_width, new_height))
        img_no_bg.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return (
            img_byte_arr.read(),
            200,
            {'Content-Type': 'image/png'}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/convert', methods=['POST'])
def convert_image():
    try:
        # Get the image and target format from the request
        image_file = request.files.get('image')
        target_format = request.form.get('format')

        if not image_file or not target_format:
            return jsonify({"error": "Image file and target format are required"}), 400

        # Open the image using Pillow
        image_file = request.files['image']
        image = Image.open(image_file.stream)

        # Create a BytesIO object to save the converted image
        converted_image = io.BytesIO()
        image.save(converted_image, format=target_format.upper())
        converted_image.seek(0)

        # Return the converted image as a response
        return (
            converted_image.read(),
            200,
            {'Content-Type': 'image/png'}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
