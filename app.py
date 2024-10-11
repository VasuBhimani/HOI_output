from flask import Flask, render_template, redirect, url_for, jsonify
import os

app = Flask(__name__)

# Function to group images based on their prefix
def get_grouped_images():
    image_folder = os.path.join(app.static_folder, 'images')
    images = os.listdir(image_folder)
    
    grouped_images = {}
    
    # Loop through the images and group them by their prefix
    for image in images:
        prefix = image.split('_')[0]
        if prefix not in grouped_images:
            grouped_images[prefix] = []
        grouped_images[prefix].append(image)
    
    # Sort the images by their names
    for key in grouped_images:
        grouped_images[key].sort()
    
    return grouped_images

@app.route('/')
def index():
    # Get the grouped images
    images_by_group = get_grouped_images()
    return render_template('index.html', images_by_group=images_by_group)

@app.route('/delete_image/<image_name>', methods=['DELETE'])
def delete_image(image_name):
    # Path to the image file
    image_path = os.path.join(app.static_folder, 'images', image_name)
    
    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            return jsonify({"message": "Image deleted"}), 200
        else:
            return jsonify({"message": "Image not found"}), 404
    except Exception as e:
        return jsonify({"message": "Failed to delete image", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8123)

