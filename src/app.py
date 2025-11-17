"""
Sample Flask application with intentionally vulnerable dependencies
This app demonstrates CI/CD security scanning capabilities
"""
import requests
import urllib3
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Disable SSL warnings for demo (DON'T DO THIS IN PRODUCTION!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Security Vulnerability Demo App",
        "status": "running"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/fetch-data')
def fetch_data():
    """
    Endpoint that uses requests library
    Demonstrates potential security vulnerability in older versions
    """
    try:
        # This could be vulnerable if using old requests version
        response = requests.get('https://api.github.com')
        return jsonify({
            "source": "GitHub API",
            "status": response.status_code,
            "headers": dict(response.headers)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST'])
def process_data():
    """
    Process JSON data
    Demonstrates urllib3 usage
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "No data provided"}), 400
    
    # Process the data (simplified for demo)
    result = {
        "processed": True,
        "input_size": len(json.dumps(data)),
        "urllib3_version": urllib3.__version__
    }
    return jsonify(result), 200

if __name__ == '__main__':
    # Run in production mode (debug=False)
    app.run(host='0.0.0.0', port=5000, debug=False)
