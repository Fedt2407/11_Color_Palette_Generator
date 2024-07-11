from flask import Flask, render_template, request
import numpy as np
from PIL import Image
from collections import Counter
import io

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Checks if the file is uploaded
    if 'file' not in request.files:
        return render_template('upload.html', error='No file part')

    file = request.files['file']

    # Checks if the file is empty
    if file.filename == '':
        return render_template('upload.html', error='No selected file')

    # Checks if the file is a valid image file
    if file and allowed_file(file.filename):
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Converts the image to RGB mode
        img_array = np.array(img)

        # Resize the image to 100x100 pixels
        small_img = img.resize((100, 100))
        small_img_array = np.array(small_img)

        # Extract the 10 most common colors from the image
        colors, counts = np.unique(small_img_array.reshape(-1, 3), axis=0, return_counts=True)
        sorted_indices = np.argsort(-counts)[:10] # Sort in descending order
        top_colors = colors[sorted_indices]
        total_pixels = small_img_array.shape[0] * small_img_array.shape[1]

        # Caculates the percentage of each color
        percentages = [(count / total_pixels) * 100 for count in counts[sorted_indices]]

        # Prepare the data to be displayed
        result_data = [{'color': tuple(color), 'percentage': round(percentage, 2)} for color, percentage in zip(top_colors, percentages)]

        return render_template('result.html', result=result_data)

    return render_template('upload.html', error='Invalid file type')

# Checks if the file is a valid image file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    app.run(debug=True)
