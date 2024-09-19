from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS to allow requests from any origin ('*')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Debugging middleware to log headers and body
@app.before_request
def log_request_info():
    print('Headers:', request.headers)
    print('Body:', request.get_data())

@app.route("/status", methods=["GET"])
def status():
    status_data = {
        "name": "def",
        "items": {
            "case1": "Load case",
            "case2": "Simulation",
            "case3": "Testing",
            "case4": "Debugging",
            "case5": "Deleting",
            "case6": "Establishing",
            "case8": "Requirements",
            "case9": "Audit",
        },
        "difficulty": {
            "case1": "Junior",
            "case2": "Senior",
            "case3": "Expert",
        }
    }
    return jsonify(status_data)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json  # Capture the JSON data sent in the request body
    print("Data received:", data)

    # Process the data as needed. Here we're just echoing it back.
    response_data = {
        "message": "Data successfully received.",
        "receivedData": data,
        "status": "Processed"
    }

    keys = list(data.keys())
    print("Keys of the received data:", keys)

    # Send the response back to the client
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=3000)
