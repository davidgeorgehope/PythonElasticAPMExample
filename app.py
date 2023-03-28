import os
import random
import time
from flask import Flask, jsonify
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
app.config["ELASTIC_APM"] = {
    "SERVICE_NAME": os.environ.get("APM_SERVICE_NAME", "flask-app"),
    "SECRET_TOKEN": os.environ.get("APM_SECRET_TOKEN", ""),
    "SERVER_URL": os.environ.get("APM_SERVER_URL", "http://localhost:8200"),
}

apm = ElasticAPM(app)

@app.route("/")
def hello():
    delay = random.randint(0, 2)
    if delay == 0:
        return jsonify({"message": "Hello, World!"})
    elif delay == 1:
        time.sleep(3)
        return jsonify({"message": "Hello, World! (slow)"})
    else:
        raise ValueError("Something went wrong!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(port)
    app.run(debug=True, host="0.0.0.0", port=port)

