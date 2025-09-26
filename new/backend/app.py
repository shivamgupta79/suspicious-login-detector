# app.py (fixed)
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import joblib
import numpy as np
# from notify import send_telegram   # disable for now if not configured
import os
import threading
import time
import uuid
import copy

app = Flask(__name__)
CORS(app)
# Use "threading" async mode to avoid requiring eventlet/gevent during local dev.
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# -------------------------
# In-memory dummy DB layer (thread-safe)
# -------------------------
class DummyCursor:
    def __init__(self, data):
        # data is already a shallow copy from the collection
        self._data = list(data)

    def sort(self, key, direction=1):
        # support sorting by "_id" (by insertion time stored in "_created")
        if key == "_id":
            self._data.sort(key=lambda d: d.get("_created", 0), reverse=(direction == -1))
        else:
            self._data.sort(key=lambda d: d.get(key, None), reverse=(direction == -1))
        return self

    def limit(self, n):
        self._data = self._data[:n]
        return self

    def __iter__(self):
        return iter(self._data)

class DummyCollection(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()

    def insert_one(self, doc):
        with self._lock:
            _id = str(uuid.uuid4())
            doc_copy = dict(doc) if isinstance(doc, dict) else {"value": doc}
            doc_copy["_id"] = _id
            doc_copy["_created"] = time.time()
            self.append(doc_copy)
            # mimic pymongo return object with inserted_id
            return type("Res", (), {"inserted_id": _id})

    def find(self, *args, **kwargs):
        # return a cursor over a shallow copy of the current list (so later mutations don't change it)
        with self._lock:
            snapshot = list(self)
        return DummyCursor(snapshot)

    def find_one(self, query=None):
        with self._lock:
            if not query:
                # return the earliest/first item or None
                return next(iter(self), None)
            for doc in self:
                if all(doc.get(k) == v for k, v in query.items()):
                    return doc
        return None

    def update_one(self, query, update, upsert=False):
        with self._lock:
            for doc in self:
                if all(doc.get(k) == v for k, v in query.items()):
                    if "$set" in update:
                        doc.update(update["$set"])
                    return
            if upsert:
                new = update.get("$set", {}).copy()
                new.update(query)
                self.insert_one(new)

# instantiate fake collections
logins = DummyCollection()
alerts = DummyCollection()
blocked_ips = DummyCollection()

# -------------------------
# Model loading with fallback
# -------------------------
model_path = 'model/isolation_forest.joblib'

if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        print("[INFO] Loaded trained model.")
    except Exception as e:
        print(f"[WARNING] Failed to load model at {model_path!r}: {e}. Using dummy model.")
        model = None
else:
    print("[WARNING] Model not found! Using dummy model instead.")
    model = None

if model is None:
    class DummyModel:
        def predict(self, X):
            # Return -1 for anomaly if failed_attempts >= 5, else 1 (normal)
            out = []
            for row in X:
                fa = int(row[0]) if len(row) > 0 else 0
                out.append(-1 if fa >= 5 else 1)
            return out
    model = DummyModel()

# -------------------------
# Feature extraction helper
# -------------------------
def featurize(payload):
    return np.array([[payload.get('failed_attempts', 0),
                      payload.get('hour', 0),
                      int(payload.get('is_new_device', 0)),
                      payload.get('time_since_last', 99999)]])

# -------------------------
# Routes
# -------------------------
@app.route('/')
def home():
    return jsonify({"status": "ok"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    ip = data.get('ip')

    # check blocked IP
    if ip and blocked_ips.find_one({"ip": ip}):
        return jsonify({"anomaly": True, "blocked": True, "msg": "IP blocked"}), 403

    # store login attempt
    res = logins.insert_one(data)

    # predict anomaly
    x = featurize(data)
    pred = model.predict(x)[0]
    is_anomaly = pred == -1

    if is_anomaly:
        alerts.insert_one({"login_id": str(res.inserted_id), "data": data})
        # broadcast a lightweight event
        try:
            socketio.emit('suspicious_login', data)
        except Exception:
            # avoid crashing if socket broadcast fails
            pass
        # send_telegram(f"Suspicious login detected: {data}")  # enable when ready

    return jsonify({"anomaly": is_anomaly, "id": str(res.inserted_id)})

@app.route('/logins', methods=['GET'])
def get_logins():
    last = list(logins.find().sort("_id", -1).limit(100))
    # return copies so we don't accidentally expose internal mutation
    safe = [copy.deepcopy(doc) for doc in last]
    return jsonify(safe)

@app.route('/alerts', methods=['GET'])
def get_alerts():
    last = list(alerts.find().sort("_id", -1).limit(50))
    safe = [copy.deepcopy(doc) for doc in last]
    return jsonify(safe)

@app.route('/block', methods=['POST'])
def block_ip():
    data = request.json or {}
    ip = data.get('ip')
    if not ip:
        return jsonify({"status": "error", "msg": "ip field required"}), 400
    blocked_ips.update_one({"ip": ip}, {"$set": {"ip": ip}}, upsert=True)
    return jsonify({"status": "blocked", "ip": ip})

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    # bind to localhost for local testing; browser use http://127.0.0.1:5000/
    print("Starting server on http://127.0.0.1:5000")
    # socketio.run will use the async mode set earlier (threading)
    socketio.run(app, host="127.0.0.1", port=int(os.getenv('PORT', 5000)), debug=True)
