from ultralytics import YOLO

from pathlib import Path

def detect_coins(url, img_save_folder):
    # Load a model
    # Add absoulute path to always find model
    model = YOLO("object_detection_model_160.pt")  

    # run model on uploaded photo

    coin_detector = model.predict(
        url,
        save=True,
        conf=0.3,
        show_labels=False,
        project=img_save_folder,
        name="predictions")

            
    for prediction_photo in coin_detector: 
        coin_count = len(prediction_photo.boxes)

    
    return coin_count


# TODO: removinti nuotraukos background 
# TODO: apkarpyti nuotrauka, kad sumazinti atstuma iki monetos (pvz. lyginant jos dydi)
# TODO: sukurti API endpointa i kuri gali kreiptis su nuotrauka




