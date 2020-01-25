import io
import os
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

# Setup Google Cloud Vision API and blacklisted labels
client = vision.ImageAnnotatorClient()
black_list = ["Cuisine", "Ingredient", "Dish", "Food", "Noodle", "Rice noodles", "Soup", "Fruit", "Dessert", "Snack cake", "Baked goods", "None", "Produce", "Staple food", "Recipe"]


@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    file_name = secure_filename(f.filename)
    dirName = 'tempDir'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    f.save(os.path.join(dirName, file_name))
    dishes = identify_dish(file_name)
    print(dishes)
    return "Dish name: {}\nConfidence: {}".format(dishes[0][0], dishes[0][1])

def identify_dish(img_file_name):
    file_name = os.path.abspath("tempDir/" + img_file_name)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    results = []
    for label in labels:
        if label.description not in black_list:
            results.append((label.description, label.score))
    
    return results


app.run(port=5000,debug=True)
