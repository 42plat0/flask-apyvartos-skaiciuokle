import os

from datetime import datetime
from cs50 import SQL 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

from detector import detect_coins


DATE_FORMAT = "%Y-%m-%d %H:%S:%M"
IMAGE_FOLDER = "/static/images/"
ORIGINAL_PHOTOS = "uploads/"
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_DIR + IMAGE_FOLDER

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def index():
    return render_template("detect_coin.html")

@app.route("/detect_coin", methods=["GET", "POST"])
def detect_coin():
    print(1)
    if request.method == "POST":
        print("Hello naxuiko")
        name = "coin_image"

        if name not in request.files:
            return "No photo was uploaded"
        
        file = request.files[name]
        print(file)
        if file.filename == "":
            return "No photo was uploaded"

        if file:
            file = request.files["coin_image"]
            date = datetime.now().strftime(DATE_FORMAT)
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"] + ORIGINAL_PHOTOS, filename)
            
            # # Save original image
            file.save(path)


            # # Pass image to model
            coin_count = detect_coins(path, app.config["UPLOAD_FOLDER"])

            prediction_img = IMAGE_FOLDER + "/predictions/" + filename
        
            return render_template("photo.html", prediction_img=prediction_img, coin_count=coin_count, csrf_token=csrf)
        
    return render_template("detect_coin.html") 


@app.route("/photo")
def photo():
    print(1)