from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import cv2
import db

def get_embedding(img_path,model = ResNet50(include_top=False, weights='imagenet', pooling='avg')):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds[0]

def calculate_cosine_similarity(embedding1, embedding2):
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    similarity_matrix = cosine_similarity(embedding1, embedding2)
    similarity = similarity_matrix[0][0]
    return similarity

def fetch_similar_products(image_path,type):
    try:
        embedding = get_embedding(image_path)
    except Exception as e:
        print("Embedding error:", e)
        return "Some issue with the image occured"
    products = db.get_product_embeddings_by_type(type)
    similar_products = []
    for product in products:
        similarity = calculate_cosine_similarity(embedding, product[1])
        similar_products.append((product[0],similarity))
    similar_products.sort(key=lambda x: x[1], reverse=True)
    return similar_products


def fetch_similar_for_class(type,embeddings):
    if(embeddings == []):
        return None
    type = type.lower()
    print("Type:",type)
    print("Embeddings:",embeddings)
    products = db.get_product_embeddings_by_type(type)
    print("Products:",products)
    similar_products = []
    for product in products:
        for embedding in embeddings:
            similarity = calculate_cosine_similarity(embedding, product[1])
            if(similarity > 0.5):
                similar_products.append((product[0],similarity))
    similar_products.sort(key=lambda x: x[1], reverse=True)
    print("Similar products:",similar_products)
    return similar_products
