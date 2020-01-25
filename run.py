import os
from flask import request, redirect, url_for
from flask import send_from_directory
from flask import Flask, render_template

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
    return render_template("home.html")
'''


# Directories for uploading Image
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set('jpg')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Check if it's an valid extensions.
def allowed_file(filename):
    # check if file name exist "."
    # 1:passed, 0:failed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Receive a file
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    if request.method == 'POST':
        # If there's no file uploaded
        if 'file' not in request.files:
            Flask('No file founded.')
            return redirect(request.url)

        # pull out data
        file = request.files['file']
        print(file)
        print(file.filename)

        # No file
        if file.filename == '':
            Flask('No file founded.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            return redirect(url_for('uploaded_file', filename=file.filename))
    return render_template('home.html')


app.run(port=5000)
