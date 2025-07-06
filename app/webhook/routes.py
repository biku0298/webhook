from flask import Blueprint, request, jsonify, render_template
from app.extensions import collection
from datetime import datetime

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == "push":
        event = {
            "author": payload.get("pusher", {}).get("name"),
            "action": "push",
            "to_branch": payload.get("ref", "").split("/")[-1],
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event)

    elif event_type == "pull_request":
        pr = payload.get("pull_request", {})
        event = {
            "author": pr.get("user", {}).get("login"),
            "action": "merge" if pr.get("merged") else "pull_request",
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event)

    return jsonify({"message": "Webhook received"}), 200

@webhook_bp.route('/get-events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(20))
    for e in events:
        e["_id"] = str(e["_id"])
        e["timestamp"] = e["timestamp"].strftime("%d %b %Y - %I:%M %p UTC")
    return jsonify(events)
