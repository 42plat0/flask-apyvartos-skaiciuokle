import os

from datetime import datetime
from cs50 import SQL 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from detector import detect_coins


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
IMAGE_FOLDER = "/static/images/"
ORIGINAL_PHOTOS = "uploads/"
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_DIR + IMAGE_FOLDER

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQL("sqlite:///apyvarta.db")

@app.route("/")
def index():
    return redirect("/detect_coin")

@app.route("/detect_coin", methods=["GET", "POST"])
def detect_coin():

    if request.method == "POST":

        name = "coin_image"

        if name not in request.files:
            return "No photo was uploaded"
        
        file = request.files[name]

        if file.filename == "":
            return "No photo was uploaded"

        if file:

            date = datetime.now().strftime(DATE_FORMAT)
            filename = secure_filename(f"my_image_{date}.jpg")
            path = os.path.join(app.config["UPLOAD_FOLDER"] + ORIGINAL_PHOTOS, filename)
            
            # # Save original image
            file.save(path)


            # # Pass image to model
            coin_count = detect_coins(path, app.config["UPLOAD_FOLDER"])

            prediction_img = IMAGE_FOLDER + "/predictions/" + filename
            
            db.execute("INSERT INTO coins (photo_name, date, coin_count, is_correct) VALUES(?,?,?,?)", 
                       filename, date, coin_count, None)
            
            return redirect(url_for("photo", prediction_img=prediction_img, coin_count=coin_count))
        
    return render_template("index.html") 


@app.route("/photo")
def photo():

    prediction_img = request.args["prediction_img"]
    coin_count = request.args["coin_count"]

    return render_template("photo.html", prediction_img=prediction_img, coin_count=coin_count)

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        prediction_img = request.form.get("prediction_img").split("/")[-1]

        correct_prediction = request.form.get("correct")
        incorrect_prediction = request.form.get("incorrect")

        if correct_prediction:
            status = True

        elif incorrect_prediction:
            status = False

        
        db.execute("UPDATE coins SET is_correct=? WHERE photo_name = ?", status, prediction_img)

        return render_template("thank_you.html")
    
    return render_template("photo.html")

