import pandas as pd

# Define points for the rule-based layer
ROLE_POINTS = {"decision maker": 20, "influencer": 10}
INDUSTRY_POINTS = {"exact": 20, "adjacent": 10}
COMPLETENESS_POINTS = 10

def calculate_rule_score(lead, ideal_use_case):
    """Calculates the rule-based score for a single lead."""
    score = 0

    # 1. Role relevance scoring
    lead_role = lead.get('role', '').lower()
    if 'head' in lead_role or 'vp' in lead_role or 'director' in lead_role or 'c-level' in lead_role:
        score += ROLE_POINTS.get("decision maker", 0)
    elif 'manager' in lead_role or 'lead' in lead_role or 'specialist' in lead_role:
        score += ROLE_POINTS.get("influencer", 0)

    # 2. Industry match scoring (simple keyword matching)
    lead_industry = lead.get('industry', '').lower()
    if ideal_use_case and ideal_use_case.lower() in lead_industry:
        score += INDUSTRY_POINTS.get("exact", 0)
    # This is a placeholder for more complex "adjacent" logic
    elif 'tech' in lead_industry or 'saas' in lead_industry:
         score += INDUSTRY_POINTS.get("adjacent", 0)

    # 3. Data completeness scoring
    required_fields = ['name', 'role', 'company', 'industry', 'location', 'linkedin_bio']
    if all(pd.notna(lead.get(field)) and lead.get(field) != '' for field in required_fields):
        score += COMPLETENESS_POINTS

    return score