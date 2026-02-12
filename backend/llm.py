import os
import json
from dotenv import load_dotenv
from google import genai
from models import EarningsOutput

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_earnings_call(text: str):
    """
    Analyzes an earnings call transcript and returns
    validated structured research output.
    """

    # Limit text to avoid token overflow
    truncated_text = text[:12000]

    prompt = f"""
You are a financial research analyst.

FIRST determine if the document is an earnings call transcript
or management discussion related to company performance.

If it is NOT an earnings-related document, return:

{{
  "document_type": "Unsupported",
  "management_tone": "Not Applicable",
  "confidence_level": "Low",
  "confidence_reasoning": "The document does not contain earnings-related discussion.",
  "key_positives": [],
  "key_concerns": [],
  "forward_guidance": {{
    "revenue": "Not Mentioned",
    "margin": "Not Mentioned",
    "capex": "Not Mentioned"
  }},
  "capacity_utilization": "Not Mentioned",
  "growth_initiatives": []
}}

If it IS an earnings transcript, return:

{{
  "document_type": "Earnings Transcript",
  "management_tone": "Optimistic | Neutral | Cautious | Pessimistic",
  "confidence_level": "High | Medium | Low",
  "confidence_reasoning": "Explain briefly why this confidence level was assigned.",
  "key_positives": [],
  "key_concerns": [],
  "forward_guidance": {{
    "revenue": "",
    "margin": "",
    "capex": ""
  }},
  "capacity_utilization": "",
  "growth_initiatives": []
}}

Rules:
- Do NOT hallucinate
- If guidance not present → "Not Mentioned"
- Return ONLY valid JSON
- Do NOT wrap in markdown

Transcript:
{truncated_text}
"""


    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw_text = response.text.strip()

        # Clean possible markdown formatting
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # Parse JSON
        parsed_json = json.loads(raw_text)

        # Validate using Pydantic schema
        validated_output = EarningsOutput(**parsed_json)

        return validated_output.dict()

    except json.JSONDecodeError:
        return {
            "error": "Model returned invalid JSON format",
            "raw_output": raw_text
        }

    except Exception as e:
        return {
            "error": "Processing failed",
            "details": str(e)
        }





