import pandas as pd
from .storage import datastore
from .ai_service import get_ai_intent # Import the new AI service

# --- Keep the existing code from Step 4 here ---
# Define points for the rule-based layer
ROLE_POINTS = {"decision maker": 20, "influencer": 10}
INDUSTRY_POINTS = {"exact": 20, "adjacent": 10}
COMPLETENESS_POINTS = 10

def calculate_rule_score(lead, ideal_use_case):
    # ... (this function remains unchanged)
    score = 0
    lead_role = lead.get('role', '').lower()
    if 'head' in lead_role or 'vp' in lead_role or 'director' in lead_role or 'c-level' in lead_role:
        score += ROLE_POINTS.get("decision maker", 0)
    elif 'manager' in lead_role or 'lead' in lead_role or 'specialist' in lead_role:
        score += ROLE_POINTS.get("influencer", 0)
    lead_industry = lead.get('industry', '').lower()
    if ideal_use_case and ideal_use_case.lower() in lead_industry:
        score += INDUSTRY_POINTS.get("exact", 0)
    elif 'tech' in lead_industry or 'saas' in lead_industry:
         score += INDUSTRY_POINTS.get("adjacent", 0)
    required_fields = ['name', 'role', 'company', 'industry', 'location', 'linkedin_bio']
    if all(pd.notna(lead.get(field)) and lead.get(field) != '' for field in required_fields):
        score += COMPLETENESS_POINTS
    return score

# --- Add the new pipeline function below ---

def run_scoring_pipeline():
    """
    Main function to score all uploaded leads.
    It calculates rule scores, gets AI scores, and combines them.
    """
    if datastore.leads_df is None or datastore.offer is None:
        raise ValueError("Leads data or offer data is not available.")

    results = []

    # Define AI points mapping
    AI_POINTS_MAP = {"High": 50, "Medium": 30, "Low": 10}

    # Get the primary ideal use case for rule matching
    ideal_use_case = datastore.offer.get('ideal_use_cases', [''])[0]

    # Iterate over each lead in the DataFrame
    for index, lead in datastore.leads_df.iterrows():
        print(f"Scoring lead: {lead['name']}...")

        # 1. Calculate Rule-based score
        rule_score = calculate_rule_score(lead, ideal_use_case)

        # 2. Get AI intent and points
        ai_result = get_ai_intent(lead, datastore.offer)
        ai_intent = ai_result.get("intent", "Medium")
        ai_reasoning = ai_result.get("reasoning", "N/A")
        ai_points = AI_POINTS_MAP.get(ai_intent, 30) # Default to Medium

        # 3. Calculate Final Score
        final_score = rule_score + ai_points

        results.append({
            "name": lead['name'],
            "role": lead['role'],
            "company": lead['company'],
            "intent": ai_intent,
            "score": final_score,
            "reasoning": ai_reasoning
        })

    # Sort results by score, descending
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)

    # Update the DataFrame in our datastore with the results
    datastore.leads_df = pd.DataFrame(sorted_results)

    print("Scoring pipeline completed.")
    return True