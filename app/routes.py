import pandas as pd
from io import StringIO
from app import app
from flask import request, jsonify
from .storage import datastore
from .scorer import run_scoring_pipeline # Import the pipeline function

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

# --- Add the new endpoints below ---

@app.route('/score', methods=['POST'])
def score_leads():
    """Triggers the scoring pipeline for the uploaded leads."""
    if datastore.leads_df is None or datastore.offer is None:
        return jsonify({"error": "Please upload leads and set an offer before scoring."}), 400

    try:
        run_scoring_pipeline()
        return jsonify({"status": "Scoring completed successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred during scoring: {e}"}), 500

@app.route('/results', methods=['GET'])
def get_results():
    """Returns the scored leads as a JSON array."""
    if datastore.leads_df is None or 'score' not in datastore.leads_df.columns:
        return jsonify({"error": "No scored results found. Please run the scoring first."}), 404

    # Convert DataFrame to a list of dictionaries (JSON)
    results = datastore.leads_df.to_dict(orient='records')
    return jsonify(results), 200