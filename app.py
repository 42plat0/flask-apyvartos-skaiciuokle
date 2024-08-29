import os

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from static.modules.detector.detector import CoinDetector
from static.modules.database.database import Database

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
ORIGINAL_PHOTOS = "uploads"
PREDICTIONS_FOLDER = "predictions"
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")

app = Flask(__name__)

IMAGE_FOLDER = os.path.join(app.static_folder, "images/")

app.config["UPLOAD_FOLDER"] = IMAGE_FOLDER

DATABASE = "apyvarta.db"
db = Database("coins", DATABASE)

model = "best.pt"
model_path = os.path.join(
    app.static_folder, os.path.join("modules/detector", "best.pt"))
cd = CoinDetector(model_path)


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
            original_image = os.path.join(
                os.path.join(app.config["UPLOAD_FOLDER"] + ORIGINAL_PHOTOS), filename)

            # To retrieve from db easily
            date = secure_filename(date)
            # Save original image
            file.save(original_image)

            prediction_folder = os.path.join(app.config["UPLOAD_FOLDER"], PREDICTIONS_FOLDER)

            prediction_img = os.path.join("/static/images/predictions/", filename)

            coin_count = cd.get_coin_count(original_image, prediction_folder)

            db.write("INSERT INTO coins (date, coins_counted, is_correct) VALUES(?,?,?)",
                     (date, coin_count, None))

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
        prediction_img = request.form.get(
            "prediction_img").split("/")[-1].split("_")
        # Get saved in db name
        saved_img = prediction_img[-2] + "_" + prediction_img[-1].split(".")[0]

        correct_prediction = request.form.get("correct")
        incorrect_prediction = request.form.get("incorrect")

        if correct_prediction:
            status = True

        elif incorrect_prediction:
            status = False

        db.write("UPDATE coins SET is_correct=? WHERE date = ?",
                 (status, saved_img))

        return redirect("/")

    return render_template("photo.html")
