import os

from datetime import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from detector import detect_coins


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
IMAGE_FOLDER = "/static/images/"
ORIGINAL_PHOTOS = "uploads/"
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_DIR + IMAGE_FOLDER

DATABASE = "apyvarta.db"

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

class Database():
    def __init__(self):
        self.coin_table = "coins"

        db = sqlite3.connect(DATABASE)

        # Check if table doesn't already exist
        table = db.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='{self.coin_table}'")
        
        if not table:
            db.execute(f"CREATE TABLE {self.coin_table}(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date TEXT NOT NULL, coins_counted INTEGER NOT NULL, is_correct BOOLEAN)")
        
        db.close()
    
    def write(self, command, values):
        db = sqlite3.connect(DATABASE)
        db.execute(command, values)
        db.commit()
        db.close()

db = Database()

@app.route("/")
def index():
    return redirect("/detect_coin")

@app.route("/detect_coin", methods=["GET", "POST"])
def detect_coin():
    global db

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
            
            # To retrieve from db easily
            date = secure_filename(date)
            # # Save original image
            file.save(path)

            # # Pass image to model
            coin_count = detect_coins(path, app.config["UPLOAD_FOLDER"])

            prediction_img = IMAGE_FOLDER + "/predictions/" + filename
            
            db.write("INSERT INTO coins (date, coins_counted, is_correct) VALUES(?,?,?)", (date, coin_count, None))

            return redirect(url_for("photo", prediction_img=prediction_img, coin_count=coin_count))
        
    return render_template("index.html") 


@app.route("/photo")
def photo():

    prediction_img = request.args["prediction_img"]
    coin_count = request.args["coin_count"]

    return render_template("photo.html", prediction_img=prediction_img, coin_count=coin_count)

@app.route("/result", methods=["GET", "POST"])
def result():
    global db

    if request.method == "POST":
        prediction_img = request.form.get("prediction_img").split("/")[-1].split("_")

        # Get saved in db name
        saved_img = prediction_img[-2] + "_" + prediction_img[-1].split(".")[0]

        correct_prediction = request.form.get("correct")
        incorrect_prediction = request.form.get("incorrect")

        if correct_prediction:
            status = True

        elif incorrect_prediction:
            status = False

        db.write("UPDATE coins SET is_correct=? WHERE date = ?", (status, saved_img))

        return render_template("thank_you.html")
    
    return render_template("photo.html")

