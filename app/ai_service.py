import google.generativeai as genai
import json
from config import GEMINI_API_KEY

# Configure the Gemini API client
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

def get_ai_intent(lead, offer):
    """
    Uses Gemini to classify lead intent and provide reasoning.
    Returns a dictionary with 'intent' and 'reasoning'.
    """
    if not model:
        return {
            "intent": "Medium", # Default value if AI fails
            "reasoning": "AI service is not available."
        }

    # Create a detailed prompt for the AI
    prompt = f"""
    You are a highly-experienced B2B sales development representative.
    Your task is to qualify a lead based on their profile and our product offer.

    **Our Product Offer:**
    - Name: {offer.get('name', 'N/A')}
    - Value Propositions: {', '.join(offer.get('value_props', []))}
    - Ideal Use Cases / Customer Profile: {', '.join(offer.get('ideal_use_cases', []))}

    **Lead's Profile:**
    - Name: {lead.get('name', 'N/A')}
    - Role: {lead.get('role', 'N/A')}
    - Company: {lead.get('company', 'N/A')}
    - Industry: {lead.get('industry', 'N/A')}
    - LinkedIn Bio: {lead.get('linkedin_bio', 'N/A')}

    **Your Task:**
    Based on the information above, classify the lead's buying intent as "High", "Medium", or "Low".
    Then, provide a 1-2 sentence explanation for your classification.

    Return your answer in a JSON format like this:
    {{
      "intent": "High/Medium/Low",
      "reasoning": "Your 1-2 sentence explanation here."
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to parse JSON correctly
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        ai_result = json.loads(cleaned_response)
        return ai_result
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return {
            "intent": "Medium",
            "reasoning": "Failed to get a valid response from the AI."
        }