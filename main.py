from flask import Flask, request, send_file
import os
from utils import require_api_key, remove_background, INPUT_FOLDER

app = Flask(__name__)


@app.route('/remove-bg', methods=['POST'])
@require_api_key
def remove_bg_endpoint():
    if 'image' not in request.files:
        return {
            'status': False,
            'error': 'No image file provided'
        }, 400

    file = request.files['image']
    if file.filename == '':
        return {
            'status': False,
            'message': 'No selected file'
        }, 400

    # if not file.filename.endswith("png"):
    #     return {
    #         "status": False,
    #         "message:": "Image must be in the form of PNG."
    #     }
    # Save the original image
    input_path = os.path.join(INPUT_FOLDER, file.filename)
    file.save(input_path)

    # Process the image to remove background
    output_path = remove_background(input_path)

    # Return the processed image
    return send_file(output_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
