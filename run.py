import io
import os
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests
app = Flask(__name__)

# Setup Google Cloud Vision API and blacklisted labels
client = vision.ImageAnnotatorClient()
black_list = ["Cuisine", "Ingredient", "Dish", "Food", "Noodle", "Rice noodles", "Soup", "Fruit", "Dessert", "Snack cake", "Baked goods", "None", "Produce", "Staple food", "Recipe"]


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    file_name = secure_filename(f.filename)
    dirName = 'tempDir'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    f.save(os.path.join(dirName, file_name))
    dishes = identify_dish(file_name)
    recipies = getRecipe(dishes[0][0])
    recipiesVideos = getRecipeVideos(dishes[0][0])
    recipies_list = []
    recipiesVideos_list = []
    for recipeVideo in recipiesVideos["videos"]:
      recipiesVideos_list.append([
        recipeVideo["title"],
        "https://www.youtube.com/watch?v="+recipeVideo["youTubeId"],
        recipeVideo["thumbnail"],
        recipeVideo["views"]
      ])
    for recipe in recipies["results"]:
      recipies_list.append([
        recipe["title"],
        recipe["readyInMinutes"],
        recipe["servings"],
        recipe["image"],
        recipe["imageUrls"],
        getRecipeIngredients(recipe["id"])
      ])
    print(recipies_list)
    return render_template("results.html", recipies=recipies_list, recipiesVideos=recipiesVideos_list)
    # return recipe+"</br>Dish name: {}\nConfidence: {}".format(dishes[0][0], dishes[0][1])

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

def getRecipe(image_dish_name):
  url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
  querystring = {"query":image_dish_name}
  headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': "2246a2d1e7msh226333d4b7b13aap12376cjsnc5cb7fc432e8"
      }
  response = requests.request("GET", url, headers=headers, params=querystring)
  return response.json()

def getRecipeVideos(image_dish_name):
  url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/videos/search"
  querystring = {"query":image_dish_name}
  headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': "2246a2d1e7msh226333d4b7b13aap12376cjsnc5cb7fc432e8"
      }
  response = requests.request("GET", url, headers=headers, params=querystring)
  # print(response)
  return response.json()

def getRecipeIngredients(recipeId):
  url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+str(recipeId)+"/ingredientWidget"
  querystring = {"defaultCss":"false"}
  headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': "2246a2d1e7msh226333d4b7b13aap12376cjsnc5cb7fc432e8",
      'accept': "text/html"
      }
  response = requests.request("GET", url, headers=headers, params=querystring)
  return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0')

