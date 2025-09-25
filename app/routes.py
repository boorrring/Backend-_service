import pandas as pd
from io import StringIO
from app import app
from flask import request, jsonify
from .storage import datastore

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Server is running!"})

@app.route('/offer', methods=['POST'])
def set_offer():
    """Accepts JSON with product/offer details."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    datastore.offer = request.get_json()
    print(f"Offer received: {datastore.offer}") # For debugging
    return jsonify({"status": "Offer details saved successfully"}), 201

@app.route('/leads/upload', methods=['POST'])
def upload_leads():
    """Accepts a CSV file of leads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        try:
            # Read the CSV file content into a pandas DataFrame
            csv_data = file.stream.read().decode("utf-8")
            datastore.leads_df = pd.read_csv(StringIO(csv_data))
            print(f"Leads CSV uploaded with {len(datastore.leads_df)} rows.") # For debugging
            return jsonify({
                "status": "Leads CSV uploaded successfully",
                "leads_count": len(datastore.leads_df)
            }), 201
        except Exception as e:
            return jsonify({"error": f"Failed to process CSV file: {e}"}), 500

    return jsonify({"error": "Invalid file type. Please upload a CSV."}), 400