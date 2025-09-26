@app.route('/login', methods=['POST'])
def login():
    data = request.json
    ip = data.get('ip')

    # comment DB stuff out
    # if blocked_ips.find_one({"ip": ip}):
    #     return jsonify({"anomaly": True, "blocked": True, "msg": "IP blocked"}), 403

    # res = logins.insert_one(data)

    # simulate prediction
    x = featurize(data)
    pred = model.predict(x)[0]
    is_anomaly = pred == -1

    if is_anomaly:
        # alerts.insert_one({"login_id": str(res.inserted_id), "data": data})
        socketio.emit('suspicious_login', data)
        # send_telegram(f"Suspicious login detected: {data}")

    return jsonify({"anomaly": is_anomaly})
