import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def load_backend_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_collection():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not configured. Add your MongoDB Atlas connection string.")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    db_name = os.getenv("MONGO_DB", "flask_assignment")
    collection_name = os.getenv("MONGO_COLLECTION", "submissions")
    return client[db_name][collection_name]

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()

    if not item_name or not item_description:
        return jsonify({
            "error": "Item Name and Item Description are required."
        }), 400

    try:
        collection = get_collection()
        result = collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return jsonify({
            "message": "To-Do item saved successfully.",
            "insertedId": str(result.inserted_id)
        }), 201

    except (RuntimeError, PyMongoError) as exc:
        return jsonify({"error": f"Database error: {exc}"}), 500
    

@app.route("/api")
def api():
    try:
        return jsonify(load_backend_data())
    except (OSError, json.JSONDecodeError) as exc:
        return jsonify({"error": f"Unable to read backend data: {exc}"}), 500


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            error = "All fields are required."
            return render_template("index.html", error=error, form=request.form), 400

        try:
            collection = get_collection()
            collection.insert_one({
                "name": name,
                "email": email,
                "message": message
            })
            return redirect(url_for("success"))
        except (RuntimeError, PyMongoError) as exc:
            error = f"Database error: {exc}"
            return render_template("index.html", error=error, form=request.form), 500

    return render_template("index.html", error=error, form={})


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/todo")
def todo_page():
    return render_template("todo.html")

if __name__ == "__main__":
    app.run(debug=True)
