from flask import Flask, request, jsonify, send_file, render_template
from model import synthesize_image
import io
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    image = request.files['image']
    input_image = Image.open(image)

    # Synthesize the image using the model
    output_tensor = synthesize_image(input_image)
    output_image = Image.fromarray(output_tensor.mul(255).byte().numpy().squeeze())

    # Save to a BytesIO object and return as response
    img_io = io.BytesIO()
    output_image.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
