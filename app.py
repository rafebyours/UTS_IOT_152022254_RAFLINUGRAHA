from flask import Flask, jsonify, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({"error": "Data file not found."}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Error reading JSON data."}), 500

    elif request.method == 'POST':
        new_data = request.get_json()

        if not new_data:
            return jsonify({"error": "No data provided"}), 400

        try:
            with open('data.json', 'r+') as file:
                data = json.load(file)
                
                # Append new entry to the existing data
                data['nilai_suhu_max_humid_max'].append({
                    "idx": len(data['nilai_suhu_max_humid_max']) + 1,
                    "suhun": new_data['temperature'],
                    "humid": new_data['humidity'],
                    "kecerahan": new_data['brightness'],
                    "timestamp": new_data['timestamp']
                })
                
                # Write updated data back to the file
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            return jsonify({"status": "success", "message": "Data submitted successfully!"}), 200
        except FileNotFoundError:
            return jsonify({"error": "Data file not found."}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Error decoding JSON data."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
