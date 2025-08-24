from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is the CI/CD demo!"

@app.route("/data")
def get_data():
    return jsonify({"status": "success", "value": 42})

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
