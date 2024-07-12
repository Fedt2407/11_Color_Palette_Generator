from flask import Flask, render_template, request
import numpy as np
from PIL import Image
from collections import Counter
import os
import webcolors

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('upload.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('upload.html', error='No selected file')

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        img = Image.open(file_path)
        img_array = np.array(img)

        # Flatten the image array
        reshaped_img = img_array.reshape(-1, img_array.shape[-1])

        # Count the occurrences of each color
        counts = Counter(map(tuple, reshaped_img))

        # Get the 10 most common colors
        most_common_colors = counts.most_common(10)
        
        # Calculate total pixels
        total_pixels = reshaped_img.shape[0]

        # Prepare the result data
        result_data = []
        for color, count in most_common_colors:
            percentage = (count / total_pixels) * 100
            hex_color = webcolors.rgb_to_hex(color)
            result_data.append({'color': hex_color, 'percentage': round(percentage, 2)})

        return render_template('upload.html', result=result_data, image_path=file_path)

    return render_template('upload.html', error='Invalid file type')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    app.run(debug=True)
