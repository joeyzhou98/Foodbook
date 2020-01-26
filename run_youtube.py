
from flask import Flask  
import os
from flask import request, redirect, url_for
from flask import send_from_directory
from flask import render_template
app = Flask(__name__)  

@app.route('/', methods=['GET'])
def uploads_file():
    return render_template('home.html')

app.run(port=5000)
