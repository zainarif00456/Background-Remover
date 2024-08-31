import os
from functools import wraps
from PIL import Image

from flask import request, jsonify
from dotenv import load_dotenv
from rembg import remove

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Paths for input and output images
INPUT_FOLDER = 'static/images'
OUTPUT_FOLDER = 'static/bg-remove'

# Ensure the output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_to_png(image_path):
    img = Image.open(image_path)
    # Convert image to RGBA (which is needed for PNG format)
    img = img.convert("RGBA")

    # Define the output path with .png extension
    output_path = os.path.splitext(image_path)[0] + '.png'
    os.remove(image_path)
    # Save the image as PNG
    img.save(output_path, 'PNG')

    return output_path


def remove_background(image_path):
    if not image_path.lower().endswith('.png'):     # to check if png else convert into png format
        image_path = convert_to_png(image_path)
    with open(image_path, 'rb') as i:
        img_data = i.read()
    result = remove(img_data)

    output_path = os.path.join(OUTPUT_FOLDER, os.path.basename(image_path))
    with open(output_path, 'wb') as o:
        o.write(result)

    return output_path


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the API key from the headers
        api_key = request.headers.get('Authorization')

        if api_key is None:
            return jsonify({
                "status": False,
                'message': 'API key is missing'}
            ), 401

        if api_key != API_KEY:
            return jsonify({
                "status": False,
                'error': 'Invalid API key'}
            ), 403

        return f(*args, **kwargs)

    return decorated_function
