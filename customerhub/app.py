import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os 
import socket
import sys

app = Flask(__name__)
CORS(app)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print(get_ip_address())

host_ip = get_ip_address()
print(host_ip)


@app.route('/createdocumentation/<document_name>', methods=['POST'])
def create_documentation(document_name):
    print("Creating documentation for " + document_name)
    
    documentation_path = '../documentation/' + document_name
    try:
        os.makedirs(documentation_path)
        print("Documentation created successfully.")
        return jsonify({"status": "OK", "message": "Documentation created successfully."})
    except Exception as e:
        print(f"Error creating documentation: {str(e)}")
        return jsonify({"status": "Error", "message": f"Error creating documentation: {str(e)}"})
    





if __name__ == '__main__':
    app.run(debug=True, host=host_ip, port=2001)
