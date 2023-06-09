# Flask App with Elastic APM and SQLite

A simple Flask app instrumented with Elastic APM that simulates slow transactions and errors, and communicates with a SQLite database.

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/davidgeorgehope/PythonElasticAPMExample
   cd PythonElasticAPMExample
   ```

2. Build and start the Docker containers:

   ```
   docker-compose up --build -d
   ```

## Usage

The Flask app is accessible at http://localhost:5001. It randomly generates one of the following responses:

- A normal "Hello, World!" response.
- A slow transaction by sleeping for 3 seconds before returning a response.
- An error by raising a `ValueError` exception.

Elastic APM captures performance metrics, slow transactions, and errors. You can visualize this data in Kibana.


## Load Testing

The `load_test.sh` script sends 1000 requests to the Flask app with a 1-second delay between each request. To run the script, make it executable and run it:

```
chmod +x load_test.sh
./load_test.sh
```

## Configuration

You can configure the Flask app and Elastic APM settings by modifying the environment variables in the `docker-compose.yml` file. Update the following variables as needed:

- `PORT`: Flask app port (default: 5000).
- `APM_SERVICE_NAME`: Elastic APM service name (default: "flask-app").
- `APM_SECRET_TOKEN`: Elastic APM secret token (default: "").
- `APM_SERVER_URL`: Elastic APM server URL (default: "http://apm_server:8200").

Remember to update the port in the `ports` section of the `docker-compose.yml` file and in the `load_test.sh` script if you change the port.
