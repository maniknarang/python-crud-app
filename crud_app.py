from flask import Flask, request, jsonify

app = Flask(__name__)
storage = {}

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(list(storage.values())), 200

@app.route("/item/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = storage.get(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/item", methods=["POST"])
def create_item():
    data = request.json
    item_id = len(storage) + 1
    item = {"id": item_id, "name": data["name"], "value": data["value"]}
    storage[item_id] = item
    return jsonify(item), 201

@app.route("/item/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id in storage:
        data = request.json
        return jsonify(storage[item_id]), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/item/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id in storage:
        del storage[item_id]
        return jsonify({"message": "Deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
