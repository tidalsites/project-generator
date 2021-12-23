from flask import Flask, request
import os
import json
from generator import generator

app = Flask(__name__)

@app.route('/generate_project', methods=['POST'])
def generate_project():
    if(not request.data):
        return {"success": False, "error": "No data"}

    if(not os.environ.get("GITHUB_TOKEN")):
        return {"success": False, "error": "No token"}
        
    try:
        token = os.environ.get("GITHUB_TOKEN")
        data = json.loads(request.data)
        generator(data, token)
        return {"success": True, "error": None, "response": "Project generated successfully"}
    except Exception as e:
        return {"success": False, "error": e}


if __name__ == "__main__":
    app.run()