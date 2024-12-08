from flask import request, jsonify, Blueprint, Response
from bson.objectid import ObjectId
import base64
from io import BytesIO
import gridfs

product_api = Blueprint("product_api", __name__)


@product_api.route("/get_product/<product_id>", methods=["GET"])
def get_product(product_id):
    from app import mongo

    fs = gridfs.GridFS(mongo.db)

    try:
        metadata = mongo.db.image_metadata.find_one({"_id": ObjectId(product_id)})

        if not metadata:
            return jsonify({"error": "Product not found"}), 404

        file_id = metadata.get("file_id")
        try:
            image_file = fs.get(file_id)
        except gridfs.errors.NoFile:
            return jsonify({"error": "Image not found"}), 404

        img_data = image_file.read()
        img_base64 = base64.b64encode(img_data).decode("utf-8")

        product_data = {
            "name": metadata["name"],
            "price": metadata["price"],
            "rating": metadata["rating"],
            "image": f"data:image/png;base64,{img_base64}",
        }

        return jsonify(product_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_api.route("/get_all_products", methods=["GET"])
def get_all_products():
    from app import mongo

    fs = gridfs.GridFS(mongo.db)

    start_index = int(request.args.get("start_index", 0))
    end_index = int(request.args.get("end_index", 4))

    if start_index < 0 or end_index < 0:
        return jsonify({"error": "start_index and end_index must be non-negative"}), 400
    if start_index >= end_index:
        return jsonify({"error": "start_index must be less than end_index"}), 400

    print(f"Getting products from {start_index} to {end_index}")

    try:
        products = []
        metadata_list = mongo.db.image_metadata.find().skip(start_index).limit(end_index - start_index)

        for metadata in metadata_list:
            file_id = metadata.get("file_id")
            try:
                image_file = fs.get(file_id)
            except gridfs.errors.NoFile:
                return jsonify({"error": "Image not found"}), 404
            img_data = image_file.read()
            img_base64 = base64.b64encode(img_data).decode("utf-8")

            product = {
                "name": metadata["name"],
                "price": metadata["price"],
                "rating": metadata["rating"],
                "image": f"data:image/png;base64,{img_base64}",
            }
            products.append(product)

        return jsonify(products)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
