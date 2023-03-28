import os
import random
import time
from flask import Flask, jsonify
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler

import logging
import elasticapm
from elasticapm import Client
import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("example.db")
cursor = connection.cursor()

# Create a table named 'users'
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

# Insert some data into the 'users' table
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))

# Commit the changes and close the connection to the database
connection.commit()
connection.close()

elastic_apm_logger = logging.getLogger("elasticapm")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
elastic_apm_logger.addHandler(console_handler)


app = Flask(__name__)
app.config["ELASTIC_APM"] = {
    "SERVICE_NAME": os.environ.get("APM_SERVICE_NAME", "flask-app"),
    "SECRET_TOKEN": os.environ.get("APM_SECRET_TOKEN", ""),
    "SERVER_URL": os.environ.get("APM_SERVER_URL", "http://localhost:8200"),
}

#apm = ElasticAPM(app, logging=True)
elasticapm.instrumentation.control.instrument()
client = Client(app.config["ELASTIC_APM"])


@elasticapm.capture_span()
def callTransaction():

    # Reopen the connection to the database
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()

    # Query the 'users' table and print the results
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection to the database
    connection.close()

@app.route("/")
def hello():
    client.begin_transaction('demo-transaction')
    elasticapm.label(platform='DemoPlatform', application='DemoApplication')

    callTransaction()
    delay = random.randint(0, 2)
    if delay == 0:
        client.end_transaction('demo-transaction', 'success')
        return jsonify({"message": "Hello, World!"})
    elif delay == 1:
        time.sleep(3)
        client.end_transaction('demo-transaction', 'success')
        return jsonify({"message": "Hello, World! (slow)"})
    else:
        client.end_transaction('demo-transaction', 'error')
        raise ValueError("Something went wrong!")
    


@app.before_request
def apm_log():
    elasticapm.label(platform = 'DemoPlatform',
                     application = 'DemoApplication')


@app.route('/hello-world/')
def helloWorld():
        return "Hello World"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(port)
    app.run(debug=True, host="0.0.0.0", port=port)

