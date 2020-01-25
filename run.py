import io
import os
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, render_template
app = Flask(__name__)

# Setup Google Cloud Vision API and blacklisted labels
client = vision.ImageAnnotatorClient()
black_list = ["Cuisine", "Ingredient", "Dish", "Food", "Noodle", "Rice noodles", "Soup", "Fruit"]


@app.route('/')
def hello_world():
    return render_template("home.html")


def identify_dish(img_file_name):
    file_name = os.path.abspath("images/" + img_file_name)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    for label in labels:
        if label.description not in black_list:
            return label


app.run(port=5000)
