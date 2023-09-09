from roboflow import Roboflow
import cv2
import embedder
import os
from collections import defaultdict

rf = Roboflow(api_key="hHXxEKbIbxbyFkXiHxUX")
project = rf.workspace().project("furniture-detection-qiufc")
model = project.version(20).model
classes = ['Bed','Chair','Sofa','Table','arm chair', 'bed','sofa','table','chair']
def find_product_embedding(img_path):
    predictions = model.predict(img_path, confidence=50, overlap=30).json()["predictions"]
    segments = []
    for prediction in predictions:
        if(prediction['class'] in classes):
            segments.append(prediction)
    if(segments):
        item = segments[0]
        image_path = item['image_path']
        image = cv2.imread(image_path)
        x = item['x']
        y = item['y']
        width = item['width']
        height = item['height']
        extracted_image = image[y-height//2:y+height//2, x-width//2:x+width//2]
        output_path = "extracted_image.jpg" 
        cv2.imwrite(output_path, extracted_image)
        embedding = embedder.get_embedding(output_path)
        try:
            os.remove(output_path)
            print(f"{output_path} has been successfully deleted.")
        except OSError as e:
            print(f"Error deleting {output_path}: {e}")
        return embedding
    else:
        return embedder.get_embedding(img_path)
    
def find_embeddings_for_query(query):
    class_dict = defaultdict(list)
    predictions = model.predict(query, confidence=50, overlap=30).json()["predictions"]
    segments = []
    for prediction in predictions:
        if(prediction['class'] in classes):
            segments.append(prediction)
    for item in segments:
        image_path = item['image_path']
        image = cv2.imread(image_path)
        x = item['x']
        y = item['y']
        width = item['width']
        height = item['height']
        extracted_image = image[y-height//2:y+height//2, x-width//2:x+width//2]
        class_name = item['class']
        output_path = "extracted_image.jpg" 
        cv2.imwrite(output_path, extracted_image)
        embedding = embedder.get_embedding(output_path)
        class_dict[class_name.lower()].append(embedding)
        try:
            os.remove(output_path)
            print(f"{output_path} has been successfully deleted.")
        except OSError as e:
            print(f"Error deleting {output_path}: {e}")
    return class_dict