import psycopg2
import numpy as np
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print("Database connection error:", e)
        return None

def run_select_query():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products where type='Sofa'")
        rows = cursor.fetchall()
        print(rows)
    except Exception as e:
        print("Select query error:", e)
        return "Error fetching data."

def add_product(product_id, name, description, product_type, images, embedding, price, status):
   try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO public.products(
                id, name, description, type, images, embedding, price, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (product_id, name, description, product_type, images, embedding, price, status)
        cursor.execute(query, values)
        conn.commit()
        print("Insert successful")
        return True
   except Exception as e:
        print("Insert error:", e)
        return False
   finally:
        if conn:
            conn.close()
            
def get_product_id():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM products")
        row = cursor.fetchone()
        if(row[0] == None):
            return 101
        return row[0]+1
    except Exception as e:
        print("Select query error:", e)
        return "Error fetching data."
    finally:
        if conn:
            conn.close()
def decode_embedding(embedding):
    embedding_string = embedding  # Replace with your actual string
    embedding_bytes = bytes.fromhex(embedding_string)
    embedding_array = np.frombuffer(embedding_bytes, dtype=np.float32)
    return embedding_array
    

def get_product_by_id(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()  # Fetch the first matching row
        if product:
            # Convert the product data to a dictionary
            product_data = {
                "id": product[0],
                "name": product[1],
                "description": product[2],
                "type": product[3],
                "images": product[4],
                "price": product[6],
                "status": product[7]
            }
            return product_data
        else:
            return None
    except Exception as e:
        print("Database query error:", e)
        return None
    finally:
        if conn:
            conn.close()
            
def get_product_embeddings_by_type(type):
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM products WHERE type = '{type}'"
        cursor = conn.cursor()
        cursor.execute(query)
        product_data = []
        products = cursor.fetchall()
        for product in products:
            embedding = decode_embedding(product[5])
            product_data.append([product[0], embedding])
        return product_data
        
    except Exception as e:
        print("Database query error:", e)
        return None
    finally:
        if conn:
            conn.close()

def  get_products_by_type(type):
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM products WHERE type = '{type}'"
        cursor = conn.cursor()
        cursor.execute(query)
        product_data = []
        products = cursor.fetchall()
        for product in products:
            product_dict = {
                "id": product[0],
                "name": product[1],
                "description": product[2],
                "type": product[3],
                "images": product[4],
                "price": product[6],
                "status": product[7]
            }
            product_data.append(product_dict)
        return product_data
    except Exception as e:
        print("Database query error:", e)
        return None
        
    
def fetch_distinct_types():
    try:
        conn = get_db_connection()
        query = "SELECT DISTINCT type FROM products"
        cursor = conn.cursor()
        cursor.execute(query)
        types = cursor.fetchall()
        types = [type[0] for type in types]
        return types
    except Exception as e:
        print("Database query error:", e)
        return None
    finally:
        if conn:
            conn.close()
