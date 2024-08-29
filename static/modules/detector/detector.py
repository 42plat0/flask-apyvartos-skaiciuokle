from ultralytics import YOLO

from ..stringparse.stringparse import delete_string_end

class CoinDetector():
    def __init__(self, weights):
        # Load a model
        self.model = YOLO(weights)

    def get_coin_count(self, image_path, save_path):
        return self.run(image_path, save_path)

    def run(self, image_path, save_path):
        save_folder = save_path.split("/")[-1]
        save_path = delete_string_end(save_path, save_folder)
        
        '''
        IN /ultralytics/cfg/__init__.py
        Line 361, change FROM 
            save_dir = increment_path(Path(project) / name, exist_ok=args.exist_ok if RANK in {-1, 0} else True)
        TO
            save_dir = Path(project) / name 
        This avoids creating new folders and stores everything IN
            project/name
        '''

        # run model on uploaded photo
        coin_detector = self.model.predict(
            image_path,
            save=True,
            conf=0.3,
            show_labels=False,
            project=save_path,
            name=save_folder,
            exist_ok=True,
            )

        self.detected_objs = coin_detector[0].boxes
        detected_obj_count = len(self.detected_objs)
        
        overlapping_objs = self.get_overlapping_obj_count()

        return detected_obj_count - overlapping_objs
    
    def get_overlapping_obj_count(self):
        self.boxes_xywh = self.detected_objs.xywh
        # Create new list with float values
        boxes = []

        for box in self.boxes_xywh:
            x_coordinates = float(box[0])
            y_coordinates = float(box[1])
            width = float(box[2])
            height = float(box[3])

            box = {
                "x": x_coordinates,
                "y": y_coordinates,
                "w": width,
                "h": height
            }
            boxes.append(box)

        # Check for overlaps
        overlapping_pairs = []

        for i in range(len(boxes)):
            for j in range(i+1, len(boxes)):
                if abs(boxes[i]["x"] - boxes[j]["x"]) < 5 and abs(boxes[i]["y"] - boxes[j]["y"]) < 5:
                    overlapping_pairs.append((boxes[i], boxes[j]))
        
        return len(overlapping_pairs)

# TODO: removinti nuotraukos background 
# TODO: apkarpyti nuotrauka, kad sumazinti atstuma iki monetos (pvz. lyginant jos dydi)
# TODO: sukurti API endpointa i kuri gali kreiptis su nuotrauka


