from flask import Flask, render_template, request, url_for
import numpy as np
from PIL import Image
from collections import Counter
import io
import os

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

        colors, counts = np.unique(img_array.reshape(-1, 3), axis=0, return_counts=True)
        sorted_indices = np.argsort(-counts)[:10]
        top_colors = colors[sorted_indices]
        total_pixels = img_array.shape[0] * img_array.shape[1]

        percentages = [(count / total_pixels) * 100 for count in counts[sorted_indices]]

        result_data = [{'color': tuple(color), 'percentage': round(percentage, 2)} for color, percentage in zip(top_colors, percentages)]

        return render_template('upload.html', result=result_data, image_path=file_path)

    return render_template('upload.html', error='Invalid file type')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    app.run(debug=True)
