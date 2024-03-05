from flask import Flask, jsonify, request
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId 
import bson.json_util as json_util
from dotenv import load_dotenv, find_dotenv
import os
import pprint


app = Flask(__name__)



##################### connect mongo

password = os.environ.get("MONGODB_PWD")
# MongoDB Atlas connection URI
MONGO_URI = f"mongodb+srv://survey-api:{password}@survey-api.hrdb54w.mongodb.net/?retryWrites=true&w=majority"

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Select database
db = client.get_database("Survey_data")

# Select collection
collection = db.get_collection("user_demographics")

# Route to create a new document
@app.route('/add', methods=['POST'])
def create_document():
    data = request.json
    if data:
        # Insert document into collection
        result = collection.insert_one(data)
    ##   x = mycol.insert_many(mylist)
    #print list of the _id values of the inserted documents:
    ## print(x.inserted_ids)
        if result.inserted_id:
            return jsonify({"message": "Document created successfully", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"message": "Failed to create document"}), 500
    else:
        return jsonify({"message": "No data provided"}), 400

# Route to get all documents
@app.route('/read', methods=['GET'])
def get_all_documents():
    documents = list(collection.find())
   # return jsonify(documents), 200
    return json_util.dumps(documents) , 200

# Route to get a single document by ID
@app.route('/read/<id>', methods=['GET'])
def get_document(id):
    document = collection.find_one({"_id": ObjectId(id)})
    if document:
     #   return jsonify(document), 200
        return json_util.dumps(document) , 200
    else:
        return jsonify({"message": "Document not found"}), 404

# Route to update a document
@app.route('/update/<id>', methods=['PUT'])
def update_document(id):
    data = request.json
    if data:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Document updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update document"}), 500
    else:
        return jsonify({"message": "No data provided"}), 400

# Route to delete a document
@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted successfully"}), 200
    else:
        return jsonify({"message": "Failed to delete document"}), 500



@app.route('/')
def home():
    return "hello"

if __name__ == '__main__':
    app.run(port=5555, debug=True)




   