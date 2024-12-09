from flask import Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routers.Products.products import product_api
import gridfs
import csv
import os

app = Flask(__name__)

load_dotenv()
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)
CORS(app)

fs = gridfs.GridFS(mongo.db)
metadata_collection = mongo.db["image_metadata"]

app.register_blueprint(product_api, url_prefix="/products/v1")


@app.route("/", methods=["GET"])
def home():
    return "Hello World!! This is Product API"

# @app.route("/upload_images", methods=["GET"])
# def upload_images():
#     image_folder = 'assets/' 
#     csv_file = 'metadata.csv'

#     if not os.path.exists(csv_file):
#         return jsonify({"error": "CSV file not found!"}), 400
    
#     with open(csv_file, 'r') as file:
#         csv_reader = csv.reader(file)
#         next(csv_reader)
        
#         for index, row in enumerate(csv_reader, start=1):
#             print(f"Processing row {index}: {row}")
#             image_path = os.path.join(image_folder, f'SamplePic{index}.png')
#             if not os.path.exists(image_path):
#                 return jsonify({"error": f"Image {image_path} not found!"}), 400
#             try:
#                 name = row[0]
#                 price = float(row[1])
#                 rating = float(row[2])
#             except ValueError as e:
#                 return jsonify({"error": f"Invalid data in CSV row {index}: {e}"}), 400
            
#             upload_image(image_path, name, price, rating)
    
#     return jsonify({'message': 'All images and metadata uploaded successfully'}), 200

# def upload_image(image_path, name, price, rating):
#     with open(image_path, 'rb') as img_file:
#         img_data = img_file.read()

#     file_id = fs.put(img_data, filename=os.path.basename(image_path))

#     metadata = {
#         'name': name,
#         'price': price,
#         'rating': rating,
#         'file_id': file_id  
#     }

#     metadata_collection.insert_one(metadata)

if __name__ == "__main__":
    app.run(debug=True)
