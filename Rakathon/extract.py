import cv2
import embedder
import os

for item in segments:
    image_path = item['image_path']
    image = cv2.imread(image_path)
    
    x = item['x']
    y = item['y']
    width = item['width']
    height = item['height']    
    extracted_image = image[y-height//2:y+height//2, x-width//2:x+width//2]
    extracted_image = cv2.resize(extracted_image, target_size)    
    output_path = "extracted_image.jpg" 
    cv2.imwrite(output_path, extracted_image)
    print(embedder.get_embedding(output_path))  
    try:
        os.remove(output_path)
        print(f"{output_path} has been successfully deleted.")
    except OSError as e:
        print(f"Error deleting {output_path}: {e}")